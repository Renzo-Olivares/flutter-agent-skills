// Regression test for https://github.com/flutter/flutter/issues/92050
// "[Windows, IME] Sogou input dropdown is mispositioned after committing"
//
// Root cause (per comment [13] on the issue): in
// packages/flutter/lib/src/widgets/editable_text.dart, `setComposingRect`
// falls back to offset 0 when `composingRange.isValid` is false:
//     final int offset = composingRange.isValid ? composingRange.start : 0;
// Sogou IME on Windows never populates `composingRange` (it composes in its
// own window), so every `setComposingRect` call from Flutter ships the rect
// at offset 0 — always the top-left of the field. Sogou places its candidate
// window where Flutter says the composing rect is, so after moving to a
// different TextField the window stays in the previous field's position.
//
// Proposed fix: use `selection.baseOffset` instead of `0` when composingRange
// is invalid, so the rect follows the caret.
//
// This test captures outgoing `TextInput.setComposingRect` calls via a mock
// method-call handler and asserts the rect's x-coordinate matches the current
// caret position, not the start of the text.
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets(
    'setComposingRect tracks the caret when composingRange is invalid',
    (WidgetTester tester) async {
      final List<MethodCall> calls = <MethodCall>[];
      tester.binding.defaultBinaryMessenger.setMockMethodCallHandler(
        SystemChannels.textInput,
        (MethodCall call) async {
          calls.add(call);
          return null;
        },
      );
      addTearDown(() {
        tester.binding.defaultBinaryMessenger.setMockMethodCallHandler(
          SystemChannels.textInput,
          null,
        );
      });

      final TextEditingController controller = TextEditingController(
        text: 'hello world',
      );
      addTearDown(controller.dispose);

      await tester.pumpWidget(
        MaterialApp(
          home: Material(child: Center(child: TextField(controller: controller))),
        ),
      );

      // Focus the field and put the caret at the end.
      await tester.tap(find.byType(TextField));
      await tester.pump();
      controller.selection = TextSelection.collapsed(
        offset: controller.text.length,
      );
      // Pump a few frames so the periodic post-frame callback fires and sends
      // setComposingRect through.
      await tester.pump(const Duration(milliseconds: 50));
      await tester.pump(const Duration(milliseconds: 50));
      await tester.pump(const Duration(milliseconds: 50));

      final List<MethodCall> composingRectCalls = calls
          .where((MethodCall c) => c.method == 'TextInput.setComposingRect')
          .toList();
      expect(
        composingRectCalls,
        isNotEmpty,
        reason: 'Expected at least one TextInput.setComposingRect call; '
                'without one the test cannot verify the bug.',
      );

      // The framework has no active composition (composingRange.isValid is
      // false), so the buggy branch uses offset 0. The correct behavior is to
      // use selection.baseOffset (here: end of text, length 11).
      final EditableTextState state = tester.state<EditableTextState>(
        find.byType(EditableText),
      );
      final RenderEditable re = state.renderEditable;
      final Rect rectAtStart = re.getLocalRectForCaret(
        const TextPosition(offset: 0),
      );
      final Rect rectAtEnd = re.getLocalRectForCaret(
        TextPosition(offset: controller.text.length),
      );

      // Sanity: the two positions are visibly different. If they're not, the
      // test can't distinguish bug from fix.
      expect(
        (rectAtStart.left - rectAtEnd.left).abs(),
        greaterThan(5.0),
        reason: 'Caret positions at offset 0 vs end-of-text should differ; '
                'test harness setup issue if not.',
      );

      final Map<Object?, Object?> args =
          composingRectCalls.last.arguments as Map<Object?, Object?>;
      final double sentX = (args['x'] as num).toDouble();

      expect(
        (sentX - rectAtEnd.left).abs(),
        lessThan(2.0),
        reason:
            'setComposingRect should pass the caret position (offset '
            '${controller.text.length}, x=${rectAtEnd.left.toStringAsFixed(1)}) '
            'when composingRange is invalid — not offset 0 '
            '(x=${rectAtStart.left.toStringAsFixed(1)}). '
            'Got x=${sentX.toStringAsFixed(1)}. '
            'See https://github.com/flutter/flutter/issues/92050',
      );
    },
  );
}

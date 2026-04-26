// Regression test for https://github.com/flutter/flutter/issues/98720
// "[Android] TextField cursor doesn't move to tapped position, but converts
//  into text selection mode after selecting input mode from virtual keyboard."
//
// Per the issue's comment summary: on certain Android keyboards (older Samsung
// Keyboard versions, later also seen on Gboard with shift-to-capitalize),
// switching to the symbols/number pane emits a `ShiftRight` key-down event
// with non-zero `metaState` but NEVER the matching key-up. Flutter's
// `HardwareKeyboard` state becomes "shift held", and subsequent taps on the
// TextField are interpreted as shift-click — they extend the selection from
// the existing caret to the tap point instead of moving the caret.
//
// Proposed framework-level fix (per @LongCatIsLooong and @dkwingsmt in the
// thread): force a `metaState` synchronization before text events so stuck
// modifier state is reconciled.
//
// Expected test outcome TODAY: the assertion on a collapsed selection
// FAILS — selection extends from offset 0 to the tap offset because shift is
// still "held" from the phantom key-down.
//
// Expected post-fix: stuck shift is detected/sanitized and the tap moves the
// caret, leaving the selection collapsed.
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets(
    'TextField tap after phantom shift-down (no matching shift-up) should '
    'move the caret, not extend the selection',
    (WidgetTester tester) async {
      final TextEditingController controller = TextEditingController(
        text: 'abcdefghij',
      );
      addTearDown(controller.dispose);

      await tester.pumpWidget(
        MaterialApp(
          home: Material(
            child: Center(child: TextField(controller: controller)),
          ),
        ),
      );

      // Focus the field and place the caret at offset 0.
      await tester.tap(find.byType(TextField));
      await tester.pump();
      controller.selection = const TextSelection.collapsed(offset: 0);
      await tester.pump();

      // Reproduce the Samsung/Gboard-style phantom key event: shift-down with
      // no matching shift-up. HardwareKeyboard is now stuck in "shift held".
      await tester.sendKeyDownEvent(LogicalKeyboardKey.shiftRight);
      expect(
        HardwareKeyboard.instance.logicalKeysPressed.contains(
          LogicalKeyboardKey.shiftRight,
        ),
        isTrue,
        reason: 'sanity: shift should be in the held-keys set after sendKeyDownEvent',
      );

      // Tap roughly in the middle of the visible text.
      final Rect fieldRect = tester.getRect(find.byType(TextField));
      await tester.tapAt(
        Offset(fieldRect.left + fieldRect.width / 2, fieldRect.center.dy),
      );
      await tester.pump();

      // Clean up for the binding (no-op once the test harness tears down, but
      // mirrors real behavior where a later keyboard event would release it).
      await tester.sendKeyUpEvent(LogicalKeyboardKey.shiftRight);

      expect(
        controller.selection.isCollapsed,
        isTrue,
        reason:
            'Tap should move the caret to the tapped offset, not extend the '
            'selection, even if HardwareKeyboard is in a stuck "shift held" '
            'state from a phantom Samsung/Gboard key event. See '
            'https://github.com/flutter/flutter/issues/98720',
      );
    },
  );
}

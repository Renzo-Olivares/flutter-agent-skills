// Regression test for https://github.com/flutter/flutter/issues/93934
//
// Bug. On desktop builds (macOS, Windows), pasting CRLF-terminated text into
// a TextField preserves the carriage-return ('\r') as a zero-width invisible
// character. Caret movement around the '\r' becomes inconsistent: arrow-left
// lands the caret between '\r' and '\n', and arrow-right then skips over
// both characters at once.
//
// Expected failure mode today. The framework's `EditableText.pasteText`
// handler (`packages/flutter/lib/src/widgets/editable_text.dart`) does not
// normalize '\r\n' to '\n' before inserting; the controller's text faithfully
// stores whatever the platform clipboard returned. Browsers and mobile
// platforms typically deliver line breaks as '\n' so the bug doesn't surface
// there, but desktop clipboards return raw CRLF.
//
// Probe rationale. The rendering and caret-stop layers for '\r' are
// engine-side (SkParagraph), so we test the only framework lever: the paste
// handler should normalize '\r\n' to '\n' on receive. Asserting the
// post-paste controller text fails as expected today, confirming the
// framework lacks normalization. A future fix that strips or normalizes '\r'
// on paste would turn this test green.

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

class _MockClipboard {
  Object? clipboardData = <String, dynamic>{'text': null};

  Future<Object?> handleMethodCall(MethodCall call) async {
    switch (call.method) {
      case 'Clipboard.getData':
        return clipboardData;
      case 'Clipboard.hasStrings':
        final Map<String, dynamic>? data = clipboardData as Map<String, dynamic>?;
        final String? text = data?['text'] as String?;
        return <String, bool>{'value': text != null && text.isNotEmpty};
      case 'Clipboard.setData':
        clipboardData = call.arguments;
    }
    return null;
  }
}

void main() {
  testWidgets('paste of CRLF text into TextField normalizes to LF', (
    WidgetTester tester,
  ) async {
    final _MockClipboard mock = _MockClipboard();
    TestWidgetsFlutterBinding.ensureInitialized().defaultBinaryMessenger
        .setMockMethodCallHandler(SystemChannels.platform, mock.handleMethodCall);
    addTearDown(() {
      TestWidgetsFlutterBinding.ensureInitialized().defaultBinaryMessenger
          .setMockMethodCallHandler(SystemChannels.platform, null);
    });

    final TextEditingController controller = TextEditingController();
    addTearDown(controller.dispose);
    final FocusNode focusNode = FocusNode();
    addTearDown(focusNode.dispose);

    await tester.pumpWidget(
      MaterialApp(
        home: Material(
          child: TextField(controller: controller, focusNode: focusNode),
        ),
      ),
    );

    await Clipboard.setData(const ClipboardData(text: 'hello\r\nworld'));
    expect(
      (mock.clipboardData! as Map<String, dynamic>)['text'],
      'hello\r\nworld',
      reason: 'Clipboard mock should hold the CRLF payload.',
    );

    focusNode.requestFocus();
    await tester.pump();

    final EditableTextState state = tester.state<EditableTextState>(
      find.byType(EditableText),
    );
    await state.pasteText(SelectionChangedCause.keyboard);
    await tester.pumpAndSettle();

    expect(
      controller.text.contains('\r'),
      isFalse,
      reason:
          "Paste should normalize CRLF (\\r\\n) to LF (\\n); current behavior "
          "preserves \\r as a zero-width invisible character that confuses "
          'caret navigation.',
    );
    expect(controller.text, equals('hello\nworld'));
  });
}

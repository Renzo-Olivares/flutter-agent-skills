import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

// https://github.com/flutter/flutter/issues/93934
// Bug: TextField with pasted CRLF endings has invisible CR char (\r)
// which messes up arrow key navigation.
// Expected failure: The text field should either strip the \r on paste,
// or handle it correctly without treating it as an invisible character that
// requires an extra arrow key press to move over.

void main() {
  testWidgets('TextField CRLF paste handling', (WidgetTester tester) async {
    final TextEditingController controller = TextEditingController();
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: TextField(
            controller: controller,
            autofocus: true,
            maxLines: null, // multiline
          ),
        ),
      ),
    );

    await tester.pumpAndSettle();

    // Simulate pasting CRLF text.
    // Assuming the framework processes it or the user pasted it.
    final String pastedText = 'Line 1\r\nLine 2';
    
    // Simulate pasting from clipboard
    await Clipboard.setData(ClipboardData(text: pastedText));
    await tester.tap(find.byType(TextField));
    await tester.pump();
    
    // Select all and paste to replace
    final targetPlatform = defaultTargetPlatform;
    final modifier = targetPlatform == TargetPlatform.macOS || targetPlatform == TargetPlatform.iOS 
        ? LogicalKeyboardKey.meta 
        : LogicalKeyboardKey.control;
        
    await tester.sendKeyDownEvent(modifier);
    await tester.sendKeyEvent(LogicalKeyboardKey.keyV);
    await tester.sendKeyUpEvent(modifier);
    
    await tester.pumpAndSettle();

    // The text length is 14. 'Line 1' (6) + '\r\n' (2) + 'Line 2' (6)
    expect(controller.text.length, 14);

    // Let's press left arrow 6 times to get to the end of Line 1 (before \r\n).
    for (int i = 0; i < 6; i++) {
      await tester.sendKeyEvent(LogicalKeyboardKey.arrowLeft);
      await tester.pumpAndSettle();
    }

    // Now we are at offset 8 (after \n). Wait, \r\n are two characters.
    // If we press left again, does it skip both \r\n or just \n?
    // In many text editors, \r\n is treated as a single newline.
    // Let's see what happens in Flutter.
    await tester.sendKeyEvent(LogicalKeyboardKey.arrowLeft);
    await tester.pumpAndSettle();

    // If it skipped \n, it's at offset 7 (between \r and \n).
    // The bug report says "cursor is placed after invisible \r char".
    // "When I press left arrow, it goes over that char to the actual text end."
    // So the offset would be 7, and we'd need another press to get to 6.
    // Ideally, it should either skip both or \r should be stripped.
    // Let's check if it stops at offset 7.
    
    // The expected behavior (if it works correctly) is that it treats \r\n as a single line break
    // or strips \r. If it strips \r, length would be 13. But if we just set text directly, it doesn't strip.
    // Let's assert that one left arrow from the start of Line 2 moves us to the end of Line 1 (offset 6).
    expect(controller.selection.baseOffset, 6, reason: 'Arrow left should skip the entire newline sequence, not leave us stuck on \\r');
  });
}

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

// https://github.com/flutter/flutter/issues/78660
// Bug: Arrow keys in RTL text move the caret in the logical direction rather than the visual direction.
// Expected failure: Pressing the left arrow key at the end of an RTL text should move the caret visually left (which is logically towards the beginning of the text, decreasing the offset).
// Currently, pressing left arrow on RTL text moves the caret logically left (which might actually be visually right or wrong depending on exact implementation, but it's known to be wrong).
// Actually, if it moves logically backward, then offset decreases. But the user complains it moves in the wrong direction.
// We assert that pressing left arrow moves the caret offset correctly.

void main() {
  testWidgets('RTL arrow keys movement', (WidgetTester tester) async {
    final TextEditingController controller = TextEditingController(text: 'مرحبا');
    // 'مرحبا' is length 5. Let's put cursor at offset 0 (logical start, visual right).
    controller.selection = const TextSelection.collapsed(offset: 0);

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Directionality(
            textDirection: TextDirection.rtl,
            child: TextField(
              controller: controller,
              autofocus: true,
            ),
          ),
        ),
      ),
    );

    await tester.pumpAndSettle();

    // Send a left arrow key event.
    // In RTL, the caret is initially at the right edge (offset 0).
    // Pressing left arrow should move the caret visually left.
    // Visually left means logically forward (offset 1).
    await tester.sendKeyEvent(LogicalKeyboardKey.arrowLeft);
    await tester.pumpAndSettle();

    // Check if the offset has moved to 1.
    expect(controller.selection.baseOffset, 1, reason: 'Left arrow should move caret visually left (logically forward in RTL)');
  });
}

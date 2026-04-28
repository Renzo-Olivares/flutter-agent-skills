// https://github.com/flutter/flutter/issues/78660
// Bug summary: When using a TextField with RTL text, the left and right arrow
// keys move the caret in the logical direction (character order) rather than
// the visual direction (left moves caret left visually).
// Expected failure mode today: Pressing Left arrow on RTL text moves the caret
// visually to the right, and vice-versa.
// Test assertion: The test presses the left arrow key and asserts that the caret
// index changes such that it visually moved left.

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Arrow keys move visually in RTL text', (WidgetTester tester) async {
    final TextEditingController controller = TextEditingController(text: 'شسيب');
    // The text 'شسيب' is RTL.
    // logical indices: 0:ش, 1:س, 2:ي, 3:ب
    // Visual order (left to right) is: ب ي س ش
    
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: TextField(
            controller: controller,
            textDirection: TextDirection.rtl,
            autofocus: true,
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();

    // Set selection to index 0. Visual position is at the far right.
    controller.selection = const TextSelection.collapsed(offset: 0);
    await tester.pumpAndSettle();

    // Press left arrow. We expect the cursor to move visually left, which means
    // it moves to index 1.
    await tester.sendKeyEvent(LogicalKeyboardKey.arrowLeft);
    await tester.pumpAndSettle();

    expect(controller.selection.baseOffset, 1);
  });
}

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

// https://github.com/flutter/flutter/issues/78660
// Bug: Arrow keys move the caret in the wrong logical direction for RTL text.
// Expected failure: The left arrow key currently moves the cursor to the right visually (which is the wrong logical direction for RTL).
// The test asserts that pressing the left arrow key moves the selection offset correctly in a visually leftward direction.

void main() {
  testWidgets('Left arrow key moves caret left visually in RTL text', (WidgetTester tester) async {
    final TextEditingController controller = TextEditingController(text: 'مرحبا بكم'); // "Welcome"
    
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: Directionality(
          textDirection: TextDirection.rtl,
          child: TextField(
            controller: controller,
            autofocus: true,
          ),
        ),
      ),
    ));
    await tester.pumpAndSettle();

    // Set cursor at the beginning (rightmost visually for RTL). 
    // In RTL, offset 0 is visually at the right.
    controller.selection = const TextSelection.collapsed(offset: 0);
    await tester.pump();

    // Press left arrow. Visually we expect the cursor to move left.
    // Since offset 0 is at the right, moving left should increase the offset.
    await tester.sendKeyEvent(LogicalKeyboardKey.arrowLeft);
    await tester.pumpAndSettle();

    // If it fails, it means the offset decreased or stayed 0 (moved right visually or hit boundary).
    expect(controller.selection.baseOffset, 1);
  });
}

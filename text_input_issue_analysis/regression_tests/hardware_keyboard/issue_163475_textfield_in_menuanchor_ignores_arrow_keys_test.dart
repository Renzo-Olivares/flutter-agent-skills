// Regression test for https://github.com/flutter/flutter/issues/163475
// "TextField surrounded by MenuAnchor does not respond to directional arrow
//  keys"
//
// Root cause (per commenter analysis): the Shortcuts widget inside
// `_RawMenuAnchorState` unconditionally registers arrow-key shortcuts that
// consume the events before the TextField can process them. Proposed fix:
// only register those arrow shortcuts when the menu is actually open.
//
// This test places a TextField inside a MenuAnchor with an EMPTY
// menuChildren + menu-closed state, focuses the field, places the caret at
// the end of the text, and sends a left-arrow key event. Expected behavior:
// the caret moves one position left. Bug behavior: the arrow event is
// consumed by MenuAnchor's Shortcuts, the caret stays put.
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets(
    'TextField inside MenuAnchor responds to arrow keys when the menu is '
    'closed',
    (WidgetTester tester) async {
      final TextEditingController controller = TextEditingController(
        text: 'abcdef',
      );
      addTearDown(controller.dispose);

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Center(
              child: MenuAnchor(
                menuChildren: const <Widget>[],
                builder:
                    (
                      BuildContext context,
                      MenuController menuController,
                      Widget? child,
                    ) {
                      return TextField(controller: controller);
                    },
              ),
            ),
          ),
        ),
      );

      // Focus the field and move the caret to the end.
      await tester.tap(find.byType(TextField));
      await tester.pump();
      controller.selection = TextSelection.collapsed(
        offset: controller.text.length,
      );
      await tester.pump();

      // Send left-arrow. Expect the caret to move one position left (offset
      // -> text.length - 1).
      await tester.sendKeyEvent(LogicalKeyboardKey.arrowLeft);
      await tester.pump();

      expect(
        controller.selection.baseOffset,
        controller.text.length - 1,
        reason:
            'The left-arrow key should move the caret inside a TextField '
            'even when the TextField is wrapped in a MenuAnchor whose menu '
            'is closed. Today the Shortcuts widget inside _RawMenuAnchorState '
            'unconditionally registers arrow-key shortcuts and consumes the '
            'event. See https://github.com/flutter/flutter/issues/163475',
      );
    },
  );
}

// Regression test for https://github.com/flutter/flutter/issues/87124
// "Mouse drag in TextField scrolls instead of selecting"
//
// Per the issue thread: vertical mouse drag inside a multiline
// TextField scrolls the inner viewport instead of extending a selection.
// Confirmed on macOS desktop and web. Native macOS / desktop browsers
// select text on mouse drag.
//
// Expected failure mode today: `controller.selection.isCollapsed` is
// true after a mouse-drag gesture across the text (scroll happened,
// no selection). Post-fix: selection is non-collapsed with the drag
// range selected.
import 'package:flutter/foundation.dart';
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets(
    'Vertical mouse drag inside multiline TextField selects text (not scrolls)',
    (WidgetTester tester) async {
      debugDefaultTargetPlatformOverride = TargetPlatform.macOS;

      final TextEditingController controller = TextEditingController(
        text: 'Line 1\nLine 2\nLine 3\nLine 4\nLine 5\nLine 6\nLine 7',
      );
      addTearDown(controller.dispose);

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: Center(
              child: SizedBox(
                width: 300,
                child: TextField(
                  controller: controller,
                  maxLines: 3,
                ),
              ),
            ),
          ),
        ),
      );

      // Focus the field first so the selection system is live.
      await tester.tap(find.byType(TextField));
      await tester.pump();

      // Grab the TextField's rect for positioning the drag.
      final Rect fieldRect = tester.getRect(find.byType(TextField));
      // Start the drag near the top-left of the field; drag downward
      // within the visible region.
      final Offset startPos = Offset(fieldRect.left + 20, fieldRect.top + 10);
      final Offset endPos = Offset(fieldRect.left + 20, fieldRect.top + 50);

      final TestGesture gesture = await tester.startGesture(
        startPos,
        kind: PointerDeviceKind.mouse,
      );
      await gesture.moveTo(endPos);
      await gesture.up();
      await tester.pumpAndSettle();

      try {
        expect(
          controller.selection.isCollapsed,
          isFalse,
          reason:
              'A mouse drag inside a multiline TextField should extend a '
              'selection — matching macOS/web native behavior. Today the '
              'drag scrolls the inner viewport instead. Selection after '
              'drag: ${controller.selection}. '
              'See https://github.com/flutter/flutter/issues/87124',
        );
      } finally {
        debugDefaultTargetPlatformOverride = null;
      }
    },
  );
}

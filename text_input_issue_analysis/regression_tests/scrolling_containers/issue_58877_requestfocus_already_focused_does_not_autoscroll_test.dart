// Regression test for https://github.com/flutter/flutter/issues/58877
// "FocusNode does not auto scroll to TextFormField when item already
//  selected (focused)"
//
// Root cause (per the thread): when the focus node already reports
// `hasFocus`, the framework skips its scroll-into-view path. Calling
// `requestFocus` on an already-focused node is effectively a no-op for
// scroll, so after manually scrolling the field off-screen the call
// doesn't bring it back. A scenario: form validation finishes, the
// field with errors is already focused (from a previous tap), but the
// user has manually scrolled away to press Submit — requestFocus
// should still scroll the field back into view.
//
// Expected failure mode today: scroll offset after `requestFocus()`
// equals the post-manual-scroll offset (no automatic scroll back).
// Post-fix: scroll offset should return to ~0 (field visible at top).
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets(
    'FocusNode.requestFocus on an already-focused TextFormField should '
    'scroll the field back into view',
    (WidgetTester tester) async {
      final FocusNode focusNode = FocusNode();
      addTearDown(focusNode.dispose);

      final ScrollController scrollController = ScrollController();
      addTearDown(scrollController.dispose);

      // A long single scroll view so the target field can be scrolled
      // far out of view. Field is placed near the top at offset 0.
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: SingleChildScrollView(
              controller: scrollController,
              child: Column(
                children: <Widget>[
                  TextFormField(
                    focusNode: focusNode,
                    decoration: const InputDecoration(labelText: 'Target'),
                  ),
                  // Huge spacer so scrolling ~800 px puts the field far above
                  // the viewport.
                  const SizedBox(height: 2000),
                  const Text('Bottom of form'),
                ],
              ),
            ),
          ),
        ),
      );

      // Focus the field once (user taps it).
      focusNode.requestFocus();
      await tester.pump();
      expect(focusNode.hasFocus, isTrue);

      // User manually scrolls down ~800 px (far enough that the field is
      // completely off the top of the viewport).
      scrollController.jumpTo(800);
      await tester.pump();
      expect(scrollController.offset, 800);

      // Node is still focused (nothing changed that state).
      expect(focusNode.hasFocus, isTrue);

      // Re-requesting focus on the already-focused node. Expected: scroll
      // back into view; Actual today: no-op because hasFocus is already
      // true, so the framework skips its scroll path.
      focusNode.requestFocus();
      await tester.pumpAndSettle();

      expect(
        scrollController.offset,
        lessThan(50),
        reason:
            'Re-requesting focus on an already-focused TextFormField '
            'should trigger scroll-into-view. Offset stayed at '
            '${scrollController.offset} instead of returning near 0. '
            'See https://github.com/flutter/flutter/issues/58877',
      );
    },
  );
}

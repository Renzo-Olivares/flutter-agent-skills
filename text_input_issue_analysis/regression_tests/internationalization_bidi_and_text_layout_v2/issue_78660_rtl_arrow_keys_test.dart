// Copyright 2014 The Flutter Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Regression probe for https://github.com/flutter/flutter/issues/78660
//
// Bug: In an RTL TextField containing Arabic text, the LEFT and RIGHT physical
// arrow keys move the caret in *logical* string order rather than *visual*
// screen order. As a result the caret moves the wrong way visually:
//
//   - ArrowRight (user expects: caret jumps visually to the right) currently
//     advances the logical offset toward the end of the string. In an RTL
//     paragraph that is the visual *left*.
//   - ArrowLeft is symmetric: it walks toward the start of the string, which
//     in RTL is the visual *right*.
//
// macOS TextEdit (and most native RTL inputs) implement visual-direction
// movement: arrow keys move in the direction printed on the key regardless of
// run direction. Per `default_text_editing_shortcuts.dart` LogicalKeyboardKey
// .arrowRight is bound to ExtendSelectionByCharacterIntent(forward: true) — a
// purely logical "forward" — so the visual flip in RTL is unaddressed.
//
// Expected today: this test FAILS, demonstrating that ArrowRight in an RTL
// paragraph still walks toward a HIGHER logical offset (visual left). A pass
// would mean visual-order navigation has landed.

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('ArrowRight in RTL TextField moves caret visually right '
      '(toward a SMALLER logical offset)', (WidgetTester tester) async {
    // Four-character Arabic word; in logical order: 'ش'(0), 'س'(1), 'ي'(2), 'ب'(3).
    // Visually rendered RTL: 'ش' is rightmost, 'ب' leftmost.
    final TextEditingController controller =
        TextEditingController(text: 'شسيب');
    addTearDown(controller.dispose);
    final FocusNode focus = FocusNode();
    addTearDown(focus.dispose);

    await tester.pumpWidget(
      MaterialApp(
        home: Directionality(
          textDirection: TextDirection.rtl,
          child: Scaffold(
            body: Center(
              child: TextField(
                controller: controller,
                focusNode: focus,
                autofocus: true,
              ),
            ),
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();
    expect(focus.hasFocus, isTrue);

    // Place caret between logical positions 2 and 3 (between ي and ب).
    controller.selection = const TextSelection.collapsed(offset: 2);
    await tester.pump();
    expect(controller.selection.baseOffset, 2);

    await tester.sendKeyEvent(LogicalKeyboardKey.arrowRight);
    await tester.pump();

    // Visual-right semantics in an RTL paragraph: the physical Right arrow
    // should move the caret toward the right edge of the screen, which in an
    // RTL string corresponds to a SMALLER logical offset (the right-most
    // glyph 'ش' has logical offset 0).
    //
    // Today's behavior: the offset advances to 3 (logical-forward / visual-
    // left). The expectation below therefore fails until visual-order arrow
    // navigation is implemented.
    expect(
      controller.selection.baseOffset,
      lessThan(2),
      reason: 'ArrowRight in an RTL paragraph should move the caret visually '
          'right, which is a SMALLER logical offset. Got '
          '${controller.selection.baseOffset} — caret moved visually LEFT, '
          'demonstrating issue #78660.',
    );
  });
}

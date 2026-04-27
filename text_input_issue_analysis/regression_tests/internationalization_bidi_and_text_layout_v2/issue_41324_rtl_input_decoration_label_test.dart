// Copyright 2014 The Flutter Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Regression probe for https://github.com/flutter/flutter/issues/41324
//
// Bug: When a TextField has `textDirection: TextDirection.rtl` set and an
// `InputDecoration(labelText: ...)`, the floating label was reported to be
// left-aligned even though the field's resolved direction is RTL. The
// reporter said `hintText` and the user-typed input were correctly right-
// aligned, but `labelText` was not.
//
// Status check: Material 3 InputDecorator now resolves the label position
// from the same TextDirection used by the field, and `test/material/
// input_decorator_test.dart:2331` already asserts this for `buildInput-
// Decorator(textDirection: TextDirection.rtl)`. This regression probe
// targets the *exact* shape from the bug report — `textDirection` set on
// the `TextField` itself rather than via a surrounding `Directionality` —
// to verify the fix covers that wiring too.
//
// Expected: with current Material 3 defaults the label is right-aligned in
// the RTL TextField, so this test should PASS, indicating the bug is no
// longer reproducible with the latest defaults.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('labelText is right-aligned when TextField has '
      'textDirection: TextDirection.rtl (M3 default)',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          // Outer Directionality is LTR — the bug scenario sets RTL only on
          // the field, not via an enclosing Directionality.
          body: Center(
            child: SizedBox(
              width: 300,
              child: TextField(
                textDirection: TextDirection.rtl,
                decoration: const InputDecoration(
                  labelText: 'Email',
                  hintText: 'hint',
                ),
              ),
            ),
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();

    final Finder labelFinder = find.text('Email');
    final Finder fieldFinder = find.byType(TextField);
    expect(labelFinder, findsOneWidget);

    final Rect labelRect = tester.getRect(labelFinder);
    final Rect fieldRect = tester.getRect(fieldFinder);

    // In RTL, the label's right edge should be near the field's right edge.
    // The InputDecorator inserts a small content-padding gap (~16 px in M3),
    // so allow a generous tolerance.
    final double rightEdgeDelta = (fieldRect.right - labelRect.right).abs();
    final double leftEdgeDelta = (labelRect.left - fieldRect.left).abs();

    expect(
      rightEdgeDelta,
      lessThan(40),
      reason: 'In RTL, labelText should be aligned near the field\'s right '
          'edge. labelRect=$labelRect, fieldRect=$fieldRect, '
          'rightEdgeDelta=$rightEdgeDelta.',
    );
    expect(
      rightEdgeDelta,
      lessThan(leftEdgeDelta),
      reason: 'In RTL, label\'s right edge should be CLOSER to the field\'s '
          'right edge than label\'s left edge is to field\'s left edge. '
          'rightEdgeDelta=$rightEdgeDelta, leftEdgeDelta=$leftEdgeDelta.',
    );
  });
}

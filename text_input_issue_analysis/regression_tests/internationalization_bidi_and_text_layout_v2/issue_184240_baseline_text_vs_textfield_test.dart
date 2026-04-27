// Copyright 2014 The Flutter Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Regression probe for https://github.com/flutter/flutter/issues/184240
//
// Bug: A `Text` widget and a collapsed `TextField` (using
// `InputDecoration.collapsed(...)`) styled with the *same* `TextStyle` —
// notably the same `leadingDistribution` and `height` — do not lay out at
// the same baseline. When `TextLeadingDistribution.proportional` is used
// the TextField sits visibly higher or lower than the Text containing the
// same glyph. Reporter expects the two widgets to have matching alphabetic
// baselines when given identical styles inside a baseline-aligned Row.
//
// Probe approach: render `Text('X', style: style)` and a collapsed
// `TextField(style: style)` containing 'X' inside a baseline-aligned Row.
// Run the comparison once for each `TextLeadingDistribution` value.
// Compare both bottom Y (baseline + same-glyph descender) AND intrinsic
// height — the bug body says the TextField goes "high or low" depending on
// leading distribution, which manifests as a height/extent mismatch even
// when baseline alignment forces the bottoms to match.
//
// Expected: at least one of the two leadingDistribution variants exposes a
// height mismatch between Text and the collapsed TextField. If both pass
// the framework probably already aligns them correctly and the test is a
// regression guard rather than a fail-as-expected witness.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

Future<void> _run(WidgetTester tester, TextLeadingDistribution dist) async {
  final TextStyle style = TextStyle(
    inherit: false,
    fontSize: 180,
    height: 1,
    letterSpacing: 0,
    textBaseline: TextBaseline.alphabetic,
    leadingDistribution: dist,
    color: const Color(0xFF000000),
  );

  final TextEditingController controller = TextEditingController(text: 'X');
  addTearDown(controller.dispose);

  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: Center(
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: <Widget>[
              Text('X', style: style),
              SizedBox(
                width: 200,
                child: TextField(
                  controller: controller,
                  style: style,
                  decoration: const InputDecoration.collapsed(hintText: ''),
                ),
              ),
            ],
          ),
        ),
      ),
    ),
  );
  await tester.pumpAndSettle();

  final Rect textRect = tester.getRect(find.text('X').first);
  final Rect fieldRect = tester.getRect(find.byType(TextField));

  // Baseline-aligned Row: glyph bottoms must coincide for the same 'X'.
  final double bottomDelta = (textRect.bottom - fieldRect.bottom).abs();
  expect(
    bottomDelta,
    lessThan(2),
    reason: 'Text vs collapsed TextField (leadingDistribution=$dist) — '
        'baseline-aligned bottoms should agree. textRect=$textRect, '
        'fieldRect=$fieldRect, bottomDelta=$bottomDelta.',
  );

  // Height parity: with the same fontSize/height/leadingDistribution the
  // intrinsic vertical extent of the rendered glyph + leading should match.
  // The bug body claims TextField "goes high or low" — observable as a
  // height delta even with baseline alignment.
  final double heightDelta = (textRect.height - fieldRect.height).abs();
  expect(
    heightDelta,
    lessThan(2),
    reason: 'Text vs collapsed TextField (leadingDistribution=$dist) — '
        'intrinsic heights should agree for identical TextStyles. '
        'textHeight=${textRect.height}, fieldHeight=${fieldRect.height}, '
        'heightDelta=$heightDelta.',
  );
}

void main() {
  testWidgets('Text and collapsed TextField agree on baseline + height '
      'with leadingDistribution: proportional', (WidgetTester tester) async {
    await _run(tester, TextLeadingDistribution.proportional);
  });

  testWidgets('Text and collapsed TextField agree on baseline + height '
      'with leadingDistribution: even', (WidgetTester tester) async {
    await _run(tester, TextLeadingDistribution.even);
  });
}

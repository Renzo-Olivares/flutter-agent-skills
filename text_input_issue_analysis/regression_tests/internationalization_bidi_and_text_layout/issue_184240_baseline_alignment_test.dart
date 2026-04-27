import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

// https://github.com/flutter/flutter/issues/184240
// Bug: Vertical baseline alignment mismatch between Text and collapsed TextField
// when changing TextLeadingDistribution.
// Expected failure: The baseline of the Text widget and the TextField (with InputDecoration.collapsed)
// should be aligned when they have the same font style and are in a Row with crossAxisAlignment: CrossAxisAlignment.baseline.

void main() {
  testWidgets('Baseline alignment between Text and collapsed TextField', (WidgetTester tester) async {
    final Key textKey = GlobalKey();
    final Key textFieldKey = GlobalKey();

    const TextStyle style = TextStyle(
      fontSize: 20,
      textBaseline: TextBaseline.alphabetic,
      leadingDistribution: TextLeadingDistribution.even, // Triggers the bug based on the issue title
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Row(
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: <Widget>[
              Text(
                'Baseline',
                key: textKey,
                style: style,
              ),
              Expanded(
                child: TextField(
                  key: textFieldKey,
                  style: style,
                  decoration: const InputDecoration.collapsed(hintText: 'Baseline'),
                ),
              ),
            ],
          ),
        ),
      ),
    );

    await tester.pumpAndSettle();

    final Offset textOffset = tester.getTopLeft(find.byKey(textKey));
    final Offset textFieldOffset = tester.getTopLeft(find.byType(EditableText));

    expect(
      textOffset.dy,
      closeTo(textFieldOffset.dy, 0.1),
      reason: 'Text and collapsed TextField should share the same vertical baseline alignment',
    );
  });
}

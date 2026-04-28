// https://github.com/flutter/flutter/issues/184240
// Bug summary: When using a TextField with InputDecoration.collapsed and
// TextLeadingDistribution.proportional, its baseline alignment does not match
// a plain Text widget with the identical TextStyle.
// Expected failure mode today: The Y-offsets of the Text and TextField will
// differ significantly when aligned in a Row with CrossAxisAlignment.baseline.
// Test assertion: The test aligns both widgets by baseline and asserts their
// top Y-coordinates match.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('TextField with proportional leading matches Text baseline', (WidgetTester tester) async {
    const textStyle = TextStyle(
      fontSize: 50,
      leadingDistribution: TextLeadingDistribution.proportional,
    );
    
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Row(
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              const Text('X', style: textStyle),
              Expanded(
                child: TextField(
                  controller: TextEditingController(text: 'X'),
                  style: textStyle,
                  decoration: const InputDecoration.collapsed(hintText: ''),
                ),
              ),
            ],
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();
    
    final RenderBox textBox = tester.renderObject(find.byType(Text).first);
    final RenderBox textFieldBox = tester.renderObject(find.byType(TextField));
    
    final double textY = textBox.localToGlobal(Offset.zero).dy;
    final double textFieldY = textFieldBox.localToGlobal(Offset.zero).dy;
    
    // We expect the tops to be aligned if they are both 'X' and baseline-aligned correctly
    expect(textFieldY, closeTo(textY, 2.0));
  });
}

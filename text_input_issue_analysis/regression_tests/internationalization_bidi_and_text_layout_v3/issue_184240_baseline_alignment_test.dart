import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Text and collapsed TextField align vertically with TextLeadingDistribution.even', (WidgetTester tester) async {
    const textStyleEven = TextStyle(
      inherit: false,
      fontSize: 50,
      height: 1,
      textBaseline: TextBaseline.alphabetic,
      leadingDistribution: TextLeadingDistribution.even,
      color: Colors.black,
    );

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Row(
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              Text('Test', style: textStyleEven),
              Expanded(
                child: TextField(
                  controller: TextEditingController(text: 'Test'),
                  style: textStyleEven,
                  decoration: const InputDecoration.collapsed(hintText: ''),
                ),
              ),
            ],
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();

    final Finder textFinder = find.byType(Text).first;
    final Finder textFieldFinder = find.byType(EditableText);

    final RenderBox textRenderBox = tester.renderObject(textFinder);
    final RenderBox textFieldRenderBox = tester.renderObject(textFieldFinder);

    final double textY = textRenderBox.localToGlobal(Offset.zero).dy;
    final double textFieldY = textFieldRenderBox.localToGlobal(Offset.zero).dy;

    // We expect the Y offsets to be very close if they are aligned properly.
    // If there's a mismatch, they will differ.
    expect((textY - textFieldY).abs(), lessThan(1.0), reason: "Text and TextField should align vertically");
  });
}

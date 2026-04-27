import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('TextField labelText is right-aligned in RTL', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: Directionality(
          textDirection: TextDirection.rtl,
          child: TextField(
            decoration: InputDecoration(
              labelText: 'label Email',
            ),
          ),
        ),
      ),
    ));
    await tester.pumpAndSettle();

    // Find the label text widget
    final Finder labelFinder = find.text('label Email');
    expect(labelFinder, findsOneWidget);

    // Get the position of the label and the text field
    final RenderBox labelBox = tester.renderObject(labelFinder);
    final RenderBox textFieldBox = tester.renderObject(find.byType(TextField));

    // In RTL, the label should be near the right edge of the text field.
    // That means the distance from the right edge of the label to the right edge
    // of the text field should be small (e.g. padding).
    final double labelRight = labelBox.localToGlobal(Offset(labelBox.size.width, 0)).dx;
    final double textFieldRight = textFieldBox.localToGlobal(Offset(textFieldBox.size.width, 0)).dx;

    // Check if the label is right-aligned (closer to the right edge than the left edge)
    final double labelLeft = labelBox.localToGlobal(Offset.zero).dx;
    final double textFieldLeft = textFieldBox.localToGlobal(Offset.zero).dx;
    
    final double distToRight = textFieldRight - labelRight;
    final double distToLeft = labelLeft - textFieldLeft;

    // The test asserts the label is closer to the right edge than the left edge
    expect(distToRight < distToLeft, isTrue, reason: "Label should be closer to right edge in RTL");
  });
}

// https://github.com/flutter/flutter/issues/41324
// Bug summary: When using a TextField with TextDirection.rtl, the labelText
// is not correctly aligned to the right. It seems to ignore the RTL text direction.
// Expected failure mode today: The label widget's right edge does not align 
// closely with the TextField's right edge.
// Test assertion: The test renders an RTL TextField with a labelText and verifies
// that the right side of the label's RenderBox is close to the right side of the TextField.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('RTL labelText aligns to the right', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Padding(
            padding: EdgeInsets.all(30.0),
            child: TextField(
              textDirection: TextDirection.rtl,
              decoration: InputDecoration(
                labelText: 'label Email',
              ),
            ),
          ),
        ),
      ),
    );
    await tester.pumpAndSettle();

    final Finder labelFinder = find.text('label Email');
    expect(labelFinder, findsOneWidget);
    
    final RenderBox labelBox = tester.renderObject(labelFinder);
    final RenderBox textFieldBox = tester.renderObject(find.byType(TextField));
    
    final double labelRight = labelBox.localToGlobal(Offset(labelBox.size.width, 0)).dx;
    final double textFieldRight = textFieldBox.localToGlobal(Offset(textFieldBox.size.width, 0)).dx;
    
    expect(labelRight, closeTo(textFieldRight, 20.0));
  });
}

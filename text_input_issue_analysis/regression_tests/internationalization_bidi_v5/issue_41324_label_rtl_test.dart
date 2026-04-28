import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

// https://github.com/flutter/flutter/issues/41324
// labelText should be right-aligned when TextDirection is rtl.
// Currently it might align to the left incorrectly.
// We assert the alignment of the label widget.

void main() {
  testWidgets('TextField labelText respects TextDirection.rtl', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
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
      ),
    );

    // Find the AnimatedDefaultTextStyle that contains the labelText
    final Finder labelTextFinder = find.text('label Email');
    expect(labelTextFinder, findsOneWidget);
    
    // We get the offset of the label
    final Offset labelOffset = tester.getTopLeft(labelTextFinder);
    final Offset textFieldOffset = tester.getTopLeft(find.byType(TextField));
    
    // In RTL, the label should be on the right side of the TextField.
    // If it's on the left side, the x offset would be close to textFieldOffset.dx
    // Let's just print the offset to see what happens.
    // The test will check if it's on the right half.
    final Size textFieldSize = tester.getSize(find.byType(TextField));
    expect(labelOffset.dx, greaterThan(textFieldOffset.dx + textFieldSize.width / 2), reason: "Label should be right-aligned");
  });
}

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

// https://github.com/flutter/flutter/issues/41324
// Bug: TextField labelText does not right-align properly when TextDirection is RTL.
// Expected failure: The labelText widget (typically an AnimatedBuilder/Text) is expected
// to be positioned on the right side of the TextField.
// We assert that the x-coordinate of the label is towards the right side of the field.

void main() {
  testWidgets('RTL labelText alignment in TextField', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 400,
            child: TextField(
              decoration: InputDecoration(
                labelText: 'الاسم',
              ),
              textDirection: TextDirection.rtl,
            ),
          ),
        ),
      ),
    );

    await tester.pumpAndSettle();

    final Finder labelFinder = find.text('الاسم');
    expect(labelFinder, findsOneWidget);

    final Offset labelTopLeft = tester.getTopLeft(labelFinder);
    final Size labelSize = tester.getSize(labelFinder);
    
    // In RTL, the right edge of the label should be near the right edge of the TextField.
    // The TextField is 400 pixels wide (from x = 0 to x = 400).
    // The right edge of the label should be close to 400.
    final double labelRightEdge = labelTopLeft.dx + labelSize.width;
    
    // Assuming some padding (e.g., 12.0 or 16.0), the right edge should be > 350.
    expect(labelRightEdge, greaterThan(350.0), reason: 'Label should be aligned to the right in RTL');
  });
}

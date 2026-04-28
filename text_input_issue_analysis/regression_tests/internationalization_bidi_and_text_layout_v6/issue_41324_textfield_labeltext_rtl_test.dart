// URL: https://github.com/flutter/flutter/issues/41324
// Bug: labelText in InputDecoration does not align right when TextDirection is RTL.
// Expected failure: The labelText (a Text widget inside InputDecoration) might be positioned on the left despite RTL.
// Assert: We check the dx offset of the label text to see if it's placed on the right side of the TextField.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('TextField labelText right-aligns in RTL', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Directionality(
            textDirection: TextDirection.rtl,
            child: TextField(
              decoration: InputDecoration(
                labelText: 'Label',
              ),
            ),
          ),
        ),
      ),
    );

    final Finder labelFinder = find.text('Label');
    expect(labelFinder, findsOneWidget);

    final Offset labelTopLeft = tester.getTopLeft(labelFinder);
    
    // In RTL, the label should be on the right side.
    // The screen is 800 wide by default. The TextField takes the whole width.
    // If it's on the right, its left offset should be significantly > 0.
    expect(labelTopLeft.dx, greaterThan(400.0));
  });
}

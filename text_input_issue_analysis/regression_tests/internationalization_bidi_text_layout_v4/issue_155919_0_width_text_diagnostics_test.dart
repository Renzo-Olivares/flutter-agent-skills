// https://github.com/flutter/flutter/issues/155919
// Bug summary: A null assertion fires in RenderParagraph when its width is
// constrained to 0 (e.g. inside an Expanded in a 0-width Row) and its
// diagnostics/children are queried.
// Expected failure mode today: Calling debugDescribeChildren on the
// RenderParagraph throws an assertion or null pointer error.
// Test assertion: The test renders a Text widget in a 0-width constraint
// and asserts that calling debugDescribeChildren returns normally.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Text inside Expanded in 0-width Row does not throw during debugDescribeChildren', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 0,
            child: Row(
              children: [
                Expanded(
                  child: Text('Spam'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
    
    final RenderBox textRenderBox = tester.renderObject(find.byType(Text));
    expect(() => textRenderBox.debugDescribeChildren(), returnsNormally);
    
    expect(tester.takeException(), isNull);
  });
}

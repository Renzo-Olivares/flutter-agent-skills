import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

// https://github.com/flutter/flutter/issues/155919
// Bug: Error where possible null is being asserted in rendering paragraph
// when BoxConstraints width collapses to 0.

void main() {
  testWidgets('RenderParagraph zero width does not crash', (WidgetTester tester) async {
    // We pump a Row with an Expanded Text and another Text, constrained to 0 width.
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: SizedBox(
            width: 0,
            child: Row(
              children: <Widget>[
                Expanded(child: Text('some')),
                Text('text'),
              ],
            ),
          ),
        ),
      ),
    );

    // If it doesn't crash, we're good. If it does, we expect the test to fail.
    // The issue says it happens during layout/paint.
    await tester.pumpAndSettle();
    
    // Check if there are any exceptions.
    final dynamic exception = tester.takeException();
    if (exception != null) {
      fail('Expected no exception, but got: $exception');
    }
  });
}

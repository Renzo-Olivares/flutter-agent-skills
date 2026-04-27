import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

// https://github.com/flutter/flutter/issues/38503
// Bug: TextField doesn't appear within a direction:Axis.vertical Wrap
// Expected failure: The test should throw an assertion error related to unbounded width in InputDecorator.

void main() {
  testWidgets('TextField inside a vertical Wrap throws unbounded width exception', (WidgetTester tester) async {
    // We expect the pumpWidget to throw a FlutterError (assertion about unbounded constraints).
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Wrap(
            direction: Axis.vertical,
            children: <Widget>[
              TextField(),
            ],
          ),
        ),
      ),
    );
  });
}

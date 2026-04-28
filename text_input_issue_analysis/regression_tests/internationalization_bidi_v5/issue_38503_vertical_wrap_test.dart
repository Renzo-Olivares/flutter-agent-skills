import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

// https://github.com/flutter/flutter/issues/38503
// TextField inside a vertical Wrap throws an unbounded width assertion.
// We expect this test to fail because InputDecorator currently requires a bounded width
// which a vertical Wrap does not provide.

void main() {
  testWidgets('TextField in vertical Wrap throws unbounded width assertion', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Wrap(
            direction: Axis.vertical,
            children: const [
              TextField(),
            ],
          ),
        ),
      ),
    );
  });
}

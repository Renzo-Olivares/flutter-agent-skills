// https://github.com/flutter/flutter/issues/38503
// Bug summary: A TextField placed directly inside a Wrap with
// direction: Axis.vertical throws an unbounded width exception.
// Expected failure mode today: Pumping the widget throws a layout exception
// indicating unbounded constraints.
// Test assertion: The test attempts to render a TextField inside a vertical
// Wrap and asserts no exception is thrown.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('TextField in vertical Wrap does not throw', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: Scaffold(
          body: Wrap(
            direction: Axis.vertical,
            children: [
              TextField(),
            ],
          ),
        ),
      ),
    );
    
    expect(tester.takeException(), isNull);
  });
}

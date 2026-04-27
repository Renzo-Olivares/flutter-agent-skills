import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('TextField in vertical Wrap does not throw unbounded width exception', (WidgetTester tester) async {
    // The issue says TextField throws "An InputDecorator, which is typically created by a TextField, cannot have an unbounded width."
    // when placed in a Wrap with direction: Axis.vertical.
    
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: Center(
          child: Wrap(
            direction: Axis.vertical,
            children: <Widget>[
              TextField(controller: TextEditingController(text: "123"))
            ],
          ),
        ),
      ),
    ));

    // If it doesn't throw, we expect to find the TextField.
    expect(find.byType(TextField), findsOneWidget);
  });
}

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

// https://github.com/flutter/flutter/issues/155919
// Asserts that a Text widget inside an Expanded with 0 width constraint does not throw null assertion.

void main() {
  testWidgets('RenderParagraph with 0 width constraint does not crash', (WidgetTester tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Row(
            children: [
              Expanded(child: Text("some text")),
              SizedBox(
                width: 0,
                child: Text("zero width text"),
              )
            ],
          ),
        ),
      ),
    );
    expect(tester.takeException(), isNull);
  });
}

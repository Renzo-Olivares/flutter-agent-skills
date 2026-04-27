import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Text in a squished Row does not throw null assertion', (WidgetTester tester) async {
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: SizedBox(
          width: 0,
          child: Row(
            children: const [
              Expanded(child: Text("some")),
              Text("text")
            ],
          ),
        ),
      ),
    ));

    expect(tester.takeException(), isNull);
  });
}

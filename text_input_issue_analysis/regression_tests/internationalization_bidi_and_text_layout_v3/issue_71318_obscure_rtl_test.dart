import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_test/flutter_test.dart';

// https://github.com/flutter/flutter/issues/71318
// Bug: In an RTL text field with obscureText=true, typing LTR characters causes the cursor
// to appear on the left (wrong side visually) while typing.
void main() {
  testWidgets('Cursor appears on the correct side for obscured LTR text in RTL TextField', (WidgetTester tester) async {
    final TextEditingController controller = TextEditingController();

    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: Directionality(
          textDirection: TextDirection.rtl,
          child: TextField(
            controller: controller,
            obscureText: true,
            autofocus: true,
          ),
        ),
      ),
    ));
    await tester.pumpAndSettle();

    // Type LTR letters "ab"
    await tester.enterText(find.byType(TextField), 'ab');
    await tester.pumpAndSettle();

    final EditableTextState state = tester.state(find.byType(EditableText));
    final RenderEditable renderEditable = state.renderEditable;
    
    final Offset caretOffset = renderEditable.getEndpointsForSelection(
      const TextSelection.collapsed(offset: 2),
    ).last.point;
    
    final Offset caretOffset1 = renderEditable.getEndpointsForSelection(
      const TextSelection.collapsed(offset: 1),
    ).last.point;

    // We expect the text to be laid out visually left-to-right (because it's LTR text).
    // So cursor for offset 2 should have a greater dx than cursor for offset 1.
    // However, because obscureText forces • characters which are neutral, they adopt RTL,
    // so they are laid out right-to-left. Therefore, caretOffset.dx will be < caretOffset1.dx,
    // which confirms the bug.
    expect(caretOffset.dx, greaterThan(caretOffset1.dx), reason: "Caret should move right for LTR input even if obscured");
  });
}

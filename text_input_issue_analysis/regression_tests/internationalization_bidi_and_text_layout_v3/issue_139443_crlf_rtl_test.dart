import 'package:flutter/material.dart';
import 'package:flutter/rendering.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Caret position is correct for RTL text with CRLF', (WidgetTester tester) async {
    final TextEditingController controller = TextEditingController(text: 'آب\r\nداد');
    
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: TextField(
          controller: controller,
          textDirection: TextDirection.rtl,
          maxLines: null,
          autofocus: true,
        ),
      ),
    ));
    await tester.pumpAndSettle();

    final EditableTextState state = tester.state(find.byType(EditableText));
    final RenderEditable renderEditable = state.renderEditable;
    
    final Offset caretOffsetCRLF = renderEditable.getEndpointsForSelection(
      const TextSelection.collapsed(offset: 4), // After \r\n
    ).last.point;
    
    controller.text = 'آب\نداد';
    await tester.pumpAndSettle();
    
    final Offset caretOffsetLF = renderEditable.getEndpointsForSelection(
      const TextSelection.collapsed(offset: 3), // After \n
    ).last.point;
    
    expect(caretOffsetCRLF.dx, caretOffsetLF.dx);
  });
}

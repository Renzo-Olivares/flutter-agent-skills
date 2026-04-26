// Regression test for https://github.com/flutter/flutter/issues/150338
// "onFieldSubmitted is not triggered in desktop platforms when
//  `readOnly: true` is set in TextFormField"
//
// Root cause (per commenter diagnosis): `_shouldCreateInputConnection`
// returns `false` for `readOnly: true` on non-web desktop, blocking
// `TextInputConnection` creation and therefore `onFieldSubmitted`. Web
// short-circuits `kIsWeb` to `true`.
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets(
    'readOnly TextFormField on desktop still fires onFieldSubmitted on Enter',
    (WidgetTester tester) async {
      debugDefaultTargetPlatformOverride = TargetPlatform.windows;
      addTearDown(() => debugDefaultTargetPlatformOverride = null);

      String? submitted;
      final FocusNode focusNode = FocusNode();
      addTearDown(focusNode.dispose);

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: TextFormField(
              focusNode: focusNode,
              readOnly: true,
              initialValue: 'hello',
              onFieldSubmitted: (String value) {
                submitted = value;
              },
            ),
          ),
        ),
      );

      focusNode.requestFocus();
      await tester.pump();

      await tester.sendKeyEvent(LogicalKeyboardKey.enter);
      await tester.pump();

      expect(
        submitted,
        'hello',
        reason:
            'onFieldSubmitted should fire on Enter even when '
            'readOnly: true on desktop platforms. Currently blocked '
            'by _shouldCreateInputConnection returning false. See '
            'https://github.com/flutter/flutter/issues/150338',
      );
    },
  );
}

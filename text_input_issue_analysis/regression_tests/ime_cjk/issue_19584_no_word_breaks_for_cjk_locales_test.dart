// Regression test for https://github.com/flutter/flutter/issues/19584
// "No word-breaks for CJK locales"
//
// Flutter's bundled ICU data (`icudtl.dat`) uses Chromium's Android ICU build,
// which omits the CJK dictionary required for word-break detection in
// Chinese/Japanese text. Without that dictionary, `TextPainter.getWordBoundary`
// returns single-character ranges for CJK text instead of true word ranges,
// so double-tap / long-press word selection only picks up one character at a
// time.
//
// The repro on the issue uses "你好吗" (nǐ hǎo ma — "how are you?"), where the
// first two characters (你好, "hello") form one word. Long-pressing either
// character should select both.
//
// Expected failure mode today: the word boundary at offset 0 has length 1,
// because the engine's ICU tokenizer treats each CJK glyph as its own word.
// When the CJK dictionary ships (or the framework delegates to platform
// tokenizers), the boundary should span multiple characters.
import 'package:flutter/painting.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('getWordBoundary groups multi-character CJK words in Chinese text', () {
    const String text = '你好吗';
    final TextPainter painter = TextPainter(
      text: const TextSpan(text: text),
      textDirection: TextDirection.ltr,
    )..layout();
    addTearDown(painter.dispose);

    final TextRange boundary = painter.getWordBoundary(
      const TextPosition(offset: 0),
    );
    expect(
      boundary.end - boundary.start,
      greaterThan(1),
      reason:
          'CJK word-break detection should group "你好" as a single word. '
          'Single-character boundaries indicate the engine ICU data lacks '
          'the CJK dictionary. See '
          'https://github.com/flutter/flutter/issues/19584',
    );
  });

  test('getWordBoundary groups multi-character CJK words in Japanese text', () {
    // "日本語学校" means "Japanese language school"; the last two characters
    // (学校 — "school") should form one word.
    const String text = '日本語学校';
    final TextPainter painter = TextPainter(
      text: const TextSpan(text: text),
      textDirection: TextDirection.ltr,
    )..layout();
    addTearDown(painter.dispose);

    // offset 3 falls inside "学校"; boundary should span 3..5.
    final TextRange boundary = painter.getWordBoundary(
      const TextPosition(offset: 3),
    );
    expect(
      boundary.end - boundary.start,
      greaterThan(1),
      reason:
          'Japanese word "学校" at offsets 3..5 should be detected as a single '
          'word. See https://github.com/flutter/flutter/issues/19584',
    );
  });
}

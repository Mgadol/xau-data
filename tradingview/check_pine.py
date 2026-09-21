#!/usr/bin/env python3
"""Pine файлыг TradingView-д буулгахаас ӨМНӨ шалгана.

Pine-ийн хамгийн хачирхалтай дүрэм: **мөр үргэлжлүүлэхэд доголын зай нь
4-т ХУВААГДАХ ЁСГҮЙ**. Хуваагдвал Pine түүнийг шинэ БЛОК гэж ойлгоод
«Syntax error at input "end of line without line continuation"»
(CE10156) гэж унана.

Python-д сурсан 4, 8, 12 зайн зуршил нь энд яг эсрэгээрээ ажиллана —
тиймээс энэ алдаа нүдэнд огт харагддаггүй. Нэг удаа гаргасан тул
машинаар барина.

Мөн шалгах зүйлс: хаалтын тэнцвэр, хаагдаагүй хашилт, ТАБ тэмдэгт,
ашиглагдаагүй хувьсагч, `ta.*` функцийг гурвалсан илэрхийлэл дотор
дуудсан эсэх (түүх нь тасарч чимээгүй буруу тоо өгдөг).

    python3 check_pine.py shahalt.pine
"""
import re
import sys

# `=>` нь функцийн тодорхойлолт — түүний дараах догол 4 нь ЗӨВ (бие нь).
CONT_END = ('?', ':', '+', '-', '*', '/', '%', ',', '(', '[', '=', '>', '<',
            'and', 'or', 'not')
STATEFUL = ('ta.barssince', 'ta.valuewhen', 'ta.highest', 'ta.lowest',
            'ta.crossover', 'ta.crossunder', 'ta.change', 'ta.cum')


def code_only(s):
    """Тайлбарыг хасаж, бичвэрийг `S` тэмдэгтээр солино.

    Бичвэрийг УСТГАВАЛ `x := "утга"` нь `x :=` болж, мөр оператороор
    төгссөн мэт харагдана — улмаар жинхэнэ блокийг үргэлжлэл гэж
    андуурна. Тиймээс устгахгүй, орлуулна.
    """
    out, q, j = [], False, 0
    while j < len(s):
        c = s[j]
        if q:
            if c == '\\':
                j += 2
                continue
            if c == '"':
                q = False
            j += 1
            continue
        if c == '"':
            q = True
            out.append('S')
            j += 1
            continue
        if c == '/' and j + 1 < len(s) and s[j + 1] == '/':
            break
        out.append(c)
        j += 1
    return ''.join(out).rstrip(), q


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'shahalt.pine'
    lines = open(path, encoding='utf-8').read().split('\n')
    body = '\n'.join(lines)
    errs, warns = [], []
    depth = 0
    declared = {}

    for i, ln in enumerate(lines, 1):
        if '\t' in ln:
            errs.append(f'{i}: ТАБ тэмдэгт — Pine зөвхөн зай хүлээнэ')
        code, unclosed = code_only(ln)
        if unclosed:
            errs.append(f'{i}: хаагдаагүй хашилт')
        depth += (code.count('(') + code.count('[')
                  - code.count(')') - code.count(']'))
        if depth < 0:
            errs.append(f'{i}: илүү хаах хаалт')
            depth = 0

        # ── Гол шалгалт: үргэлжлэлийн доголын зай ──────────────────
        if i > 1 and ln.strip() and not ln.lstrip().startswith('//'):
            ind = len(ln) - len(ln.lstrip(' '))
            prev, _ = code_only(lines[i - 2])
            # `=>`-ээр төгссөн нь функцийн тодорхойлолт — дараагийн
            # догол 4 нь түүний БИЕ, үргэлжлэл биш. (`>` нь CONT_END-д
            # байгаа тул тусад нь хасахгүй бол андуурна.)
            if (ind and ind % 4 == 0 and prev.endswith(CONT_END)
                    and not prev.endswith('=>')):
                errs.append(
                    f'{i}: үргэлжлэлийн мөрийн догол {ind} зай — 4-т '
                    f'хуваагдаж байна. {ind + 1} болго (CE10156)')

        # ── Төлөвтэй функц гурвалсан илэрхийлэл дотор ──────────────
        for fn in STATEFUL:
            if fn in code and '?' in code:
                if code.index('?') < code.index(fn):
                    warns.append(
                        f'{i}: {fn}() гурвалсан илэрхийлэл ДОТОР — түүх нь '
                        f'тасарч буруу тоо өгнө. Гадна нь бодож ав.')

        m = re.match(r'^(?:var\s+\w+\s+)?(\w+)\s*=[^=]', code)
        if m and not code.lstrip().startswith(('if ', 'else')):
            declared.setdefault(m.group(1), i)

    if depth:
        errs.append(f'файлын төгсгөлд {depth} хаалт хаагдаагүй')

    groups = {k for k in declared if re.match(r'^g[A-Z]?[a-z]?$', k)}
    unused = [(v, k) for k, v in declared.items()
              if k not in groups and len(re.findall(rf'\b{k}\b', body)) < 2]

    print(f'{path}: {len(lines)} мөр')
    for e in errs:
        print(f'  ✗ {e}')
    for w in warns:
        print(f'  ⚠ {w}')
    for v, k in sorted(unused):
        print(f'  ⚠ {v}: `{k}` зарлагдсан ч ашиглагдаагүй')
    if not errs:
        print('  ✓ алдаа олдсонгүй')
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main())

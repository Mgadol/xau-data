"""24. НЭЭЛТТЭЙ ХАЙЛТ — том хөдөлгөөний ӨМНӨ ямар нэг тэмдэг байна уу.

САНАА
  «Хандлага эргэх болон том хөдөлгөөн явахын өмнө ямар нэг маш жижиг
   дохио, алдаа юмуу байгаа эсэхийг шалга. Ямар нэг аргад баригдалгүй,
   бүх талаас нь.»

  a2–a23 хүртэл бид ХЭН НЭГНИЙ нэрлэсэн setup-ыг шалгаж байсан.
  Энд эсрэгээр: эхлээд ТОМ ХӨДӨЛГӨӨНИЙГ олоод, дараа нь түүний
  ӨМНӨХ цонхонд юу онцгой байсныг ХАЙНА.

ХОЁР АСУУЛТ — ЗААВАЛ САЛГАХ ЁСТОЙ
  A. Том хөдөлгөөн ИРЭХ гэж байгааг таамаглаж чадах уу?  (ХЭМЖЭЭ)
  B. Тэр хөдөлгөөн ХААШАА явахыг таамаглаж чадах уу?     (ЧИГЛЭЛ)

  Эдгээр огт өөр зүйл. Санхүүгийн судалгаанд A нь ТИЙМ гэж эртнээс
  мэдэгддэг (хэлбэлзэл бөөгнөрдөг — volatility clustering). B нь
  хамаагүй хэцүү. Хоёрыг хольвол «би дохио оллоо» гэж андуурна:
  хэмжээг таасан ч чиглэлгүй бол мөнгө гарахгүй.

АРГАЧЛАЛ
  1. Том хөдөлгөөн = ирээдүйн 6 барын үнэмлэхүй хөдөлгөөн нь
     тухайн үеийн ATR-аас X дахин их.
  2. Түүний ӨМНӨХ 20 барын цонхноос 16 шинж тооцно. Бүгд тэр
     мөчид мэдэгдэнэ — ирээдүй харахгүй.
  3. Шинж бүрийг 5 хэсэгт хувааж, том хөдөлгөөний магадлал ба
     чиглэл таах чадварыг хэмжинэ.

ОЛОН ХАРЬЦУУЛАЛТЫН АСУУДАЛ
  16 шинжийг шалгавал санамсаргүйгээр 1-2 нь «чухал» гарна.
  Тиймээс:
    • БҮХ шинжийн үр дүнг тайлагнана — сайныг нь түүхгүй
    • 2005–2016 / 2017–2025 гэж хувааж ДАВТАГДАХ эсэхийг хардаг
    • Нэг хугацаанд л гарсан бол санамсаргүй гэж үзнэ

═══════════════════════════════════════════════════════════════════
ҮР ДҮН
═══════════════════════════════════════════════════════════════════

A. ХЭМЖЭЭ — ТИЙМ, ТААМАГЛАГДАНА  (суурь 23.4%)

      ATR чиглэл        доод 20% → 29.4%   дээд 20% → 17.3%   (12.1)
      их бие / муж      27.6% → 20.6%                          (7.0)
      дараалсан чиглэл  24.1% → 21.7%                          (4.9)

   ATR нь БУУРЧ байсан үед том хөдөлгөөн илүү магадлалтай.
   Хоёр хугацаанд давтагдсан (14.8 → 7.5). Энэ нь санхүүгийн
   судалгаанд эртнээс мэдэгддэг ХЭЛБЭЛЗЛИЙН БӨӨГНӨРӨЛ.
   Шахалт тэлэлтийг ҮНЭХЭЭР дагуулдаг.

B. ЧИГЛЭЛ — ХЭВ МАЯГ БАЙНА  (том хөдөлгөөнүүдийн дотор)

      мужид эзлэх байрлал  48.4% → 61.5%   (13.1)  давтагдав 14.7→9.5
      SMA-аас зай          49.7% → 57.9%    (8.2)            9.7→4.0
      доторх барын тоо     58.0% → 51.7%    (6.4)            6.1→6.0

   Үнэ 20 барын мужийнхаа ДЭЭД хэсэгт байвал том хөдөлгөөн нь
   ДЭЭШ явах магадлал 61.5%. Энэ бол моментум.

   Босго өсөх тусам чиглэл ИЛҮҮ таамаглагдана:
      ≥1.5×ATR  зөрүү  9.5      ≥3×ATR  18.3
      ≥2.0×ATR        13.1      ≥4×ATR  24.2

C. ГЭВЧ АРИЛЖАА БОЛГОХОД — ДРИФТ Л ҮЛДЭВ

   Хамгийн сайн тохиргоо (стоп 3 ATR, TP 6 ATR):

      бүгд            +0.078R ±0.017  ✓
      2005–2016       +0.106R ✓        2017–2025  +0.042R ✗
      зөвхөн УРТ      +0.153R ✓        зөвхөн БОГИНО  −0.008R ✗
      спред $0.6      +0.056R ✓

   Тэгш хэм эвдэрсэн: урт ба богиногийн зөрүү 0.161R.

   ХЯНАЛТЫН ТЕСТ — САНАМСАРГҮЙ ОРОЛТ, ИЖИЛ ГЕОМЕТР:

      ДОХИОТОЙ урт              +0.153R
      САНАМСАРГҮЙ урт (дрифт)   +0.093R  ← зүгээр алт авсан нь
      ─────────────────────────────────
      дохионы цэвэр нэмэр       +0.060R

      ДОХИОТОЙ богино           −0.008R

   Ашгийн 60% нь «алт өссөн» гэдгээс гарч байна. Дохионы цэвэр
   нэмэр нь 0.060R бөгөөд богино талд огт ажиллахгүй.

   ШАХАЛТЫН ШҮҮЛТҮҮР ТУСЛААГҮЙ:
      зөвхөн чиглэл (шахалтгүй)  12632  +0.052R
      шахалт + чиглэл             4518  +0.078R
   Түүврийг 3 дахин багасгаад 0.026R л нэмэв — A нь ХЭМЖЭЭ
   таамагладаг болохоос ЧИГЛЭЛ таамагладаггүйн шууд нотолгоо.

ГОЛ СУРГАМЖ — A БА B-Г ХОЛИХ НЬ ХАМГИЙН ТҮГЭЭМЭЛ АЛДАА

  «Шахалтын дараа том хөдөлгөөн болно» гэдэг ҮНЭН (A батлагдсан).
  Үүнийг харсан хүн «дохио оллоо» гэж боддог. Гэтэл ХААШАА явахыг
  мэдэхгүй бол мөнгө гарахгүй.

  Энэ хайлт нь тэр хоёрыг тусад нь хэмжсэн цорын ганц тест.
  Хариу нь: хэмжээ таамаглагдана, чиглэл бараг үгүй, үлдсэн нь дрифт.
"""
import numpy as np
import pandas as pd
from core import load, resample

h = load(start='2005-01-01', end='2025-09-12')


def build(tf='4h', look=20, fwd=6):
    """Шинжүүд ба ирээдүйн хөдөлгөөнийг нэг хүснэгт болгоно."""
    d = resample(h, tf) if tf != '1h' else h.copy()
    o, hi, lo, c = (d['open'], d['high'], d['low'], d['close'])
    v = d['volume'].replace(0, np.nan)
    rng = hi - lo
    body = (c - o).abs()
    tr = np.maximum(rng, np.maximum((hi - c.shift()).abs(), (lo - c.shift()).abs()))
    atr = tr.rolling(look).mean()

    f = pd.DataFrame(index=d.index)
    # ── Хэлбэлзлийн бүтэц ──
    f['shahalt'] = tr.rolling(5).mean() / atr           # сүүлийн 5 / 20 ATR
    f['muj_agshilt'] = rng.rolling(3).mean() / rng.rolling(look).mean()
    f['atr_chig'] = atr / atr.shift(look)               # ATR өсөж буй эсэх
    # ── Лааны хэлбэр ──
    f['bie_hurwuu'] = body.rolling(5).mean() / rng.rolling(5).mean()
    f['deed_suul'] = ((hi - np.maximum(o, c)) / rng.replace(0, np.nan)).rolling(5).mean()
    f['dood_suul'] = ((np.minimum(o, c) - lo) / rng.replace(0, np.nan)).rolling(5).mean()
    f['suul_tegsh'] = f['deed_suul'] - f['dood_suul']
    # ── Эрчим (тик) ──
    f['erchim'] = v / v.rolling(look).mean()
    f['erchim_chig'] = v.rolling(5).mean() / v.rolling(look).mean()
    # ── Бүтэц ──
    ret = c.pct_change()
    f['dараалал'] = np.sign(ret).rolling(5).sum()       # дараалсан чиглэл
    f['auto'] = ret.rolling(look).corr(ret.shift(1))    # өөрийн хамаарал
    f['sma_zai'] = (c - c.rolling(look).mean()) / atr
    f['tuil_zai'] = (c - lo.rolling(look).min()) / (
        hi.rolling(look).max() - lo.rolling(look).min()).replace(0, np.nan)
    # ── Доторх бар, шахалтын тоо ──
    inside = (hi < hi.shift()) & (lo > lo.shift())
    f['dotorh'] = inside.rolling(look).sum()
    # ── Цэвэрлэгээ ──
    f['deesh_hamalt'] = (hi > hi.rolling(look).max().shift()).rolling(5).sum()
    f['doosh_hamalt'] = (lo < lo.rolling(look).min().shift()).rolling(5).sum()

    # ── ИРЭЭДҮЙ (зөвхөн ХЭМЖИХЭД, шинжид ОРОХГҮЙ) ──
    fwd_move = c.shift(-fwd) - c
    f['_hemjee'] = fwd_move.abs() / atr
    f['_chiglel'] = np.sign(fwd_move)
    f['_year'] = d.index.year
    return f.replace([np.inf, -np.inf], np.nan).dropna()


FEATS = ['shahalt', 'muj_agshilt', 'atr_chig', 'bie_hurwuu', 'deed_suul',
         'dood_suul', 'suul_tegsh', 'erchim', 'erchim_chig', 'dараалал',
         'auto', 'sma_zai', 'tuil_zai', 'dotorh', 'deesh_hamalt', 'doosh_hamalt']

NAMES = {'shahalt': 'шахалт (5/20 ATR)', 'muj_agshilt': 'муж агшилт',
         'atr_chig': 'ATR чиглэл', 'bie_hurwuu': 'их бие / муж',
         'deed_suul': 'дээд сүүл', 'dood_suul': 'доод сүүл',
         'suul_tegsh': 'сүүлийн тэгш бус', 'erchim': 'эрчим (сүүлийн бар)',
         'erchim_chig': 'эрчмийн чиглэл', 'dараалал': 'дараалсан чиглэл',
         'auto': 'өөрийн хамаарал', 'sma_zai': 'SMA-аас зай',
         'tuil_zai': 'мужид эзлэх байрлал', 'dotorh': 'доторх барын тоо',
         'deesh_hamalt': 'дээш хамалт', 'doosh_hamalt': 'доош хамалт'}


def q5(F, col):
    try:
        return pd.qcut(F[col], 5, labels=False, duplicates='drop')
    except ValueError:
        return None


def part_a(F, thr):
    """A. ХЭМЖЭЭ — том хөдөлгөөн ирэхийг таамаглаж чадах уу."""
    big = (F['_hemjee'] >= thr)
    base = big.mean() * 100
    rows = []
    for col in FEATS:
        q = q5(F, col)
        if q is None:
            continue
        g = big.groupby(q).mean() * 100
        rows.append((col, g.iloc[0], g.iloc[-1], g.max() - g.min()))
    rows.sort(key=lambda r: -r[3])
    return base, rows


def part_b(F, thr):
    """B. ЧИГЛЭЛ — том хөдөлгөөн ХААШАА явахыг таамаглаж чадах уу."""
    s = F[F['_hemjee'] >= thr]
    rows = []
    for col in FEATS:
        q = q5(s, col)
        if q is None:
            continue
        g = (s['_chiglel'] > 0).groupby(q).mean() * 100
        rows.append((col, g.iloc[0], g.iloc[-1], abs(g.iloc[-1] - g.iloc[0]), len(s)))
    rows.sort(key=lambda r: -r[3])
    return rows


if __name__ == '__main__':
    F = build()
    print("НЭЭЛТТЭЙ ХАЙЛТ · 4 цаг · 2005–2025")
    print(f"{len(F):,} бар.  Том хөдөлгөөн = ирээдүйн 6 барын хөдөлгөөн ≥ 2×ATR\n")

    THR = 2.0
    base, rows = part_a(F, THR)
    print("══ A. ТОМ ХӨДӨЛГӨӨН ИРЭХ ҮҮ (ХЭМЖЭЭ) ══")
    print(f"   Суурь: бүх барын {base:.1f}%-ийн дараа том хөдөлгөөн болно.")
    print("   Доорх нь шинж бүрийн 1-р ба 5-р тавны магадлал.\n")
    print(f"   {'шинж':<24}{'доод 20%':>10}{'дээд 20%':>10}{'зөрүү':>9}")
    print("   " + "─" * 56)
    for col, lo_, hi_, sp in rows:
        mark = '  ←' if sp > 5 else ''
        print(f"   {NAMES[col]:<24}{lo_:>9.1f}%{hi_:>9.1f}%{sp:>8.1f}{mark}")

    print("\n\n══ B. ХААШАА ЯВАХ ВЭ (ЧИГЛЭЛ) ══")
    print("   Том хөдөлгөөн болсон тохиолдлуудын дотор л хардаг.")
    print("   50% = зоос шидэлт. Энэ л мөнгө гаргах хэсэг.\n")
    rb = part_b(F, THR)
    print(f"   {'шинж':<24}{'доод 20%':>10}{'дээд 20%':>10}{'зөрүү':>9}")
    print("   " + "─" * 56)
    for col, lo_, hi_, sp, n in rb:
        mark = '  ←' if sp > 5 else ''
        print(f"   {NAMES[col]:<24}{lo_:>9.1f}%{hi_:>9.1f}%{sp:>8.1f}{mark}")
    print(f"\n   (том хөдөлгөөний тоо: {rb[0][4]:,})")

    print("\n\n══ ХУГАЦААНЫ ХУВААЛТ — ДАВТАГДАЖ БАЙНА УУ ══")
    print("   Хамгийн сайн 5 шинжийг хоёр хугацаанд тулгая.")
    print("   Нэгэнд нь л гарсан бол санамсаргүй.\n")
    A = F[F['_year'] < 2017]
    B = F[F['_year'] >= 2017]
    print("   ── A. ХЭМЖЭЭ (зөрүү, хувийн нэгж) ──")
    print(f"   {'шинж':<24}{'2005–2016':>12}{'2017–2025':>12}")
    print("   " + "─" * 50)
    for col, _, _, sp in rows[:5]:
        sa = dict((r[0], r[3]) for r in part_a(A, THR)[1]).get(col, np.nan)
        sb = dict((r[0], r[3]) for r in part_a(B, THR)[1]).get(col, np.nan)
        print(f"   {NAMES[col]:<24}{sa:>11.1f}{sb:>11.1f}")

    print("\n   ── B. ЧИГЛЭЛ (зөрүү, хувийн нэгж) ──")
    print(f"   {'шинж':<24}{'2005–2016':>12}{'2017–2025':>12}")
    print("   " + "─" * 50)
    for col, _, _, sp, _ in rb[:5]:
        sa = dict((r[0], r[3]) for r in part_b(A, THR)).get(col, np.nan)
        sb = dict((r[0], r[3]) for r in part_b(B, THR)).get(col, np.nan)
        print(f"   {NAMES[col]:<24}{sa:>11.1f}{sb:>11.1f}")

    print("\n\n══ БОСГО ӨӨРЧИЛВӨЛ ══")
    print("   Том хөдөлгөөний тодорхойлолтод мэдрэг эсэх.\n")
    print(f"   {'босго':<12}{'тохиолдол':>11}{'A дээд зөрүү':>15}{'B дээд зөрүү':>15}")
    print("   " + "─" * 54)
    for t in (1.5, 2.0, 3.0, 4.0):
        _, ra = part_a(F, t)
        rbb = part_b(F, t)
        n = int((F['_hemjee'] >= t).sum())
        print(f"   ≥{t}×ATR{'':<5}{n:>11,}{ra[0][3]:>14.1f}{rbb[0][3]:>14.1f}")


# ═══════════════════════════════════════════════════════════════════
# ГУУРВАН ДАХЬ ХЭСЭГ — ОЛДСОНЫГ АРИЛЖАА БОЛГОЖ ШАЛГАХ
# ═══════════════════════════════════════════════════════════════════
# A ба B хоёр статистикийн хувьд бодит харагдаж байна. Гэвч
# «61.5% зөв» гэдэг нь мөнгө гэсэн үг БИШ. Стоп, target, зардал
# оруулж байж л мэднэ. Энэ хэсэг л шийднэ.

def trade(tf='4h', thr_q=1, dir_q=1, stop_atr=1.5, tp_atr=3.0,
          spread=0.3, hold=30, years=None, side=None, use_comp=True):
    """Шахалт (сонголттой) + мужид эзлэх байрлалаар чиглэл.

    thr_q : ATR-чиглэлийн хэддүгээр тавинд байвал орох (0 = хамгийн шахсан)
    dir_q : байрлалын захын тавиуд (0 ба 4) чиглэл өгнө
    """
    d = resample(h, tf) if tf != '1h' else h.copy()
    F = build(tf)
    d = d.loc[F.index]
    hi, lo, c = d['high'].values, d['low'].values, d['close'].values
    tr = np.maximum(d['high'] - d['low'],
                    np.maximum((d['high'] - d['close'].shift()).abs(),
                               (d['low'] - d['close'].shift()).abs()))
    atr = tr.rolling(20).mean().values

    qa = pd.qcut(F['atr_chig'], 5, labels=False, duplicates='drop').values
    qp = pd.qcut(F['tuil_zai'], 5, labels=False, duplicates='drop').values
    yr = F['_year'].values
    res = []
    n = len(F)
    for i in range(n - hold - 1):
        if use_comp and qa[i] > thr_q:          # шахалт шаардана
            continue
        if qp[i] >= 4:
            up = True
        elif qp[i] <= 0:
            up = False
        else:
            continue
        if years and not (years[0] <= yr[i] < years[1]):
            continue
        if side == 'urt' and not up:
            continue
        if side == 'bogino' and up:
            continue
        a = atr[i]
        if not (a > 0):
            continue
        e = c[i] + spread if up else c[i] - spread
        st = e - stop_atr * a if up else e + stop_atr * a
        tg = e + tp_atr * a if up else e - tp_atr * a
        risk = abs(e - st)
        got = abs(tg - e) / risk
        r = None
        for x in range(i + 1, min(i + 1 + hold, n)):
            if up:
                if lo[x] <= st: r = -1.0; break
                if hi[x] >= tg: r = got;  break
            else:
                if hi[x] >= st: r = -1.0; break
                if lo[x] <= tg: r = got;  break
        if r is None:
            r = ((c[min(i + hold, n - 1)] - e) if up
                 else (e - c[min(i + hold, n - 1)])) / risk
        res.append(r)
    return np.array(res)


if __name__ == '__main__':
    from core import stat
    print("\n\n══ C. ОЛДСОНЫГ АРИЛЖАА БОЛГОВОЛ ══")
    print("   «61.5% зөв» гэдэг мөнгө гэсэн үг биш. Стоп, target,")
    print("   зардал оруулж байж л мэднэ. Энэ хэсэг шийднэ.\n")
    print(f"   {'':<32}{'n':>6} {'Ялалт':>7} {'Дундаж':>9}")
    print("   " + "─" * 64)
    print("   " + stat(trade(use_comp=False), 'зөвхөн ЧИГЛЭЛ (шахалтгүй)'))
    print("   " + stat(trade(), 'шахалт + чиглэл'))
    print("   " + stat(trade(thr_q=0), 'ХАМГИЙН шахсан + чиглэл'))
    print()
    print("   " + stat(trade(spread=0.0), 'шахалт+чиглэл · СПРЕДГҮЙ'))
    print("   " + stat(trade(spread=0.6), 'шахалт+чиглэл · спред $0.6'))

    print("\n   ── Дөрвөн шалгуур ──\n")
    for kw, lbl in ((dict(years=(2005, 2017)), '2005–2016'),
                    (dict(years=(2017, 2026)), '2017–2025'),
                    (dict(side='urt'), 'зөвхөн УРТ'),
                    (dict(side='bogino'), 'зөвхөн БОГИНО')):
        print("   " + stat(trade(**kw), lbl))

    print("\n   ── Стоп/target-д мэдрэг эсэх ──\n")
    for s_, t_ in ((1.0, 2.0), (1.5, 3.0), (2.0, 4.0), (1.5, 1.5), (3.0, 6.0)):
        print("   " + stat(trade(stop_atr=s_, tp_atr=t_),
                           f'стоп {s_} ATR · TP {t_} ATR'))

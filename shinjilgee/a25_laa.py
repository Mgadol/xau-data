"""25. ЛААНЫ БҮТЭЦ — чиглэл хэлдэг хэлбэр байна уу.

САНАА
  «Чиглэл бас дохиотой л байгаа. Хоосон, сул нэг зүйл байгаа —
   лааны бүтэц юм уу, судлая.»

  a24-д лааны шинжийг 5 барын ДУНДЖААР л харсан — хэт бүдүүн.
  Энд лаа БҮРИЙН хэлбэрийг, нэрлэсэн хэв маягаар нь тусад нь
  шалгана.

ШАЛГАХ ХЭВ МАЯГ (бүгд лаа хаагдахад мэдэгдэнэ)

  НЭГ ЛАА
    doji        их бие < мужийн 10%          — эргэлзээ, «хоосон»
    sul         их бие < мужийн 30%          — сул лаа
    marubozu    их бие > мужийн 80%          — шийдэмгий
    algur       доод сүүл > 2×бие, дээд богино (hammer)
    buudah      дээд сүүл > 2×бие, доод богино (shooting star)

  ХОЁР ЛАА
    engulf_up   өмнөх улаан, одоо ногоон, биеийг нь бүрэн хамарна
    engulf_dn   эсрэгээр
    dotorh      өндөр нь бага, нам нь их (inside bar)
    gadna       өндөр нь их, нам нь бага (outside bar)

  ГУРВАН ЛАА
    uglooniy    улаан → жижиг → ногоон (morning star)
    oroin       ногоон → жижиг → улаан (evening star)
    3_tsagaan   гурван дараалсан ногоон
    3_hara      гурван дараалсан улаан

ДРИФТЭЭС ЦЭВЭРЛЭХ — a24-ИЙН СУРГАМЖ
  Алт 2005–2025 онд 5 дахин өссөн тул «дээш явах» нь ямар ч
  нөхцөлд 50%-иас их гарна. Тиймээс хэв маяг бүрийг СУУРЬТАЙ
  харьцуулна. Зөвхөн «57% дээш явлаа» гэвэл утгагүй — суурь нь
  хэдэн хувь байсан бэ гэдэг нь чухал.

  Тайлагнах тоо: ИЛҮҮДЭЛ = хэв маягийн хувь − суурийн хувь.

════════════════════════════════════════════════════════════════
ҮР ДҮН

1. ЧИГЛЭЛ ТААХ ХУВИАР бараг юу ч алга.
   13 хэв маягийн ИЛҮҮДЭЛ бүгд −2.5 … +2.3 нэгж хувийн дотор.
   «Хоосон/сул лаа» гэсэн таамаг НЭ БАТЛАГДСАНГҮЙ:
       doji  −0.4     sul  −0.6
   Хугацааны хүрээ солиход тэмдэг эргэдэг (3_hara: 1ц +1.4,
   өдөр −4.3) — тогтвортой зүйл биш.

2. АРИЛЖАА БОЛГОВОЛ түүхий тоо сайхан харагдана:
       хамрах дээш → урт    2266   +0.109R ±0.030  ✓
       өглөөний од → урт    2072   +0.064R ±0.032  ✓
   Гэвч дрифтийн суурь (ижил геометрээр САНАМСАРГҮЙ урт орох)
   нь +0.023R. Хасвал +0.086 ба +0.041R үлдэнэ.

3. ХОЁР ТАЛ ЗӨВ ТЭМДЭГТЭЙ — 25 шинжилгээнд АНХ УДАА.
   6 сонгодог хэв маягийн 5 нь өөрийн талын дрифтээс дээш
   (+0.037 … +0.086R). Богино тал нь цэвэр алдагдалтай хэвээр
   (−0.046R) боловч санамсаргүй богиноос (−0.108R) ДЭЭР.
   Өөрөөр хэлбэл лааны хэлбэрт чиглэлийн мэдээлэл БАЙНА.

4. ГЭХДЭЭ ТЭР МЭДЭЭЛЭЛ НЬ ЗҮГЭЭР Л «СҮҮЛИЙН ЛАА НОГООН».
   Бүтцийн хяналт:
       зүгээр ногоон лаа → урт   16111   +0.050R  дрифтээс +0.027
       ногоон + муж өргөссөн      8126   +0.061R  дрифтээс +0.038
       хамрах дээш                2266   +0.109R  дрифтээс +0.086
       өглөөний од                2072   +0.064R  дрифтээс +0.041
   Өглөөний одны бүх нэмэр нь «ногоон лаа»-гаас ирж байна
   (+0.041 vs +0.027 — ялгаа алдааны дотор). Хамрах нь л
   хэлбэрээсээ болж ~+0.05R нэмж байна.

5. ТЭР Ч СҮҮЛИЙН ҮЕД АЛГА БОЛСОН.
                          2005–2016   2017–2025
       ногоон лаа           +0.039R     +0.012R
       хамрах дээш          +0.140R     +0.014R
   Хоёулаа +0.013R орчимд нийлж байна. 1.5 ATR стоп ≈ $14 эрсдэл
   тул +0.013R ≈ $0.18 — спредийн ХЭЛБЭЛЗЭЛ ($0.12→$0.50) үүнээс
   том. Өөрөөр хэлбэл 2017 оноос хойш зардлын доор оржээ.

ДҮГНЭЛТ
  Лааны хэлбэрт чиглэлийн мэдээлэл ҮНЭХЭЭР бий — энэ нь a25-ын
  жинхэнэ олз. Гэвч (а) ихэнх нь «сүүлийн лаа ямар өнгөтэй байв»
  гэдгээс цаашгүй, (б) хэмжээ нь 2017 оноос хойш спредээс доош
  унасан. Сонгодог нэрсийн 13-аас ганц хамрах л хэлбэрээсээ
  нэмэр өгч байсан, тэр ч сүүлдээ алга.
"""
import numpy as np
import pandas as pd
from core import load, resample, stat


h = load(start='2005-01-01', end='2025-09-12')


def pat_dict(d):
    """Лааны хэв маягийн тэмдэглэгээ. ЭНЭ Л ГАНЦ тодорхойлолт —
    хүснэгт ч, арилжааны тест ч эндээс авна (томьёо давхардуулахгүй)."""
    o, hi, lo, c = d['open'], d['high'], d['low'], d['close']
    rng = (hi - lo).replace(0, np.nan)
    body = (c - o).abs()
    br = body / rng                                  # биеийн эзлэх хувь
    up_w = (hi - np.maximum(o, c)) / rng             # дээд сүүл
    dn_w = (np.minimum(o, c) - lo) / rng             # доод сүүл
    green = c > o
    red = c < o
    P = {}
    # ── Нэг лаа ──
    P['doji'] = br < 0.10
    P['sul'] = br < 0.30
    P['marubozu'] = br > 0.80
    P['algur (hammer)'] = (dn_w > 2 * br) & (up_w < br) & (br > 0.05)
    P['buudah (star)'] = (up_w > 2 * br) & (dn_w < br) & (br > 0.05)
    # ── Хоёр лаа ──
    pb_hi = np.maximum(o.shift(), c.shift())
    pb_lo = np.minimum(o.shift(), c.shift())
    P['engulf_up'] = red.shift(1) & green & (c >= pb_hi) & (o <= pb_lo)
    P['engulf_dn'] = green.shift(1) & red & (o >= pb_hi) & (c <= pb_lo)
    P['dotorh (inside)'] = (hi < hi.shift()) & (lo > lo.shift())
    P['gadna (outside)'] = (hi > hi.shift()) & (lo < lo.shift())
    # ── Гурван лаа ──
    small = br.shift(1) < 0.35
    P['uglooniy (morning)'] = red.shift(2) & small & green & (c > (o.shift(2) + c.shift(2)) / 2)
    P['oroin (evening)'] = green.shift(2) & small & red & (c < (o.shift(2) + c.shift(2)) / 2)
    P['3_tsagaan'] = green & green.shift(1) & green.shift(2)
    P['3_hara'] = red & red.shift(1) & red.shift(2)
    return {k: v.fillna(False) for k, v in P.items()}


def patterns(tf='4h', fwd=6):
    """Хэв маяг бүрийг тэмдэглээд ирээдүйн чиглэлийг хавсаргана."""
    d = resample(h, tf) if tf != '1h' else h.copy()
    c, hi, lo = d['close'], d['high'], d['low']
    tr = np.maximum(hi - lo, np.maximum((hi - c.shift()).abs(),
                                        (lo - c.shift()).abs()))
    atr = tr.rolling(20).mean()
    P = pat_dict(d)

    fwd_move = c.shift(-fwd) - c
    F = pd.DataFrame({'up': fwd_move > 0,
                      'move': fwd_move / atr,
                      'year': d.index.year})
    for k, v in P.items():
        F[k] = v.fillna(False)
    return F.dropna()


def trade(tf, mask, side, k=1.5, rr=2.0, spread=0.3, years=None):
    """Хэв маягийг ЖИНХЭНЭ арилжаа болгож шалгана.

    Дохио лаа ХААГДАХАД мэдэгдэнэ → ДАРААГИЙН барын нээлтээр орно.
    Стоп = k×ATR, зорилт = k×rr×ATR. Нэг бар дотор хоёулаа хүрвэл
    СТОП хүрсэн гэж үзнэ (болгоомжтой тал).
    """
    d = resample(h, tf) if tf != '1h' else h.copy()
    o, hi, lo, c = d['open'], d['high'], d['low'], d['close']
    tr = np.maximum(hi - lo, np.maximum((hi - c.shift()).abs(),
                                        (lo - c.shift()).abs()))
    atr = tr.rolling(20).mean()
    O, H, L = o.values, hi.values, lo.values
    A, yr = atr.values, d.index.year.values
    sig = np.where(mask.reindex(d.index).fillna(False).values)[0]
    R = []
    for i in sig:
        j = i + 1                                   # дараагийн бар дээр орно
        if j >= len(d) or not (A[i] == A[i]) or A[i] <= 0:
            continue
        if years and not (years[0] <= yr[j] <= years[1]):
            continue
        risk = k * A[i]
        ent = O[j] + side * spread / 2              # спред орох талдаа
        stp = ent - side * risk
        tgt = ent + side * risk * rr
        out = None
        for m in range(j, min(j + 60, len(d))):
            if side > 0:
                if L[m] <= stp: out = -1.0; break
                if H[m] >= tgt: out = rr; break
            else:
                if H[m] >= stp: out = -1.0; break
                if L[m] <= tgt: out = rr; break
        if out is None:                             # хугацаа дуусав
            out = side * (c.values[min(j + 59, len(d) - 1)] - ent) / risk
        R.append(out - spread / risk)               # гарах талын спред
    return R


PATS = ['doji', 'sul', 'marubozu', 'algur (hammer)', 'buudah (star)',
        'engulf_up', 'engulf_dn', 'dotorh (inside)', 'gadna (outside)',
        'uglooniy (morning)', 'oroin (evening)', '3_tsagaan', '3_hara']

# Хэв маяг бүрийн ТААМАГЛАСАН чиглэл (сонгодог сургаалаар)
EXPECT = {'algur (hammer)': +1, 'buudah (star)': -1, 'engulf_up': +1,
          'engulf_dn': -1, 'uglooniy (morning)': +1, 'oroin (evening)': -1,
          '3_tsagaan': +1, '3_hara': -1, 'marubozu': 0, 'doji': 0,
          'sul': 0, 'dotorh (inside)': 0, 'gadna (outside)': 0}


def table(F, title, min_n=60):
    base = F['up'].mean() * 100
    base_m = F['move'].mean()
    print(f"\n   {title}")
    print(f"   Суурь: дээш явах {base:.1f}%,  дундаж хөдөлгөөн {base_m:+.3f} ATR\n")
    print(f"   {'хэв маяг':<22}{'n':>6}{'дээш%':>8}{'ИЛҮҮДЭЛ':>10}"
          f"{'хөдөлгөөн':>11}{'илүүдэл':>10}")
    print("   " + "─" * 70)
    rows = []
    for p in PATS:
        s = F[F[p]]
        if len(s) < min_n:
            rows.append((p, len(s), np.nan, np.nan, np.nan, np.nan))
            continue
        u = s['up'].mean() * 100
        m = s['move'].mean()
        rows.append((p, len(s), u, u - base, m, m - base_m))
    rows.sort(key=lambda r: -(abs(r[3]) if r[3] == r[3] else -1))
    for p, n, u, ex, m, exm in rows:
        if n < min_n:
            print(f"   {p:<22}{n:>6}   (цөөн)")
            continue
        mark = '  ←' if abs(ex) >= 3 else ''
        print(f"   {p:<22}{n:>6}{u:>7.1f}%{ex:>+9.1f}{m:>+11.3f}{exm:>+10.3f}{mark}")
    return rows


if __name__ == '__main__':
    F = patterns('4h')
    print("ЛААНЫ БҮТЭЦ · 4 цаг · 2005–2025")
    print(f"{len(F):,} бар.  Ирээдүйн 6 барын чиглэлийг хэмжинэ.")
    print("ИЛҮҮДЭЛ = хэв маягийн хувь − суурийн хувь (дрифт хасагдсан).")
    table(F, "══ БҮХ ХУГАЦАА ══")

    print("\n\n══ СОНГОДОГ СУРГААЛ ЗӨВ ҮҮ ══")
    print("   Хэв маяг бүр ТААМАГЛАСАН чиглэлдээ явж байна уу.\n")
    base = F['up'].mean() * 100
    print(f"   {'хэв маяг':<22}{'таамаг':>8}{'n':>7}{'зөв%':>8}{'илүүдэл':>10}")
    print("   " + "─" * 58)
    for p, e in EXPECT.items():
        if e == 0:
            continue
        s = F[F[p]]
        if len(s) < 60:
            print(f"   {p:<22}{'дээш' if e > 0 else 'доош':>8}{len(s):>7}   (цөөн)")
            continue
        ok = (s['up'].mean() if e > 0 else (1 - s['up'].mean())) * 100
        exp_base = base if e > 0 else 100 - base
        print(f"   {p:<22}{'дээш' if e > 0 else 'доош':>8}{len(s):>7}"
              f"{ok:>7.1f}%{ok - exp_base:>+9.1f}")

    print("\n\n══ ХУГАЦААНЫ ХУВААЛТ ══")
    print("   Нэг хугацаанд л гарсан бол санамсаргүй.\n")
    A, B = F[F['year'] < 2017], F[F['year'] >= 2017]
    ba, bb = A['up'].mean() * 100, B['up'].mean() * 100
    print(f"   {'хэв маяг':<22}{'2005–2016':>14}{'2017–2025':>14}")
    print("   " + "─" * 52)
    for p in PATS:
        sa, sb = A[A[p]], B[B[p]]
        if len(sa) < 40 or len(sb) < 40:
            continue
        ea = sa['up'].mean() * 100 - ba
        eb = sb['up'].mean() * 100 - bb
        same = '  ✓ ижил тэмдэг' if ea * eb > 0 else ''
        print(f"   {p:<22}{ea:>+13.1f}{eb:>+13.1f}{same}")

    print("\n\n══ ӨӨР ХУГАЦААНЫ ХҮРЭЭНД ══")
    for tf in ('1h', '1D'):
        G = patterns(tf)
        print(f"\n   ── {tf} ── (суурь {G['up'].mean() * 100:.1f}%)")
        bs = G['up'].mean() * 100
        out = []
        for p in PATS:
            s = G[G[p]]
            if len(s) < 60:
                continue
            out.append((p, len(s), s['up'].mean() * 100 - bs))
        out.sort(key=lambda r: -abs(r[2]))
        for p, n, ex in out[:6]:
            print(f"      {p:<22}{n:>7}{ex:>+9.1f}")

    # ────────────────────────────────────────────────────────────────
    print("\n\n══ ЖИНХЭНЭ АРИЛЖАА БОЛГОВОЛ ══")
    print("   Стоп 1.5 ATR, зорилт 3.0 ATR, спред $0.3.")
    print("   Дохио лаа хаагдахад → дараагийн барын нээлтээр орно.\n")
    D4 = resample(h, '4h')
    M = pat_dict(D4)
    CAND = [('Өглөөний од → УРТ', M['uglooniy (morning)'], +1),
            ('Буудах од → БОГИНО', M['buudah (star)'], -1),
            ('Алгуур → УРТ', M['algur (hammer)'], +1),
            ('Оройн од → БОГИНО', M['oroin (evening)'], -1),
            ('Хамрах дээш → УРТ', M['engulf_up'], +1),
            ('Хамрах доош → БОГИНО', M['engulf_dn'], -1)]
    def drift(side, **kw):
        """Дрифтийн суурь — ЯГ ижил геометрээр санамсаргүй орох.
        НЭГ үртэс азтай байж мэднэ (эхлээд 7-гоор +0.104R гарч,
        өглөөний одыг дийлж байсан — 12 үртэсээр +0.023R болов)."""
        allR = []
        for seed in range(12):
            rng = np.random.default_rng(seed)
            rm = pd.Series(rng.random(len(D4)) < 0.05, index=D4.index)
            allR += trade('4h', rm, side, **kw)
        return np.mean(allR)

    dL, dS = drift(+1), drift(-1)
    print(f"   Дрифтийн суурь (12 үртэс): УРТ {dL:+.3f}R, "
          f"БОГИНО {dS:+.3f}R\n")
    for name, m, side in CAND:
        R = trade('4h', m, side)
        base = dL if side > 0 else dS
        print("  " + stat(R, name) +
              f"   дрифтээс {np.mean(R) - base:+.3f}R")

    print("\n   ── Хугацааны хуваалт (эхний хоёр) ──")
    for name, m, side in (CAND[0], CAND[4]):
        for yy in ((2005, 2016), (2017, 2025)):
            b = drift(side, years=yy)
            R = trade('4h', m, side, years=yy)
            print("  " + stat(R, f"   {name.split(' →')[0]} {yy[0]}–{yy[1]}") +
                  f"   дрифтээс {np.mean(R) - b:+.3f}R")

    print("\n   ── Параметрийн мэдрэг байдал ──")
    print("   Зөвхөн нэг тохиргоонд гардаг бол олдвор (a10-ын сургамж).")
    print("   Дрифтээс ХАСНА — өргөн стоп нь спредийн харьцаагаар л")
    print("   дээшилдэг тул түүхий тоо төөрөгдүүлнэ.")
    for lbl, m in (('Өглөөний од', M['uglooniy (morning)']),
                   ('Хамрах дээш', M['engulf_up'])):
        print(f"\n     {lbl}")
        for k in (1.0, 1.5, 2.5):
            for rr in (1.5, 2.0, 3.0):
                b = drift(+1, k=k, rr=rr)
                R = trade('4h', m, +1, k=k, rr=rr)
                print("  " + stat(R, f"     стоп {k}ATR  RR 1:{rr}") +
                      f"   дрифтээс {np.mean(R) - b:+.3f}R")

    print("\n   ── БҮТЦИЙН ХЯНАЛТ: хэлбэр үү, эсвэл зүгээр л өнгө үү ──")
    print("   Хэв маягийн ДОТОР нь энгийн бүрэлдэхүүн байна:")
    print("   «сүүлийн лаа ногоон», «муж өргөссөн». Хэрэв тэр хоёр л")
    print("   ажиллаж байгаа бол хэлбэр нь нэмэр өгөхгүй.\n")
    o4, c4, hi4, lo4 = D4['open'], D4['close'], D4['high'], D4['low']
    g4 = c4 > o4
    exp4 = (hi4 - lo4) > (hi4 - lo4).shift()
    CTRL = [('зүгээр НОГООН лаа', g4, +1),
            ('зүгээр УЛААН лаа', c4 < o4, -1),
            ('ногоон + муж өргөссөн', g4 & exp4, +1),
            ('улаан + муж өргөссөн', (c4 < o4) & exp4, -1)]
    for lbl, m, side in CTRL:
        R = trade('4h', m, side)
        base = dL if side > 0 else dS
        print("  " + stat(R, lbl) + f"   дрифтээс {np.mean(R) - base:+.3f}R")

    print("\n   ── Спредийн мэдрэг байдал ──")
    for lbl, m in (('Өглөөний од', M['uglooniy (morning)']),
                   ('Хамрах дээш', M['engulf_up'])):
        print(f"\n     {lbl}")
        for sp in (0.0, 0.12, 0.3, 0.5):
            print("  " + stat(trade('4h', m, +1, spread=sp),
                              f"     спред ${sp:.2f}"))

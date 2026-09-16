"""26. СУЛ ЗАЙ — чиглэлийг ЭЗЛЭХҮҮНЭЭС олох оролдлого.

САНАА (хэрэглэгчийн залруулга)
  «Түрүүн том хөдөлгөөн бол дохио өгч байсан. Чиглэл олоход тэр
   бусад арга барил огт хэрэггүй. Өөр арга зам байж л байгаа —
   ганц дээшээ биш доошоо байж болно. Сул зай гэдэг нь лаа биш,
   ямар нэг алдаа юмуу дохио гэсэн үг.»

  a25-д би «сул» гэдгийг лааны БИЕ гэж ойлгосон — буруу байлаа.
  Энд үнийн хэлбэрийг огт хардаггүй. Оронд нь ЭЗЛЭХҮҮН үнийн
  тэнхлэг дээр хэрхэн ТАРААГДСАНЫГ хардаг.

ТААМАГ
  Үнэ ЗУЗААН бүсэд зогсоно, НИМГЭН бүсээр гүйнэ. Нимгэн бүс гэдэг
  нь зах зээл тэнд бага арилжаа хийсэн, тохирох захиалга цөөн,
  тэнцвэргүй үлдсэн газар — «сул зай».

  Хэрэв одоогийн үнээс ДЭЭШ нимгэн, ДООШ зузаан бол тэлэлт
  дээшээ гарах ёстой. Эсрэгээр бол доошоо.

  a24 нь ХЭЗЭЭ том хөдөлгөөн болохыг хэлдэг (ATR шахалт).
  Хэрэв энэ нь ХААШАА гэдгийг хэлж чадвал хоёрыг нийлүүлээд
  бүрэн аргачлал болно. Тэр л энэ файлын гол зорилго.

ХЭМЖИХ АРГА
  Сүүлийн W барын эзлэхүүнийг бар бүрийн [нам, өндөр] мужид ЖИГД
  тараана (нягт = эзлэхүүн / муж). Дараа нь одоогийн үнээс дээш
  B×ATR, доош B×ATR хоёр туузан дахь эзлэхүүнийг нийлбэрээр авна.

      НИМГЭН = (доош − дээш) / (доош + дээш)

  +1 → дээш талд огт эзлэхүүн алга (цоо нимгэн) → ДЭЭШ хүлээнэ
  −1 → доош тал нимгэн → ДООШ хүлээнэ

  Эзлэхүүн нь тикийн тоо тул 2005 (18) ба 2024 (4800) харьцуулах
  боломжгүй. Гэхдээ ЭНЭ хэмжүүр нь нэг цонхон дотор харьцаа авдаг
  тул эрин үеийн ялгаа өөрөө хасагдана.

БУСАД «АЛДАА/ДОХИО» — мөн шалгав
  цоорхой   өмнөх хаалтаас өөр үнээр нээгдэх (амралтын өдрийн)
  шингээлт  эзлэхүүн их, муж жижиг — хэн нэг нь эсэргүүцэж байна
  хоосон    эзлэхүүн бага, муж том — эсэргүүцэлгүй гулссан

ШАЛГАХ ДАРААЛАЛ
  A. НИМГЭН нь ирээдүйн чиглэлийг таамаглаж байна уу (хувиар)
  B. Шахалттай үед л шалгавал илүү тод болох уу (a24-тэй хослол)
  C. Цоорхой, шингээлт, хоосон бар — тус бүрд
  D. Арилжаа болгоод ДРИФТИЙН ХЯНАЛТ, БҮТЦИЙН ХЯНАЛТтай харьцуулах
     (a25-ын сургамж: дрифтээс дээш байхад хангалтгүй, өөрийнх нь
      энгийн хувилбараас дээш байх ёстой)

════════════════════════════════════════════════════════════════
ҮР ДҮН — 26 шинжилгээнд ХАМГИЙН ХОЛ ЯВСАН, гэвч эцэст нь унасан

1. ЧИГЛЭЛ ТААХ ХУВИАР шууд юу ч алга.
   НИМГЭН-ийг 5 хэсэгт хуваахад: +1.5 +0.7 −2.1 −1.4 +1.4.
   Дараалал байхгүй, зөрүү −0.1. Эзлэхүүн, муж, цоорхой ч мөн адил.

2. ГЭВЧ АРИЛЖАА БОЛГОХОД тод гарч ирэв.
       нимгэн>0.8 → урт     1872   +0.161R ±0.034  ✓
   Дрифтийн суурь (12 үртэс) +0.027R тул илүүдэл +0.134R.

   Яагаад хувиар харагдахгүй байж R-ээр гарав? Учир нь энэ нь
   чиглэл БИШ, ХЭМЖЭЭ таамагладаг — a24-ийн яг тэр зүйл. Зөв
   тохиолдолд илүү хол явдаг тул 1:2 геометр дээр л илэрнэ.

3. БҮТЦИЙН ХЯНАЛТЫГ ДАВАВ — 26 тестэд анх удаа.
   «Дээш нимгэн» ≈ «үнэ мужийн дээд ирмэг дээр» (r = 0.60).
   Байрлалыг ТОГТМОЛ барьж шалгахад:
       зүгээр байрлал>0.8          8740   +0.089R   дрифтээс +0.058
       байрлал>0.8 + нимгэн>0.5    3728   +0.124R   дрифтээс +0.095
       байрлал>0.8 + нимгэн>0.8    1825   +0.159R   дрифтээс +0.131
       байрлал>0.8 + нимгэн<0      1635   −0.001R   дрифтээс −0.024
   Ижил бүтцийн дотор нимгэн нь +0.159 ба −0.001 гэж ХУВААЖ байна.
   Энэ бол a25-ын хамрах лаанаас хамаагүй тод.

4. СПРЕДЭД ОНЦГОЙ ТЭСВЭРТЭЙ — энэ нь бүх багцад хамгийн ховор зүйл.
       $0.00 +0.201  $0.12 +0.184  $0.30 +0.159
       $0.50 +0.127  $0.80 +0.077  ← бүгд ✓
   Стоп 1.5 ATR ≈ $14 тул спред эрсдэлийн 2% л эзэлнэ.

5. ПАРАМЕТРТ ТЭСВЭРТЭЙ.
   Стоп/RR-ийн 9 хослол: илүүдэл +0.118 … +0.172R, бүгд ✓.
   Хэмжүүрийн параметр (цонх W=90/180/360, тууз B=0.75/1.5/3.0):
   илүүдэл +0.109 … +0.138R, бүгд ✓.

6. ГЭВЧ ХОЁР ШАЛГУУР УНАВ.

   (а) УРТ/БОГИНО ТЭГШ ХЭМ — толин тусгал огт ажиллахгүй:
       байрлал>0.8 + нимгэн>0.8  → урт     +0.159R  дрифтээс +0.131
       байрлал<0.2 + нимгэн<-0.8 → богино  −0.136R  дрифтээс −0.011
   Богино тал нь санамсаргүй богиноос ЯЛГААГҮЙ. a25-д 6-гийн 5 нь
   хоёр талдаа зөв тэмдэгтэй байсан — энд ганц тал.

   (б) ХУГАЦААНЫ ХУВААЛТ — эрэмбэ нь ДАВТАГДАХГҮЙ.
   Ижил байрлал, ижил хугацаа, зөвхөн нимгэн ялгаатай:

                          2005–2016      2017–2025
       нимгэн > 0.8        +0.049R ✗      +0.305R ✓
       нимгэн 0 … 0.8      +0.102R ✓      +0.073R ✓
       нимгэн < 0          −0.079R ✗      +0.099R ✗

   Эхний хугацаанд ДУНДАЖ хэсэг нь хамгийн сайн, хамгийн нимгэн нь
   хоёрдугаарт. Хоёр дахь хугацаанд эсрэгээрээ. Бүх хугацаагаар
   нийлүүлэхэд гоё дараалал (+0.159 / +0.089 / −0.001) гарч байгаа
   нь хоёр ЗӨРЧИЛДӨХ хагасын дундаж юм.

   Өөрөөр хэлбэл «нимгэн байх тусам сайн» гэсэн ХАМААРАЛ байхгүй.
   Бүхэл дүн нь 2017–2025 оны ганц хагасаас гарч байна.

ДҮГНЭЛТ
  «Сул зай» гэсэн санаа зөв чиглэлд байсан — эзлэхүүний хуваарилалт
  нь үнийн хэлбэрээс хамаагүй их мэдээлэл агуулж байна (a25-ын бүх
  13 хэв маягийг дийлэв, бүтцийн хяналтыг давав, спредэд тэсвэртэй).

  Гэвч тэр мэдээлэл нь ЧИГЛЭЛ биш. Толин тусгал нь ажиллахгүй,
  эрэмбэ нь хугацаанд давтагдахгүй. Хоёр хагас нь бие биенээ
  үгүйсгэж байгаа тул үлдсэн тоо нь дундаж, аргачлал биш.

  Гурав дахь удаагаа ижил хана: ХЭМЖЭЭ таамаглагдана, ЧИГЛЭЛ үгүй.
  (a24 — шахалт, a25 — лааны хэлбэр, a26 — эзлэхүүний нимгэн зай.)
"""
import numpy as np
import pandas as pd
from core import load, resample, stat

h = load(start='2005-01-01', end='2025-09-12')


def prep(tf='4h', W=180, B=1.5):
    """Бар бүрт НИМГЭН хэмжүүр болон бусад шинжийг тооцно."""
    d = resample(h, tf) if tf != '1h' else h.copy()
    o, hi, lo, c = (d['open'].values, d['high'].values,
                    d['low'].values, d['close'].values)
    v = d['volume'].values.astype(float)
    tr = np.maximum(d['high'] - d['low'],
                    np.maximum((d['high'] - d['close'].shift()).abs(),
                               (d['low'] - d['close'].shift()).abs()))
    atr = tr.rolling(20).mean().values
    n = len(d)
    rng = np.maximum(hi - lo, 1e-9)
    dens = v / rng                      # нэгж үнэд ногдох эзлэхүүн

    thin = np.full(n, np.nan)
    for i in range(W, n):
        if not (atr[i] == atr[i]) or atr[i] <= 0:
            continue
        p, b = c[i], B * atr[i]
        s = slice(i - W, i)             # ӨМНӨХ барууд — өнөөдрийг оруулахгүй
        L, H, D = lo[s], hi[s], dens[s]
        # [p, p+b] ба [p-b, p] мужтай давхцах хэмжээгээр эзлэхүүн авна
        up = np.clip(np.minimum(H, p + b) - np.maximum(L, p), 0, None) * D
        dn = np.clip(np.minimum(H, p) - np.maximum(L, p - b), 0, None) * D
        U, Dw = up.sum(), dn.sum()
        if U + Dw > 0:
            thin[i] = (Dw - U) / (Dw + U)

    vz = (pd.Series(v).rolling(100).mean())
    vrel = v / vz.values                # эзлэхүүн сүүлийн 100-гийн дунджид
    rrel = (hi - lo) / atr              # муж ATR-д
    gap = np.r_[np.nan, o[1:] - c[:-1]] / atr

    return d, pd.DataFrame({
        'thin': thin, 'atr': atr, 'vrel': vrel, 'rrel': rrel, 'gap': gap,
        'atr_ch': atr / pd.Series(atr).shift(20).values,   # a24-ийн шахалт
        'c': c, 'year': d.index.year}, index=d.index)


def fwd_dir(d, F, fwd=6):
    """Ирээдүйн чиглэл — fwd барын дараах хаалт одоогийнхоос дээш үү."""
    c = d['close']
    F = F.copy()
    F['up'] = (c.shift(-fwd) > c).values
    F['mv'] = ((c.shift(-fwd) - c) / F['atr']).values
    return F.dropna(subset=['thin', 'up', 'mv'])


def bucket(F, col, label, q=5, sub=None):
    """Шинжийг q хэсэгт хувааж, тус бүрийн дээш явах хувийг харна."""
    G = F if sub is None else F[sub]
    G = G.dropna(subset=[col])
    if len(G) < 500:
        print(f"   {label:<34}(цөөн {len(G)})")
        return
    base = G['up'].mean() * 100
    try:
        lab = pd.qcut(G[col], q, labels=False, duplicates='drop')
    except ValueError:
        print(f"   {label:<34}(хуваагдахгүй)")
        return
    print(f"   {label}   (суурь {base:.1f}%, n={len(G):,})")
    cells = []
    for b in range(int(lab.max()) + 1):
        s = G[lab == b]
        cells.append(f"{s['up'].mean() * 100 - base:+6.1f}")
    lo_ex = G[lab == 0]['up'].mean() * 100 - base
    hi_ex = G[lab == int(lab.max())]['up'].mean() * 100 - base
    print(f"      доод→дээд: {'  '.join(cells)}      "
          f"зөрүү {hi_ex - lo_ex:+.1f}")


def trade(d, sig_up, sig_dn, k=1.5, rr=2.0, spread=0.3, years=None,
          maxbars=60):
    """Дохиог арилжаа болгоно. Дохио бар ХААГДАХАД мэдэгдэнэ →
    ДАРААГИЙН барын нээлтээр орно. Нэг бар дотор хоёулаа хүрвэл
    стоп хүрсэн гэж үзнэ (болгоомжтой тал)."""
    o, hi, lo, c = (d['open'].values, d['high'].values,
                    d['low'].values, d['close'].values)
    tr = np.maximum(d['high'] - d['low'],
                    np.maximum((d['high'] - d['close'].shift()).abs(),
                               (d['low'] - d['close'].shift()).abs()))
    A = tr.rolling(20).mean().values
    yr = d.index.year.values
    su = np.asarray(sig_up, bool)
    sd = np.asarray(sig_dn, bool)
    R = []
    for i in np.where(su | sd)[0]:
        side = 1 if su[i] else -1
        j = i + 1
        if j >= len(d) or not (A[i] == A[i]) or A[i] <= 0:
            continue
        if years and not (years[0] <= yr[j] <= years[1]):
            continue
        risk = k * A[i]
        ent = o[j] + side * spread / 2
        stp, tgt = ent - side * risk, ent + side * risk * rr
        out = None
        for m in range(j, min(j + maxbars, len(d))):
            if side > 0:
                if lo[m] <= stp: out = -1.0; break
                if hi[m] >= tgt: out = rr; break
            else:
                if hi[m] >= stp: out = -1.0; break
                if lo[m] <= tgt: out = rr; break
        if out is None:
            out = side * (c[min(j + maxbars - 1, len(d) - 1)] - ent) / risk
        R.append(out - spread / risk)
    return R


def drift(d, n_sig, side, seeds=12, **kw):
    """Ижил тоо, ижил геометрээр САНАМСАРГҮЙ орох.
    a25-ын сургамж: НЭГ үртэс дүгнэлтийг эсрэгээр эргүүлж байсан."""
    p = n_sig / len(d)
    R = []
    for s in range(seeds):
        rng = np.random.default_rng(s)
        m = rng.random(len(d)) < p
        z = np.zeros(len(d), bool)
        R += trade(d, m if side > 0 else z, z if side > 0 else m, **kw)
    return np.mean(R), len(R)


if __name__ == '__main__':
    d, P = prep('4h')
    F = fwd_dir(d, P)
    print("СУЛ ЗАЙ · 4 цаг · 2005–2025")
    print(f"{len(F):,} бар.  Ирээдүйн 6 барын чиглэлийг хэмжинэ.")
    print("НИМГЭН = (доош эзлэхүүн − дээш эзлэхүүн) / нийлбэр")
    print("  +1 → дээш тал цоо хоосон → ДЭЭШ хүлээнэ\n")

    print("══ A. НИМГЭН нь чиглэл хэлж байна уу ══\n")
    bucket(F, 'thin', 'НИМГЭН (5 хэсэг)')
    print()
    bucket(F, 'vrel', 'эзлэхүүн / 100-гийн дундаж')
    print()
    bucket(F, 'rrel', 'муж / ATR')
    print()
    bucket(F, 'gap', 'цоорхой / ATR')

    print("\n\n══ B. ШАХАЛТТАЙ ҮЕД (a24-тэй хослол) ══")
    print("   ATR буурсан = том хөдөлгөөн ойрхон. Тэр үед НИМГЭН нь")
    print("   чиглэлийг хэлж чадвал хоёр нийлээд аргачлал болно.\n")
    comp = F['atr_ch'] < F['atr_ch'].quantile(0.25)
    bucket(F, 'thin', 'НИМГЭН · зөвхөн шахалттай', sub=comp)
    print()
    bucket(F, 'thin', 'НИМГЭН · зөвхөн тэлэлттэй',
           sub=F['atr_ch'] > F['atr_ch'].quantile(0.75))

    print("\n\n══ C. ХУГАЦААНЫ ХУВААЛТ ══")
    print("   Хоёуланд давтагдахгүй бол санамсаргүй.\n")
    for yy, nm in (((2005, 2016), '2005–2016'), ((2017, 2025), '2017–2025')):
        s = (F['year'] >= yy[0]) & (F['year'] <= yy[1])
        bucket(F, 'thin', f'НИМГЭН · {nm}', sub=s)
        print()

    print("\n══ D. АРИЛЖАА БОЛГОВОЛ ══")
    print("   Стоп 1.5 ATR, зорилт 3.0 ATR, спред $0.3.\n")
    T = P['thin'].reindex(d.index)
    for thr, nm in ((0.5, '±0.5'), (0.8, '±0.8'), (0.95, '±0.95')):
        up = (T > thr).fillna(False).values
        dn = (T < -thr).fillna(False).values
        for m, side, lbl in ((up, +1, 'нимгэн ДЭЭШ → урт'),
                             (dn, -1, 'нимгэн ДООШ → богино')):
            z = np.zeros(len(d), bool)
            R = trade(d, m if side > 0 else z, z if side > 0 else m)
            if len(R) < 25:
                continue
            b, _ = drift(d, int(m.sum()), side)
            print("  " + stat(R, f"{lbl} {nm}") +
                  f"   дрифтээс {np.mean(R) - b:+.3f}R")
        print()

    print("   ── БҮТЦИЙН ХЯНАЛТ (a25-ын сургамж) ──")
    print("   «Дээш тал нимгэн» гэдэг нь ихэвчлэн «үнэ сүүлийн үеийн")
    print("   ДЭЭД ирмэг дээр байна» гэсэнтэй ижил. Тэр энгийн зүйл нь")
    print("   ямар үр дүн өгдгийг эхлээд мэдэх ёстой.\n")
    W = 180
    hh = d['high'].rolling(W).max()
    ll = d['low'].rolling(W).min()
    pos = ((d['close'] - ll) / (hh - ll).replace(0, np.nan))
    print(f"   Нимгэн ба байрлалын хамаарал: "
          f"r = {T.corr(pos):.2f}\n")
    for lo_t, hi_t in ((0.8, 0.2),):
        for m, side, lbl in (((pos > lo_t).fillna(False).values, +1,
                              f'зүгээр БАЙРЛАЛ>{lo_t} → урт'),
                             ((pos < hi_t).fillna(False).values, -1,
                              f'зүгээр БАЙРЛАЛ<{hi_t} → богино')):
            z = np.zeros(len(d), bool)
            R = trade(d, m if side > 0 else z, z if side > 0 else m)
            b, _ = drift(d, int(m.sum()), side)
            print("  " + stat(R, lbl) +
                  f"   дрифтээс {np.mean(R) - b:+.3f}R")
    print()
    print("   Байрлалыг ТОГТМОЛ барьж, нимгэнийг НЭМЭХЭД юу нэмэгдэх вэ:")
    hp = (pos > 0.8).fillna(False).values
    for thr in (0.5, 0.8):
        m = hp & (T > thr).fillna(False).values
        z = np.zeros(len(d), bool)
        R = trade(d, m, z)
        b, _ = drift(d, int(m.sum()), +1)
        print("  " + stat(R, f'   байрлал>0.8 + нимгэн>{thr}') +
              f"   дрифтээс {np.mean(R) - b:+.3f}R")
    m = hp & (T < 0).fillna(False).values
    R = trade(d, m, np.zeros(len(d), bool))
    b, _ = drift(d, int(m.sum()), +1)
    print("  " + stat(R, '   байрлал>0.8 + нимгэн<0 (эсрэг)') +
          f"   дрифтээс {np.mean(R) - b:+.3f}R")

    print("\n\n══ E. ДӨРВӨН ШАЛГУУР ══")
    print("   «байрлал>0.8 + нимгэн>0.8» нь бүтцийн хяналтыг давав.")
    print("   Одоо үлдсэн шалгуурууд.\n")
    best = hp & (T > 0.8).fillna(False).values
    lp = (pos < 0.2).fillna(False).values
    mirror = lp & (T < -0.8).fillna(False).values
    z = np.zeros(len(d), bool)

    print("   ── 1. УРТ/БОГИНО ТЭГШ ХЭМ (толин тусгал) ──")
    for m, side, lbl in ((best, +1, 'байрлал>0.8 + нимгэн>0.8 → урт'),
                         (mirror, -1, 'байрлал<0.2 + нимгэн<-0.8 → богино')):
        R = trade(d, m if side > 0 else z, z if side > 0 else m)
        if len(R) < 25:
            print(f"  {lbl:<38}{len(R):>6}  (цөөн)")
            continue
        b, _ = drift(d, int(m.sum()), side)
        print("  " + stat(R, lbl) + f"   дрифтээс {np.mean(R) - b:+.3f}R")

    print("\n   ── 2. ХУГАЦААНЫ ХУВААЛТ ──")
    for yy in ((2005, 2016), (2017, 2025)):
        for m, side, lbl in ((best, +1, 'урт'), (mirror, -1, 'богино')):
            R = trade(d, m if side > 0 else z, z if side > 0 else m, years=yy)
            if len(R) < 25:
                print(f"     {lbl} {yy[0]}–{yy[1]:<12}{len(R):>6}  (цөөн)")
                continue
            b, _ = drift(d, int(m.sum()), side, years=yy)
            print("  " + stat(R, f"   {lbl} {yy[0]}–{yy[1]}") +
                  f"   дрифтээс {np.mean(R) - b:+.3f}R")

    print("\n   ── 3. СПРЕД ──")
    for sp in (0.0, 0.12, 0.3, 0.5, 0.8):
        print("  " + stat(trade(d, best, z, spread=sp), f"   спред ${sp:.2f}"))

    print("\n   ── 4. ПАРАМЕТР (a10-ын сургамж) ──")
    print("   Зөвхөн нэг тохиргоонд гардаг бол олдвор.")
    for k in (1.0, 1.5, 2.5):
        for rr in (1.5, 2.0, 3.0):
            R = trade(d, best, z, k=k, rr=rr)
            b, _ = drift(d, int(best.sum()), +1, k=k, rr=rr)
            print("  " + stat(R, f"   стоп {k}ATR  RR 1:{rr}") +
                  f"   дрифтээс {np.mean(R) - b:+.3f}R")

    print("\n   ── 5. ХЭМЖҮҮРИЙН ПАРАМЕТР (цонх W, туузны өргөн B) ──")
    print("   Нимгэнийг өөрөөр хэмжвэл үр дүн тогтвортой байх ёстой.")
    for W2, B2 in ((90, 1.5), (180, 1.5), (360, 1.5),
                   (180, 0.75), (180, 3.0)):
        d2, P2 = prep('4h', W=W2, B=B2)
        T2 = P2['thin'].reindex(d2.index)
        hh2 = d2['high'].rolling(180).max()
        ll2 = d2['low'].rolling(180).min()
        pos2 = (d2['close'] - ll2) / (hh2 - ll2).replace(0, np.nan)
        m2 = ((pos2 > 0.8).fillna(False).values
              & (T2 > 0.8).fillna(False).values)
        z2 = np.zeros(len(d2), bool)
        R = trade(d2, m2, z2)
        if len(R) < 25:
            print(f"     W={W2} B={B2:<6}{len(R):>6}  (цөөн)")
            continue
        b, _ = drift(d2, int(m2.sum()), +1)
        print("  " + stat(R, f"   W={W2}  B={B2}") +
              f"   дрифтээс {np.mean(R) - b:+.3f}R")

    print("\n   ── Шахалт + нимгэн хоёуланг нь шаардвал ──")
    cmask = (P['atr_ch'] < P['atr_ch'].quantile(0.25)).fillna(False).values
    for thr in (0.3, 0.5):
        up = ((T > thr).fillna(False).values) & cmask
        dn = ((T < -thr).fillna(False).values) & cmask
        for m, side, lbl in ((up, +1, f'шахалт+нимгэн>{thr} → урт'),
                             (dn, -1, f'шахалт+нимгэн<-{thr} → богино')):
            z = np.zeros(len(d), bool)
            R = trade(d, m if side > 0 else z, z if side > 0 else m)
            if len(R) < 25:
                print(f"  {lbl:<30}{len(R):>6}  (цөөн)")
                continue
            b, _ = drift(d, int(m.sum()), side)
            print("  " + stat(R, lbl) +
                  f"   дрифтээс {np.mean(R) - b:+.3f}R")

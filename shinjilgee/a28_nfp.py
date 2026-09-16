"""28. АНУ-ЫН ТОМ МЭДЭЭ — чиглэлд нөлөөлж байна уу.

САНАА
  «АНУ-ын 3 том мэдээ их чухал байгаа. Тэд чиглэлд хэр нөлөө
   үзүүлж байна вэ?»

  Гурав нь: NFP (ажил эрхлэлт), CPI (инфляц), FOMC (хүүгийн шийдвэр).

ЯАГААД ЗӨВХӨН NFP-Г ГҮНЗГИЙ ШАЛГАВ
  Бидэнд эдийн засгийн хуанли БАЙХГҮЙ. Тиймээс мэдээний өдрийг
  өгөгдлөөс өөрөөс нь таних ёстой болов.

    NFP  — сар бүрийн ЭХНИЙ БААСАН, 8:30 ET. Бүрэн тодорхой,
           хуанли хэрэггүй. 248 үйл явдал. ✓
    CPI  — 8:30 ET, ихэвчлэн сарын 10–15. Огноо нь хөвдөг тул
           зөвхөн ЦОНХООР нь ойролцоолж болно. Нарийвчлал муу.
    FOMC — 14:00 ET, жилд 8 удаа. Хэлбэлзлээр таних оролдлого
           БҮТСЭНГҮЙ: илрүүлсэн өдрүүдийн 9 нь 2-р сард, 12 нь
           8-р сард гарсан — тэр хоёр сард FOMC хуралддаггүй.
           Өөрөөр хэлбэл 2 цагийн оргилын ихэнх нь FOMC биш.
           Худал өгөгдөл дээр дүгнэлт хийхгүйн тулд орхив.

  NFP бол гурвуулангийн хамгийн том, хамгийн цэвэр нь. Түүн дээр
  гарсан хариу бусад хоёрт ч ерөнхийдөө хамаарна.

БРОКЕРИЙН ЦАГ
  8:30 ET нь брокерийн 15 цагийн бар дотор байна (2011 оноос
  хойш). 2005–2010 онд брокерийн бүс өөр байсан тул 14 цаг.
  Үүнийг эхний баасан гарагийн хэлбэлзлийн оргилоор баталгаажуулав.

ШАЛГАХ ЗҮЙЛС
  A. Хэмжээ — мэдээ хэдэн дахин хөдөлгөж байна вэ
  B. ЧИГЛЭЛ — мэдээний эхний хөдөлгөөн цаашдыг хэлж байна уу
       • үргэлжлэл: эхний 5 минутын чиглэлээр орох
       • эсрэг: эхний хөдөлгөөнийг бүдүүлэг гэж үзэж эсрэг орох
       • мэдээний ӨМНӨХ чиглэл дараахыг хэлэх үү
  C. ЗАРДЛЫН БОДИТ БАЙДАЛ — мэдээний үед спред $0.3 биш.
     NFP-ийн эхний секундүүдэд алтны спред $2–10 болдог.
     Тиймээс $0.3, $1, $3, $5 дөрвүүлэнг нь тооцно.
  D. Дрифтийн хяналт, урт/богино тэгш хэм, хугацааны хуваалт

════════════════════════════════════════════════════════════════
ҮР ДҮН

1. ХЭМЖЭЭНД НӨЛӨӨ АСАР ТОМ — энэ нь эргэлзээгүй.
       Fed 14:00 ET        суурийн 4.42 дахин   ← хамгийн том
       NFP                 суурийн 3.87 дахин
       CPI цонх (10–15)    суурийн 2.14 дахин
   NFP-ийн мэдээний цагт дундаж муж $10.93, ердийн цагт $2.82.
   Нөлөө нь 3 цаг үргэлжилнэ (+1ц 2.73×, +2ц 2.23×, +3ц 1.61×),
   харин ӨМНӨХ цаг нь ердийнхөөс ТАЙВАН (0.87×) — зах зээл
   хүлээж зогсдог.

2. ЧИГЛЭЛД НӨЛӨӨ БАРАГ ТЭГ.
   Мэдээний барын чиглэл дараагийн 1–8 цагт үргэлжлэх нь суурийн
   +3.8 … +3.9 нэгж хувь. Сонсоход сайн, гэвч n=242 тул алдааны
   зурвас ±6.4. Өөрөөр хэлбэл ЯЛГААГҮЙ.
   24 цагийн дараа −1.2 болж алга болно.
   Мэдээний ӨМНӨХ чиглэл дараахыг огт хэлэхгүй (49.2%, 48.8%).

3. ГАНЦ АЧ ХОЛБОГДОЛТОЙ ОЛДВОР — ЭХНИЙ 5 МИНУТ ЭРГЭДЭГ.
   Эхний 5м барын чиглэл дараагийн 5м барт зөвхөн 41.7% үргэлжилнэ
   (суурь 48.8%, илүүдэл −7.1, 2 SE давав). Өөрөөр хэлбэл 58.3%
   эргэнэ — анхны хэт үсрэлт буцдаг.

   ГЭВЧ АРИЛЖААНД ОРУУЛАХ БОЛОМЖГҮЙ:
       спред $0.30  −0.142R      ← ердийн үеийн спредээр ч алдагдалтай
       спред $1.00  −0.735R
       спред $3.00  −2.396R
   Шалтгаан нь стопын хэмжээ: 5м дээр 1.5 ATR = ердөө $2.22.
       $0.30 = эрсдэлийн 14%
       $1.00 = эрсдэлийн 45%
       $3.00 = эрсдэлийн 135%   ← стопоос ИЛҮҮ
   Мэдээний эхний секундэд алтны спред яг тэр $2–10 болдог.
   Энэ бол a16-гийн Баасан гарагтай яг ижил хэлбэр: статистик
   байна, гүйцэтгэх боломж байхгүй.

4. АРИЛЖАА БОЛГОХОД ХОЁР ТАЛ АДИЛХАН АЛДАГДАЛТАЙ.
       үргэлжлэл, спред $0.30   −0.060R
       эсрэг,     спред $0.30   −0.060R
   Хоёулаа ЯГ ижил гарсан нь чиглэлийн мэдээлэл ТЭГ гэдгийн шууд
   нотолгоо — үлдсэн зөрүү нь зөвхөн зардал.
   Бодит мэдээний спредээр: −1.06R ($3), −1.74R ($5).

   Санамсаргүй урт −0.031R. Мэдээгээр орох нь түүнээс ДОР.
   Хоёр хугацаанд хоёулаа сөрөг (−0.299R, −0.318R).

ДҮГНЭЛТ
  «АНУ-ын том мэдээ чухал» гэдэг ҮНЭН — гэхдээ зөвхөн ХЭМЖЭЭНИЙ
  хувьд. Үнэ 4 дахин их хөдөлнө. Харин ХААШАА хөдлөхийг мэдээ
  өөрөө ч, түүний эхний хариу үйлдэл ч хэлэхгүй.

  Түүнээс ч дор: мэдээ бол арилжаа хийх ХАМГИЙН ҮНЭТЭЙ мөч.
  Хэлбэлзэл 4 дахин өсөхөд спред 10 дахин өсдөг. Тиймээс мэдээ бол
  боломж биш, ЭРСДЭЛ.

  Тав дахь удаагаа ижил хана (a24 шахалт, a25 лаа, a26 эзлэхүүн,
  a27 момент, a28 мэдээ): хэмжээ таамаглагдана, чиглэл үгүй.

ХИЙГЭЭГҮЙ ЗҮЙЛ — ШУДАРГА ХЭЛЭХЭД
  FOMC-ийн ЯГ огноог өгөгдлөөс таних оролдлого бүтсэнгүй.
  Хэлбэлзлээр илрүүлсэн өдрүүдийн 9 нь 2-р сард, 12 нь 8-р сард
  гарсан — тэр хоёр сард FOMC хуралддаггүй (тэр нь ихэвчлэн
  протоколын нийтлэл байв). Тиймээс «Fed 14:00 ET» гэдэг нь
  шийдвэр ба протокол хоёрыг ХОЛИСОН тоо. Хэмжээний дүгнэлтэд
  хангалттай, чиглэлийн дүгнэлтэд ХАНГАЛТГҮЙ.
  CPI мөн адил — зөвхөн 10–15-ны цонхоор ойролцоолов.
  Жинхэнэ хуанлийн файл байвал хоёуланг нь зөв хийж болно.
"""
import numpy as np
import pandas as pd
from core import load, stat

H1 = load(start='2005-01-01', end='2025-09-12')
M5 = load('XAU_5m_data.csv', start='2005-01-01', end='2025-09-12')


def nfp_hour(year):
    """Брокерийн аль цагийн бар дотор 8:30 ET байна вэ."""
    return 14 if year <= 2010 else 15


def nfp_days(idx):
    """Сар бүрийн эхний баасан."""
    return (idx.dayofweek == 4) & (idx.day <= 7)


def events():
    """NFP үйл явдал бүрийн мэдээний барын эхлэл (брокерийн цаг)."""
    d = H1.index
    mask = nfp_days(d) & np.array([h == nfp_hour(y)
                                   for h, y in zip(d.hour, d.year)])
    return H1.index[mask]


if __name__ == '__main__':
    E = events()
    print("АНУ-ЫН ТОМ МЭДЭЭ · NFP · 2005–2025")
    print(f"{len(E)} үйл явдал (сар бүрийн эхний баасан).\n")

    # ── A. ХЭМЖЭЭ ──
    print("══ A. ХЭМЖЭЭ — мэдээ хэр хөдөлгөж байна ══\n")
    rngs = (H1['high'] - H1['low'])
    base = rngs.median()
    for off in (-2, -1, 0, 1, 2, 3):
        t = E + pd.Timedelta(hours=off)
        r = rngs.reindex(t).dropna()
        lbl = ('МЭДЭЭНИЙ БАР' if off == 0
               else f'{off:+d} цаг')
        print(f"   {lbl:<16}{len(r):>5}   дундаж муж ${r.median():>6.2f}"
              f"   суурийн {r.median() / base:>5.2f} дахин")

    # ── B. ЧИГЛЭЛ ──
    print("\n\n══ B. ЧИГЛЭЛ — эхний хөдөлгөөн цаашдыг хэлж байна уу ══")
    print("   Мэдээний бар (1 цаг) хаагдахад чиглэл мэдэгдэнэ.")
    print("   Дараагийн N цагт тэр чиглэлээ үргэлжлүүлж байна уу.\n")
    o, c = H1['open'], H1['close']
    up = (c > o).reindex(E)
    print(f"   {'дараагийн':<12}{'n':>5}{'үргэлжлэх%':>12}{'суурь%':>9}"
          f"{'ИЛҮҮДЭЛ':>10}")
    print("   " + "─" * 48)
    allup = (c > o)
    for n in (1, 2, 4, 8, 24):
        fwd = (c.shift(-n) > c).reindex(E)
        ok = (up == fwd)
        s = ok.dropna()
        # суурь: ижил геометрээр БҮХ барт
        b = ((allup) == (c.shift(-n) > c)).dropna().mean() * 100
        se = np.sqrt(s.mean() * (1 - s.mean()) / len(s)) * 100
        mk = '  ←' if abs(s.mean() * 100 - b) > 2 * se else ''
        print(f"   {n} цаг{'':<7}{len(s):>5}{s.mean() * 100:>11.1f}%"
              f"{b:>8.1f}%{s.mean() * 100 - b:>+9.1f}{mk}")

    print("\n   ── Эхний 5 МИНУТ цаашдыг хэлэх үү ──")
    print("   (мэдээний эхний 5м бар хаагдахад чиглэл мэдэгдэнэ)\n")
    m5o, m5c = M5['open'], M5['close']
    f5 = E + pd.Timedelta(minutes=30)      # 8:30 ET = барын 30 дахь минут
    up5 = (m5c.reindex(f5) > m5o.reindex(f5))
    print(f"   {'дараагийн':<12}{'n':>5}{'үргэлжлэх%':>12}{'суурь%':>9}"
          f"{'ИЛҮҮДЭЛ':>10}")
    print("   " + "─" * 48)
    allup5 = (m5c > m5o)
    for n in (1, 3, 6, 12, 48):
        fwd = (m5c.shift(-n).reindex(f5) > m5c.reindex(f5))
        ok = (up5 == fwd).dropna()
        b = (allup5 == (m5c.shift(-n) > m5c)).dropna().mean() * 100
        se = np.sqrt(ok.mean() * (1 - ok.mean()) / len(ok)) * 100
        mk = '  ←' if abs(ok.mean() * 100 - b) > 2 * se else ''
        print(f"   {n * 5} минут{'':<4}{len(ok):>5}{ok.mean() * 100:>11.1f}%"
              f"{b:>8.1f}%{ok.mean() * 100 - b:>+9.1f}{mk}")

    print("\n   ── Мэдээний ӨМНӨХ чиглэл дараахыг хэлэх үү ──\n")
    pre = (c.shift(1) > o.shift(1)).reindex(E)     # мэдээний өмнөх цаг
    for n in (1, 4, 24):
        fwd = (c.shift(-n) > c).reindex(E)
        ok = (pre == fwd).dropna()
        se = np.sqrt(ok.mean() * (1 - ok.mean()) / len(ok)) * 100
        print(f"      өмнөх цаг → дараах {n} цаг{'':<3}{len(ok):>5}"
              f"{ok.mean() * 100:>8.1f}%   ±{2 * se:.1f}")


    # ── C/D. АРИЛЖАА ──
    print("\n\n══ C. АРИЛЖАА БОЛГОВОЛ — ЗАРДЛЫГ БОДИТООР ══")
    print("   Мэдээний үед спред $0.3 БИШ. NFP-ийн эхний секундэд")
    print("   алтны спред $2–10 болдог. Дөрвүүлэнг нь тооцов.\n")

    def trade(sig_t, side_fn, k=1.5, rr=2.0, spread=0.3, maxbars=24,
              years=None):
        """Дохионы бар хаагдахад → дараагийн цагийн нээлтээр орно."""
        o_, h_, l_, c_ = (H1['open'].values, H1['high'].values,
                          H1['low'].values, H1['close'].values)
        tr = np.maximum(H1['high'] - H1['low'],
                        np.maximum((H1['high'] - H1['close'].shift()).abs(),
                                   (H1['low'] - H1['close'].shift()).abs()))
        A = tr.rolling(20).mean().values
        pos = H1.index.get_indexer(sig_t)
        R = []
        for i in pos:
            if i < 0 or i + 1 >= len(H1):
                continue
            if years and not (years[0] <= H1.index[i].year <= years[1]):
                continue
            side = side_fn(i)
            if side == 0 or not (A[i] == A[i]) or A[i] <= 0:
                continue
            j = i + 1
            risk = k * A[i]
            ent = o_[j] + side * spread / 2
            stp, tgt = ent - side * risk, ent + side * risk * rr
            out = None
            for m in range(j, min(j + maxbars, len(H1))):
                if side > 0:
                    if l_[m] <= stp: out = -1.0; break
                    if h_[m] >= tgt: out = rr; break
                else:
                    if h_[m] >= stp: out = -1.0; break
                    if l_[m] <= tgt: out = rr; break
            if out is None:
                out = side * (c_[min(j + maxbars - 1, len(H1) - 1)]
                              - ent) / risk
            R.append(out - spread / risk)
        return R

    ov = (H1['close'] > H1['open']).values

    def cont(i):    # үргэлжлэл — мэдээний барын чиглэлээр
        return 1 if ov[i] else -1

    def fade(i):    # эсрэг — мэдээний барыг бүдүүлэг гэж үзэх
        return -1 if ov[i] else 1

    print("   ── Үргэлжлэл (мэдээний чиглэлээр орох) ──")
    for sp in (0.3, 1.0, 3.0, 5.0):
        print("  " + stat(trade(E, cont, spread=sp), f"     спред ${sp:.2f}"))
    print("\n   ── Эсрэг (мэдээний чиглэлийн эсрэг орох) ──")
    for sp in (0.3, 1.0, 3.0, 5.0):
        print("  " + stat(trade(E, fade, spread=sp), f"     спред ${sp:.2f}"))

    print("\n   ── Дрифтийн хяналт: ижил геометр, САНАМСАРГҮЙ өдөр ──")
    for seed_lbl, fn in (('санамсаргүй урт', lambda i: 1),
                         ('санамсаргүй богино', lambda i: -1)):
        allR = []
        for s in range(12):
            rng = np.random.default_rng(s)
            pick = H1.index[rng.choice(len(H1), len(E), replace=False)]
            allR += trade(pick, fn)
        print("  " + stat(allR, f"     {seed_lbl}"))

    print("\n   ── Урт/богино тал тусад нь (үргэлжлэл, спред $1) ──")
    for lbl, fn in (('мэдээ ДЭЭШ → урт',
                     lambda i: 1 if ov[i] else 0),
                    ('мэдээ ДООШ → богино',
                     lambda i: -1 if not ov[i] else 0)):
        print("  " + stat(trade(E, fn, spread=1.0), f"     {lbl}"))

    print("\n   ── Хугацааны хуваалт (үргэлжлэл, спред $1) ──")
    for yy in ((2005, 2016), (2017, 2025)):
        print("  " + stat(trade(E, cont, spread=1.0, years=yy),
                          f"     {yy[0]}–{yy[1]}"))

    # ── E. ЦОРЫН ГАНЦ АЧ ХОЛБОГДОЛТОЙ ОЛДВОР ──
    print("\n\n══ E. ЭХНИЙ 5 МИНУТЫН ЭРГЭЛТ ══")
    print("   B хэсэгт ганц ач холбогдолтой зүйл гарсан: мэдээний")
    print("   эхний 5м бар дараагийн 5м барт 58.3% ЭРГЭДЭГ.")
    print("   Энэ нь анхны хэт үсрэлт (overshoot) байх магадлалтай.")
    print("   Арилжаа болгоё — 5м стоп нь ЖИЖИГ тул спред хамаагүй том.\n")

    def trade5(sig_t, side_fn, k=1.5, rr=2.0, spread=0.3, maxbars=24):
        o_, h_, l_, c_ = (M5['open'].values, M5['high'].values,
                          M5['low'].values, M5['close'].values)
        tr = np.maximum(M5['high'] - M5['low'],
                        np.maximum((M5['high'] - M5['close'].shift()).abs(),
                                   (M5['low'] - M5['close'].shift()).abs()))
        A = tr.rolling(20).mean().values
        pos = M5.index.get_indexer(sig_t)
        R, risks = [], []
        for i in pos:
            if i < 0 or i + 1 >= len(M5):
                continue
            side = side_fn(i)
            if side == 0 or not (A[i] == A[i]) or A[i] <= 0:
                continue
            j = i + 1
            risk = k * A[i]
            risks.append(risk)
            ent = o_[j] + side * spread / 2
            stp, tgt = ent - side * risk, ent + side * risk * rr
            out = None
            for m in range(j, min(j + maxbars, len(M5))):
                if side > 0:
                    if l_[m] <= stp: out = -1.0; break
                    if h_[m] >= tgt: out = rr; break
                else:
                    if h_[m] >= stp: out = -1.0; break
                    if l_[m] <= tgt: out = rr; break
            if out is None:
                out = side * (c_[min(j + maxbars - 1, len(M5) - 1)]
                              - ent) / risk
            R.append(out - spread / risk)
        return R, np.median(risks) if risks else np.nan

    ov5 = (M5['close'] > M5['open']).values
    f5i = M5.index.get_indexer(f5)
    med_risk = None
    print("   ── Эсрэг орох (эхний 5м барын эсрэг) ──")
    for sp in (0.3, 1.0, 3.0):
        R, mr = trade5(f5, lambda i: -1 if ov5[i] else 1, spread=sp)
        med_risk = mr
        print("  " + stat(R, f"     спред ${sp:.2f}"))
    print(f"\n   Дундаж эрсдэл (1.5 ATR 5м): ${med_risk:.2f}")
    for sp in (0.3, 1.0, 3.0):
        print(f"      спред ${sp:.2f} нь эрсдэлийн {sp / med_risk * 100:.0f}%")
    print("   → Мэдээний үеийн бодит спред эрсдэлийг БҮХЭЛД нь иднэ.")

    # ── F. НӨГӨӨ ХОЁР МЭДЭЭ ──
    print("\n\n══ F. CPI БА FED — ойролцоо тодорхойлолт ══")
    print("   Эдгээрийн огноо тогтмол БИШ тул нарийвчлал муу.")
    print("   Зөвхөн ХЭМЖЭЭГ харна, чиглэлийн дүгнэлт хийхгүй.\n")
    d = H1.index
    hr_ok = np.array([h == nfp_hour(y) for h, y in zip(d.hour, d.year)])
    cpi = H1.index[hr_ok & (d.day >= 10) & (d.day <= 15)
                   & (d.dayofweek < 5) & ~nfp_days(d)]
    fed_rows = []
    for yr in sorted(set(d.year)):
        x = H1[(d.year == yr) & (d.hour == nfp_hour(yr) + 6)
               & (d.dayofweek == 2)]
        if len(x) < 20:
            continue
        fed_rows.append((x['high'] - x['low']).nlargest(8).index)
    fed = pd.DatetimeIndex(np.concatenate([f.values for f in fed_rows]))
    for lbl, T in (('NFP (тодорхой)', E),
                   ('CPI цонх (10–15)', cpi),
                   ('Fed 14:00 ET (8/жил)', fed)):
        r = rngs.reindex(T).dropna()
        print(f"   {lbl:<24}{len(r):>5}   муж ${r.median():>6.2f}"
              f"   суурийн {r.median() / base:>5.2f} дахин")
        # чиглэлийн үргэлжлэл 4 цагт
        u = (c > o).reindex(T)
        fw = (c.shift(-4) > c).reindex(T)
        ok = (u == fw).dropna()
        se = np.sqrt(ok.mean() * (1 - ok.mean()) / len(ok)) * 100
        b4 = ((c > o) == (c.shift(-4) > c)).dropna().mean() * 100
        print(f"   {'':<24}{'':>5}   4ц үргэлжлэл {ok.mean() * 100:.1f}%"
              f"  (суурь {b4:.1f}%, ±{2 * se:.1f})")

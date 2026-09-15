"""8. Трендлайны 3 дахь хүрэлт — «алт 3 дахь хүрэлт дээр их явдаг».

ЯАГААД 3 ДАХЬ ВЭ
  Шугам зурахад хоёр цэг хэрэгтэй. Тэр хоёр нь 1, 2 дахь хүрэлт.
  Шугам ЗУРАГДСАНЫ дараах анхны хүрэлт нь ГУРАВ дахь нь болно.
  Өөрөөр хэлбэл «3 дахь хүрэлт» гэдэг нь «шугамын анхны ЖИНХЭНЭ
  шалгалт» гэсэн үг — өмнөх хоёр нь шугамыг тодорхойлсон цэгүүд.

АРГАЧЛАЛ
  Тулгуур шугам : дараалсан хоёр батлагдсан ЁРООЛ, налуу нь ӨСӨХ
  Эсэргүүцэл    : дараалсан хоёр батлагдсан ОРГИЛ, налуу нь БУУРАХ
  Идэвхтэй болох: 2 дахь пивот БАТЛАГДСАН мөчөөс (ирээдүй харахгүй)
  Хүрэлт        : барын туйл шугамаас ±tol×ATR дотор орох
  Эвдрэх        : хаалт шугамаас brk×ATR цааш гарах → шугам үхнэ
  Хүрэлт хооронд хамгийн багадаа `gap` бар — нэг ойртолтыг
                  олон удаа тоолохоос сэргийлнэ

  Оролт : хүрэлтийн бар ХААГДАХАД
  Стоп  : шугамаас brk×ATR цааш
  Target: 2R

ГАЖУУДЛЫН АНХААРУУЛГА
  «3 дахь хүрэлт ажилладаг» гэдэг нь амархан хуурмаг гардаг: шугам
  хоёр удаа БАРЬСАН тохиолдолд л 3 дахь хүрэлт ХАРАГДАНА. Барьж
  чадаагүй шугамууд нүднээс алга болдог. Тиймээс энд 3, 4, 5 дахь
  хүрэлтийг ХАРЬЦУУЛЖ, мөн суурьтай нь тулгана.

ҮР ДҮН: 3 дахь хүрэлт ОНЦГОЙ БИШ.

      3 дахь хүрэлт      2975   32.0%   −0.050R ±0.025
      4 дэх хүрэлт       1553   31.7%   −0.057R ±0.035
      5 дахь хүрэлт       805   33.0%   −0.027R ±0.049
      6+ дахь хүрэлт     1075   31.4%   −0.059R ±0.042
      БҮХ хүрэлт (суурь) 6408   32.0%   −0.050R ±0.017

  3 дахь хүрэлт нь суурьтай ЯГ ижил (−0.050 vs −0.050), ялалтын хувь
  нь ч ижил (32.0% vs 32.0%). Ялгаа огт алга.

ХАМГИЙН ХҮЧТЭЙ НОТОЛГОО — ШУГАМД САНАХ ОЙ БАЙХГҮЙ
  Хүрэлт бүрийн дараа шугам амьд үлдэх магадлал:

      3 → 4   52%
      4 → 5   52%
      5 → 6   58%
      6 → 7   57%
      7 → 8   56%
      8 → 9   57%

  Хэд дэх хүрэлт байхаас үл хамааран ~55% тогтмол. Хэрэв «шугам
  бэхжиж байгаа» бол энэ хувь өсөх ёстой; «ядарч байгаа» бол буурах
  ёстой. Аль нь ч болоогүй — тогтмол байна. Энэ бол санамсаргүй
  үйл явцын яг тэр шинж. Шугам өмнө нь хэдэн удаа барьсныг «санадаггүй».

  Тохиргоо (tol, ZigZag %, өдрийн хүрээ, пивот алгасах) бүгдэд нь
  ижил — нэг ч хувилбарт эерэг гараагүй.

ЯАГААД ЧАРТ ДЭЭР ӨӨРӨӨР ХАРАГДДАГ ВЭ
  Барьсан 3 дахь хүрэлт нь чарт дээр тод үлддэг — шугам зурагдсан
  хэвээр, хажууд нь том лаа. Барьж чадаагүй нь харагдахаа больдог,
  учир нь шугамыг нь бид дахин зурдаггүй. Нүд нь амьд үлдсэнийг нь
  л тоолдог. Энэ тоо (52%) бол хоёуланг нь тоолсон дүн.
"""
import numpy as np
import pandas as pd
from core import load, resample, zigzag, confirm_index, stat, bar_len

h = load(start='2005-01-01', end='2025-09-12')
D5 = load('XAU_5m_data.csv', start='2005-01-01', end='2025-09-12')
H5, L5, C5, I5 = (D5['high'].values, D5['low'].values,
                  D5['close'].values, D5.index)


def frame(tf):
    d = resample(h, tf)
    H, L, C = d['high'].values, d['low'].values, d['close'].values
    tr = np.maximum(H[1:] - L[1:], np.maximum(abs(H[1:] - C[:-1]),
                                              abs(L[1:] - C[:-1])))
    atr = pd.Series(np.concatenate([[H[0] - L[0]], tr])).rolling(14).mean().values
    return d, H, L, C, atr


def touches(tf='4h', pct=0.01, tol=0.35, brk=0.5, gap=3, skip=1, maxlen=400):
    """Бүх шугамын бүх хүрэлтийг олно.  Буцаах: жагсаалт dict.

    skip : 1 = дараалсан хоёр пивот.  2 = нэгийг алгасаад холбоно
           (хүмүүс бодит дээр ингэж ч зурдаг).
    """
    d, H, L, C, atr = frame(tf)
    dt = bar_len(tf)
    piv = zigzag(d, pct)
    conf = {}
    for (pi, pv, pdir) in piv:
        ci = confirm_index(d, pi, pv, pdir, pct)
        if ci is not None:
            conf[pi] = ci

    out = []
    for want, is_sup in ((-1, True), (1, False)):
        pts = [(pi, pv) for (pi, pv, pdir) in piv if pdir == want and pi in conf]
        for k in range(len(pts) - skip):
            (ia, pa), (ib, pb) = pts[k], pts[k + skip]
            if ib <= ia:
                continue
            slope = (pb - pa) / (ib - ia)
            # Тулгуур нь ӨСӨХ, эсэргүүцэл нь БУУРАХ ёстой — эс тэгвэл
            # энэ нь трендлайн биш, зүгээр хоёр цэгийн шулуун.
            if is_sup and slope <= 0:
                continue
            if (not is_sup) and slope >= 0:
                continue

            start = conf[ib] + 1          # шугам ЭНДЭЭС л мэдэгдэнэ
            n, last = 2, -99              # эхний хоёр хүрэлт = тулгуур цэгүүд
            for x in range(start, min(start + maxlen, len(d))):
                a = atr[x]
                if not (a > 0):
                    continue
                v = pa + slope * (x - ia)
                if v <= 0:
                    break
                if C[x] < v - brk * a if is_sup else C[x] > v + brk * a:
                    break                  # шугам эвдэрсэн
                near = (L[x] <= v + tol * a) if is_sup else (H[x] >= v - tol * a)
                if not near or x - last < gap:
                    continue
                n += 1
                last = x
                stop = v - brk * a if is_sup else v + brk * a
                out.append(dict(t=d.index[x] + dt, n=n, sup=is_sup,
                                entry=C[x], stop=stop, atr=a,
                                year=d.index[x].year))
    return out


def run(tf='4h', rr=2.0, hold=40, spread=0.3, nsel=None, side=None,
        years=None, **kw):
    """Хүрэлтүүдийг 5 минутын өгөгдөл дээр гүйцэтгэж R буцаана.

    nsel : хэд дэх хүрэлтийг авах вэ.  3 | 4 | (5, 99) | None = бүгд
    """
    nb = int(bar_len(tf) / pd.Timedelta('5min')) * hold
    res = []
    for s in touches(tf, **kw):
        if nsel is not None:
            lo, hi = nsel if isinstance(nsel, tuple) else (nsel, nsel)
            if not (lo <= s['n'] <= hi):
                continue
        if years and not (years[0] <= s['year'] < years[1]):
            continue
        if side == 'urt' and not s['sup']:
            continue
        if side == 'bogino' and s['sup']:
            continue
        up = s['sup']                       # тулгуур дээр УРТ
        e = s['entry'] + spread if up else s['entry'] - spread
        st = s['stop']
        risk = (e - st) if up else (st - e)
        if risk <= 0:
            continue
        tg = e + rr * risk if up else e - rr * risk
        k = I5.searchsorted(s['t'])
        if k >= len(I5) - nb:
            continue
        r = None
        for j in range(k, k + nb):
            if up:
                if L5[j] <= st: r = -1.0; break
                if H5[j] >= tg: r = rr;   break
            else:
                if H5[j] >= st: r = -1.0; break
                if L5[j] <= tg: r = rr;   break
        if r is None:
            px = C5[k + nb - 1]
            r = ((px - e) if up else (e - px)) / risk
        res.append(r)
    return np.array(res)


if __name__ == '__main__':
    print("Трендлайны хүрэлт.  4 цаг, ZigZag 1%, стоп = шугамаас 0.5 ATR,")
    print("target 1:2, 5 минутын гүйцэтгэл, спред $0.3\n")

    print("── 1. ХЭД дэх хүрэлт вэ ──")
    print("   Таны таамаг: 3 дахь нь онцгой.\n")
    print(f"   {'':<30}{'n':>6} {'Ялалт':>7} {'Дундаж':>9}")
    print("   " + "─" * 62)
    for sel, lbl in ((3, '3 дахь хүрэлт'), (4, '4 дэх хүрэлт'),
                     (5, '5 дахь хүрэлт'), ((6, 99), '6+ дахь хүрэлт'),
                     (None, 'бүх хүрэлт (суурь)')):
        print("   " + stat(run(nsel=sel), lbl))

    print("\n── 2. 3 дахь хүрэлтийг дөрвөн шалгуураар ──\n")
    for kw, lbl in ((dict(years=(2005, 2017)), '2005–2016'),
                    (dict(years=(2017, 2026)), '2017–2025'),
                    (dict(side='urt'), 'тулгуур (УРТ)'),
                    (dict(side='bogino'), 'эсэргүүцэл (БОГИНО)'),
                    (dict(spread=0.6), 'спред $0.6'),
                    (dict(spread=0.0), 'спредгүй')):
        print("   " + stat(run(nsel=3, **kw), lbl))

    print("\n── 3. Тохиргоонд мэдрэг эсэх (3 дахь хүрэлт) ──")
    print("   Зөвхөн нэг тохиргоонд ажиллавал тэр нь тохироо.\n")
    for kw, lbl in ((dict(tol=0.20), 'хүрэлт нарийн 0.2 ATR'),
                    (dict(tol=0.50), 'хүрэлт өргөн 0.5 ATR'),
                    (dict(pct=0.02), 'ZigZag 2%'),
                    (dict(skip=2), 'нэг пивот алгасаж зурсан'),
                    (dict(tf='1D'), 'өдрийн шугам')):
        print("   " + stat(run(nsel=3, **kw), lbl))

    print("\n── 4. Target-ээс хамаарах уу (3 дахь хүрэлт) ──\n")
    for rr in (1.0, 2.0, 3.0):
        print("   " + stat(run(nsel=3, rr=rr), f'TP 1:{rr:.0f}'))

    print("\n── 5. Шугам хэр удаан амьдардаг вэ ──\n")
    ts = touches()
    c = pd.Series([s['n'] for s in ts]).value_counts().sort_index()
    tot = len(set())
    prev = None
    for n, cnt in c.items():
        extra = f"   ({cnt / prev * 100:>4.0f}% нь өмнөхөөс үлдсэн)" if prev else ""
        print(f"      {n} дахь хүрэлт  {cnt:>6}{extra}")
        prev = cnt

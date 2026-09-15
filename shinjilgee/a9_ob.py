"""9. Order Block — бүтэц эвдэхийн өмнөх сүүлчийн эсрэг лаа.

БҮТЭЦ
    1. Үнэ өмнөх L барын дээд цэгийг ЭВДЭНЭ (BOS)
    2. Тэр эвдрэлийн ӨМНӨХ сүүлчийн БУУРАХ лаа = Order Block
    3. Үнэ буцаж тэр лааны мужид ирэхэд ОРНО (урт)

    Муж  : [OB-ийн доод, OB-ийн дээд]
    Стоп : OB-ийн доод цэгээс buf×ATR доош
    TP   : 2R

BOS-ийг ЯАЖ ТОДОРХОЙЛСОН БЭ
  Өмнөх L барын хамгийн өндөр цэгээс ДЭЭШ хаагдах = эвдрэл.
  Энэ нь тухайн барын хаалтад мэдэгдэнэ — ирээдүй харахгүй.
  (zigzag ашиглаж болох ч түүнд confirm хүлээх шаардлагатай болж
   OB хэт хоцордог. Rolling max нь илүү шууд.)

ХОЁР ОРОЛТ ХАРЬЦУУЛНА — a2-ийн гол дүгнэлтийг дахин шалгах
    limit    : муждаа хүрмэгц (сонгодог OB арилжаа)
    batalgaa : мужид хүрээд тэндээсээ буцаж хаагдтал хүлээнэ

ҮР ДҮН: ДАВУУ ТАЛГҮЙ.

      1ц · limit      5900   33.0%   −0.028R ±0.018
      1ц · баталгаа   5118   32.2%   −0.065R ±0.019
      4ц · limit      1740   32.6%   −0.036R ±0.033
      4ц · баталгаа   1559   31.6%   −0.069R ±0.035
      өдөр · limit     367   31.1%   −0.068R ±0.072
      өдөр · баталгаа  350   31.1%   −0.067R ±0.074

  Бүх хугацаа, бүх оролт, бүх тохиргоонд сөрөг. TP 1:1, 1:2, 1:3
  бүгд ижил (−0.069, −0.069, −0.073) — target-ээс огт хамаарахгүй нь
  бүтэц өөрөө мэдээлэл агуулаагүйн шинж.

ЭНД БАТАЛГАА ТУСЛААГҮЙ — ЯАГААД ВЭ (a2, a7-оос ЯЛГААТАЙ)
  a2 болон a7-д «баталгаа хүлээх» нь тодорхой тусалсан. Энд ЭСРЭГЭЭР
  болов: limit −0.036R, баталгаа −0.069R.

  Шалтгаан нь стопын байрлалд байна. a2-т стоп нь БҮТЭЦЭЭС хамаарч
  хол байсан тул хүлээхэд эрсдэл өсдөггүй. OB-д стоп нь мужийн цаана
  ТОГТСОН — хүлээж байгаад дээгүүр орох тусам оролт стопоос холдож,
  эрсдэл өсөж, R жижгэрдэг. Хожих нь сайжирсан ч R нь хорогдоно.

  Сургамж: «баталгаа хүлээ» гэдэг бүх нөхцөлд хүчинтэй дүрэм БИШ.
  Стоп нь бүтцээс хамаарч ХӨДӨЛДӨГ үед л ажиллана.

  Спредгүй бол −0.007R буюу яг тэг. Өөрөөр хэлбэл order block нь
  санамсаргүй цэгээс ялгарахгүй.
"""
import numpy as np
import pandas as pd
from core import load, resample, stat, bar_len

h = load(start='2005-01-01', end='2025-09-12')
D5 = load('XAU_5m_data.csv', start='2005-01-01', end='2025-09-12')
H5, L5, C5, I5 = (D5['high'].values, D5['low'].values,
                  D5['close'].values, D5.index)


def frame(tf):
    d = resample(h, tf)
    H, L, C, O = (d['high'].values, d['low'].values,
                  d['close'].values, d['open'].values)
    tr = np.maximum(H[1:] - L[1:], np.maximum(abs(H[1:] - C[:-1]),
                                              abs(L[1:] - C[:-1])))
    atr = pd.Series(np.concatenate([[H[0] - L[0]], tr])).rolling(14).mean().values
    return d, H, L, C, O, atr


def blocks(tf='4h', look=20, win=10):
    """Order block-уудыг олно.  win = OB-г хайх ухрах цонх."""
    d, H, L, C, O, atr = frame(tf)
    dt = bar_len(tf)
    ph = pd.Series(H).rolling(look).max().shift(1).values   # өмнөх L барын дээд
    pl = pd.Series(L).rolling(look).min().shift(1).values
    out, seen = [], set()
    for x in range(look + 1, len(d)):
        a = atr[x]
        if not (a > 0):
            continue
        for up in (True, False):
            if up and not (C[x] > ph[x]):
                continue
            if (not up) and not (C[x] < pl[x]):
                continue
            j = None
            for k in range(x - 1, max(x - 1 - win, 0), -1):
                if (C[k] < O[k]) if up else (C[k] > O[k]):
                    j = k
                    break
            if j is None or (j, up) in seen:
                continue
            seen.add((j, up))
            if H[j] <= L[j]:
                continue
            out.append(dict(t=d.index[x] + dt, up=up,
                            hi=H[j], lo=L[j], atr=a,
                            year=d.index[x].year))
    return out


def run(tf='4h', mode='limit', rr=2.0, buf=0.1, hold=60, spread=0.3,
        side=None, years=None, **kw):
    """OB-уудыг 5 минутын өгөгдөл дээр гүйцэтгэнэ.

    mode: 'limit'    = мужид хүрмэгц
          'batalgaa' = мужид хүрээд буцаж хаагдтал хүлээнэ
    """
    nb = int(bar_len(tf) / pd.Timedelta('5min')) * hold
    res = []
    for b in blocks(tf, **kw):
        if years and not (years[0] <= b['year'] < years[1]):
            continue
        up = b['up']
        if side == 'urt' and not up:
            continue
        if side == 'bogino' and up:
            continue
        lvl = b['hi'] if up else b['lo']          # мужийн ойрын ирмэг
        st = (b['lo'] - buf * b['atr']) if up else (b['hi'] + buf * b['atr'])
        k = I5.searchsorted(b['t'])
        if k >= len(I5) - nb:
            continue

        ei = None
        touched = False
        for i in range(k, k + nb):
            if up:
                if L5[i] <= st:                   # муж эвдэрсэн — арилжаа алга
                    break
                if mode == 'limit':
                    if L5[i] <= lvl:
                        e, ei = lvl, i; break
                else:
                    if L5[i] <= lvl:
                        touched = True
                    if touched and C5[i] > lvl:
                        e, ei = C5[i], i; break
            else:
                if H5[i] >= st:
                    break
                if mode == 'limit':
                    if H5[i] >= lvl:
                        e, ei = lvl, i; break
                else:
                    if H5[i] >= lvl:
                        touched = True
                    if touched and C5[i] < lvl:
                        e, ei = C5[i], i; break
        if ei is None:
            continue

        e = e + spread if up else e - spread
        risk = (e - st) if up else (st - e)
        if risk <= 0:
            continue
        tg = e + rr * risk if up else e - rr * risk
        # limit-д оролтын бар дотор стоп ч хүрсэн бол алдагдал гэж үзнэ
        if mode == 'limit' and ((up and L5[ei] <= st) or ((not up) and H5[ei] >= st)):
            res.append(-1.0)
            continue
        r = None
        for j in range(ei + 1, min(k + nb, len(I5))):
            if up:
                if L5[j] <= st: r = -1.0; break
                if H5[j] >= tg: r = rr;   break
            else:
                if H5[j] >= st: r = -1.0; break
                if L5[j] <= tg: r = rr;   break
        if r is None:
            px = C5[min(k + nb, len(I5)) - 1]
            r = ((px - e) if up else (e - px)) / risk
        res.append(r)
    return np.array(res)


if __name__ == '__main__':
    print("Order Block.  Стоп = мужийн цаана 0.1 ATR, TP 1:2,")
    print("5 минутын гүйцэтгэл, спред $0.3\n")

    print("── 1. Хугацаа × оролтын арга ──\n")
    print(f"   {'':<30}{'n':>6} {'Ялалт':>7} {'Дундаж':>9}")
    print("   " + "─" * 62)
    for tf in ('1h', '4h', '1D'):
        for m, ml in (('limit', 'limit'), ('batalgaa', 'БАТАЛГАА')):
            print("   " + stat(run(tf, m), f'{tf} · {ml}'))
        print()

    print("── 2. Дөрвөн шалгуур (4ц, баталгаатай оролт) ──\n")
    for kw, lbl in ((dict(years=(2005, 2017)), '2005–2016'),
                    (dict(years=(2017, 2026)), '2017–2025'),
                    (dict(side='urt'), 'зөвхөн УРТ'),
                    (dict(side='bogino'), 'зөвхөн БОГИНО'),
                    (dict(spread=0.6), 'спред $0.6'),
                    (dict(spread=0.0), 'спредгүй')):
        print("   " + stat(run('4h', 'batalgaa', **kw), lbl))

    print("\n── 3. Тохиргоонд мэдрэг эсэх (4ц, баталгаатай) ──\n")
    for kw, lbl in ((dict(look=10), 'BOS цонх 10 бар'),
                    (dict(look=40), 'BOS цонх 40 бар'),
                    (dict(buf=0.3), 'стоп илүү зайтай'),
                    (dict(rr=1.0), 'TP 1:1'),
                    (dict(rr=3.0), 'TP 1:3')):
        print("   " + stat(run('4h', 'batalgaa', **kw), lbl))

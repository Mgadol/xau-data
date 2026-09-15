"""10. FVG / Fair Value Gap — тэнцвэргүй байдлын цоорхой.

БҮТЭЦ (3 лаа)
    Өсөх FVG :  low[i+1] > high[i-1]   → дунд нь ЦООРХОЙ үлдэнэ
    Буурах FVG:  high[i+1] < low[i-1]

    Муж   : [high[i-1], low[i+1]]
    Идэвх : i+1 лаа ХААГДАХАД мэдэгдэнэ (ирээдүй харахгүй)
    Оролт : үнэ буцаж цоорхойд ирэхэд
    Стоп  : цоорхойн цаана buf×ATR
    TP    : 2R

ГУРВАН ОРОЛТЫН ЦЭГ ХАРЬЦУУЛНА
    ирмэг  : цоорхойн ойрын ирмэг (хамгийн эрт, хамгийн их эрсдэл)
    дунд   : 50% (CE — consequent encroachment, хамгийн түгээмэл)
    алс    : цоорхойн алсын ирмэг (хамгийн сайн үнэ, ирэхгүй байж болно)

ХОЁР ӨӨР АСУУЛТ
  1. Цоорхой ДҮҮРДЭГ үү?  (үнэ буцаж ирдэг үү)
  2. Цоорхой ТУЛГУУР болдог уу?  (ирээд эргэдэг үү)
  Эхнийх нь бараг үргэлж «тийм» — тэр нь зах зээлийн хэлбэлзлийн шинж,
  давуу тал биш. Хоёр дахь нь л чухал.

ҮР ДҮН 1: ЦООРХОЙ БАРАГ ҮРГЭЛЖ ДҮҮРДЭГ (гэхдээ энэ нь ашиггүй мэдээлэл)

      1ц   n=24023   хэсэгчлэн 91.5%   бүрэн 84.8%
      4ц   n= 6652   хэсэгчлэн 90.5%   бүрэн 83.7%
      өдөр n= 1238   хэсэгчлэн 90.5%   бүрэн 83.7%

  «FVG дүүрдэг» гэдэг үнэн. Гэвч үүнээс мөнгө гарахгүй: үнэ хаашаа ч
  явсан эргэж дайрдаг. Энэ бол хэлбэлзлийн шинж, таамаглал биш.

ҮР ДҮН 2: ТУЛГУУР БОЛОХ ЧАДВАР — ДАВУУ ТАЛГҮЙ

      4ц · ирмэг       5454   32.6%   −0.028R
      4ц · дунд (CE)   4826   32.4%   −0.028R
      1ц · дунд       15755   31.1%   −0.070R
      өдөр · дунд       986   31.3%   −0.061R

  Цоорхойн ХЭМЖЭЭ ч нэмэргүй: ≥0.5 ATR −0.001R, ≥1 ATR −0.062R,
  ≥2 ATR −0.159R. Том цоорхой нь илүү хүчтэй гэдэг нь батлагдаагүй.

ҮР ДҮН 3: «АЛС ИРМЭГ» ГЭДЭГ ХУУРМАГ ЭЕРЭГ — ЯАЖ ИЛРҮҮЛСЭН БЭ

  Цоорхойн алс ирмэгт орох хувилбар +0.133R ±0.025 өгсөн. n=3312,
  5.3 стандарт алдаа. Дөрвөн шалгуурын дөрвийг нь ч давсан:
  2005–2016 +0.096R, 2017–2025 +0.180R, урт +0.178R, богино +0.084R.

  Гэвч энэ нь ирмэг БИШ. Хоёр зүйл илчилсэн:

    Стопын зайг өөрчлөхөд:        Спредийг өөрчлөхөд:
      0.10 ATR   +0.133R  ✓         $0.3   +0.133R  ✓
      0.25 ATR   +0.030R  ✗         $0.6   −0.114R  ✗
      0.50 ATR   −0.015R  ✗         $1.0   −0.302R  ✗
      1.00 ATR   −0.021R  ✗

  Зөвхөн ХАМГИЙН нарийн стоп дээр л ажиллаж, бага зэрэг тавихад
  шууд алга болно. Бодит тоогоор: 4ц-ийн ATR дунджаар $7.08, тэгэхээр
  стоп нь $0.71, target нь $1.42. Спред $0.3 нь эрсдэлийн 42%!

  Өөрөөр хэлбэл энэ нь FVG-ийн шинж чанар биш, зүгээр л «маш нарийн
  стоптой скальп». Ийм стоп нь спред өргөсөхөд, slippage-д, ямар ч
  бодит гүйцэтгэлд амьд үлдэхгүй.

  СУРГАМЖ: дөрвөн шалгуур давсан ч болоогүй. Тохиргооны МЭДРЭГ
  ШИНЖИЛГЭЭ (энд стопын зай) нь тусдаа шаардлагатай. Нэг параметрийн
  хамгийн захын утга дээр л ажиллаж байвал тэр нь олдвор биш.
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
    H, L, C = d['high'].values, d['low'].values, d['close'].values
    tr = np.maximum(H[1:] - L[1:], np.maximum(abs(H[1:] - C[:-1]),
                                              abs(L[1:] - C[:-1])))
    atr = pd.Series(np.concatenate([[H[0] - L[0]], tr])).rolling(14).mean().values
    return d, H, L, C, atr


def gaps(tf='4h', minsz=0.0):
    """FVG-үүдийг олно.  minsz = хамгийн бага хэмжээ (ATR-ээр)."""
    d, H, L, C, atr = frame(tf)
    dt = bar_len(tf)
    out = []
    for i in range(1, len(d) - 1):
        a = atr[i + 1]
        if not (a > 0):
            continue
        for up in (True, False):
            if up:
                lo_, hi_ = H[i - 1], L[i + 1]      # цоорхойн доод, дээд
            else:
                lo_, hi_ = H[i + 1], L[i - 1]
            if hi_ <= lo_:
                continue
            if (hi_ - lo_) < minsz * a:
                continue
            out.append(dict(t=d.index[i + 1] + dt, up=up,
                            lo=lo_, hi=hi_, atr=a, year=d.index[i].year))
    return out


def run(tf='4h', at='dund', rr=2.0, buf=0.1, hold=60, spread=0.3,
        side=None, years=None, **kw):
    """at: 'irmeg' | 'dund' | 'als'"""
    nb = int(bar_len(tf) / pd.Timedelta('5min')) * hold
    res = []
    for g in gaps(tf, **kw):
        if years and not (years[0] <= g['year'] < years[1]):
            continue
        up = g['up']
        if side == 'urt' and not up:
            continue
        if side == 'bogino' and up:
            continue
        # Өсөх FVG-д үнэ ДЭЭРЭЭС буцаж ирнэ: ойрын ирмэг = цоорхойн дээд
        if up:
            near, far = g['hi'], g['lo']
        else:
            near, far = g['lo'], g['hi']
        lvl = {'irmeg': near, 'als': far,
               'dund': (g['lo'] + g['hi']) / 2}[at]
        st = (g['lo'] - buf * g['atr']) if up else (g['hi'] + buf * g['atr'])

        k = I5.searchsorted(g['t'])
        if k >= len(I5) - nb:
            continue
        ei = None
        for i in range(k, k + nb):
            if up:
                if L5[i] <= st:
                    break                       # цоорхой бүрэн эвдэрсэн
                if L5[i] <= lvl:
                    ei = i; break
            else:
                if H5[i] >= st:
                    break
                if H5[i] >= lvl:
                    ei = i; break
        if ei is None:
            continue

        e = lvl + spread if up else lvl - spread
        risk = (e - st) if up else (st - e)
        if risk <= 0:
            continue
        tg = e + rr * risk if up else e - rr * risk
        if (up and L5[ei] <= st) or ((not up) and H5[ei] >= st):
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


def fill_rate(tf='4h', hold=60, **kw):
    """Цоорхой хэдэн хувь нь дүүрдэг вэ (ойрын ирмэгт хүрэх)."""
    nb = int(bar_len(tf) / pd.Timedelta('5min')) * hold
    n = hit = full = 0
    for g in gaps(tf, **kw):
        k = I5.searchsorted(g['t'])
        if k >= len(I5) - nb:
            continue
        n += 1
        w = slice(k, k + nb)
        if g['up']:
            if L5[w].min() <= g['hi']: hit += 1
            if L5[w].min() <= g['lo']: full += 1
        else:
            if H5[w].max() >= g['lo']: hit += 1
            if H5[w].max() >= g['hi']: full += 1
    return n, hit / n * 100, full / n * 100


if __name__ == '__main__':
    print("FVG.  Стоп = цоорхойн цаана 0.1 ATR, TP 1:2,")
    print("5 минутын гүйцэтгэл, спред $0.3\n")

    print("── 1. Цоорхой ДҮҮРДЭГ ҮҮ (60 лааны дотор) ──")
    print("   Энэ нь давуу тал биш — хэлбэлзлийн шинж. Харьцуулах суурь.\n")
    for tf in ('1h', '4h', '1D'):
        n, a, b = fill_rate(tf)
        print(f"   {tf:<6} n={n:>6}   хэсэгчлэн дүүрсэн {a:>5.1f}%   "
              f"бүрэн дүүрсэн {b:>5.1f}%")

    print("\n── 2. Оролтын цэг × хугацаа ──\n")
    print(f"   {'':<30}{'n':>6} {'Ялалт':>7} {'Дундаж':>9}")
    print("   " + "─" * 62)
    for tf in ('1h', '4h', '1D'):
        for at, al in (('irmeg', 'ирмэг'), ('dund', 'дунд (CE)'), ('als', 'алс ирмэг')):
            print("   " + stat(run(tf, at), f'{tf} · {al}'))
        print()

    print("── 3. Цоорхойн ХЭМЖЭЭ чухал уу (4ц, дунд) ──")
    print("   Том цоорхой = хүчтэй тэнцвэргүй байдал гэж үздэг.\n")
    for ms in (0.0, 0.5, 1.0, 2.0):
        print("   " + stat(run('4h', 'dund', minsz=ms), f'хэмжээ ≥ {ms} ATR'))

    print("\n── 4. Дөрвөн шалгуур (4ц, дунд) ──\n")
    for kw, lbl in ((dict(years=(2005, 2017)), '2005–2016'),
                    (dict(years=(2017, 2026)), '2017–2025'),
                    (dict(side='urt'), 'зөвхөн УРТ'),
                    (dict(side='bogino'), 'зөвхөн БОГИНО'),
                    (dict(spread=0.6), 'спред $0.6'),
                    (dict(spread=0.0), 'спредгүй')):
        print("   " + stat(run('4h', 'dund', **kw), lbl))

    print("\n── 5. «Алс ирмэг» эерэг гарсан нь ЯАГААД ХУУРМАГ вэ ──")
    print("   Дөрвөн шалгуурыг давсан ч ЭНЭ хоёр шалгалтад унана.\n")
    print("   Дөрвөн шалгуур (бүгд давсан):")
    for kw, lbl in ((dict(years=(2005, 2017)), '2005–2016'),
                    (dict(years=(2017, 2026)), '2017–2025'),
                    (dict(side='urt'), 'зөвхөн УРТ'),
                    (dict(side='bogino'), 'зөвхөн БОГИНО')):
        print("   " + stat(run('4h', 'als', **kw), lbl))
    print("\n   Стопын зайд МЭДРЭГ эсэх (энд л унана):")
    for b in (0.1, 0.25, 0.5, 1.0):
        print("   " + stat(run('4h', 'als', buf=b), f'стоп {b} ATR цаана'))
    print("\n   Спредэд МЭДРЭГ эсэх:")
    for sp in (0.3, 0.6, 1.0):
        print("   " + stat(run('4h', 'als', spread=sp), f'спред ${sp}'))
    print("\n   4ц ATR дунджаар $7.08 → стоп $0.71, TP $1.42.")
    print("   Спред $0.3 нь эрсдэлийн 42%. Энэ бол ирмэг биш, шуугиан.")

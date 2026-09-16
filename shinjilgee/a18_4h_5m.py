"""18. «4H Sweep + 5m shift + Target 4H High» — нийгмийн сүлжээний setup.

БҮТЭЦ (зурган дээрхээр)
    4 цагийн лаа муж тогтооно      → доод = SSL, дээд = BSL
    Дараагийн лаа доод талыг ЦЭВЭРЛЭНЭ
    5 МИНУТ дээр бүтэц эргэнэ («shift»)
    Оролт : тэр 5м мөчид
    Стоп  : цэвэрлэгээний хамгийн доод цэг
    Target: 4 цагийн лааны ДЭЭД тал

  Энэ нь a7 (CRT)-тэй бараг ижил — ГАНЦ ялгаа нь ОРОЛТЫН МӨЧ:
      a7   4 цагийн лаа хаагдахад ордог
      a18  5 минут дээр бүтэц эргэмэгц ордог   ← илүү эрт, стоп нарийн

  «Стоп нарийсвал R өснө» гэсэн логик. Үүнийг шалгана.

«SHIFT»-ИЙГ ХОЁР ЯНЗААР ТОДОРХОЙЛНО
  Зураг дээр «shift» гэдэг нь тодорхойгүй тул хоёуланг нь шалгана:

    close : 5м лаа түвшний ДОТОГШОО хаагдана        (энгийн)
    mss   : цэвэрлэгээний ӨМНӨХ 12 барын дээд цэгээс
            дээш хаагдана                            (жинхэнэ MSS)

  mss нь илүү хатуу — хоцорч ордог ч бүтэц үнэхээр эргэсэн байна.

ИРЭЭДҮЙ ХАРАХГҮЙ
  Түвшин нь ӨМНӨХ 4 цагийн лааных — тухайн лаа эхлэхэд аль хэдийн
  мэдэгдэнэ. Оролт, стоп, target бүгд тэр мөчид тодорхой.
  a4-ийн bar_len алдаа энд гарах боломжгүй.

═══════════════════════════════════════════════════════════════════
ҮР ДҮН: ДАВУУ ТАЛГҮЙ. Бүх шинжилгээн дундаас ХАМГИЙН ТОМ түүвэр.
═══════════════════════════════════════════════════════════════════

      shift = дотогшоо хаагдав   22796   31.8%   −0.172R ±0.010
      shift = MSS (12 бар)        8936   57.4%   −0.099R ±0.009

  n=22,796 тул алдааны зурвас ±0.010 — эргэлзэх зай алга.

  Дөрвөн шалгуур: 2005–2016 −0.183, 2017–2025 −0.158, урт −0.163,
  богино −0.181. Бүгд сөрөг, бүгд ижил.

  MSS хувилбар 57.4% ЯЛДАГ нь хууртах зүйл — стоп нь өргөн, target
  нь ойрхон учир R жижиг. Олон удаа бага хожиж, цөөн удаа их алддаг.

  Target-ээс хамаарахгүй (4ц эсрэг тал −0.172, 1:1 −0.158, 1:2 −0.140,
  1:3 −0.126). Цэвэрлэгээг 2–3 лаа хүлээсэн ч ижил.

ГОЛ ОЛДВОР: «5 МИНУТ ДЭЭР ОРВОЛ СТОП НАРИЙН → R ИХ» ГЭДЭГ БУРУУ

  Энэ setup-ын бүх сонирхол тэр логикт байдаг. Өгөгдөл ЭСРЭГ хариу өгөв.

  Спредийг тэг болговол:

      спред $0.0   +0.012R ±0.013   ← ЯГ ТЭГ
      спред $0.3   −0.172R
      спред $0.6   −0.280R
      спред $1.0   −0.373R

  Түүхий бүтэц нь давуу талгүй (тэг), бүх алдагдал нь ЗАРДЛААС.

  Учир нь стоп нь хэт нарийн:

      5м оролтын стоп   медиан $1.70  → спред нь эрсдэлийн 17.6%
      MSS-ийн стоп      медиан $4.06  → 7.4%
      a7-гийн 4ц оролт  ойролцоо $7   → 4.3%

  Стопыг ӨРГӨН болгох тусам үр дүн ЖИГД сайжирна:

      бүгд        −0.172R
      стоп ≥ $1   −0.125R
      стоп ≥ $2   −0.064R
      стоп ≥ $4   −0.031R

  Яг эсрэгээрээ. Нарийн стоп нь давуу тал биш, зардлын урхи.

  Ижил санааны гурван хувилбарыг зэрэгцүүлбэл:

      a18  4ц түвшин · 5М оролт    22796   −0.172R   ← хамгийн муу
      a7   4ц түвшин · 4Ц оролт     8883   −0.088R
      a4   4ц пивот  · 5м оролт     2026   −0.066R
      a18  ӨДРИЙН түвшин · 5м       4278   −0.037R   ← хамгийн сайн

  Оролтын хугацаа ТОМ болох тусам сайжирна. Setup-ын амлалт нь
  яг буруу зүг рүү чиглүүлж байна.
"""
import numpy as np
import pandas as pd
from core import load, resample, stat, bar_len

h = load(start='2005-01-01', end='2025-09-12')
D5 = load('XAU_5m_data.csv', start='2005-01-01', end='2025-09-12')
H5, L5, C5, I5 = (D5['high'].values, D5['low'].values,
                  D5['close'].values, D5.index)


def setups(tf='4h', mode='close', look=1, pre=12):
    """Зурган дээрх бүтцүүдийг олно.

    look : цэвэрлэгээг хэдэн лааны дотор хүлээх вэ
    pre  : mss горимд цэвэрлэгээний өмнөх хэдэн барын дээдийг авах вэ
    """
    d = resample(h, tf)
    H, L = d['high'].values, d['low'].values
    dt = bar_len(tf)
    nb = int(dt / pd.Timedelta('5min')) * look
    out = []
    for i in range(len(d) - 1):
        h1, l1 = H[i], L[i]
        if h1 <= l1:
            continue
        t0 = d.index[i] + dt              # C1 хаагдсан мөч
        k = I5.searchsorted(t0)
        if k < pre + 2 or k >= len(I5) - nb - 288:
            continue

        for up in (True, False):
            lvl = l1 if up else h1        # доод талыг цэвэрлэвэл УРТ
            tgt = h1 if up else l1        # target = эсрэг тал
            far = lvl
            j = None                      # цэвэрлэгээний туйлын бар
            for x in range(k, k + nb):
                breached = L5[x] < lvl if up else H5[x] > lvl
                if breached:
                    if j is None or (L5[x] < far if up else H5[x] > far):
                        far = L5[x] if up else H5[x]
                        j = x
                    continue
                if j is None:
                    continue
                # ── SHIFT болов уу ──
                if mode == 'close':
                    hit = C5[x] > lvl if up else C5[x] < lvl
                else:
                    ref = (H5[max(0, j - pre):j].max() if up
                           else L5[max(0, j - pre):j].min())
                    if not (ref == ref):
                        break
                    hit = C5[x] > ref if up else C5[x] < ref
                if not hit:
                    continue
                out.append(dict(t=I5[x], i5=x, up=up, entry=C5[x],
                                stop=far, tgt=tgt, year=I5[x].year,
                                lvl=lvl))
                break
    return out


def run(tf='4h', mode='close', spread=0.3, hold=288, side=None,
        years=None, min_risk=None, rr=None, buf=0.0, **kw):
    """R-ийн жагсаалт. rr өгвөл target-ийг түүгээр солино."""
    res = []
    for s in setups(tf, mode, **kw):
        if years and not (years[0] <= s['year'] < years[1]):
            continue
        up = s['up']
        if side == 'urt' and not up:
            continue
        if side == 'bogino' and up:
            continue
        e = s['entry'] + spread if up else s['entry'] - spread
        st = s['stop'] - buf if up else s['stop'] + buf
        risk = (e - st) if up else (st - e)
        if risk <= 0:
            continue
        if min_risk is not None and risk < min_risk:
            continue
        tg = (e + rr * risk if up else e - rr * risk) if rr else s['tgt']
        got = ((tg - e) if up else (e - tg)) / risk
        if got <= 0:
            continue
        k = s['i5']
        r = None
        for x in range(k + 1, min(k + hold, len(I5))):
            if up:
                if L5[x] <= st: r = -1.0; break
                if H5[x] >= tg: r = got;  break
            else:
                if H5[x] >= st: r = -1.0; break
                if L5[x] <= tg: r = got;  break
        if r is None:
            px = C5[min(k + hold, len(I5)) - 1]
            r = ((px - e) if up else (e - px)) / risk
        res.append(r)
    return np.array(res)


def risks(tf='4h', mode='close', **kw):
    """Стопын зайн хуваарилалт — $-аар."""
    out = []
    for s in setups(tf, mode, **kw):
        d = abs(s['entry'] - s['stop'])
        if d > 0:
            out.append(d)
    return np.array(out)


if __name__ == '__main__':
    print("«4H Sweep + 5m shift + Target 4H High»\n")

    print("── 1. SHIFT-ийн хоёр тодорхойлолт (спред $0.3) ──\n")
    print(f"   {'':<32}{'n':>6} {'Ялалт':>7} {'Дундаж':>9}")
    print("   " + "─" * 64)
    print("   " + stat(run(mode='close'), 'shift = дотогшоо хаагдав'))
    print("   " + stat(run(mode='mss'), 'shift = MSS (12 барын дээд)'))

    print("\n── 2. Стопын зай — setup-ын ГОЛ маргаан ──")
    print("   «5м дээр орвол стоп нарийн → R их» гэсэн логикийг шалгая.\n")
    for m in ('close', 'mss'):
        rk = risks(mode=m)
        print(f"   {m:<8} медиан ${np.median(rk):>5.2f}   "
              f"25% ${np.percentile(rk, 25):>5.2f}   75% ${np.percentile(rk, 75):>6.2f}"
              f"   спред $0.3 = {0.3 / np.median(rk) * 100:>4.1f}%")
    print("\n   Харьцуулалт: a7-гийн 4ц оролтын стоп ≈ $7 → спред 4.3%")

    print("\n   Стопын зайгаар шүүвэл (close):\n")
    for mr, lbl in ((None, 'бүгд'), (1.0, 'стоп ≥ $1'),
                    (2.0, 'стоп ≥ $2'), (4.0, 'стоп ≥ $4')):
        print("   " + stat(run(mode='close', min_risk=mr), lbl))

    print("\n── 3. Спредэд мэдрэг эсэх ──\n")
    for sp in (0.0, 0.3, 0.6, 1.0):
        print("   " + stat(run(mode='close', spread=sp), f'спред ${sp}'))

    print("\n── 4. Дөрвөн шалгуур (close) ──\n")
    for kw, lbl in ((dict(years=(2005, 2017)), '2005–2016'),
                    (dict(years=(2017, 2026)), '2017–2025'),
                    (dict(side='urt'), 'зөвхөн УРТ'),
                    (dict(side='bogino'), 'зөвхөн БОГИНО')):
        print("   " + stat(run(mode='close', **kw), lbl))

    print("\n── 5. Target-ээс хамаарах уу ──")
    print("   Зураг дээрх нь 4ц эсрэг тал. Тогтмол R-тэй харьцуулъя.\n")
    print("   " + stat(run(mode='close'), '4ц эсрэг тал (зурган дээрх)'))
    for rr in (1.0, 2.0, 3.0):
        print("   " + stat(run(mode='close', rr=rr), f'TP 1:{rr:.0f}'))

    print("\n── 6. Цэвэрлэгээг хэдэн лааны дотор хүлээх вэ ──\n")
    for lk in (1, 2, 3):
        print("   " + stat(run(mode='close', look=lk), f'{lk} лааны дотор'))

    print("\n── 7. ХУГАЦААНЫ ХҮРЭЭ — a7-той харьцуулалт ──")
    print("   Ижил санаа, зөвхөн оролтын мөч өөр.\n")
    print("   " + stat(run(tf='4h', mode='close'), '4ц түвшин · 5м оролт (энэ)'))
    print("   " + stat(run(tf='1D', mode='close'), 'өдрийн түвшин · 5м оролт'))
    print("\n   a7 (4ц түвшин · 4ц оролт) .....  8883   45.4%   −0.088R")
    print("   a4 (4ц пивот · 5м оролт) ......  2026   32.5%   −0.066R")

"""11. Сессийн хөрвөх чадвар — Азийн муж, өмнөх өдөр/долоо хоногийн туйл.

Брокерийн цаг (EET).  Улаанбаатар = +5.

    Ази     00:00–08:00    (УБ 05:00–13:00)
    Лондон  08:00–16:00    (УБ 13:00–21:00)
    Нью-Йорк 13:00–21:00   (УБ 18:00–02:00)

ДӨРВӨН ТҮВШИН ШАЛГАНА
    Азийн дээд / доод   — Лондон, NY-д цэвэрлэгддэг гэж үздэг
    PDH / PDL           — өмнөх өдрийн дээд / доод
    PWH / PWL           — өмнөх долоо хоногийн дээд / доод

БҮТЭЦ (бүгдэд ижил)
    1. Үнэ түвшинг ДАВНА (цэвэрлэгээ)
    2. 5м лаа буцаж түвшний дотогшоо ХААГДАНА       ← оролт
    3. Стоп = цэвэрлэгээний туйл,  TP = 2R

  a4-тэй ижил механизм, гэхдээ түвшин нь zigzag пивот биш, СЕССИЙН
  тогтсон түвшин. Эдгээр нь бодитоор мэдэгддэг (тооцоолол шаардахгүй,
  бүх хүн ижил газар зурдаг) тул хамгийн бодит хувилбар.

ИРЭЭДҮЙ ХАРАХГҮЙ
  Азийн муж 08:00-д ДУУСНА — арилжааг зөвхөн 08:00-аас хойш хийнэ.
  PDH/PDL нь өмнөх өдрийн, PWH/PWL нь өмнөх долоо хоногийн — бүгд
  бүрэн хаагдсан хугацааных.
"""
import numpy as np
import pandas as pd
from core import load, stat

D5 = load('XAU_5m_data.csv', start='2005-01-01', end='2025-09-12')
H5, L5, C5 = D5['high'].values, D5['low'].values, D5['close'].values
IDX = D5.index
DAY = IDX.normalize()
MIN = IDX.hour * 60 + IDX.minute


def levels():
    """Өдөр бүрд шалгах түвшнүүдийг бэлдэнэ.

    Буцаах: {өдөр: {нэр: (үнэ, эхлэх_минут)}}
    эхлэх_минут — тэр өдрийн хэдэн минутаас хойш арилжаалж болох вэ.
    """
    df = pd.DataFrame({'d': DAY, 'm': MIN, 'h': H5, 'l': L5})
    g = df.groupby('d')
    day_hi, day_lo = g['h'].max(), g['l'].min()
    asia = df[df['m'] < 8 * 60].groupby('d')
    a_hi, a_lo = asia['h'].max(), asia['l'].min()

    days = list(day_hi.index)
    wk = pd.Series(days, index=days).groupby(
        pd.DatetimeIndex(days).to_period('W')).first()
    week_hi = day_hi.groupby(pd.DatetimeIndex(day_hi.index).to_period('W')).max()
    week_lo = day_lo.groupby(pd.DatetimeIndex(day_lo.index).to_period('W')).min()

    out = {}
    for i, d in enumerate(days):
        if i == 0:
            continue
        p = days[i - 1]
        w = pd.Period(d, 'W') - 1
        lv = {}
        if d in a_hi.index and a_hi[d] > a_lo[d]:
            lv['Ази дээд'] = (a_hi[d], 8 * 60)      # 08:00-аас хойш
            lv['Ази доод'] = (a_lo[d], 8 * 60)
        lv['PDH'] = (day_hi[p], 0)
        lv['PDL'] = (day_lo[p], 0)
        if w in week_hi.index:
            lv['PWH'] = (week_hi[w], 0)
            lv['PWL'] = (week_lo[w], 0)
        out[d] = lv
    return out


LV = levels()
DAY_START = {d: i for i, d in zip(range(len(DAY)), DAY)}
_starts = pd.Series(range(len(DAY)), index=DAY).groupby(level=0).first()


def run(name, rr=2.0, spread=0.3, cut=21 * 60, years=None, side=None,
        min_depth=None, maxbars=288):
    """Нэг түвшний төрлийг туулж R буцаана.

    cut : энэ минутаас хойш шинэ оролт хийхгүй (өдрийн төгсгөл)
    """
    res = []
    for d, lv in LV.items():
        if name not in lv:
            continue
        if years and not (years[0] <= d.year < years[1]):
            continue
        px, from_min = lv[name]
        s = _starts.get(d)
        if s is None or s >= len(IDX) - maxbars:
            continue
        e_idx = min(s + 288, len(IDX))
        # дээд түвшин → цэвэрлээд БОГИНО, доод түвшин → УРТ
        short = name.endswith(('дээд', 'H'))
        if side == 'urt' and short:
            continue
        if side == 'bogino' and not short:
            continue

        far = px
        for i in range(s, e_idx):
            if MIN[i] < from_min or MIN[i] > cut:
                continue
            if not (H5[i] > px if short else L5[i] < px):
                continue
            far = max(far, H5[i]) if short else min(far, L5[i])
            if not (C5[i] < px if short else C5[i] > px):
                continue
            if min_depth is not None and abs(far - px) < min_depth:
                break
            e = C5[i] - spread if short else C5[i] + spread
            st = far
            risk = (st - e) if short else (e - st)
            if risk <= 0:
                break
            tg = e - rr * risk if short else e + rr * risk
            r = None
            for j in range(i + 1, min(i + maxbars, len(IDX))):
                if short:
                    if H5[j] >= st: r = -1.0; break
                    if L5[j] <= tg: r = rr;   break
                else:
                    if L5[j] <= st: r = -1.0; break
                    if H5[j] >= tg: r = rr;   break
            if r is None:
                p2 = C5[min(i + maxbars, len(IDX)) - 1]
                r = ((e - p2) if short else (p2 - e)) / risk
            res.append(r)
            break
    return np.array(res)


NAMES = ['Ази дээд', 'Ази доод', 'PDH', 'PDL', 'PWH', 'PWL']

if __name__ == '__main__':
    print("Сессийн хөрвөх чадвар.  Цэвэрлээд буцаж хаагдвал оролт,")
    print("стоп = цэвэрлэгээний туйл, TP 1:2, спред $0.3\n")

    print("── 1. Түвшин бүрээр ──\n")
    print(f"   {'':<30}{'n':>6} {'Ялалт':>7} {'Дундаж':>9}")
    print("   " + "─" * 62)
    for n in NAMES:
        print("   " + stat(run(n), n))

    print("\n── 2. Бүлгээр нэгтгэсэн ──\n")
    for grp, lbl in ((('Ази дээд', 'Ази доод'), 'Ази (хоёр тал)'),
                     (('PDH', 'PDL'), 'Өмнөх өдөр'),
                     (('PWH', 'PWL'), 'Өмнөх долоо хоног')):
        R = np.concatenate([run(n) for n in grp])
        print("   " + stat(R, lbl))

    print("\n── 3. Өмнөх өдрийн туйлыг дөрвөн шалгуураар ──\n")
    for kw, lbl in ((dict(years=(2005, 2017)), '2005–2016'),
                    (dict(years=(2017, 2026)), '2017–2025'),
                    (dict(side='urt'), 'зөвхөн УРТ (PDL)'),
                    (dict(side='bogino'), 'зөвхөн БОГИНО (PDH)'),
                    (dict(spread=0.6), 'спред $0.6'),
                    (dict(spread=0.0), 'спредгүй')):
        R = np.concatenate([run('PDH', **kw), run('PDL', **kw)])
        print("   " + stat(R, lbl))

    print("\n── 4. Цэвэрлэгээний ГҮН (a5-ийн санааг сессийн түвшинд) ──\n")
    for md in (None, 1.0, 3.0, 6.0):
        R = np.concatenate([run(n, min_depth=md) for n in ('PDH', 'PDL')])
        print("   " + stat(R, f'гүн ≥ ${md}' if md else 'бүгд'))

    print("\n── 5. Оролтын цагийн хязгаар (өмнөх өдрийн туйл) ──")
    print("   a5-д УБ 23:00-аас хойш муу гарсан. Дахин шалгая.\n")
    for c, lbl in ((12 * 60, '12:00 хүртэл (УБ 17:00)'),
                   (16 * 60, '16:00 хүртэл (УБ 21:00)'),
                   (18 * 60, '18:00 хүртэл (УБ 23:00)'),
                   (21 * 60, '21:00 хүртэл (УБ 02:00)')):
        R = np.concatenate([run('PDH', cut=c), run('PDL', cut=c)])
        print("   " + stat(R, lbl))

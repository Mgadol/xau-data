"""7. CRT (Candle Range Theory) — лааны мужийн онол.

БҮТЭЦ (3 лаа)
    C1  муж тогтооно            (дээд = H1, доод = L1)
    C2  нэг талыг нь ЦЭВЭРЛЭНЭ  (H1-ээс дээш гарна)
        ба буцаж C1-ийн муж руу ХААГДАНА          ← өдөөлт
    C3  эсрэг тал руу тэлнэ                        ← арилжаа

    Оролт : C2 ХААГДАХ мөчид
    Стоп  : C2-ийн цэвэрлэсэн туйл
    Target: C1-ийн эсрэг тал (сонгодог CRT) эсвэл тогтмол R

ЦЭВЭРЛЭГЭЭТЭЙ ЯМАР ХОЛБООТОЙ ВЭ
  CRT бол a4-ийн цэвэрлэгээний нэг ТӨРӨЛ. Хоёр ялгаа:

    a4   түвшин = zigzag пивот      баталгаа = 5м лаа буцаж хаагдана
    CRT  түвшин = өмнөх ЛААНЫ туйл  баталгаа = тэр лаа өөрөө дотогшоо хаагдана

  Хоёр дахь ялгаа нь ЧУХАЛ. a2-т «баталгаа хүлээх» нь бүх шинжилгээн
  дундаас хамгийн том нөлөө үзүүлсэн (0.38R). CRT-д тэр баталгаа нь
  дүрэмдээ шингэсэн байдаг — тодорхойлолтоороо хоцорч ордог.
  Тиймээс CRT нь a4-ийн цэвэрлэгээнээс ДЭЭР гарах ёстой гэсэн
  урьдчилсан таамаг байв.

  Мөн CRT-д ирээдүй харах алдаа гарах боломж бага: түвшин нь өмнөх
  лаа, баталгаа нь тухайн лааны хаалт — хоёулаа НЭГ хугацааны хүрээнд.
  a4-ийн алдаа (4ц/5м холилдох) энд байхгүй.

ҮР ДҮН: ДАВУУ ТАЛГҮЙ. Таамаг батлагдаагүй.

      1ц    35279   44.1%   −0.165R ±0.006
      4ц     8883   45.4%   −0.088R ±0.013
      өдөр   1661   46.7%   +0.014R ±0.032

  n нь маш том (a4-ийнхаас 4 дахин) тул алдааны зурвас нарийн —
  энэ бол бат бөх сөрөг хариу, тодорхойгүй байдал биш.
  Жижиг хугацаа руу явах тусам ДОРДОНО (1ц нь хамгийн муу).

  Дөрвөн шалгуур: 2005–2016 −0.096R, 2017–2025 −0.078R, урт −0.072R,
  богино −0.103R. Бүгд сөрөг, бүгд ижил — тогтвортойгоор алдагдалтай.

БАТАЛГАА ҮНЭХЭЭР ТУСАЛДАГ (гэхдээ хангалтгүй)

      дотогшоо хаагдсан (жинхэнэ CRT)   8883   −0.088R
      зүгээр цэвэрлэсэн                21394   −0.157R

  0.07R-ийн ялгаа. Энэ нь a2-ийн «баталгаа хүлээ» гэсэн дүгнэлтийг
  ДАХИН баталж байна — өөр өгөгдөл, өөр бүтэц, ижил чиглэл.
  Харин CRT-г ашигтай болгоход хүрэлцэхгүй.

  «Их бие нь ч дотор» гэсэн хатуу хувилбар нэмэлт өгөөгүй (−0.087R).

СПРЕД Л АЛЖ БАЙНА

      спредгүй      +0.035R ±0.016  ✓
      спред $0.3    −0.088R
      спред $0.6    −0.171R

  Түүхий бүтэц нь үнэхээр бага зэрэг эерэг. Гэвч CRT-ийн стоп нь нэг
  лааны дотор байдаг тул маш нарийн — спред түүнийг бүхэлд нь иднэ.
  Өдрийн хүрээнд стоп өргөн болохоор тэг рүү ойртдог нь үүнийг
  батална. Энэ бол «бараг ажиллах» биш, «зардал даахгүй» гэсэн үг.
"""
import numpy as np
import pandas as pd
from core import load, resample, zigzag, confirm_index, stat, bar_len

h = load(start='2005-01-01', end='2025-09-12')
D5 = load('XAU_5m_data.csv', start='2005-01-01', end='2025-09-12')
F5 = {'h': D5['high'].values, 'l': D5['low'].values,
      'c': D5['close'].values, 'i': D5.index}


def find(tf='4h', strict=False, need_close_in=True):
    """CRT бүтцүүдийг олно.  Буцаах: жагсаалт dict.

    strict        : C2 нь C1-ийн мужид БҮРЭН хаагдахыг шаардана
                    (зөвхөн хаалт биш, C2-ийн их бие)
    need_close_in : буцаж дотогшоо хаагдах шаардлага. False бол
                    ердөө «цэвэрлэсэн» — баталгааны үнэ цэнийг тусгаарлана
    """
    d = resample(h, tf)
    H, L, C, O = (d['high'].values, d['low'].values,
                  d['close'].values, d['open'].values)
    dt = bar_len(tf)
    out, both = [], 0
    for i in range(1, len(d)):
        h1, l1 = H[i - 1], L[i - 1]
        if h1 <= l1:
            continue
        up_sweep = H[i] > h1        # дээд талыг цэвэрлэв → БОГИНО хүлээнэ
        dn_sweep = L[i] < l1        # доод талыг цэвэрлэв → УРТ хүлээнэ
        if up_sweep and dn_sweep:
            both += 1               # хоёр талыг цэвэрлэсэн — тодорхойгүй
            continue
        if not (up_sweep or dn_sweep):
            continue
        short = up_sweep
        if need_close_in:
            if short and not (C[i] < h1):
                continue
            if (not short) and not (C[i] > l1):
                continue
            if strict:
                body_out = max(C[i], O[i]) > h1 if short else min(C[i], O[i]) < l1
                if body_out:
                    continue
        out.append(dict(
            t=d.index[i] + dt,              # C2 ХААГДАХ мөч = оролт
            short=short, entry=C[i],
            stop=H[i] if short else L[i],   # цэвэрлэгээний туйл
            opp=l1 if short else h1,        # C1-ийн эсрэг тал = сонгодог target
            rng=h1 - l1,
            year=d.index[i].year))
    return out, both


def run(tf='4h', rr=None, hold=3, spread=0.3, side=None,
        years=None, min_rr=None, **kw):
    """CRT-үүдийг 5 минутын өгөгдөл дээр гүйцэтгэж R буцаана.

    rr     : None бол target = C1-ийн эсрэг тал (сонгодог CRT).
             Тоо бол тогтмол R олгоно.
    hold   : хэдэн лааны турш барих вэ (tf-ийн нэгжээр)
    min_rr : сонгодог target нь энэ R-ээс бага бол алгасна
    """
    setups, _ = find(tf, **kw)
    nb = int(bar_len(tf) / pd.Timedelta('5min')) * hold
    H5, L5, C5, I5 = F5['h'], F5['l'], F5['c'], F5['i']
    res = []
    for s in setups:
        if years and not (years[0] <= s['year'] < years[1]):
            continue
        if side == 'urt' and s['short']:
            continue
        if side == 'bogino' and not s['short']:
            continue
        short = s['short']
        e = s['entry'] - spread if short else s['entry'] + spread
        st = s['stop']
        risk = (st - e) if short else (e - st)
        if risk <= 0:
            continue
        tg = (e - rr * risk) if rr else s['opp']
        got = (e - tg) / risk if short else (tg - e) / risk
        if got <= 0:
            continue
        if min_rr is not None and got < min_rr:
            continue

        k = I5.searchsorted(s['t'])         # C2 хаагдсаны ДАРААХ 5м бар
        if k >= len(I5) - nb:
            continue
        r = None
        for j in range(k, k + nb):
            if short:
                if H5[j] >= st: r = -1.0; break
                if L5[j] <= tg: r = got;  break
            else:
                if L5[j] <= st: r = -1.0; break
                if H5[j] >= tg: r = got;  break
        if r is None:                        # дуусаагүйг зах зээлийн үнээр хаана
            px = C5[k + nb - 1]
            r = ((e - px) if short else (px - e)) / risk
        res.append(r)
    return np.array(res)


if __name__ == '__main__':
    print("CRT — лааны мужийн онол.  5 минутын гүйцэтгэл, спред $0.3\n")

    print("── 1. Хугацааны хүрээ бүрээр (target = C1-ийн эсрэг тал) ──\n")
    print(f"   {'':<30}{'n':>6} {'Ялалт':>7} {'Дундаж':>9}")
    print("   " + "─" * 62)
    for tf in ('1h', '4h', '1D'):
        n_all, both = find(tf)
        print("   " + stat(run(tf), f"{tf}  (2 тал цэвэрлэсэн: {both})"))

    print("\n── 2. БАТАЛГАА үнэ цэнэтэй юу (4ц) ──")
    print("   Цэвэрлээд буцаж дотогшоо хаагдах шаардлагыг авч үзье.\n")
    print("   " + stat(run('4h', need_close_in=True), 'дотогшоо хаагдсан (CRT)'))
    print("   " + stat(run('4h', need_close_in=False), 'зүгээр цэвэрлэсэн'))
    print("   " + stat(run('4h', strict=True), 'их бие нь ч дотор (хатуу)'))

    print("\n── 3. Тогтмол target (4ц) ──\n")
    for rr in (1.0, 2.0, 3.0):
        print("   " + stat(run('4h', rr=rr), f'TP 1:{rr:.0f}'))

    print("\n── 4. Барих хугацаа (4ц, сонгодог target) ──\n")
    for hd in (1, 2, 3, 6):
        print("   " + stat(run('4h', hold=hd), f'{hd} лааны дотор'))

    print("\n── 5. Дөрвөн шалгуур (4ц, сонгодог target) ──")
    print("   Аль нэг мөр унавал олдвор биш.\n")
    for kw, lbl in ((dict(years=(2005, 2017)), '2005–2016'),
                    (dict(years=(2017, 2026)), '2017–2025'),
                    (dict(side='urt'), 'зөвхөн УРТ'),
                    (dict(side='bogino'), 'зөвхөн БОГИНО'),
                    (dict(spread=0.6), 'спред $0.6'),
                    (dict(spread=0.0), 'спредгүй')):
        print("   " + stat(run('4h', **kw), lbl))

    print("\n── 6. CRT vs a4-ийн цэвэрлэгээ ──")
    print("   Хоёулаа ижил механизм. CRT-д баталгаа нь дүрэмдээ шингэсэн.\n")
    print("   " + stat(run('4h', rr=2.0), 'CRT · TP 1:2'))
    print("   a4-ийн цэвэрлэгээ · TP 1:2 ......  2026   32.5%   -0.066R")

"""23. Шатлан гаргах (scale out) — 0.01 × 3, TP-г 20/50/100 pip болгож хуваах.

САНАА
  «0.01-аар 3 удаа ороод 20 pip, 50 pip, 100 pip гэж салгаж TP-гээ авъя.»

  Нэг байрлалыг гурав хувааж, өөр өөр target-д гаргана. Стоп нь
  гурвуулд ижил.

МАТЕМАТИКИЙН УРЬДЧИЛСАН ХАРИУ
  Хэрэв стоп ХӨДӨЛӨХГҮЙ бол шатлан гаргах нь гурван ТУСДАА
  стратегийн ЖИГД ДУНДАЖ болно — өөр юу ч биш:

      E[шат] = (E[TP1] + E[TP2] + E[TP3]) / 3

  Энэ нь тодорхойлолтоороо тийм. Тиймээс гурвын дундажаас
  ДЭЭГҮҮР гарах боломжгүй. Илбэ байхгүй.

  ГЭХДЭЭ ХОЁР ЗҮЙЛ ӨӨРЧЛӨГДӨНӨ:
    1. ХЭЛБЭЛЗЭЛ буурна — үр дүн төвдөө цуглана
    2. Ихэнх хүн TP1 хүрсний дараа стопоо BE рүү зөөдөг.
       ТЭР нь математикийг өөрчилнө (a22-т BE дордуулсан).

ТИЙМЭЭС ГУРВАН ХУВИЛБАР ШАЛГАНА
    a) Шатлан, стоп ХӨДӨЛӨХГҮЙ      → дундаж байх ёстой
    b) Шатлан + TP1-ийн дараа BE    → бодит хүмүүсийн хийдэг нь
    c) Ганц TP (харьцуулалт)

PIP-ИЙН ТОХИРОЛЦОО
  Алтан дээр 1 pip = $0.10 гэвэл 20/50/100 pip = $2/$5/$10.
  1 pip = $1.00 гэвэл = $20/$50/$100.
  Хоёуланг нь шалгана — аль нь ч байсан дүгнэлт гарна.

═══════════════════════════════════════════════════════════════════
ҮР ДҮН
═══════════════════════════════════════════════════════════════════

1. МАТЕМАТИКИЙН ТААМАГ ЯГ БАТЛАГДАВ

   $2/$5/$10:
      ганц TP $2     62.2%   −0.081R   хэлбэлзэл 0.77
      ганц TP $5     44.8%   −0.056R                1.18
      ганц TP $10    33.8%   −0.047R                1.58
      ─────────────────────────────────────────────────
      ШАТЛАН         42.5%   −0.061R                1.05
      гурвын дундаж          −0.061R   ← ЯГ ИЖИЛ

   $20/$50/$100:
      ШАТЛАН                 −0.012R
      гурвын дундаж          −0.012R   ← ЯГ ИЖИЛ

   Шатлан гаргах нь ирмэг НЭМДЭГГҮЙ, ХАСДАГГҮЙ. Тодорхойлолтоороо
   гурван стратегийн жигд дундаж. Гурвын хамгийн сайнаас ДЭЭГҮҮР
   гарах боломжгүй — энэ бол математик, тохиргооны асуудал биш.

2. ХАРИН ХЭЛБЭЛЗЭЛ ҮНЭХЭЭР БУУРНА

      stds-ийн жигд дундаж  (0.77+1.18+1.58)/3 = 1.18
      ШАТЛАЛТЫН бодит std                      = 1.05

   11% бага. Гурван target нэг зэрэг ажилладаггүй тул төрөлжилтийн
   нөлөө гарна. ЭНЭ Л шатлан гаргахын ЖИНХЭНЭ ашиг — ирмэг биш,
   ХЭЛБЭЛЗЛИЙН ХЯНАЛТ.

3. TP1-ИЙН ДАРАА BE ЗӨӨВӨЛ ДОРДОНО

      ШАТЛАН            −0.061R
      + TP1 дараа BE    −0.083R
      + TP2 дараа BE    −0.068R

   a22-ийн дүгнэлттэй бүрэн нийцэж байна. Ихэнх хүн яг ЭНЭ
   хослолыг хийдэг (шатлан гаргаад BE зөөх) — тэр нь хамгийн муу.

4. ЗҮЙ ТОГТОЛ ДАХИН ДАВТАГДАВ — TARGET ХОЛ БАЙХ ТУСАМ ДЭЭР

      TP $2   −0.081R      TP $20   −0.023R
      TP $5   −0.056R      TP $50   −0.007R
      TP $10  −0.047R      TP $100  −0.005R

   $100 target нь −0.005R ±0.023 буюу бүх судалгаан дундаас
   ТЭГ-д хамгийн ойр. Учир нь стоп нь дунджаар $4.40, target нь
   $100 — спред эрсдэлийн 7% биш, ашгийн 0.3% болно.

5. ДӨРВӨН ШАЛГУУР ($20/$50/$100)

      бүгд           −0.012R ±0.021
      2005–2016      +0.025R ±0.031
      2017–2025      −0.059R ±0.029   ← ХУГАЦААНД ДАВТАГДААГҮЙ
      зөвхөн УРТ     +0.029R ±0.029
      зөвхөн БОГИНО  −0.051R ±0.031   ← ТЭГШ ХЭМ АЛДАРСАН
      спред $0.6     −0.089R ±0.019

   Тэг рүү ойртсон ч дөрвөн шалгуурыг даваагүй.

ДҮГНЭЛТ
  Шатлан гаргах нь МӨНГӨ УДИРДАХ хэрэгсэл, ирмэг бүтээх арга БИШ.
  Хэлбэлзлийг 11% бууруулна — тэр нь бодит ашиг. Гэхдээ дундаж
  үр дүн нь гурван target-ынхаа дундажаас хэзээ ч хэтрэхгүй.

  Хэрэв гурван target-ын АЛЬ НЬ Ч эерэг биш бол тэдгээрийн
  дундаж ч эерэг байхгүй. Ирмэггүй байрлалыг хэрхэн хуваасан ч
  ирмэг үүсэхгүй.
"""
import numpy as np
import pandas as pd
from core import load, resample, stat, bar_len

h = load(start='2005-01-01', end='2025-09-12')
D5 = load('XAU_5m_data.csv', start='2005-01-01', end='2025-09-12')
H5, L5, C5, I5 = (D5['high'].values, D5['low'].values,
                  D5['close'].values, D5.index)


def setups(tf='4h', K=3):
    """a19/a22-тэй ИЖИЛ Turtle Soup бүтэц — харьцуулалт хийхийн тулд."""
    d = resample(h, tf)
    H, L, C = d['high'].values, d['low'].values, d['close'].values
    dt = bar_len(tf)
    out = []
    for i in range(K, len(d) - 1):
        for short in (True, False):
            if short:
                lvl = H[i - K:i].max()
                if not (H[i] > lvl and C[i] < lvl):
                    continue
                far = H[i]
            else:
                lvl = L[i - K:i].min()
                if not (L[i] < lvl and C[i] > lvl):
                    continue
                far = L[i]
            out.append(dict(t=d.index[i] + dt, short=short,
                            entry=C[i], stop=far, year=d.index[i].year))
    return out


SET = setups()


def run(tps=(2.0, 5.0, 10.0), be_after=0, spread=0.3, hold=288,
        side=None, years=None, single=None):
    """tps      : гурван target $-аар (хэсэг тус бүр 1/3)
       be_after : TP хэдэн ширхэг хүрсний ДАРАА стопыг BE рүү зөөх.
                  0 = зөөхгүй. 1 = эхний TP-ийн дараа.
       single   : $ өгвөл ГАНЦ target-аар бүх байрлалыг гаргана
    """
    targets = [single] if single is not None else list(tps)
    w = 1.0 / len(targets)
    res = []
    for s in SET:
        if years and not (years[0] <= s['year'] < years[1]):
            continue
        short = s['short']
        if side == 'urt' and short:
            continue
        if side == 'bogino' and not short:
            continue
        e = s['entry'] - spread if short else s['entry'] + spread
        st0 = s['stop']
        risk = (st0 - e) if short else (e - st0)
        if risk <= 0:
            continue

        k = I5.searchsorted(s['t'])
        if k >= len(I5) - hold:
            continue

        left = list(range(len(targets)))     # гараагүй хэсгүүд
        pnl = 0.0                            # $-аар хуримтлагдана
        st = st0
        filled = 0
        for x in range(k, k + hold):
            # ── Стопыг ЭХЛЭЭД шалгана (болгоомжтой) ──
            hit_stop = (H5[x] >= st) if short else (L5[x] <= st)
            if hit_stop:
                for _ in left:
                    pnl += w * ((e - st) if short else (st - e))
                    if st == e:
                        pnl -= w * spread    # BE дээр гарахад спред дахин
                left = []
                break
            # ── TP-үүд ──
            for idx in list(left):
                t = targets[idx]
                tg = e - t if short else e + t
                reach = (L5[x] <= tg) if short else (H5[x] >= tg)
                if reach:
                    pnl += w * t
                    left.remove(idx)
                    filled += 1
                    if be_after and filled >= be_after and st != e:
                        st = e
            if not left:
                break
        if left:                              # хугацаа дуусав — зах зээлээр
            px = C5[min(k + hold, len(I5)) - 1]
            for _ in left:
                pnl += w * ((e - px) if short else (px - e))
        res.append(pnl / risk)                # R болгоно
    return np.array(res)


def rep(lbl, R):
    if len(R) < 25:
        return f"   {lbl:<32}{len(R):>6}  (цөөн)"
    se = R.std() / np.sqrt(len(R))
    return (f"   {lbl:<32}{len(R):>6}{(R > 0).mean() * 100:>7.1f}%"
            f"{R.mean():>+9.3f}R ±{se:.3f}{R.std():>8.2f}"
            f"{'  ✓' if R.mean() > 2 * se else ''}")


HDR = f"   {'':<32}{'n':>6}{'ялалт':>8}{'дундаж':>10}{'±SE':>7}{'хэлбэлз':>8}"

if __name__ == '__main__':
    print("Шатлан гаргах · Turtle Soup · 4 цаг · спред $0.3")
    print(f"{len(SET):,} setup.  Байрлалыг 3 хувааж, тус бүрд өөр TP.\n")

    for tag, tps in (('1 pip = $0.10  →  $2 / $5 / $10', (2.0, 5.0, 10.0)),
                     ('1 pip = $1.00  →  $20 / $50 / $100', (20.0, 50.0, 100.0))):
        print(f"══ {tag} ══\n")
        print(HDR)
        print("   " + "─" * 72)
        for t in tps:
            print(rep(f'ГАНЦ TP ${t:.0f}', run(single=t)))
        print("   " + "─" * 72)
        a = run(tps=tps)
        print(rep('ШАТЛАН (стоп хөдлөхгүй)', a))
        # Гурвын жигд дундаж — шатлантай ЯГ таарах ёстой
        m = np.mean([run(single=t).mean() for t in tps])
        print(f"   {'гурвын жигд дундаж':<32}{'':>6}{'':>8}{m:>+9.3f}R"
              f"        ← шатлантай ижил байх ёстой")
        print("   " + "─" * 72)
        print(rep('ШАТЛАН + TP1-ийн дараа BE', run(tps=tps, be_after=1)))
        print(rep('ШАТЛАН + TP2-ийн дараа BE', run(tps=tps, be_after=2)))
        print()

    print("══ Жишиг: a19/a22-ийн ганц TP 1:2 ══\n")
    print(HDR)
    print("   " + "─" * 72)

    def fixed_rr(rr=2.0, spread=0.3, hold=288):
        out = []
        for s in SET:
            short = s['short']
            e = s['entry'] - spread if short else s['entry'] + spread
            st = s['stop']
            risk = (st - e) if short else (e - st)
            if risk <= 0:
                continue
            tg = e - rr * risk if short else e + rr * risk
            k = I5.searchsorted(s['t'])
            if k >= len(I5) - hold:
                continue
            r = None
            for x in range(k, k + hold):
                if short:
                    if H5[x] >= st: r = -1.0; break
                    if L5[x] <= tg: r = rr;   break
                else:
                    if L5[x] <= st: r = -1.0; break
                    if H5[x] >= tg: r = rr;   break
            if r is None:
                px = C5[min(k + hold, len(I5)) - 1]
                r = ((e - px) if short else (px - e)) / risk
            out.append(r)
        return np.array(out)

    print(rep('ганц TP 1:2 (R-ээр)', fixed_rr()))

    print("\n══ Дөрвөн шалгуур — хамгийн сайн шатлалт ══\n")
    print(HDR)
    print("   " + "─" * 72)
    best = (20.0, 50.0, 100.0)
    print(rep('$20/$50/$100 · бүгд', run(tps=best)))
    for kw, lbl in ((dict(years=(2005, 2017)), '2005–2016'),
                    (dict(years=(2017, 2026)), '2017–2025'),
                    (dict(side='urt'), 'зөвхөн УРТ'),
                    (dict(side='bogino'), 'зөвхөн БОГИНО'),
                    (dict(spread=0.6), 'спред $0.6')):
        print(rep('  ' + lbl, run(tps=best, **kw)))

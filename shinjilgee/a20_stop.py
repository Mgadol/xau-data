"""20. Стопоо ШАХВАЛ юу болох вэ — ижил оролт дээр.

АСУУЛТ
  «Стопоо шахвал эрсдэл багасаж, ижил хөдөлгөөн ИЛҮҮ R өгнө биз дээ?»

  Арилжаачдын хамгийн түгээмэл логик. Математикийн хувьд зөв харагдана:
      оролт нэг, target нэг, стоп ойр  →  R = target_зай / стоп_зай  ↑

ЭНЭ НЬ a18/a19-ИЙН ШИНЖИЛГЭЭНЭЭС ӨӨР АСУУЛТ
  Тэнд «стоп ≥ $2» гэж ШҮҮХЭД үр дүн сайжирч байсан. Гэвч тэр нь
  стопыг шахсан биш — өргөн стоптой БАЙСАН арилжааг сонгосон юм.
  Өөр арилжаанууд, өөр зах зээлийн нөхцөл. Энэ хоёрыг андуурч
  болохгүй байв.

  Энд ЯГ ИЖИЛ арилжаан дээр зөвхөн стопын зайг өөрчилнө. Цорын ганц
  өөрчлөгдөж буй зүйл нь стоп. Энэ л таны асуултын жинхэнэ хариу.

ХОЁР ТОХИРГОО — ХОЁУЛАНГ НЬ ШАЛГАХ ЁСТОЙ

  A. TARGET ТОГТМОЛ ($-аар)
     Стоп шахагдахад R өснө (шагнал хэвээр, эрсдэл бага).
     Энэ бол ЯГ таны хэлж буй зүйл.

  B. TARGET нь R-ээр тогтмол (TP 1:2)
     Стоп шахагдахад target ч ойртоно. Зөвхөн масштаб өөрчлөгдөнө.

  A дээр «стоп шахвал R өснө» гэдэг ҮНЭН. Асуулт нь: стоп хүрэх нь
  хэр их нэмэгдэх вэ. Хоёр нөлөө эсрэг чиглэлтэй — өгөгдөл шийднэ.

ЗАРДАЛ
  Спред нь $-аар ТОГТМОЛ. Стоп шахагдах тусам тэр нь эрсдэлийн улам
  их хувийг эзэлнэ. Гуравдахь нөлөө нь энэ.
"""
import numpy as np
import pandas as pd
from core import load, resample, stat, bar_len

h = load(start='2005-01-01', end='2025-09-12')
D5 = load('XAU_5m_data.csv', start='2005-01-01', end='2025-09-12')
H5, L5, C5, I5 = (D5['high'].values, D5['low'].values,
                  D5['close'].values, D5.index)


def base_setups(tf='4h', K=3):
    """a19-ийн Turtle Soup бүтцүүд — оролт, «байгалийн» стоп, target."""
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
                far, tgt = H[i], L[i - K:i].min()
            else:
                lvl = L[i - K:i].min()
                if not (L[i] < lvl and C[i] > lvl):
                    continue
                far, tgt = L[i], H[i - K:i].max()
            nat = abs(C[i] - far)              # байгалийн стопын зай
            rew = abs(tgt - C[i])              # target хүртэлх зай ($)
            if nat <= 0 or rew <= 0:
                continue
            out.append(dict(t=d.index[i] + dt, short=short, entry=C[i],
                            nat=nat, rew=rew, year=d.index[i].year))
    return out


SET = base_setups()


def run(mult=1.0, mode='fixed_target', rr=2.0, spread=0.3, hold=288,
        side=None, years=None):
    """mult = стопын зайг байгалийнхаас хэдэн дахин болгох вэ.

    mode 'fixed_target' : target нь $-аар тогтмол (таны асуулт)
         'fixed_rr'     : target нь R-ээр тогтмол
    """
    res, risks = [], []
    for s in SET:
        if years and not (years[0] <= s['year'] < years[1]):
            continue
        short = s['short']
        if side == 'urt' and short:
            continue
        if side == 'bogino' and not short:
            continue
        e = s['entry'] - spread if short else s['entry'] + spread
        risk = s['nat'] * mult
        st = e + risk if short else e - risk
        if mode == 'fixed_target':
            tg = e - s['rew'] if short else e + s['rew']
            got = s['rew'] / risk
        else:
            tg = e - rr * risk if short else e + rr * risk
            got = rr
        k = I5.searchsorted(s['t'])
        if k >= len(I5) - hold:
            continue
        r = None
        for x in range(k, k + hold):
            if short:
                if H5[x] >= st: r = -1.0; break
                if L5[x] <= tg: r = got;  break
            else:
                if L5[x] <= st: r = -1.0; break
                if H5[x] >= tg: r = got;  break
        if r is None:
            px = C5[k + hold - 1]
            r = ((e - px) if short else (px - e)) / risk
        res.append(r)
        risks.append(risk)
    return np.array(res), np.array(risks)


def line(mult, mode, **kw):
    R, rk = run(mult, mode, **kw)
    if len(R) < 25:
        return f"   ×{mult:<5.2f}{len(R):>7}  (цөөн)"
    se = R.std() / np.sqrt(len(R))
    med = np.median(rk)
    return (f"   ×{mult:<5.2f}{len(R):>7}{(R > 0).mean() * 100:>7.1f}%"
            f"{R.mean():>+9.3f}R ±{se:.3f}"
            f"{med:>9.2f}${0.3 / med * 100:>7.1f}%"
            f"{'  ✓' if R.mean() > 2 * se else ''}")


MULTS = (0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0)

if __name__ == '__main__':
    print("Стопоо ШАХВАЛ юу болох вэ — ИЖИЛ оролт, зөвхөн стоп өөрчлөгдөнө")
    print(f"Turtle Soup бүтэц, 4 цаг, {len(SET):,} setup, спред $0.3\n")

    print("── A. TARGET ТОГТМОЛ ($-аар) — ЯГ ТАНЫ АСУУЛТ ──")
    print("   Стоп шахагдахад R өснө. Стоп хүрэх нь ч нэмэгдэнэ.")
    print("   Аль нь давамгайлах вэ?\n")
    print(f"   {'стоп':<7}{'n':>7}{'ялалт':>8}{'дундаж':>11}"
          f"{'':>7}{'медиан':>7}{'спред%':>8}")
    print("   " + "─" * 62)
    for m in MULTS:
        print(line(m, 'fixed_target'))
    print("\n   ×1.00 = байгалийн стоп (цэвэрлэгээний туйл)")

    print("\n── B. TARGET нь R-ЭЭР тогтмол (TP 1:2) ──")
    print("   Стоп шахагдахад target ч ойртоно — зөвхөн масштаб.\n")
    print(f"   {'стоп':<7}{'n':>7}{'ялалт':>8}{'дундаж':>11}"
          f"{'':>7}{'медиан':>7}{'спред%':>8}")
    print("   " + "─" * 62)
    for m in MULTS:
        print(line(m, 'fixed_rr'))

    print("\n── C. СПРЕДГҮЙ БОЛ (зардлын нөлөөг тусгаарлая) ──")
    print("   Спред нь $-аар тогтмол тул шахсан стопыг илүү иддэг.")
    print("   Түүнийг хасвал жинхэнэ зах зээлийн нөлөө үлдэнэ.\n")
    print(f"   {'стоп':<7}{'n':>7}{'ялалт':>8}{'дундаж':>11}")
    print("   " + "─" * 46)
    for m in MULTS:
        R, _ = run(m, 'fixed_target', spread=0.0)
        if len(R) < 25:
            continue
        se = R.std() / np.sqrt(len(R))
        print(f"   ×{m:<5.2f}{len(R):>7}{(R > 0).mean() * 100:>7.1f}%"
              f"{R.mean():>+9.3f}R ±{se:.3f}{'  ✓' if R.mean() > 2 * se else ''}")

    print("\n── D. Хугацааны хуваалт (target тогтмол) ──\n")
    for yrs, tag in (((2005, 2017), '2005–2016'), ((2017, 2026), '2017–2025')):
        print(f"   ── {tag} ──")
        for m in (0.5, 1.0, 2.0, 3.0):
            print(line(m, 'fixed_target', years=yrs))
        print()

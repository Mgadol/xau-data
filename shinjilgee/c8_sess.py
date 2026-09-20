"""c8. Задрал АЛЬ СЕССТ болов — Ази, Лондон, Нью-Йорк.

c4-д бүтэц зөвхөн ӨДРИЙН давхрагад оршдог нь гарсан. Гэхдээ өдрийн
задрал нь тодорхой ЦАГТ тохиолддог. Тэр цаг нь чухал уу?

Арга: шахалт ба хилийг ӨДРИЙН барнаас (тэнд л ажилладаг), харин
задрах МӨЧИЙГ 1 цагийн барнаас олно. Ингэснээр «өдрийн дохио, цагийн
гүйцэтгэл» болно — c4-ийн дүгнэлтийг зөрчихгүй.

Сервер цаг: 15:30-д мэдээний оргил (a15) → АНУ-ын 08:30 EST. Тиймээс
сервер = EST + 7 цаг. Үүнээс сессүүд:

    Ази    01:00–08:00   (Токио, Хонконг)
    Лондон 09:00–14:00   (Европын нээлт)
    Нью-Йорк 15:00–22:00 (АНУ-ын нээлт, мэдээ)
    Нам    23:00–00:00   (хаалтын зай)

ХОЁР ЗАНГА ЭНД БАРИГДСАН (хоёулаа дүнг эрс өөрчилсөн):

  1. ӨДРИЙН БАРЫН ХИЛ. Өдрийн бар 18:00-д хиллэдэг атал эхэндээ
     ХУАНЛИЙН өдрөөр (00:00-23:59) хайсан тул өмнөх оройн хөдөлгөөн
     «01:00-ын задрал» болж, задралын 62% нь хуурамчаар «Ази» болж
     байв. Хилийг тааруулсны дараа тэр нь 19:00 руу шилжсэн — өөрөөр
     хэлбэл асуудал нь сесс биш, ХАЙЛТЫН ЭХНИЙ ЦАГ байв.

  2. НЭЭЛТЭЭР ХЭТЭРСЭН. Задралын 47%-д үнэ өдөр нээгдэхэд аль хэдийн
     хилээс цааш байдаг. Эдгээрт «хил дээр орлоо» гэж тооцвол
     боломжгүй үнээр орсон болно. Жинхэнэ нээлтийн үнээр тооцоход
     тэр бүлгийн R нь +0.527 → +0.219 болж буурав.

ЗАНГА: NY сесст хөдөлгөөн угаасаа том (16:00-д 0.220%, 23:00-д
0.071% — 3.1 дахин). Тиймээс «NY-д задрал том явдаг» гэсэн тоо нь
сессийн давуу тал биш, зүгээр л тэр цагийн хэлбэлзэл байж болно.
Үүнээс сэргийлж бүх зүйлийг ӨДРИЙН ATR-ийн дахинаар хэмжинэ —
тэгвэл сесс хоорондоо зэрэгцүүлэгдэнэ.

    python3 c8_sess.py
"""
import argparse
import numpy as np
import pandas as pd
from core import load
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range

SESS = [('Ази', 1, 8), ('Лондон', 9, 14), ('Нью-Йорк', 15, 22),
        ('нам', 23, 24)]


def which(h):
    for nm, a, b in SESS:
        if a <= h <= b:
            return nm
    return 'нам'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--wait', type=int, default=5)
    ap.add_argument('--hold', type=int, default=10)
    ap.add_argument('--spread', type=float, default=.25)
    a = ap.parse_args()

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr14'] = tr.rolling(14).mean()
    d['sq'] = d.atr14 / tr.rolling(100).mean()
    m20 = d.close.rolling(20).mean()
    d['up'] = m20 + 1.5 * d.atr14
    d['dn'] = m20 - 1.5 * d.atr14
    d = d.dropna(subset=['sq', 'up', 'atr14'])
    q20 = d.sq.quantile(.2)

    h1 = load('XAU_5m_data.csv').resample('1h').agg(
        open=('open', 'first'), high=('high', 'max'), low=('low', 'min'),
        close=('close', 'last')).dropna()
    hi_a, lo_a, op_a = (h1.high.to_numpy(), h1.low.to_numpy(),
                        h1.open.to_numpy())
    hidx = h1.index

    D = d.index
    DH, DL, DC = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    A, U, DN = d.atr14.to_numpy(), d.up.to_numpy(), d.dn.to_numpy()
    n = len(d)
    rows = []

    for i in np.where((d.sq <= q20).to_numpy())[0]:
        if not np.isfinite(A[i]) or A[i] <= 0:
            continue
        # Өдрийн барнаас аль өдөр задарснаа олно
        ej = side = None
        for j in range(i + 1, min(i + 1 + a.wait, n)):
            hu, hd = DH[j] >= U[i], DL[j] <= DN[i]
            if hu and hd:
                break
            if hu:
                ej, side = j, 1
                break
            if hd:
                ej, side = j, -1
                break
        if ej is None:
            continue
        lvl = U[i] if side > 0 else DN[i]
        # Тэр ӨДРИЙН БАРЫН хугацаанаас яг хэдэн цагт хүрснийг олно.
        # АНХААР: өдрийн бар 18:00-д хиллэдэг (DAY_CLOSE_HOUR) тул
        # ХУАНЛИЙН өдрөөр (00:00-23:59) хайж БОЛОХГҮЙ. Тэгвэл өмнөх
        # оройд аль хэдийн хэтэрсэн зүйлийг «01:00-д задарлаа» гэж
        # бүртгэж, задралын 62%-ийг хуурамчаар «Ази» болгодог байв.
        day0 = D[ej - 1] if ej > 0 else D[ej]
        t0 = day0.normalize() + pd.Timedelta(hours=DAY_CLOSE_HOUR + 1)
        t1 = D[ej].normalize() + pd.Timedelta(hours=DAY_CLOSE_HOUR + 1)
        m = (hidx >= t0) & (hidx <= t1)
        hh, ll, oo, ix = hi_a[m], lo_a[m], op_a[m], hidx[m]
        if len(ix) == 0:
            continue
        # Өдөр нээгдэхэд АЛЬ ХЭДИЙН хилээс хэтэрсэн байвал энэ нь
        # тухайн цагийн задрал БИШ — өмнөх өдрийн үлдэц. Тусад нь
        # ангилахгүй бол эхний цаг бүх задралын 2/3-ыг залгидаг:
        # 18:00 хилтэй үед «19:00», хуанлийн өдөртэй үед «01:00».
        opened_past = (oo[0] >= lvl) if side > 0 else (oo[0] <= lvl)
        if opened_past:
            hour, sess = -1, 'нээлтээр'
            # Хил дээр орох нь БОЛОМЖГҮЙ — үнэ аль хэдийн цааш
            # нээгдсэн. Жинхэнэ орох үнэ нь нээлт. Үүнийг зассан нь
            # энэ бүлгийн R-ийг +0.527 → +0.219 болгож буулгана
            # (медиан 0.61 ATR хожуу орж байна).
            lvl = oo[0]
        else:
            hour = None
            for k in range(len(ix)):
                if (hh[k] >= lvl) if side > 0 else (ll[k] <= lvl):
                    hour = ix[k].hour
                    break
            if hour is None:
                continue
            sess = which(hour)
        # Үр дүн — өдрийн барнаас, ӨДРИЙН ATR-ээр
        k2 = min(ej + a.hold, n)
        top, bot = DH[ej:k2].max(), DL[ej:k2].min()
        mfe = (top - lvl) / A[i] if side > 0 else (lvl - bot) / A[i]
        risk = 2.0 * A[i]
        stop, targ = lvl - side * risk, lvl + side * 4.0 * A[i]
        out = None
        for j in range(ej, k2):
            sh = (DL[j] <= stop) if side > 0 else (DH[j] >= stop)
            th = (DH[j] >= targ) if side > 0 else (DL[j] <= targ)
            if sh:
                out = stop
                break
            if th:
                out = targ
                break
        if out is None:
            out = DC[k2 - 1]
        r = side * (out - lvl) / risk - a.spread / risk
        rows.append((D[ej], hour, sess, side, mfe, r))

    t = pd.DataFrame(rows, columns=['date', 'hour', 'sess', 'side',
                                    'mfe', 'R'])
    print(f'{len(t)} задрал   2005–2026   хил = 20 барын дундаж ± 1.5 ATR\n')
    print(f'{"сесс":12} {"тоо":>6} {"хувь":>7} {"ҮРГЭЛЖЛЭЛ":>10} '
          f'{"R дундаж":>10} {"ялсан":>7} {"дээш%":>7}')
    print('─' * 64)
    for nm in ['нээлтээр'] + [x[0] for x in SESS]:
        g = t[t.sess == nm]
        if len(g) < 15:
            continue
        print(f'{nm:12} {len(g):6} {len(g) / len(t):7.0%} '
              f'{g.mfe.median():10.2f} {g.R.mean():+10.3f} '
              f'{(g.R > 0).mean():7.0%} {(g.side > 0).mean():7.0%}')

    print('\n  Цагаар нарийвчилбал (10-аас дээш задралтай цаг):')
    for hr, g in t.groupby('hour'):
        if len(g) < 10:
            continue
        print(f'    {hr:02d}:00  n={len(g):4}  үргэлжлэл {g.mfe.median():5.2f}  '
              f'R {g.R.mean():+.3f}')

    best = t.groupby('sess').R.mean()
    print(f'\n  Хамгийн сайн {best.idxmax()} ({best.max():+.3f}R), '
          f'хамгийн муу {best.idxmin()} ({best.min():+.3f}R)')
    print('  Зөрүү бага бол — задрал аль сесст болсон нь хамаагүй.')


if __name__ == '__main__':
    main()

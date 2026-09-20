"""d6. УНАЛТ юунаас эхэлдэг вэ — шахалт биш бол юу?

b7-d5 бүгдэд доош задрал ажиллаагүй. Энэ нь хоёр тайлбартай:

  A. Алт өсдөг тул доош юу ч ажиллахгүй (дрифтийн тайлбар)
  B. Уналт нь ӨӨР механизмаар болдог — шахалтаас биш, тэлэлтээс.
     Шахалтын дараа ЭВДЭРЧ уналт болдоггүй, харин өндөр
     хэлбэлзлээс ШУУД унадаг.

Хэрэв B үнэн бол шахалтаар уналт хайх нь буруу хэрэгсэл — алх барьж
шураг эргүүлэхтэй адил. Тэгвэл уналтыг ӨӨР газраас хайх хэрэгтэй.

Шалгах арга: том уналт ба том өсөлтийн ӨМНӨХ төлвийг харьцуулна.

    шахалтын түвшин (ATR14/ATR100)
    байрлал зурваст
    сүүлийн 5 хоногийн чиглэл
    хэлбэлзлийн өөрчлөлт (өсөж байна уу, буурч байна уу)
    tick идэвх

Хоёр бүлгийн ӨМНӨХ төлөв ижил бол — уналт, өсөлт хоёр ижил
механизмтай, ялгаа нь зөвхөн дрифт (тайлбар A). Өөр бол уналтад
өөрийн гэсэн шинж бий (тайлбар B).

    python3 d6_unalt.py
"""
import argparse
import numpy as np
import pandas as pd
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--horizon', type=int, default=5)
    ap.add_argument('--q', type=float, default=.10,
                    help='дээд/доод хэдэн хувийг «том» гэх вэ')
    a = ap.parse_args()

    d = daily(close_hour=DAY_CLOSE_HOUR)
    d = d[d.index >= '2005-01-01'].copy()
    tr = true_range(d)
    d['atr'] = tr.rolling(14).mean()
    d['sq'] = d.atr / tr.rolling(100).mean()
    m20 = d.close.rolling(20).mean()
    d['pos'] = (d.close - (m20 - 1.5 * d.atr)) / (3 * d.atr)
    d['mom5'] = d.close.pct_change(5) * 100
    d['dvol'] = d.atr / d.atr.shift(10)            # хэлбэлзэл өсөж байна уу
    v = d.volume
    sgn = np.sign(d.close.diff())
    d['vdir'] = ((sgn * v).rolling(5).sum() / v.rolling(5).sum())
    d['act'] = v / v.rolling(100).mean()

    H = a.horizon
    d['fwd'] = (d.close.shift(-H) / d.close - 1) * 100
    d = d.dropna(subset=['sq', 'pos', 'mom5', 'dvol', 'vdir', 'act', 'fwd'])

    lo, hi = d.fwd.quantile(a.q), d.fwd.quantile(1 - a.q)
    down, up = d[d.fwd <= lo], d[d.fwd >= hi]
    mid = d[(d.fwd > lo) & (d.fwd < hi)]
    print(f'{len(d):,} өдөр   {H} хоногийн урагшхи өгөөж\n')
    print(f'  ТОМ УНАЛТ  n={len(down):4}  дундаж {down.fwd.mean():+.2f}%  '
          f'(босго {lo:.2f}%)')
    print(f'  ТОМ ӨСӨЛТ  n={len(up):4}  дундаж {up.fwd.mean():+.2f}%  '
          f'(босго {hi:.2f}%)')
    print(f'  дунд       n={len(mid):4}\n')

    cols = [('sq', 'шахалт (ATR14/100)'), ('pos', 'байрлал зурваст'),
            ('mom5', 'сүүлийн 5х өгөөж %'), ('dvol', 'хэлбэлзлийн өөрчлөлт'),
            ('vdir', 'идэвхийн чиглэл'), ('act', 'идэвх')]
    print(f'  {"шинж":22}{"УНАЛТЫН өмнө":>15}{"ӨСӨЛТИЙН өмнө":>16}'
          f'{"дунд":>10}{"зөрүү":>10}')
    print('  ' + '─' * 72)
    for c, nm in cols:
        dm, um, mm = down[c].median(), up[c].median(), mid[c].median()
        print(f'  {nm:22}{dm:15.3f}{um:16.3f}{mm:10.3f}{dm - um:+10.3f}')

    print('\n  ШАХАЛТЫН ТҮВШНИЙ тархалт (том уналтын өмнө):')
    for q in (.1, .25, .5, .75, .9):
        print(f'    {q:4.0%}  уналт {down.sq.quantile(q):.2f}   '
              f'өсөлт {up.sq.quantile(q):.2f}   дунд {mid.sq.quantile(q):.2f}')

    # Том уналтын хэдэн хувь нь ШАХАЛТААС гарсан бэ
    q20 = d.sq.quantile(.2)
    q80 = d.sq.quantile(.8)
    print('\n  Том хөдөлгөөн ямар төлвөөс эхэлсэн бэ:')
    print(f'    {"":12}{"шахагдсан":>12}{"дунд":>10}{"тэлсэн":>10}')
    for nm, g in (('УНАЛТ', down), ('ӨСӨЛТ', up), ('дунд', mid)):
        s = (g.sq <= q20).mean()
        e = (g.sq >= q80).mean()
        print(f'    {nm:12}{s:12.0%}{1 - s - e:10.0%}{e:10.0%}')

    print('\n  Хэрэв уналт нь өсөлттэй ижил хувиар шахалтаас эхэлж байвал —')
    print('  уналтад өөрийн гэсэн шинж байхгүй, ялгаа нь зөвхөн дрифт.')


if __name__ == '__main__':
    main()

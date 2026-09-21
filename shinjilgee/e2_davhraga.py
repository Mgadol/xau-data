"""e2. Давхрага бүр ЖИНХЭНЭ оролтоор хэр байна вэ.

d5-д бүх давхрага «хил дээр орлоо» гэж тооцогдсон — нээлт хилээс
хэтэрсэн барт ч. c8-д энэ занга нэг удаа баригдаж зассан боловч
d3/d5 руу дамжаагүй байв (`collect` нь `open`-ийг огт хардаггүй).

Энд хоёр тооцоог ЗЭРЭГЦҮҮЛЖ гаргана:

    өөдрөг  — хил дээр орлоо гэнэ (d5-ийн байдал)
    үнэн    — нээлт хэтэрсэн бол НЭЭЛТИЙН үнээр орно

Зөрүү нь тухайн давхрагад «хэр олон удаа хилийг үсэрч гардаг» вэ
гэдгээс хамаарна. Доод давхрагад бар богино тул хил ойрхон, үсрэлт
олон — тиймээс зөрүү нь ТОМ байх ёстой.

    python3 e2_davhraga.py
"""
import argparse
import numpy as np
import pandas as pd
from core import load
from b1_features import daily, DAY_CLOSE_HOUR
from b6_shahalt import true_range
from e1_pine import pine

TFS = [('1h', 60), ('2h', 120), ('3h', 180), ('4h', 240),
       ('6h', 360), ('8h', 480)]


def bands(d, slow=100):
    pc = d.close.shift(1)
    tr = pd.concat([d.high - d.low, (d.high - pc).abs(),
                    (d.low - pc).abs()], axis=1).max(axis=1)
    d['atr'] = tr.rolling(14).mean()
    d['sq'] = d.atr / tr.rolling(slow).mean()
    m = d.close.rolling(20).mean()
    d['up'], d['dn'] = m + 1.5 * d.atr, m - 1.5 * d.atr
    return d.dropna(subset=['sq', 'up', 'atr'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--spread', type=float, default=.25)
    ap.add_argument('--pos', type=float, default=.50)
    a = ap.parse_args()

    dd = daily(close_hour=DAY_CLOSE_HOUR)
    dd = dd[dd.index >= '2005-01-01'].copy()
    tr = true_range(dd)
    dd['atr'] = tr.rolling(14).mean()
    dd['sq'] = dd.atr / tr.rolling(100).mean()
    m = dd.close.rolling(20).mean()
    dd['up'], dd['dn'] = m + 1.5 * dd.atr, m - 1.5 * dd.atr
    dd = dd.dropna(subset=['sq', 'up', 'atr'])

    h5 = load('XAU_5m_data.csv')
    sets = []
    for tf, mins in TFS:
        d = h5.resample(tf).agg(open=('open', 'first'), high=('high', 'max'),
                                low=('low', 'min'), close=('close', 'last'),
                                volume=('volume', 'sum')).dropna()
        sets.append((tf, mins, bands(d[d.index >= '2010-01-01'].copy())))
    sets.append(('өдөр', 1440, dd))

    print(f'\nСпред ${a.spread:.2f}   байрлал ≥ {a.pos:.2f}   '
          f'стоп 2 ATR, зорилт 4 ATR\n')
    print(f'  {"давхрага":10}{"n":>6}{"ӨӨДРӨГ":>11}{"ҮНЭН":>10}'
          f'{"зөрүү":>9}{"ялсан":>8}{"жилд":>7}{"эерэг жил":>12}')
    print('  ' + '─' * 73)
    out = []
    for tf, mins, d in sets:
        opt, _, _ = pine(d, .80, pos_min=a.pos, gap='ignore',
                         spread=a.spread)
        tru, _, gp = pine(d, .80, pos_min=a.pos, gap='open',
                          spread=a.spread)
        if not len(tru):
            continue
        yrs = (d.index[-1] - d.index[0]).days / 365.25
        tru = tru.copy()
        tru['y'] = pd.to_datetime(tru.date).dt.year
        g = tru.groupby('y').R.mean()
        py = f'{(g > 0).sum()}/{len(g)}'
        print(f'  {tf:10}{len(tru):6}{opt.R.mean():+11.3f}'
              f'{tru.R.mean():+10.3f}{tru.R.mean() - opt.R.mean():+9.3f}'
              f'{(tru.R > 0).mean():8.0%}{len(tru) / yrs:7.1f}{py:>12}')
        out.append((tf, mins, tru.R.mean(), len(tru) / yrs,
                    (g > 0).sum(), len(g)))

    print('\n  ӨӨДРӨГ = хил дээр орлоо гэнэ (d5-ийн таамаг)')
    print('  ҮНЭН   = нээлт хилээс хэтэрсэн бол нээлтийн үнээр орно')
    print('\n  Доод давхрагад зөрүү ТОМ — бар богино тул хил ойрхон,')
    print('  үнэ түүнийг үсэрч гардаг нь олон. Өдрийн график хамгийн')
    print('  бага гажуудалтай.')

    print('\n── Спредэд тэсвэртэй юу (ҮНЭН оролтоор) ──')
    print(f'  {"давхрага":10}{"$0.00":>9}{"$0.25":>9}{"$0.50":>9}'
          f'{"$1.00":>9}')
    for tf, mins, d in sets:
        cells = []
        for sp in (0.0, .25, .50, 1.0):
            t, _, _ = pine(d, .80, pos_min=a.pos, gap='open', spread=sp)
            cells.append(f'{t.R.mean():+.3f}' if len(t) else '—')
        print(f'  {tf:10}' + ''.join(c.rjust(9) for c in cells))

    print('\n── Pine-д бичих хүлээлт (ҮНЭН тоо) ──')
    for tf, mins, r, per, py, ny in out:
        print(f'  {tf:8} {mins:5} мин  →  {r:+.2f}R   жилд {per:.0f}   '
              f'эерэг жил {py}/{ny}')


if __name__ == '__main__':
    main()

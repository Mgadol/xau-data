"""c3. 15 МИНУТ дээр шахалт — цагийн хэмнэлийг арилгаж байж.

Асуулт: өдрийн доторх шахалтыг барьж болох уу?

ХАМГИЙН ТОМ ЗАНГА — ЦАГИЙН ХЭМНЭЛ. Алтны 15 минутын бар нь 23:00-д
дунджаар 0.071%, 16:00-д 0.220% хөдөлдөг — **3.1 дахин** зөрүү.
Тиймээс ATR14/ATR96 гэсэн энгийн харьцаа нь «шахалт» биш, зүгээр л
«одоо Ази байна» гэдгийг олно. Тэр дохиогоор арилжаалвал өдөр бүр
ижил цагт ижил дохио гарна — мэдээлэл тэг.

Тиймээс хоёр хувилбарыг ЗЭРЭГЦҮҮЛЖ шалгана:

    түүхий  — ATR14/ATR96, цаг тооцоогүй
    цэвэр   — бар бүрийн TR-ийг ТУХАЙН ЦАГИЙН ердийн TR-т хуваасны
              ДАРАА ижил харьцааг бодсон

Хэрэв түүхий нь сайн, цэвэр нь муу гарвал — «шахалт» нь цагийн
хэмнэл байсан гэсэн үг.

ХОЁР ДАХЬ ЗАНГА — ЗАРДАЛ. Спред нь доллараар тогтмол ($0.20-0.30)
боловч 15м-ийн хөдөлгөөн өдрийнхөөс 20-30 дахин бага. Тиймээс
зардал нь ATR-ийн хэдэн хувь болохыг ЗААВАЛ хэмжинэ — a18, a23-д
«жижиг хугацаа = зардлаар үхэх» гэж гарсан.

    python3 c3_15min.py
"""
import argparse
import numpy as np
import pandas as pd
from core import load


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--tf', default='15min')
    ap.add_argument('--fast', type=int, default=14)
    ap.add_argument('--slow', type=int, default=96)   # 96×15м = 24 цаг
    ap.add_argument('--fwd', type=int, default=16)    # 4 цаг урагш
    ap.add_argument('--spread', type=float, default=.25, help='доллараар')
    a = ap.parse_args()

    h = load('XAU_5m_data.csv')
    d = h.resample(a.tf).agg(open=('open', 'first'), high=('high', 'max'),
                             low=('low', 'min'), close=('close', 'last'),
                             volume=('volume', 'sum')).dropna()
    d = d[d.index >= '2015-01-01']
    pc = d.close.shift(1)
    tr = pd.concat([d.high - d.low, (d.high - pc).abs(),
                    (d.low - pc).abs()], axis=1).max(axis=1)
    d['tr'] = tr
    d['atr'] = tr.rolling(a.fast).mean()

    # ── Цагийн хэмнэлийн профиль ─────────────────────────────────────
    # ГАЖУУДАХААС сэргийлж ӨНГӨРСӨН өгөгдлөөр л бодно: тухайн цагийн
    # ердийн TR-ийг өмнөх 60 хоногийн ижил цагийн дунджаар авна.
    key = d.index.hour * 60 + d.index.minute
    d['key'] = key
    d['trn'] = np.nan
    for k, g in d.groupby('key'):
        prof = g.tr.rolling(60, min_periods=20).mean().shift(1)
        d.loc[g.index, 'trn'] = (g.tr / prof).to_numpy()

    d['atr_raw'] = d.tr.rolling(a.fast).mean() / d.tr.rolling(a.slow).mean()
    d['atr_cln'] = d.trn.rolling(a.fast).mean() / d.trn.rolling(a.slow).mean()

    # ── Урагшаа хэр явах вэ (ATR-ийн дахинаар) ───────────────────────
    H, L, C = d.high.to_numpy(), d.low.to_numpy(), d.close.to_numpy()
    A = d.atr.to_numpy()
    n = len(d)
    mfe = np.full(n, np.nan)
    for i in range(n - a.fwd):
        if not np.isfinite(A[i]) or A[i] <= 0:
            continue
        hh = H[i + 1:i + 1 + a.fwd].max()
        ll = L[i + 1:i + 1 + a.fwd].min()
        mfe[i] = max(hh - C[i], C[i] - ll) / A[i]
    d['mfe'] = mfe
    d = d.dropna(subset=['atr_raw', 'atr_cln', 'mfe'])

    print(f'{a.tf}: {len(d):,} бар   {d.index.min().date()} → '
          f'{d.index.max().date()}   {a.fwd} бар урагш')
    print(f'ATR-{a.fast} дундаж: ${d.atr.mean():.2f}   '
          f'спред ${a.spread:.2f} = ATR-ийн {a.spread / d.atr.mean():.0%}\n')

    for nm, col in (('ТҮҮХИЙ (цаг тооцоогүй)', 'atr_raw'),
                    ('ЦЭВЭР (цаг арилгасан)', 'atr_cln')):
        d['bin'] = pd.qcut(d[col], 5, labels=False, duplicates='drop')
        print(f'  {nm}')
        print(f'    {"бүлэг":>6} {"харьцаа":>8} {"явсан (ATR)":>12} '
              f'{"голч цаг":>9}')
        for b in sorted(d.bin.dropna().unique()):
            g = d[d.bin == b]
            print(f'    {int(b) + 1:>6} {g[col].mean():8.2f} '
                  f'{g.mfe.mean():12.2f} {int(g.index.hour.to_series().median()):9d}:00')
        lo = d[d.bin == 0].mfe.mean()
        hi = d[d.bin == d.bin.max()].mfe.mean()
        print(f'    шахагдсан ÷ тэлсэн = {lo / hi:.2f} дахин\n')

    print('  Өдрийн график дээр энэ харьцаа 1.58 байсан (b6).')
    print('  ЦЭВЭР хувилбарын харьцаа түүнээс эрс бага бол — 15 минутын')
    print('  «шахалт» гэдэг нь ихэнхдээ цагийн хэмнэл байсан гэсэн үг.')


if __name__ == '__main__':
    main()

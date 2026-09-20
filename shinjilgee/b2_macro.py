"""b2. Гадаад цуваануудыг алтны багцад нэмнэ.

`b1_features.py`-ийн гаргасан 45 багана БҮГД алтны үнийн хувирал тул
шинэ мэдээлэл агуулдаггүй. Жинхэнэ шинэ зүйл нь эндээс — VIX, өгөөжийн
муруй, зээлийн спред, доллар, хөрөнгийн зах, газрын тос, биткойн.

Гурван дүрэм, гурвуулаа НЭВЧИЛТЭЭС хамгаалахад чиглэсэн:

1. ЗӨВХӨН УРАГШ нөхнө. АНУ-ын баяраар эдгээр цуваа гардаггүй ч алт
   арилждаг (VIX 32 өдөр, T10Y2Y 66 өдөр дутуу). Сүүлд МЭДЭГДСЭН утгыг
   авч явна. Ухрааж нөхвөл тухайн өдөр хараахан гараагүй байсан тоог
   ашигласан болно.

2. Түвшин биш ӨӨРЧЛӨЛТ. S&P 500 нь 2 237-оос 7 799 болсон — түвшнийг
   нь шинж болгон өгвөл загвар «индекс өндөр = алт өснө» гэж сурна, энэ
   нь зүгээр л хоёулаа цаг хугацаагаар өссөн гэсэн үг. Өгөөж нь дэглэм
   солигдоход тогтвортой.

3. Сөрөг үнийн ЗАНГА. WTI 2020-04-20-нд −36.98 хүртэл унасан (агуулах
   дүүрч, худалдан авагчид мөнгө нэхсэн). Сөрөг үнээс хувийн өөрчлөлт
   бодвол −305%, +127% гэх мэт утгагүй тоо гарч, загвар тэр хоёр өдөрт
   наалддаг. Хоёр үнэ ХОЁУЛАА эерэг үед л өгөөж бодно.

Нэмэгдэх багана (гаднаас ирсэн дээжийн нэрсийг дагав):

    macro_vix, macro_vix_change_1d, macro_vix_ma5
    macro_yield_spread, macro_yield_spread_change
    macro_credit_spread, macro_credit_spread_change
    macro_dxy_change, mkt_dxy_return
    mkt_equity_return, mkt_oil_return, mkt_bitcoin_return
    mkt_gold_vs_equity, mkt_gold_vs_bonds
    mkt_gold_equity_beta_20d

    python3 b2_macro.py
"""
import argparse
import os
import numpy as np
import pandas as pd
from core import DATA

FRED = os.path.join(DATA, 'fred')

# FRED код → (файл, энэ нь ТҮВШИН үү ҮНЭ үү)
#   'level' — түвшнийг шууд өгнө (VIX, спредүүд: аль хэдийн харьцаа)
#   'price' — өгөөж болгож хувиргана (индекс, үнэ)
SERIES = {
    'VIXCLS':     ('level', 'VIX'),
    'T10Y2Y':     ('level', 'Өгөөжийн зөрүү 10ж−2ж'),
    'BAA10Y':     ('level', 'Baa зээлийн спред'),
    'DTWEXBGS':   ('price', 'Долларын индекс'),
    'SP500':      ('price', 'S&P 500'),
    'DCOILWTICO': ('price', 'WTI газрын тос'),
    'CBBTCUSD':   ('price', 'Биткойн'),
}


def load_series(code):
    """FRED-ийн CSV → нэг баганатай цуваа. Хоосон нүд, `.` нь NaN болно."""
    path = os.path.join(FRED, f'{code}.csv')
    v = pd.read_csv(path)
    dc = v.columns[0]
    # ALFRED-ээс татсан бол хэд хэдэн vintage багана байж болно —
    # хамгийн СҮҮЛИЙНХ нь бүрэн, түүнийг авна (зөрүү нь зөвхөн сүүлийн
    # өдөрт байдгийг шалгасан).
    col = v.columns[-1]
    s = pd.Series(pd.to_numeric(v[col], errors='coerce').values,
                  index=pd.to_datetime(v[dc]), name=code)
    return s[~s.index.duplicated(keep='last')].sort_index()


def safe_return(s):
    """Хувийн өөрчлөлт — хоёр үнэ ХОЁУЛАА эерэг үед л. Сөрөг үнийн занга."""
    prev = s.shift(1)
    ok = (s > 0) & (prev > 0)
    return np.where(ok, (s / prev - 1) * 100, np.nan)


def attach(g):
    """Алтны багц (g) дээр гадаад баганууд нэмнэ."""
    idx = pd.DatetimeIndex(g['date'])
    out = g.copy()
    raw = {}

    for code, (kind, _name) in SERIES.items():
        s = load_series(code)
        # Алтны хоногт тааруулна. reindex + ffill = ЗӨВХӨН УРАГШ нөхөлт:
        # тухайн өдрийн утга байхгүй бол СҮҮЛД МЭДЭГДСЭН утгыг авна.
        # limit=5 — 5-аас олон хоног дараалан байхгүй бол нөхөхгүй
        # (ийм завсар нь цуваа тасарсан гэсэн үг, хуучин утгаар
        # дүүргэвэл худал өгөгдөл болно).
        al = s.reindex(s.index.union(idx)).ffill(limit=5).reindex(idx)
        raw[code] = pd.Series(al.values, index=out.index)

    vix = raw['VIXCLS']
    out['macro_vix'] = vix
    out['macro_vix_change_1d'] = vix.diff()
    out['macro_vix_ma5'] = vix.rolling(5).mean()

    ysp = raw['T10Y2Y']
    out['macro_yield_spread'] = ysp
    out['macro_yield_spread_change'] = ysp.diff()

    csp = raw['BAA10Y']
    out['macro_credit_spread'] = csp
    out['macro_credit_spread_change'] = csp.diff()

    dxy = pd.Series(safe_return(raw['DTWEXBGS']), index=out.index)
    out['macro_dxy_change'] = dxy
    out['mkt_dxy_return'] = dxy

    eq = pd.Series(safe_return(raw['SP500']), index=out.index)
    out['mkt_equity_return'] = eq
    out['mkt_oil_return'] = safe_return(raw['DCOILWTICO'])
    out['mkt_bitcoin_return'] = safe_return(raw['CBBTCUSD'])

    # Алт бусдаас хэр ЗӨРЖ байна — эрсдэлээс зугтах үед алт хөрөнгийн
    # захаас салж дээшилдэг. Энэ зөрүү нь түвшнээс илүү мэдээлэлтэй.
    gr = out['price_return_1d']
    out['mkt_gold_vs_equity'] = gr - eq
    out['mkt_gold_vs_bonds'] = gr + ysp.diff()     # өгөөж буурах = бонд өсөх
    out['mkt_gold_equity_beta_20d'] = (
        gr.rolling(20).cov(eq) / eq.rolling(20).var())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--in', dest='src', default='GOLD_Features_2020_2026.csv')
    ap.add_argument('--out', default='GOLD_Features_Full.csv')
    a = ap.parse_args()

    g = pd.read_csv(os.path.join(DATA, a.src), parse_dates=['date'])
    print(f'Алтны багц: {len(g):,} мөр × {g.shape[1]} багана')

    out = attach(g)
    new = [c for c in out.columns if c not in g.columns]
    print(f'Нэмэгдсэн  : {len(new)} багана\n')

    print(f'{"багана":28} {"утга":>6} {"хоосон":>7}  муж')
    for c in new:
        s = out[c]
        print(f'  {c:26} {int(s.notna().sum()):6} {int(s.isna().sum()):7}  '
              f'{s.min():9.3f} … {s.max():9.3f}')

    out['date'] = out['date'].dt.strftime('%Y-%m-%d')
    path = os.path.join(DATA, a.out)
    out.to_csv(path, index=False)
    print(f'\n{a.out}: {len(out):,} мөр × {out.shape[1]} багана')


if __name__ == '__main__':
    main()

"""1. Өгөгдлийн чанарын шалгалт — ямар ч дүгнэлт гаргахын ӨМНӨ ажиллуулна.

Муу өгөгдөл дээр хийсэн төгс шинжилгээ бол төгс буруу хариу.
"""
import numpy as np, pandas as pd
from core import load

for name in ('XAU_1h_data.csv', 'XAU_5m_data.csv'):
    try: d = load(name)
    except FileNotFoundError:
        print(f"{name}: олдсонгүй (5м нь .rar дотор — unrar x ../XAU_5m_data.rar ..)"); continue
    print(f"\n{'='*64}\n{name}\n{'='*64}")
    print(f"Мөр {len(d):,}   {d.index.min()} → {d.index.max()}")
    print(f"{'✓' if not d.index.duplicated().any() else '✗'} Давхардсан огноо: {d.index.duplicated().sum()}")
    bad = ((d.high<d.low)|(d.high<d.open)|(d.high<d.close)|(d.low>d.open)|(d.low>d.close)).sum()
    print(f"{'✓' if bad==0 else '✗'} OHLC зөрчил: {bad}")
    print(f"{'✓' if (d[['open','high','low','close']]<=0).sum().sum()==0 else '✗'} Тэг/сөрөг үнэ")

    g = pd.Series(d.index).diff()
    big = g[g > pd.Timedelta(hours=72)]
    print(f"\n72 цагаас урт завсар: {len(big)}  (ихэнх нь баяр ёслол — хэвийн)")
    worst = g.nlargest(3)
    print("Хамгийн урт гурав:")
    for i in worst.index:
        print(f"   {d.index[i]}  ← {g[i].total_seconds()/3600:.0f} цаг")

    print("\nЖилд хэдэн бар:")
    per = d.groupby(d.index.year).size()
    med = per.median()
    for y, n in per.items():
        flag = '   ← дутуу' if n < med*0.85 else ''
        print(f"   {y}  {n:>7,}{flag}")

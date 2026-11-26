import json, urllib.request, datetime

SYMS = {"KOSPI": "%5EKS11"}
KST = datetime.timezone(datetime.timedelta(hours=9))
out = {"updated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "items": []}

for name, sym in SYMS.items():
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=3mo&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    d = json.load(urllib.request.urlopen(req, timeout=20))["chart"]["result"][0]
    m = d["meta"]
    pairs = [(t, c) for t, c in zip(d["timestamp"], d["indicators"]["quote"][0]["close"]) if c is not None]
    closes = [round(c, 2) for _, c in pairs]
    price = m.get("regularMarketPrice", closes[-1])
    mt = m.get("regularMarketTime", pairs[-1][0])
    last_day = datetime.datetime.fromtimestamp(pairs[-1][0], KST).date()
    mkt_day = datetime.datetime.fromtimestamp(mt, KST).date()
    if mkt_day > last_day:
        closes.append(round(price, 2))
    else:
        closes[-1] = round(price, 2)
    prev = closes[-2] if len(closes) > 1 else None
    out["items"].append({"name": name, "price": price, "prev": prev, "closes": closes, "time": mt})

with open("market/kr.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False)
print(json.dumps(out, ensure_ascii=False)[:300])

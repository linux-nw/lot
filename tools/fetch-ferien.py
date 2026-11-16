#!/usr/bin/env python3
"""Holt amtliche Schulferien (OpenHolidays API) und schreibt sie kompakt als JSON.
Aufruf: python3 tools/fetch-ferien.py 2025 2029 > tools/ferien.json"""
import json, sys, urllib.request
y0, y1 = int(sys.argv[1]), int(sys.argv[2])
def get(u):
    r = urllib.request.Request(u, headers={"accept": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=30))
out = {}
for cc in ("DE",):
    subs = get(f"https://openholidaysapi.org/Subdivisions?countryIsoCode={cc}&languageIsoCode=DE")
    for s in subs:
        code = s["code"]
        hs = []
        for y in range(y0, y1 + 1):
            hs += get(f"https://openholidaysapi.org/SchoolHolidays?countryIsoCode={cc}&languageIsoCode=DE&validFrom={y}-01-01&validTo={y}-12-31&subdivisionCode={code}")
        seen = {}
        for h in hs: seen[h["id"]] = h
        hs = list(seen.values())
        out[code] = sorted([[h["startDate"], h["endDate"], h["name"][0]["text"]] for h in hs])
        sys.stderr.write(f"{code}: {len(out[code])}\n")
json.dump(out, sys.stdout, ensure_ascii=False, separators=(",", ":"))

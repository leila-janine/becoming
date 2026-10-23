# Use the right conversion denominator
# Run locally. Implement the function, then run the checks below.

def channel_rates(rows):
    totals = {}
    for row in rows:
        counts = totals.setdefault(row["channel"], [0,0])
        counts[0] += row["visits"]
        counts[1] += row["conversions"]
    return {channel: converted / visits if visits else None for channel,(visits,converted) in totals.items()}

from math import isclose
rows=[{"channel":"search","visits":100,"conversions":10},{"channel":"search","visits":10,"conversions":5},{"channel":"empty","visits":0,"conversions":0}]
result=channel_rates(rows)
assert isclose(result["search"],15/110)
assert result["empty"] is None
assert channel_rates([]) == {}
print("Checks passed")

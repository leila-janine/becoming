# Make a batch load repeatable
# Run locally. Implement the function, then run the checks below.

def merge_events(existing, incoming):
    by_id = {}
    for row in existing + incoming:
        by_id[row["id"]] = dict(row)
    return [by_id[key] for key in sorted(by_id)]

existing=[{"id":"a","value":1}]
incoming=[{"id":"a","value":2},{"id":"b","value":3}]
first=merge_events(existing,incoming)
assert first == [{"id":"a","value":2},{"id":"b","value":3}]
assert merge_events(first,incoming) == first
assert existing == [{"id":"a","value":1}]
first[0]["value"]=99
assert incoming[0]["value"] == 2
assert merge_events([],[]) == []
print("Checks passed")

# Make a batch load repeatable
# Run locally. Implement the function, then run the checks below.

def merge_events(existing, incoming):
    raise NotImplementedError("Implement this function")

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

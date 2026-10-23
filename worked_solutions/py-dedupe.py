# Keep the first occurrence
# Run locally. Implement the function, then run the checks below.

def stable_unique(values):
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result

original = ["a", "b", "a", "c", "b"]
assert stable_unique(original) == ["a", "b", "c"]
assert original == ["a", "b", "a", "c", "b"]
assert stable_unique([]) == []
assert stable_unique(["x", "x"]) == ["x"]
print("Checks passed")

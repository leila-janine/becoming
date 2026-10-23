# Find two amounts that match a target
# Run locally. Implement the function, then run the checks below.

def two_sum(values, target):
    seen = {}
    for index, value in enumerate(values):
        complement = target - value
        if complement in seen:
            return seen[complement], index
        seen.setdefault(value, index)
    return None

assert two_sum([200, 700, 1100, 1500], 900) == (0, 1)
assert two_sum([300, 300], 600) == (0, 1)
assert two_sum([100], 200) is None
assert two_sum([], 0) is None
assert two_sum([-100, 400], 300) == (0, 1)
assert two_sum([100, 100, 200], 300) == (0, 2)
print("Checks passed")

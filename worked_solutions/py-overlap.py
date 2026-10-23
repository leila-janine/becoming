# Prevent an appointment conflict
# Run locally. Implement the function, then run the checks below.

def overlaps(a, b):
    return a[0] < b[1] and b[0] < a[1]

assert not overlaps((540, 600), (600, 660))
assert overlaps((540, 610), (600, 660))
assert overlaps((540, 660), (570, 600))
assert overlaps((540, 600), (540, 600))
assert not overlaps((0, 10), (20, 30))
print("Checks passed")

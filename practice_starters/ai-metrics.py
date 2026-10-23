# Evaluate binary predictions
# Run locally. Implement the function, then run the checks below.

def binary_metrics(actual, predicted):
    raise NotImplementedError("Implement this function")

assert binary_metrics([1,1,0,0], [1,0,1,0]) == {"precision":.5,"recall":.5,"f1":.5}
assert binary_metrics([], []) == {"precision":0.,"recall":0.,"f1":0.}
assert binary_metrics([1,1], [1,1])["f1"] == 1.
assert binary_metrics([1,1], [0,0])["recall"] == 0.
for a,p in [([1],[]),([2],[0]),([True],[1])]:
    try:
        binary_metrics(a,p)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected validation error")
print("Checks passed")

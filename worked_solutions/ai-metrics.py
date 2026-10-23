# Evaluate binary predictions
# Run locally. Implement the function, then run the checks below.

def binary_metrics(actual, predicted):
    if len(actual) != len(predicted) or any(type(x) is not int or x not in (0, 1) for x in list(actual) + list(predicted)):
        raise ValueError("Expected equally sized binary integer labels")
    tp = sum(a == 1 and p == 1 for a, p in zip(actual, predicted))
    fp = sum(a == 0 and p == 1 for a, p in zip(actual, predicted))
    fn = sum(a == 1 and p == 0 for a, p in zip(actual, predicted))
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}

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

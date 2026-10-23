# Debug a shared default
# Run locally. Implement the function, then run the checks below.

def add_task(title, tasks=None):
    if tasks is None:
        tasks = []
    tasks.append(title)
    return tasks

assert add_task("A") == ["A"]
assert add_task("B") == ["B"]
existing = ["C"]
result = add_task("D", existing)
assert result is existing
assert existing == ["C", "D"]
print("Checks passed")

"""Original practice exercises. Submitted code is stored as text, never executed by the app."""
from datetime import date, timedelta

CHALLENGES = [
    dict(id='py-dedupe', track='Python', title='Keep the first occurrence', skill='Collections & complexity', level='Foundation', minutes=15,
         prompt='Implement stable_unique(values) for a list of strings. Return a new list with duplicates removed, preserving first-seen order. Do not change the input. Explain the expected time and space cost.',
         cases="['a', 'b', 'a', 'c', 'b'] → ['a', 'b', 'c']\n[] → []\n['x', 'x'] → ['x']",
         hint='Keep both an output list and a set of items already encountered. Appending only unseen values preserves the input order.',
         starter='def stable_unique(values):\n    raise NotImplementedError("Implement this function")\n',
         solution='def stable_unique(values):\n    seen = set()\n    result = []\n    for value in values:\n        if value not in seen:\n            seen.add(value)\n            result.append(value)\n    return result\n',
         checks='original = ["a", "b", "a", "c", "b"]\nassert stable_unique(original) == ["a", "b", "c"]\nassert original == ["a", "b", "a", "c", "b"]\nassert stable_unique([]) == []\nassert stable_unique(["x", "x"]) == ["x"]\nprint("Checks passed")\n',
         review='Average O(n) time for hash-set membership and O(k) extra space for k unique strings. Why would sorting a set fail the required order?',
         url='https://docs.python.org/3/tutorial/datastructures.html',language='python',extension='py'),
    dict(id='py-overlap',track='Python',title='Prevent an appointment conflict',skill='Intervals & edge cases',level='Foundation',minutes=20,
         prompt='Implement overlaps(a, b). Each appointment is a valid (start, end) pair of integer minutes with start < end. Use half-open intervals: an appointment ending at 10:00 does not overlap one starting at 10:00.',
         cases='(540, 600), (600, 660) → False\n(540, 610), (600, 660) → True\n(540, 660), (570, 600) → True',
         hint='Overlap requires each interval to begin before the other ends. Be careful to use strict comparisons at touching endpoints.',
         starter='def overlaps(a, b):\n    raise NotImplementedError("Implement this function")\n',
         solution='def overlaps(a, b):\n    return a[0] < b[1] and b[0] < a[1]\n',
         checks='assert not overlaps((540, 600), (600, 660))\nassert overlaps((540, 610), (600, 660))\nassert overlaps((540, 660), (570, 600))\nassert overlaps((540, 600), (540, 600))\nassert not overlaps((0, 10), (20, 30))\nprint("Checks passed")\n',
         review='O(1) time and O(1) extra space. Add tests for reversed input order, identical intervals, and a one-minute overlap. Explain why touching endpoints should not collide.',
         url='https://docs.python.org/3/library/unittest.html',language='python',extension='py'),
    dict(id='py-mutable',track='Python',title='Debug a shared default',skill='Debugging & regression tests',level='Foundation',minutes=15,
         prompt='The starter leaks tasks across calls because it uses a shared default list. Fix add_task(title, tasks=None) so separate calls without a list are independent. When an explicit list is supplied, mutate and return that same list. Write a regression test that fails on the original implementation.',
         cases="add_task('A') → ['A']\nadd_task('B') → ['B']\nexisting=['C']; add_task('D', existing) → existing becomes ['C','D']",
         hint='Default argument objects are created once. Use None as the default and create a fresh list inside the function only when no list was supplied.',
         starter='def add_task(title, tasks=[]):\n    tasks.append(title)\n    return tasks\n',
         solution='def add_task(title, tasks=None):\n    if tasks is None:\n        tasks = []\n    tasks.append(title)\n    return tasks\n',
         checks='assert add_task("A") == ["A"]\nassert add_task("B") == ["B"]\nexisting = ["C"]\nresult = add_task("D", existing)\nassert result is existing\nassert existing == ["C", "D"]\nprint("Checks passed")\n',
         review='Explain default-argument lifetime and the difference between intended mutation and accidental shared state. Preserve the specified behavior rather than changing the API contract.',
         url='https://docs.python.org/3/tutorial/controlflow.html#default-argument-values',language='python',extension='py'),
    dict(id='py-two-sum',track='Python',title='Find two amounts that match a target',skill='Problem solving & hash maps',level='Developing',minutes=25,
         prompt='Implement two_sum(values, target) for integer amounts (such as centavos). Return a tuple of distinct indices whose values add to target, or None if absent. If several answers exist, return the first found while scanning left-to-right. Do not reuse an index or change the input.',
         cases='[200, 700, 1100, 1500], 900 → (0, 1)\n[300, 300], 600 → (0, 1)\n[100], 200 → None',
         hint='For each value, check whether its complement has already been seen before storing the current index. Keep the earliest index for repeated values.',
         starter='def two_sum(values, target):\n    raise NotImplementedError("Implement this function")\n',
         solution='def two_sum(values, target):\n    seen = {}\n    for index, value in enumerate(values):\n        complement = target - value\n        if complement in seen:\n            return seen[complement], index\n        seen.setdefault(value, index)\n    return None\n',
         checks='assert two_sum([200, 700, 1100, 1500], 900) == (0, 1)\nassert two_sum([300, 300], 600) == (0, 1)\nassert two_sum([100], 200) is None\nassert two_sum([], 0) is None\nassert two_sum([-100, 400], 300) == (0, 1)\nassert two_sum([100, 100, 200], 300) == (0, 2)\nprint("Checks passed")\n',
         review='Compare a nested-loop O(n²) solution with the expected O(n) hash-map approach. Explain the memory tradeoff and why using integer minor units avoids floating-point money surprises.',
         url='https://docs.python.org/3/tutorial/datastructures.html#dictionaries',language='python',extension='py'),
    dict(id='dart-markers',track='Dart / Flutter',title='Toggle a puzzle marker without mutation',skill='Immutable state & tests',level='Foundation',minutes=20,
         prompt='Implement toggleMarker(current, cell) for a 6×6 board. Valid cells are integers 0–35. Return a new set that adds an absent cell or removes a present one. Leave current unchanged. Throw RangeError for invalid cells.',
         cases='{1, 4}, 4 → {1}\n{1}, 5 → {1,5}\n{}, 36 → RangeError',
         hint='Validate the index, copy the set with Set<int>.from(current), and use add/remove on the copy.',
         starter='Set<int> toggleMarker(Set<int> current, int cell) {\n  throw UnimplementedError();\n}\n',
         solution='Set<int> toggleMarker(Set<int> current, int cell) {\n  if (cell < 0 || cell >= 36) {\n    throw RangeError.range(cell, 0, 35);\n  }\n  final next = Set<int>.from(current);\n  if (next.contains(cell)) {\n    next.remove(cell);\n  } else {\n    next.add(cell);\n  }\n  return next;\n}\n',
         checks='void main() {\n  final original = <int>{1, 4};\n  final next = toggleMarker(original, 4);\n  if (next.length != 1 || !next.contains(1)) throw StateError("Remove failed");\n  if (original.length != 2) throw StateError("Input mutated");\n  final added = toggleMarker(<int>{1}, 5);\n  if (added.length != 2 || !added.containsAll(<int>{1, 5})) throw StateError("Add failed");\n  var rejected = false;\n  try { toggleMarker(<int>{}, 36); } on RangeError { rejected = true; }\n  if (!rejected) throw StateError("Invalid cell accepted");\n  print("Checks passed");\n}\n',
         review='Why does returning a new set help make state changes easier to reason about? Add cases for cells -1, 0, and 35. Later, turn these checks into package:test unit tests.',
         url='https://dart.dev/language/collections',language='dart',extension='dart'),
    dict(id='dart-rank',track='Dart / Flutter',title='Rank scores without changing the source',skill='Sorting & deterministic behavior',level='Developing',minutes=20,
         prompt='Implement rankedScores(scores), where scores maps a unique player name to an integer score. Return names ordered by score descending. Break ties by case-sensitive name comparison ascending. Do not change the map. Return an empty list for an empty map.',
         cases="{'Mika': 10, 'Aya': 10, 'Lea': 4} → ['Aya', 'Mika', 'Lea']\n{} → []",
         hint='Sort a copied list of entries with a comparator. Compare scores in the reverse direction, then compare names only for a tie.',
         starter='List<String> rankedScores(Map<String, int> scores) {\n  throw UnimplementedError();\n}\n',
         solution='List<String> rankedScores(Map<String, int> scores) {\n  final entries = scores.entries.toList();\n  entries.sort((a, b) {\n    final byScore = b.value.compareTo(a.value);\n    return byScore != 0 ? byScore : a.key.compareTo(b.key);\n  });\n  return entries.map((entry) => entry.key).toList();\n}\n',
         checks='void main() {\n  final scores = <String, int>{"Mika": 10, "Aya": 10, "Lea": 4};\n  final result = rankedScores(scores);\n  if (result.join(",") != "Aya,Mika,Lea") throw StateError("Ranking failed");\n  if (scores["Mika"] != 10 || scores.length != 3) throw StateError("Map changed");\n  if (rankedScores(<String, int>{}).isNotEmpty) throw StateError("Empty map failed");\n  print("Checks passed");\n}\n',
         review='Explain O(n log n) sorting and O(n) copied data. Why is an explicit tie-breaker useful for reproducible rankings?',
         url='https://dart.dev/effective-dart',language='dart',extension='dart'),
    dict(id='sql-zero',track='SQL & systems',title='Keep users with no transactions',skill='SQL joins & aggregation',level='Foundation',minutes=20,
         prompt='Using the supplied temporary practice tables, list every user with their total transaction amount in centavos, including users with no transactions as zero. Return user_id, name, and total_centavos, ordered by user_id. Do not omit zero-activity users.',
         cases='1 | Aya | 3500\n2 | Mika | 0\n3 | Lea | 500',
         hint='Start from users, LEFT JOIN transactions, group by user, and replace a null SUM with zero using COALESCE.',
         starter='SELECT /* write your columns here */\nFROM practice_users AS u;\n',
         solution='SELECT u.id AS user_id, u.name,\n       COALESCE(SUM(t.amount_centavos), 0) AS total_centavos\nFROM practice_users AS u\nLEFT JOIN practice_transactions AS t ON t.user_id = u.id\nGROUP BY u.id, u.name\nORDER BY u.id;\n',
         setup='CREATE TEMP TABLE practice_users (id INTEGER PRIMARY KEY, name TEXT NOT NULL);\nCREATE TEMP TABLE practice_transactions (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, amount_centavos INTEGER NOT NULL);\nINSERT INTO practice_users VALUES (1, \'Aya\'), (2, \'Mika\'), (3, \'Lea\');\nINSERT INTO practice_transactions VALUES (1, 1, 1000), (2, 1, 2500), (3, 3, 500);\n',
         checks='',review='Explain why INNER JOIN omits Mika and why filtering joined rows in WHERE can accidentally change a LEFT JOIN’s meaning. Run only in a new practice database/session.',
         url='https://www.postgresql.org/docs/current/tutorial-join.html',language='sql',extension='sql'),
    dict(id='systems-retry',track='SQL & systems',title='Review a retry that could duplicate a payment',skill='API design & code review',level='Developing',minutes=20,
         prompt='A client sends POST /orders. The server creates the order, but the response times out. The client retries the same request, and a second order is created. Write a short design proposal to prevent duplicate orders while allowing safe retries. Do not use real payment data.',
         cases='Same customer + same key + same payload → same stored outcome\nSame customer + same key + different payload → explicit conflict\nTwo simultaneous requests with the same key → one order',
         hint='Think about a client-generated idempotency key, user scoping, a request fingerprint, a database uniqueness constraint, and an atomic transaction.',
         starter='# Safe retry design\n\n## Failure scenario\n\n## Request contract\n\n## Storage and concurrency\n\n## Error handling\n\n## Tests\n',
         solution='Use a client-generated idempotency key scoped to the authenticated customer and operation. Store a canonical request fingerprint and a durable result. Enforce a unique database constraint on the scoped key. Create the order and associate the result atomically. Replays with the same fingerprint return the stored result; a changed payload under the same key returns a documented conflict. Define behavior for in-flight requests, retries after crashes, expiration, and downstream operations. Test duplicate sequential requests, concurrent requests, timeouts after commit, different users using the same key, and mismatched payloads.',
         checks='',review='There is no single correct architecture. Explain transaction boundaries, crash recovery, and any downstream side effects. A uniqueness check performed only in application code is insufficient under concurrency.',
         url='https://developer.mozilla.org/en-US/docs/Glossary/Idempotent',language='markdown',extension='md'),
]


def practice_file(challenge, solution=False):
    code=challenge['solution'] if solution else challenge['starter']
    if challenge['extension']=='sql':
        return '-- Use a new practice database/session.\n'+challenge['setup']+'\n'+code
    if challenge['extension']=='md':
        return '# '+challenge['title']+'\n\n'+challenge['prompt']+'\n\n'+code
    prefix='# ' if challenge['extension']=='py' else '// '
    return prefix+challenge['title']+'\n'+prefix+'Run locally. Implement the function, then run the checks below.\n\n'+code+'\n'+challenge['checks']


def recommend(challenges, attempts, selected):
    latest={}
    for item in sorted(attempts,key=lambda a:a.get('logged_at','')):
        latest[item['challenge_id']]=item
    due=[c for c in challenges if c['id'] in latest and latest[c['id']]['review_on']<=selected.isoformat()]
    if due: return due[0], 'Ready for a review from memory'
    new=[c for c in challenges if c['id'] not in latest]
    if new: return new[0], 'A new, manageable practice step'
    return (challenges[0], 'All current reviews are scheduled; choose a small transfer to your own project') if challenges else (None,'No exercises in this track')


def review_date(selected, independent, passed):
    return (selected+timedelta(days=3 if independent and passed else 1)).isoformat()

CHALLENGES.extend([
    dict(id='ai-metrics',track='AI engineering',title='Evaluate binary predictions',skill='Model evaluation & edge cases',level='Developing',minutes=25,
         prompt='Implement binary_metrics(actual, predicted) for equal-length lists containing only integer 0 or 1. Return precision, recall, and F1 for positive class 1. Use 0.0 when a denominator is zero. Raise ValueError for unequal lengths or labels outside 0/1. Explain why accuracy alone can hide important errors.',
         cases='actual=[1,1,0,0], predicted=[1,0,1,0] → precision=0.5, recall=0.5, f1=0.5\nactual=[], predicted=[] → all metrics 0.0',
         hint='Count true positives, false positives, and false negatives. Derive each metric from those counts, and handle a zero denominator explicitly.',
         starter='def binary_metrics(actual, predicted):\n    raise NotImplementedError("Implement this function")\n',
         solution='def binary_metrics(actual, predicted):\n    if len(actual) != len(predicted) or any(type(x) is not int or x not in (0, 1) for x in list(actual) + list(predicted)):\n        raise ValueError("Expected equally sized binary integer labels")\n    tp = sum(a == 1 and p == 1 for a, p in zip(actual, predicted))\n    fp = sum(a == 0 and p == 1 for a, p in zip(actual, predicted))\n    fn = sum(a == 1 and p == 0 for a, p in zip(actual, predicted))\n    precision = tp / (tp + fp) if tp + fp else 0.0\n    recall = tp / (tp + fn) if tp + fn else 0.0\n    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0\n    return {"precision": precision, "recall": recall, "f1": f1}\n',
         checks='assert binary_metrics([1,1,0,0], [1,0,1,0]) == {"precision":.5,"recall":.5,"f1":.5}\nassert binary_metrics([], []) == {"precision":0.,"recall":0.,"f1":0.}\nassert binary_metrics([1,1], [1,1])["f1"] == 1.\nassert binary_metrics([1,1], [0,0])["recall"] == 0.\nfor a,p in [([1],[]),([2],[0]),([True],[1])]:\n    try:\n        binary_metrics(a,p)\n    except ValueError:\n        pass\n    else:\n        raise AssertionError("Expected validation error")\nprint("Checks passed")\n',
         review='These metrics evaluate supplied labels; they do not establish that a model is unbiased or ready for deployment. Check split design, leakage, class balance, the cost of each error, and whether the evaluation data reflects use.',
         url='https://scikit-learn.org/stable/modules/model_evaluation.html',language='python',extension='py'),
    dict(id='de-repeatable',track='Data engineering',title='Make a batch load repeatable',skill='Idempotent ingestion & data contracts',level='Developing',minutes=25,
         prompt='Implement merge_events(existing, incoming) for lists of records with a unique string id and integer value. Return copied records sorted by id. Incoming records replace existing ones with the same id; later records in each input win. Leave both inputs unchanged. Assume the records satisfy the stated schema.',
         cases="existing=[{'id':'a','value':1}], incoming=[{'id':'a','value':2},{'id':'b','value':3}] → a=2,b=3\nLoading the same incoming batch twice → same result",
         hint='Index copied records by their id, process existing then incoming, and return records in sorted-key order.',
         starter='def merge_events(existing, incoming):\n    raise NotImplementedError("Implement this function")\n',
         solution='def merge_events(existing, incoming):\n    by_id = {}\n    for row in existing + incoming:\n        by_id[row["id"]] = dict(row)\n    return [by_id[key] for key in sorted(by_id)]\n',
         checks='existing=[{"id":"a","value":1}]\nincoming=[{"id":"a","value":2},{"id":"b","value":3}]\nfirst=merge_events(existing,incoming)\nassert first == [{"id":"a","value":2},{"id":"b","value":3}]\nassert merge_events(first,incoming) == first\nassert existing == [{"id":"a","value":1}]\nfirst[0]["value"]=99\nassert incoming[0]["value"] == 2\nassert merge_events([],[]) == []\nprint("Checks passed")\n',
         review='This is an in-memory exercise, not a complete production loader. Explain how validation, database constraints, transactions, late events, and failed-batch recovery change the design.',
         url='https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html',language='python',extension='py'),
    dict(id='da-denominator',track='Data analytics',title='Use the right conversion denominator',skill='Metrics & analytical communication',level='Developing',minutes=20,
         prompt='Implement channel_rates(rows), where each row has a string channel and nonnegative integer visits and conversions, with conversions <= visits. Aggregate counts by channel first, then calculate conversions / visits. Return a mapping from channel to rate; use None when total visits is zero. Do not average row percentages.',
         cases="[{'channel':'search','visits':100,'conversions':10},{'channel':'search','visits':10,'conversions':5}] → search: 15/110\nzero total visits → None",
         hint='Sum numerators and denominators within each channel before dividing. A simple mean would give a small batch the same weight as a much larger batch.',
         starter='def channel_rates(rows):\n    raise NotImplementedError("Implement this function")\n',
         solution='def channel_rates(rows):\n    totals = {}\n    for row in rows:\n        counts = totals.setdefault(row["channel"], [0,0])\n        counts[0] += row["visits"]\n        counts[1] += row["conversions"]\n    return {channel: converted / visits if visits else None for channel,(visits,converted) in totals.items()}\n',
         checks='from math import isclose\nrows=[{"channel":"search","visits":100,"conversions":10},{"channel":"search","visits":10,"conversions":5},{"channel":"empty","visits":0,"conversions":0}]\nresult=channel_rates(rows)\nassert isclose(result["search"],15/110)\nassert result["empty"] is None\nassert channel_rates([]) == {}\nprint("Checks passed")\n',
         review='Explain the metric definition, time window, and assumptions. A difference in conversion rate is not by itself evidence that the channel caused the difference.',
         url='https://pandas.pydata.org/docs/getting_started/intro_tutorials/index.html',language='python',extension='py'),
])

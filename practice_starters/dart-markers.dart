// Toggle a puzzle marker without mutation
// Run locally. Implement the function, then run the checks below.

Set<int> toggleMarker(Set<int> current, int cell) {
  throw UnimplementedError();
}

void main() {
  final original = <int>{1, 4};
  final next = toggleMarker(original, 4);
  if (next.length != 1 || !next.contains(1)) throw StateError("Remove failed");
  if (original.length != 2) throw StateError("Input mutated");
  final added = toggleMarker(<int>{1}, 5);
  if (added.length != 2 || !added.containsAll(<int>{1, 5})) throw StateError("Add failed");
  var rejected = false;
  try { toggleMarker(<int>{}, 36); } on RangeError { rejected = true; }
  if (!rejected) throw StateError("Invalid cell accepted");
  print("Checks passed");
}

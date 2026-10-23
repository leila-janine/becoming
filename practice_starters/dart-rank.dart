// Rank scores without changing the source
// Run locally. Implement the function, then run the checks below.

List<String> rankedScores(Map<String, int> scores) {
  throw UnimplementedError();
}

void main() {
  final scores = <String, int>{"Mika": 10, "Aya": 10, "Lea": 4};
  final result = rankedScores(scores);
  if (result.join(",") != "Aya,Mika,Lea") throw StateError("Ranking failed");
  if (scores["Mika"] != 10 || scores.length != 3) throw StateError("Map changed");
  if (rankedScores(<String, int>{}).isNotEmpty) throw StateError("Empty map failed");
  print("Checks passed");
}

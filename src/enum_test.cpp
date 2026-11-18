// Hypothesis test: are targets reachable by short programs from the starts alone?
// Exhaustive DFS over straight-line programs (value sets) up to depth K.
// Input: limit ns nt starts targets. Output: for each target, min depth found (or -1).
#include <bits/stdc++.h>
using namespace std;
typedef long long ll; typedef __int128 i128;
ll LIM; int K;
unordered_map<ll,int> tgt;  // target -> best depth
vector<ll> vals;
void dfs(int depth) {
    int n = vals.size();
    for (int i = 0; i < n; i++) for (int j = 0; j <= i; j++) {
        ll x = vals[i], y = vals[j];
        if (x < y) swap(x, y);
        ll cand[4]; int c = 0;
        if (x <= LIM - y) cand[c++] = x + y;
        if (x > y) cand[c++] = x - y;
        if ((i128)x * y <= LIM) cand[c++] = x * y;
        if (y > 1 && x % y == 0) cand[c++] = x / y;
        for (int k = 0; k < c; k++) {
            ll z = cand[k];
            if (find(vals.begin(), vals.end(), z) != vals.end()) continue;
            auto it = tgt.find(z);
            if (it != tgt.end() && it->second > depth + 1) it->second = depth + 1;
            if (depth + 1 < K) { vals.push_back(z); dfs(depth + 1); vals.pop_back(); }
        }
    }
}
int main(int argc, char** argv) {
    K = atoi(argv[1]);
    int ns, nt; cin >> LIM >> ns >> nt;
    vals.resize(ns); for (auto& v : vals) cin >> v;
    vector<ll> T(nt); for (auto& t : T) { cin >> t; tgt[t] = 99; }
    dfs(0);
    for (ll t : T) printf("%d ", tgt[t] == 99 ? -1 : tgt[t]);
    printf("\n");
}

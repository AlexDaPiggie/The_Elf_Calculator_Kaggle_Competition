// Elf Calculator solver v1.
// Input lines: id limit ns nt s1..sns t1..tnt     Output: id <json program>
// Per target: build a cost<=2 dictionary from live registers, then a backward
// beam search over residuals r = X*f +/- a, r = a - X, r = X + a, with
// two-term meet-in-the-middle terminals. Registers: LRU eviction with pinning.
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef __int128 i128;

static ll LIM;
static int BEAM = 8, DEPTH = 14, ORDER = 0;
static double ALPHA = 0.18;
static int APPROX = 2;
static uint64_t SEED = 1;

struct Ent { ll v; int a, b; char op; int c; };  // a,b: indices into dict (-1 for leaf)

struct Index {
    vector<ll> k; vector<int> id; vector<int> used; size_t m;
    Index(int bits) : k(1u << bits, 0), id(1u << bits), m((1u << bits) - 1) {}
    inline size_t slot(ll v) const {
        uint64_t h = uint64_t(v) * 0x9e3779b97f4a7c15ULL; h ^= h >> 29;
        size_t i = h & m;
        while (k[i] && k[i] != v) i = (i + 1) & m;
        return i;
    }
    inline int get(ll v) const { size_t i = slot(v); return k[i] ? id[i] : -1; }
    inline bool put(ll v, int x) { size_t i = slot(v); if (k[i]) return false; k[i] = v; id[i] = x; used.push_back(i); return true; }
    void clear() { for (size_t i : used) k[i] = 0; used.clear(); }
};

struct Dict {
    vector<Ent> e; Index ix{23}; int n0 = 0, n1 = 0;
    vector<pair<ll,int>> sorted;  // all entries sorted by value
    inline void add(ll v, int a, int b, char op, int c) {
        if (v > 0 && v <= LIM && ix.put(v, e.size())) e.push_back({v, a, b, op, c});
    }
    inline void comb(int i, int j, int c) {
        ll x = e[i].v, y = e[j].v;
        if (x < y) { swap(x, y); swap(i, j); }
        if (x <= LIM - y) add(x + y, i, j, '+', c);
        if (x != y) add(x - y, i, j, '-', c);
        if ((i128)x * y <= LIM) add(x * y, i, j, '*', c);
        if (x % y == 0 && y > 1) add(x / y, i, j, '/', c);
    }
    void build(const vector<ll>& leaves, bool two) {
        ix.clear(); e.clear(); sorted.clear();
        for (ll v : leaves) add(v, -1, -1, 0, 0);
        n0 = e.size();
        for (int i = 0; i < n0; i++) for (int j = 0; j <= i; j++) comb(i, j, 1);
        n1 = e.size();
        if (two) for (int i = n0; i < n1; i++) for (int j = 0; j < n0; j++) comb(i, j, 2);
        sorted.reserve(e.size());
        for (int i = 0; i < (int)e.size(); i++) sorted.push_back({e[i].v, i});
        sort(sorted.begin(), sorted.end());
    }
};

// Search node: residual r; how to get parent residual from r:
// parent = r*f + a (op '+'), r*f - a ('-'), a - r ('r'). f/a = dict ids or -1.
struct Link { int f = -1, a = -1; char op = '+'; int f2 = -1; };  // op 'P': parent = child + f*f2 ; 'M': parent = f*f2 - child
struct Node { ll r; int g; int parent; Link l; double rank; };
// Terminal kinds: r = dict[t1] (t2=-1), or r = dict[t1] op dict[t2]
struct Term { int node = -1; int t1 = -1, t2 = -1; char op = 0; };

struct Search {
    Dict& d; int best = 1 << 30; Term bt; vector<Node> hist; vector<Node> nxt;
    unordered_map<ll,int> seen;
    Search(Dict& d) : d(d) {}
    inline int ec(int id) const { return id < 0 ? 0 : d.e[id].c; }
    void terminal(int p, ll r) {
        int g = hist[p].g;
        int id = d.ix.get(r);
        if (id >= 0) { if (g + d.e[id].c < best) { best = g + d.e[id].c; bt = {p, id, -1, 0}; } return; }
        if (g + 1 >= best) return;
        // two-term: r = x op y, x in D0..D1 (cost<=1), y any dict entry
        int lim1 = d.n1;
        for (int i = 0; i < lim1; i++) {
            const Ent& x = d.e[i];
            int base = g + x.c + 1;
            if (base >= best) continue;
            ll xv = x.v;
            if (xv < r) { int j = d.ix.get(r - xv); if (j >= 0 && base + d.e[j].c < best) { best = base + d.e[j].c; bt = {p, i, j, '+'}; } }
            if (xv <= LIM - r) { int j = d.ix.get(r + xv); if (j >= 0 && base + d.e[j].c < best) { best = base + d.e[j].c; bt = {p, j, i, '-'}; } }
            if (xv > r) { int j = d.ix.get(xv - r); if (j >= 0 && base + d.e[j].c < best) { best = base + d.e[j].c; bt = {p, i, j, '-'}; } }
            if (xv > 1 && r % xv == 0) { int j = d.ix.get(r / xv); if (j >= 0 && base + d.e[j].c < best) { best = base + d.e[j].c; bt = {p, i, j, '*'}; } }
            if (xv > 1 && (i128)r * xv <= LIM) { int j = d.ix.get(r * xv); if (j >= 0 && base + d.e[j].c < best) { best = base + d.e[j].c; bt = {p, j, i, '/'}; } }
        }
    }
    void offer(int p, ll v, int f, int a, char op, int f2 = -1) {
        if (v <= 0 || v > LIM) return;
        int g = hist[p].g + (f >= 0 ? ec(f) + 1 : 0) + (a >= 0 ? ec(a) + 1 : 0);
        if (f2 >= 0) g = hist[p].g + ec(f) + ec(f2) + 2;
        if (g + 1 >= best) return;
        if (v >= hist[p].r) return;
        auto it = seen.find(v);
        if (it != seen.end() && it->second <= g) return;
        double rank = g + ALPHA * log2((double)v);
        if ((int)nxt.size() >= BEAM && rank >= nxt.back().rank) return;
        for (auto q = nxt.begin(); q != nxt.end(); ++q) if (q->r == v) { if (q->g <= g) return; nxt.erase(q); break; }
        Node s{v, g, p, {f, a, op, f2}, rank};
        auto pos = upper_bound(nxt.begin(), nxt.end(), rank, [](double k, const Node& x) { return k < x.rank; });
        nxt.insert(pos, s);
        if ((int)nxt.size() > BEAM) nxt.pop_back();
    }
    void expand(int p) {
        ll r = hist[p].r;
        // nearest dictionary values: r = X + a, r = a - X
        auto it = lower_bound(d.sorted.begin(), d.sorted.end(), make_pair(r, -1));
        for (int k = -6; k < 6; k++) {
            long pos = (it - d.sorted.begin()) + k;
            if (pos < 0 || pos >= (long)d.sorted.size()) continue;
            auto [a, id] = d.sorted[pos];
            if (a < r) offer(p, r - a, -1, id, '+');
            else if (a > r) offer(p, a - r, -1, id, 'r');
        }
        // r = X*f + a / X*f - a, f in cost<=1
        for (int i = 0; i < d.n1; i++) {
            ll f = d.e[i].v;
            if (f < 2 || f >= r) continue;
            ll q = r / f, rem = r % f;
            if (rem == 0) { offer(p, q, i, -1, '+'); continue; }
            int j = d.ix.get(rem);
            if (j >= 0) offer(p, q, i, j, '+');
            j = d.ix.get(f - rem);
            if (j >= 0) offer(p, q + 1, i, j, '-');
            if (APPROX && q > 16) {
                auto it2 = lower_bound(d.sorted.begin(), d.sorted.end(), make_pair(q, -1));
                for (int k = -APPROX; k < APPROX; k++) {
                    long pos = (it2 - d.sorted.begin()) + k;
                    if (pos < 0 || pos >= (long)d.sorted.size()) continue;
                    auto [y, yi] = d.sorted[pos];
                    if ((i128)f * y > LIM) continue;
                    ll m = f * y;
                    if (m < r) offer(p, r - m, i, -1, 'P', yi);
                    else if (m > r) offer(p, m - r, i, -1, 'M', yi);
                }
            }
        }
    }
    void run(ll t) {
        hist.push_back({t, 0, -1, {}, 0});
        terminal(0, t);
        vector<int> front{0};
        for (int depth = 0; depth < DEPTH && !front.empty(); depth++) {
            nxt.clear();
            for (int p : front) if (hist[p].g + 2 < best) expand(p);
            front.clear();
            for (Node& s : nxt) {
                if (s.g + 1 >= best) continue;
                seen[s.r] = s.g;
                int id = hist.size(); hist.push_back(s);
                terminal(id, s.r);
                front.push_back(id);
            }
        }
    }
};

// ---------- Puzzle state with real registers ----------
struct Instr { char op; int a, b, d; };
struct Recipe { char op; ll x, y; };  // value = x op y

struct Solver {
    vector<ll> starts, targets; int R = 48;
    array<ll,48> reg{}; array<long,48> last{}; long clock = 0;
    vector<Instr> prog; unordered_set<ll> covered; set<ll> need;
    mt19937_64 rng;
    Solver(uint64_t s) : rng(s) {}

    int find(ll v) { for (int i = 0; i < R; i++) if (reg[i] == v) return i; return -1; }
    static ll apply(char op, ll x, ll y) {
        if (op == '+') return x + y; if (op == '-') return x - y; if (op == '*') return x * y; return x / y;
    }
    // Emit recipes in order; recipes reference values that are either live or produced earlier.
    void emit(const vector<pair<ll,Recipe>>& plan) {
        // remaining-use counts for pinning
        unordered_map<ll,int> uses;
        for (auto& [v, rc] : plan) { uses[rc.x]++; uses[rc.y]++; }
        for (auto& [v, rc] : plan) {
            int ra = find(rc.x), rb = find(rc.y);
            if (ra < 0 || rb < 0) { fprintf(stderr, "emit: missing operand\n"); exit(1); }
            uses[rc.x]--; uses[rc.y]--;
            last[ra] = last[rb] = ++clock;
            int dst = find(v);
            if (dst < 0) {
                long bestt = LONG_MAX; dst = -1;
                for (int i = 0; i < R; i++) {
                    if (reg[i] == 0) { dst = i; break; }
                    auto u = uses.find(reg[i]);
                    if (u != uses.end() && u->second > 0) continue;
                    if (i == ra || i == rb) { /* overwriting a source is fine if not needed later */ }
                    long pr = last[i] + (need.count(reg[i]) ? 0 : 0);
                    if (pr < bestt) { bestt = pr; dst = i; }
                }
                if (dst < 0) { fprintf(stderr, "emit: no register\n"); exit(1); }
            }
            prog.push_back({rc.op, ra, rb, dst});
            reg[dst] = v; last[dst] = ++clock;
            need.erase(v);
        }
    }
    // Collect recipes for a dict entry (post-order, dedup by value)
    void collect(Dict& d, int id, vector<pair<ll,Recipe>>& plan, unordered_set<ll>& have) {
        const Ent& e = d.e[id];
        if (have.count(e.v)) return;
        if (e.a < 0) return;  // leaf = live register
        collect(d, e.a, plan, have); collect(d, e.b, plan, have);
        if (have.insert(e.v).second) plan.push_back({e.v, {e.op, d.e[e.a].v, d.e[e.b].v}});
    }
    void addv(ll v, Recipe rc, vector<pair<ll,Recipe>>& plan, unordered_set<ll>& have) {
        if (have.insert(v).second) plan.push_back({v, rc});
    }
    // Fallback binary method from 1 (always valid when limit >= target)
    int solveTarget(ll t, Dict& d) {
        vector<ll> leaves;
        for (int i = 0; i < R; i++) if (reg[i]) leaves.push_back(reg[i]);
        d.build(leaves, true);
        int ob = BEAM, od = DEPTH;
        unique_ptr<Search> sp(new Search(d));
        sp->run(t);
        while (sp->bt.node < 0 && DEPTH < 80) {  // widen until found
            BEAM *= 2; DEPTH *= 2;
            sp.reset(new Search(d)); sp->run(t);
        }
        BEAM = ob; DEPTH = od;
        Search& s = *sp;
        if (s.bt.node < 0) return -1;
        vector<pair<ll,Recipe>> plan; unordered_set<ll> have(leaves.begin(), leaves.end());
        // terminal value
        ll v;
        Term& T = s.bt;
        if (T.t2 < 0) { collect(d, T.t1, plan, have); v = d.e[T.t1].v; }
        else {
            collect(d, T.t1, plan, have); collect(d, T.t2, plan, have);
            ll x = d.e[T.t1].v, y = d.e[T.t2].v; v = apply(T.op, x, y);
            addv(v, {T.op, x, y}, plan, have);
        }
        for (int p = T.node; s.hist[p].parent >= 0; p = s.hist[p].parent) {
            Link l = s.hist[p].l;
            if (l.f2 >= 0) {
                collect(d, l.f, plan, have); collect(d, l.f2, plan, have);
                ll x = d.e[l.f].v, y = d.e[l.f2].v, m = x * y;
                addv(m, {'*', x, y}, plan, have);
                ll nv = l.op == 'P' ? v + m : m - v;
                addv(nv, {l.op == 'P' ? '+' : '-', l.op == 'P' ? v : m, l.op == 'P' ? m : v}, plan, have);
                v = nv; continue;
            }
            if (l.f >= 0) { collect(d, l.f, plan, have); ll f = d.e[l.f].v; ll nv = v * f; addv(nv, {'*', v, f}, plan, have); v = nv; }
            if (l.a >= 0) {
                collect(d, l.a, plan, have); ll a = d.e[l.a].v; ll nv;
                if (l.op == 'r') { nv = a - v; addv(nv, {'-', a, v}, plan, have); }
                else if (l.op == '+') { nv = v + a; addv(nv, {'+', v, a}, plan, have); }
                else { nv = v - a; addv(nv, {'-', v, a}, plan, have); }
                v = nv;
            }
        }
        if (v != t) { fprintf(stderr, "reconstruct mismatch %lld %lld\n", v, t); exit(1); }
        emit(plan);
        if (getenv("ELF_DEBUG")) fprintf(stderr, "%lld cost %zu\n", t, plan.size());
        return plan.size();
    }
    void run() {
        for (size_t i = 0; i < starts.size(); i++) { reg[i] = starts[i]; last[i] = 0; }
        for (ll t : targets) need.insert(t);
        for (ll s : starts) need.erase(s);
        static Dict d;
        vector<ll> order(need.begin(), need.end());
        if (ORDER == 1) reverse(order.begin(), order.end());
        if (ORDER == 2) shuffle(order.begin(), order.end(), rng);
        for (ll t : order) {
            if (!need.count(t)) continue;
            if (find(t) >= 0) { need.erase(t); continue; }
            int tries = 0;
            while (solveTarget(t, d) < 0) {
                // bootstrap: materialize the smallest missing small constant reachable in the dict
                bool added = false;
                for (ll c = 1; c <= 64 && !added; c++) {
                    if (find(c) >= 0) continue;
                    int id = d.ix.get(c);
                    if (id < 0) continue;
                    vector<pair<ll,Recipe>> plan; unordered_set<ll> have;
                    for (int i = 0; i < R; i++) if (reg[i]) have.insert(reg[i]);
                    collect(d, id, plan, have); emit(plan); added = true;
                }
                if (!added || ++tries > 64) { fprintf(stderr, "no solution for %lld\n", t); exit(1); }
            }
        }
    }
};

int main(int argc, char** argv) {
    for (int i = 1; i + 1 < argc; i += 2) {
        string k = argv[i]; double v = atof(argv[i + 1]);
        if (k == "-w") BEAM = v; else if (k == "-d") DEPTH = v; else if (k == "-a") ALPHA = v;
        else if (k == "-o") ORDER = v; else if (k == "-x") APPROX = v; else if (k == "-s") SEED = v;
    }
    string id; ll limit; int ns, nt;
    while (cin >> id >> limit >> ns >> nt) {
        LIM = limit;
        Solver S(SEED);
        S.starts.resize(ns); S.targets.resize(nt);
        for (auto& x : S.starts) cin >> x;
        for (auto& x : S.targets) cin >> x;
        S.run();
        printf("%s [", id.c_str());
        for (size_t k = 0; k < S.prog.size(); k++) {
            auto& in = S.prog[k];
            printf("%s[\"%c\",%d,%d,%d]", k ? "," : "", in.op, in.a, in.b, in.d);
        }
        printf("]\n"); fflush(stdout);
    }
}

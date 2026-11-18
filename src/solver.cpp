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
static int APPROX = 2, TIEBIG = 0;
static double NOISE = 0;
static int SUMAPPROX = 0, KEEP = 0, TRI = 0, DEEP = 0, PALETTE = 0, VC = 0, VSET = 1, PREFIX = 0, HV = 0; static ll KSMALL = 1 << 16; static long UCW = 40;
static bool DEBUG = getenv("ELF_DEBUG") != nullptr;
static uint64_t SEED = 1;

struct Ent { ll v; int a, b; char op; int c; };  // a,b: indices into dict (-1 for leaf); op 'V': virtual leaf, a = index into vleaves
struct Recipe { char op; ll x, y; };  // value = x op y
struct VLeaf { ll v; vector<pair<ll,Recipe>> chain; };  // value not in registers + recipe chain from live values

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
    const vector<VLeaf>* vl = nullptr;
    inline void add(ll v, int a, int b, char op, int c) {
        if (v <= 0 || v > LIM) return;
        size_t s = ix.slot(v);
        if (!ix.k[s]) { ix.k[s] = v; ix.id[s] = e.size(); ix.used.push_back(s); e.push_back({v, a, b, op, c}); return; }
        Ent& o = e[ix.id[s]];
        if (c < o.c) o = {v, a, b, op, c};  // cheaper recipe (only possible with virtual leaves)
    }
    inline void comb(int i, int j, int) {
        int c = 1 + e[i].c + (i == j ? 0 : e[j].c);
        ll x = e[i].v, y = e[j].v;
        if (x < y) { swap(x, y); swap(i, j); }
        if (x <= LIM - y) add(x + y, i, j, '+', c);
        if (x != y) add(x - y, i, j, '-', c);
        if ((i128)x * y <= LIM) add(x * y, i, j, '*', c);
        if (x % y == 0 && y > 1) add(x / y, i, j, '/', c);
    }
    void build(const vector<ll>& leaves, bool two, const vector<VLeaf>* virt = nullptr) {
        ix.clear(); e.clear(); sorted.clear(); vl = virt;
        for (ll v : leaves) add(v, -1, -1, 0, 0);
        if (virt) for (int k = 0; k < (int)virt->size(); k++) add((*virt)[k].v, k, -1, 'V', (*virt)[k].chain.size());
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
struct Term { int node = -1; int t1 = -1, t2 = -1; char op = 0; int t3 = -1; };  // op 'A': t1*t2+t3, 'B': t1*t2-t3

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
        if (TRI && g + 3 < best) {
            // three-term: r = A*B +/- C, all from dict. Full dict at root, cost<=1 for A elsewhere.
            int n = (p == 0 || TRI > 1) ? (int)d.e.size() : d.n1;
            for (int i = 0; i < n; i++) {
                const Ent& A = d.e[i];
                if (A.v < 2 || A.v > r) continue;
                int base = g + A.c + 2;
                if (base >= best) continue;
                ll q = r / A.v;
                for (ll B = q; B <= q + 1; B++) {
                    if (B < 2 || (i128)A.v * B > LIM) continue;
                    int j = d.ix.get(B);
                    if (j < 0 || base + d.e[j].c >= best) continue;
                    ll m = A.v * B;
                    if (m == r) continue;  // pure product handled by two-term
                    ll C = m < r ? r - m : m - r;
                    int k = d.ix.get(C);
                    if (k < 0) continue;
                    int tot = base + d.e[j].c + d.e[k].c;
                    if (tot < best) { best = tot; bt = {p, i, j, m < r ? 'A' : 'B', k}; }
                }
            }
        }
        // two-term: r = x op y, x in D0..D1 (cost<=1), y any dict entry
        int lim1 = (DEEP && p == 0) ? (int)d.e.size() : d.n1;
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
            if (j >= 0 && (i128)(q + 1) * f <= LIM) offer(p, q + 1, i, j, '-');
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
        // additive two-term approximation: r ~ x + y, x cost<=1, y nearest in full dict
        if (SUMAPPROX) for (int i = 0; i < d.n1; i++) {
            ll x = d.e[i].v;
            if (x >= r) continue;
            ll q = r - x;
            auto it2 = lower_bound(d.sorted.begin(), d.sorted.end(), make_pair(q, -1));
            for (int k = -SUMAPPROX; k < SUMAPPROX; k++) {
                long pos = (it2 - d.sorted.begin()) + k;
                if (pos < 0 || pos >= (long)d.sorted.size()) continue;
                auto [y, yi] = d.sorted[pos];
                if (y == q || x > LIM - y) continue;
                ll m = x + y;
                if (m < r) offer(p, r - m, i, -1, 'S', yi);
                else offer(p, m - r, i, -1, 'T', yi);
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
struct Solver {
    vector<ll> starts, targets; int R = 48; vector<Instr> pre; vector<ll> histv;  // values ever held (most recent last)
    array<ll,48> reg{}; array<long,48> last{}; array<int,48> uc{}; long clock = 0;
    vector<Instr> prog; unordered_set<ll> covered, keep; set<ll> need;
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
            last[ra] = last[rb] = ++clock; uc[ra]++; uc[rb]++;
            int dst = find(v);
            if (dst < 0) {
                long bestt = LONG_MAX; dst = -1;
                for (int i = 0; i < R; i++) {
                    if (reg[i] == 0) { dst = i; break; }
                    auto u = uses.find(reg[i]);
                    if (u != uses.end() && u->second > 0) continue;
                    if (i == ra || i == rb) { /* overwriting a source is fine if not needed later */ }
                    long pr = last[i];
                    if (KEEP == 1) pr += keep.count(reg[i]) ? (long)1e12 : 0;
                    else if (KEEP == 4) pr += keep.count(reg[i]) ? (long)1e12 : (long)uc[i] * UCW;  // reuse evidence protects scratch
                    else if (KEEP >= 2) {  // protect starts and small helpers; finished targets are ordinary
                        bool st = std::find(starts.begin(), starts.end(), reg[i]) != starts.end();
                        if (st || reg[i] < KSMALL) pr += (long)1e12;
                        if (KEEP == 3 && !st && keep.count(reg[i])) pr -= (long)1e6;  // done targets go first
                    }
                    if (pr < bestt) { bestt = pr; dst = i; }
                }
                if (dst < 0) { fprintf(stderr, "emit: no register\n"); exit(1); }
            }
            prog.push_back({rc.op, ra, rb, dst}); histv.push_back(v);
            reg[dst] = v; last[dst] = ++clock; uc[dst] = 0;
            need.erase(v);
        }
    }
    // Collect recipes for a dict entry (post-order, dedup by value)
    void collect(Dict& d, int id, vector<pair<ll,Recipe>>& plan, unordered_set<ll>& have) {
        const Ent& e = d.e[id];
        if (have.count(e.v)) return;
        if (e.a < 0) return;  // leaf = live register
        if (e.op == 'V') { for (auto& [v, rc] : (*d.vl)[e.a].chain) addv(v, rc, plan, have); return; }
        collect(d, e.a, plan, have); collect(d, e.b, plan, have);
        if (have.insert(e.v).second) plan.push_back({e.v, {e.op, d.e[e.a].v, d.e[e.b].v}});
    }
    void addv(ll v, Recipe rc, vector<pair<ll,Recipe>>& plan, unordered_set<ll>& have) {
        if (have.insert(v).second) plan.push_back({v, rc});
    }
    vector<VLeaf> vleaves;
    // Virtual leaves: small constants and powers of two not in registers, with their cheapest
    // recipe chain from live values (Bellman-Ford over a small candidate set).
    void makeVirtual(const vector<ll>& live) {
        vleaves.clear();
        if (!VC) return;
        vector<ll> S;
        for (ll c = 1; c <= 16; c++) S.push_back(c);
        for (ll p = 32; p <= LIM && p > 0; p *= 2) { S.push_back(p); if (p > LIM / 2) break; }
        if (VSET == 2) for (ll p = 32; p <= LIM / 2; p *= 2) { S.push_back(p - 1); S.push_back(p + 1); }
        if (VSET == 3) for (ll p = 16; p <= LIM / 3; p *= 2) S.push_back(3 * p);
        unordered_set<ll> L(live.begin(), live.end());
        for (ll v : live) S.push_back(v);
        if (HV) {  // recently held values that were evicted: rebuildable at a price
            unordered_set<ll> L0(live.begin(), live.end()); int cnt = 0;
            for (int i = (int)histv.size() - 1; i >= 0 && cnt < HV; i--)
                if (!L0.count(histv[i])) { S.push_back(histv[i]); cnt++; }
            for (ll v : starts) S.push_back(v);
        }
        sort(S.begin(), S.end()); S.erase(unique(S.begin(), S.end()), S.end());
        int n = S.size();
        unordered_map<ll,int> pos; for (int i = 0; i < n; i++) pos[S[i]] = i;
        vector<int> cost(n, 1 << 20); vector<Recipe> rc(n);
        for (int i = 0; i < n; i++) if (L.count(S[i])) cost[i] = 0;
        int i1 = pos.count(1) ? pos[1] : -1;
        if (i1 >= 0 && cost[i1] > 1 && !live.empty()) { cost[i1] = 1; rc[i1] = {'/', live[0], live[0]}; }
        for (bool ch = true; ch;) {
            ch = false;
            for (int i = 0; i < n; i++) if (cost[i] < 1 << 20) for (int j = 0; j <= i; j++) if (cost[j] < 1 << 20) {
                ll x = S[i], y = S[j]; int c = 1 + cost[i] + (i == j ? 0 : cost[j]);
                ll cand[3]; char op[3] = {'+', '-', '*'}; bool ok[3];
                ok[0] = x <= LIM - y; cand[0] = x + y;
                ok[1] = x > y; cand[1] = x - y;
                ok[2] = (i128)x * y <= LIM; cand[2] = ok[2] ? x * y : 0;
                for (int k = 0; k < 3; k++) if (ok[k]) {
                    auto it = pos.find(cand[k]);
                    if (it != pos.end() && c < cost[it->second]) { cost[it->second] = c; rc[it->second] = {op[k], x, y}; ch = true; }
                }
            }
        }
        // build deduplicated chains
        function<void(ll, vector<pair<ll,Recipe>>&, unordered_set<ll>&)> chain = [&](ll v, vector<pair<ll,Recipe>>& out, unordered_set<ll>& have) {
            if (L.count(v) || have.count(v)) return;
            int i = pos[v];
            chain(rc[i].x, out, have); chain(rc[i].y, out, have);
            if (have.insert(v).second) out.push_back({v, rc[i]});
        };
        for (int i = 0; i < n; i++) {
            if (cost[i] == 0 || cost[i] > 64) continue;
            VLeaf v{S[i], {}}; unordered_set<ll> have;
            chain(S[i], v.chain, have);
            if ((int)v.chain.size() <= VC) vleaves.push_back(move(v));
        }
    }
    void buildDict(Dict& d) {
        vector<ll> leaves;
        for (int i = 0; i < R; i++) if (reg[i]) leaves.push_back(reg[i]);
        makeVirtual(leaves);
        d.build(leaves, true, &vleaves);
    }
    unique_ptr<Search> searchT(ll t, Dict& d) {
        int ob = BEAM, od = DEPTH;
        unique_ptr<Search> sp(new Search(d));
        sp->run(t);
        while (sp->bt.node < 0 && DEPTH < 80) {  // widen until found
            BEAM *= 2; DEPTH *= 2;
            sp.reset(new Search(d)); sp->run(t);
        }
        BEAM = ob; DEPTH = od;
        return sp;
    }
    vector<pair<ll,Recipe>> makePlan(ll t, Search& s, Dict& d) {
        vector<pair<ll,Recipe>> plan; unordered_set<ll> have;
        for (int i = 0; i < R; i++) if (reg[i]) have.insert(reg[i]);
        ll v;
        Term& T = s.bt;
        if (T.t2 < 0) { collect(d, T.t1, plan, have); v = d.e[T.t1].v; }
        else if (T.op == 'A' || T.op == 'B') {
            collect(d, T.t1, plan, have); collect(d, T.t2, plan, have); collect(d, T.t3, plan, have);
            ll x = d.e[T.t1].v, y = d.e[T.t2].v, c = d.e[T.t3].v, m = x * y;
            addv(m, {'*', x, y}, plan, have);
            v = T.op == 'A' ? m + c : m - c;
            addv(v, {T.op == 'A' ? '+' : '-', m, c}, plan, have);
        }
        else {
            collect(d, T.t1, plan, have); collect(d, T.t2, plan, have);
            ll x = d.e[T.t1].v, y = d.e[T.t2].v; v = apply(T.op, x, y);
            addv(v, {T.op, x, y}, plan, have);
        }
        for (int p = T.node; s.hist[p].parent >= 0; p = s.hist[p].parent) {
            Link l = s.hist[p].l;
            if (l.f2 >= 0) {
                collect(d, l.f, plan, have); collect(d, l.f2, plan, have);
                bool sum = l.op == 'S' || l.op == 'T', up = l.op == 'P' || l.op == 'S';
                ll x = d.e[l.f].v, y = d.e[l.f2].v, m = sum ? x + y : x * y;
                addv(m, {sum ? '+' : '*', x, y}, plan, have);
                ll nv = up ? v + m : m - v;
                addv(nv, {up ? '+' : '-', up ? v : m, up ? m : v}, plan, have);
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
        return plan;
    }
    int solveTarget(ll t, Dict& d) {
        buildDict(d);
        auto sp = searchT(t, d);
        if (sp->bt.node < 0) return -1;
        auto plan = makePlan(t, *sp, d);
        emit(plan);
        if (DEBUG) fprintf(stderr, "%lld cost %d\n", t, (int)plan.size());
        return plan.size();
    }
    bool bootstrap(Dict& d) {
        for (ll c = 1; c <= 64; c++) {
            if (find(c) >= 0) continue;
            int id = d.ix.get(c);
            if (id < 0) continue;
            vector<pair<ll,Recipe>> plan; unordered_set<ll> have;
            for (int i = 0; i < R; i++) if (reg[i]) have.insert(reg[i]);
            collect(d, id, plan, have); emit(plan); return true;
        }
        return false;
    }
    // Seed registers with a power-of-two ladder (and small odd constants for PALETTE>=2).
    void op1(char op, ll x, ll y) {
        ll v = apply(op, x, y);
        if (v <= 0 || v > LIM || find(v) >= 0) return;
        vector<pair<ll,Recipe>> plan{{v, {op, x, y}}};
        emit(plan); keep.insert(v);
    }
    void seedPalette() {
        ll s0 = starts[0];
        if (find(1) < 0) op1('/', s0, s0);
        keep.insert(1);
        op1('+', 1, 1);
        ll p = 2;
        for (int k = 0; k < 5; k++) { if ((i128)p * p > LIM) break; op1('*', p, p); p = p * p; }  // 4,16,256,65536,2^32
        if (PALETTE >= 2) {
            op1('+', 2, 1);  // 3
            op1('+', 4, 1);  // 5
            if (LIM >= 16) op1('-', 16, 1);  // 15
            if (LIM >= 17) op1('+', 16, 1);  // 17
        }
    }
    // Greedy: each step search all remaining targets on one dictionary, emit the cheapest.
    void runGreedy(Dict& d) {
        uniform_real_distribution<double> U(0, 1);
        int guard = 0;
        while (!need.empty()) {
            for (auto it = need.begin(); it != need.end();) { if (find(*it) >= 0) it = need.erase(it); else ++it; }
            if (need.empty()) break;
            buildDict(d);
            vector<tuple<double,ll,int>> cand;
            for (ll t : need) {
                auto sp = searchT(t, d);
                if (sp->bt.node < 0) continue;
                // noise for restarts: perturb cost slightly
                double key = sp->best + (NOISE > 0 ? NOISE * U(rng) : 0) + 1e-9 * (TIEBIG ? -(double)t : (double)t);
                cand.push_back({key, t, sp->best});
            }
            if (cand.empty()) { if (!bootstrap(d) || ++guard > 64) { fprintf(stderr, "stuck\n"); exit(1); } continue; }
            sort(cand.begin(), cand.end());
            ll t = get<1>(cand[0]);
            auto sp = searchT(t, d);
            auto plan = makePlan(t, *sp, d);
            emit(plan);
        }
    }
    void run() {
        for (size_t i = 0; i < starts.size(); i++) { reg[i] = starts[i]; last[i] = 0; }
        for (ll t : targets) { need.insert(t); keep.insert(t); }
        for (ll s0 : starts) keep.insert(s0);
        for (ll s : starts) need.erase(s);
        for (auto& in : pre) {  // replay a given prefix program
            ll v = apply(in.op, reg[in.a], reg[in.b]);
            reg[in.d] = v; last[in.a] = last[in.b] = ++clock; last[in.d] = ++clock;
            prog.push_back(in); need.erase(v); histv.push_back(v);
        }
        static Dict d;
        if (PALETTE) seedPalette();
        if (ORDER == 3) { runGreedy(d); return; }
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
        else if (k == "-o") ORDER = v; else if (k == "-x") APPROX = v; else if (k == "-s") SEED = v; else if (k == "-n") NOISE = v; else if (k == "-sx") SUMAPPROX = v; else if (k == "-k") KEEP = v; else if (k == "-t") TRI = v; else if (k == "-D") DEEP = v; else if (k == "-p") PALETTE = v; else if (k == "-tb") TIEBIG = v; else if (k == "-V") VC = v; else if (k == "-vs") VSET = v; else if (k == "-P") PREFIX = v; else if (k == "-H") HV = v; else if (k == "-ks") KSMALL = (ll)v; else if (k == "-uw") UCW = (long)v;
    }
    string id; ll limit; int ns, nt;
    while (cin >> id >> limit >> ns >> nt) {
        LIM = limit;
        Solver S(SEED);
        S.starts.resize(ns); S.targets.resize(nt);
        for (auto& x : S.starts) cin >> x;
        for (auto& x : S.targets) cin >> x;
        if (PREFIX) {
            int np; cin >> np; S.pre.resize(np);
            for (auto& in : S.pre) { string op; cin >> op >> in.a >> in.b >> in.d; in.op = op[0]; }
        }
        S.run();
        printf("%s [", id.c_str());
        for (size_t k = 0; k < S.prog.size(); k++) {
            auto& in = S.prog[k];
            printf("%s[\"%c\",%d,%d,%d]", k ? "," : "", in.op, in.a, in.b, in.d);
        }
        printf("]\n"); fflush(stdout);
    }
}

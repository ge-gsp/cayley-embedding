"""Independent recomputation of the completion census, n=2..7.
gamma+ : addition-only cost / m .  gamma_tri : edit cost / m .
Host must be connected (Convention 2.3)."""
import networkx as nx, itertools, numpy as np
from networkx.generators.atlas import graph_atlas_g

def groups(n):
    """abelian groups of order n as tuples of cyclic factors"""
    def parts(k):
        if k==1: yield (); return
        for d in range(2,k+1):
            if k%d==0:
                for r in parts(k//d):
                    if not r or d<=r[0]: yield (d,)+r
    return list(parts(n))

def elems(G): return list(itertools.product(*[range(o) for o in G]))
def add(G,a,b): return tuple((x+y)%o for x,y,o in zip(a,b,G))
def neg(G,a): return tuple((-x)%o for x,o in zip(a,G))

def classes_of(G):
    """pair up d with -d; return list of (frozenset_class, n_edges_if_included)"""
    els=elems(G); N=len(els); e0=tuple(0 for _ in G)
    seen=set(); out=[]
    for d in els:
        if d==e0 or d in seen: continue
        nd=neg(G,d); seen|={d,nd}
        out.append((frozenset({d,nd}), N//2 if d==nd else N))
    return out

def gammas(Gr):
    n=Gr.number_of_nodes(); m=Gr.number_of_edges()
    if m==0: return None
    V=sorted(Gr.nodes()); best_p=None; best_t=None
    for Gg in groups(n):
        els=elems(Gg); e0=els[0]
        cls=classes_of(Gg); K=len(cls)
        idx={}
        for i,(c,_) in enumerate(cls):
            for d in c: idx[d]=i
        sizes=[s for _,s in cls]
        gens=[next(iter(c)) for c,_ in cls]
        # which subsets of classes generate Gg (connected host)?
        conn=[False]*(1<<K)
        for mask in range(1,1<<K):
            S=set()
            for i in range(K):
                if mask>>i & 1: S|=set(cls[i][0])
            H=nx.Graph(); H.add_nodes_from(els)
            for x in els:
                for s in S: H.add_edge(x,add(Gg,x,s))
            H.remove_edges_from(nx.selfloop_edges(H))
            conn[mask]=nx.is_connected(H)
        rest=V[1:]
        for perm in itertools.permutations(els[1:],n-1):
            lam=dict(zip(rest,perm)); lam[V[0]]=e0
            c=[0]*K
            for u,v in Gr.edges():
                d=add(Gg,lam[u],neg(Gg,lam[v])); c[idx[d]]+=1
            # gamma+ : must include every class that carries an edge
            need=0
            for i in range(K):
                if c[i]: need |= 1<<i
            for mask in range(need,1<<K):
                if mask & need != need or not conn[mask]: continue
                cost=sum(sizes[i] for i in range(K) if mask>>i&1)-m
                if best_p is None or cost<best_p: best_p=cost
            # gamma_tri : any subset, pay symmetric difference
            for mask in range(1,1<<K):
                if not conn[mask]: continue
                cost=sum((sizes[i]-c[i]) if mask>>i&1 else c[i] for i in range(K))
                if best_t is None or cost<best_t: best_t=cost
    return best_p/m, best_t/m

if __name__=='__main__':
    import sys, json, time
    rows=[]; t0=time.time()
    for G in graph_atlas_g():
        n=G.number_of_nodes()
        if n<2 or n>7 or not nx.is_connected(G): continue
        r=gammas(G)
        if r is None: continue
        gp,gt=r
        Gc=nx.convert_node_labels_to_integers(G)
        D=max(d for _,d in Gc.degree()); m=Gc.number_of_edges()
        nD=n*D
        Dstar=D if nD%2==0 else D+1
        bound_plain=max(0,n*D/(2*m)-1)
        bound_star=max(0,n*Dstar/(2*m)-1)
        rows.append(dict(n=n,m=m,gp=gp,gt=gt,bp=bound_plain,bs=bound_star))
    json.dump(rows,open('census_rows.json','w'))
    print(f"{len(rows)} graphs, {time.time()-t0:.1f}s")

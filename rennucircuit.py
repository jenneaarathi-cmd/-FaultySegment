import sys

def build_graph(matrix, N):
    node_id = {}
    id_node = {}
    idx = 0

    # assign IDs to every cell
    for i in range(N):
        for j in range(N):
            node_id[(i, j)] = idx
            id_node[idx] = (i, j)
            idx += 1

    edges = []
    terminals = []
    for i in range(N):
        for j in range(N):
            c = matrix[i][j]
            u = node_id[(i, j)]
            if c == '.':
                terminals.append(u)
            if c in "-+" and j + 1 < N:
                if matrix[i][j+1] in "-+.":
                    v = node_id[(i, j+1)]
                    edges.append((u, v, 1))
            if c in "|+" and i + 1 < N:
                if matrix[i+1][j] in "|+.":
                    v = node_id[(i+1, j)]
                    edges.append((u, v, 1))
    return edges, terminals, node_id

def gaussian_elimination(a, b):
    """ Solve Ax = b using Gaussian elimination (no numpy). """
    n = len(b)
    for i in range(n):
        # pivot
        max_row = max(range(i, n), key=lambda r: abs(a[r][i]))
        if abs(a[max_row][i]) < 1e-12:
            continue
        if max_row != i:
            a[i], a[max_row] = a[max_row], a[i]
            b[i], b[max_row] = b[max_row], b[i]
        # normalize
        div = a[i][i]
        for j in range(i, n):
            a[i][j] /= div
        b[i] /= div
        # eliminate
        for r in range(n):
            if r != i:
                factor = a[r][i]
                for j in range(i, n):
                    a[r][j] -= factor * a[i][j]
                b[r] -= factor * b[i]
    return b

def equivalent_resistance(edges, n, s, t):
    # Build Laplacian
    L = [[0.0]*n for _ in range(n)]
    for u, v, r in edges:
        g = 1.0/r
        L[u][u] += g
        L[v][v] += g
        L[u][v] -= g
        L[v][u] -= g

    # Build system: remove one reference node (say last one)
    ref = t
    unknowns = [i for i in range(n) if i != ref]
    m = len(unknowns)

    A = [[0.0]*m for _ in range(m)]
    b = [0.0]*m

    for ii, i in enumerate(unknowns):
        for jj, j in enumerate(unknowns):
            A[ii][jj] = L[i][j]
        if i == s:
            b[ii] = 1.0
        elif i == t:
            b[ii] = -1.0

    x = gaussian_elimination(A, b)

    # voltage difference = V[s] - V[t], with I=1
    Vs = 0
    for ii, i in enumerate(unknowns):
        if i == s:
            Vs = x[ii]
    Vt = 0  # reference node
    return round(Vs - Vt)

# ---------------- MAIN ----------------
data = sys.stdin.read().strip().splitlines()
if not data:
    sys.exit(0)

N = int(data[0])
matrix = data[1:]

edges, terminals, node_id = build_graph(matrix, N)

if len(terminals) != 2:
    print(0)
    sys.exit(0)

s, t = terminals
res = equivalent_resistance(edges, N*N, s, t)
print(res)

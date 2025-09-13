import sys
sys.setrecursionlimit(10000)

# Read input
lines = [line.strip() for line in sys.stdin.read().splitlines() if line.strip()]
M, N = map(int, lines[0].split())

grid = []
for i in range(1, 1 + M):
    row = lines[i].split()  # input is space-separated
    grid.append(row)

# Directions: 0=up, 1=right, 2=down, 3=left
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

# Reflection rules
next_dir = {
    '/': {0: 1, 1: 0, 2: 3, 3: 2},
    '\\': {0: 3, 3: 0, 2: 1, 1: 2}
}

def inside(r, c):
    return 0 <= r < M and 0 <= c < N

max_loop = 0
visited_global = set()

for r0 in range(M):
    for c0 in range(N):
        for d0 in range(4):
            if (r0, c0, d0) in visited_global:
                continue
            path = {}
            r, c, d = r0, c0, d0
            step = 0
            while inside(r, c):
                state = (r, c, d)
                if state in path:
                    # cycle found → length = total steps - index of first occurrence
                    cycle_len = step - path[state]
                    max_loop = max(max_loop, cycle_len)
                    break
                if state in visited_global:
                    break
                path[state] = step
                visited_global.add(state)
                step += 1
                cell = grid[r][c]
                if cell in next_dir:
                    d = next_dir[cell][d]
                r += dr[d]
                c += dc[d]

# Print result without extra newline
print(max_loop, end="")

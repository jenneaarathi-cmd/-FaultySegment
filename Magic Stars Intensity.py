import sys
from collections import defaultdict
from itertools import combinations

def on_segment(x1, y1, x2, y2, x, y):
    """Check if point (x, y) lies on line segment (x1, y1)-(x2, y2)"""
    return min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)

def line_intersection(l1, l2):
    """Find intersection point of two line segments if exists"""
    x1, y1, x2, y2 = l1
    x3, y3, x4, y4 = l2

    denom = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
    if denom == 0:
        return None  # parallel or coincident

    px = ((x1*y2 - y1*x2)*(x3-x4) - (x1-x2)*(x3*y4 - y3*x4)) / denom
    py = ((x1*y2 - y1*x2)*(y3-y4) - (y1-y2)*(x3*y4 - y3*x4)) / denom

    if on_segment(x1,y1,x2,y2,px,py) and on_segment(x3,y3,x4,y4,px,py):
        return (round(px,6), round(py,6))
    return None

def cells_touched(x1, y1, x2, y2, px, py):
    """
    Count number of unit cells a line touches 
    from intersection (px,py) to endpoint.
    """
    dx = 1 if x2 > px else -1 if x2 < px else 0
    dy = 1 if y2 > py else -1 if y2 < py else 0

    cx, cy = px, py
    steps = 0
    while (round(cx,6), round(cy,6)) != (x2, y2):
        if dx != 0:
            cx += dx
        if dy != 0:
            cy += dy
        steps += 1
        if steps > 200:  # safeguard
            break
    return steps if steps>0 else 1

def star_intensity(lines, star_point, star_lines):
    px, py = star_point
    counts = []
    for line in star_lines:
        x1,y1,x2,y2 = line
        # check case: star cuts line in 2 parts or lies on endpoint
        if (px,py)==(x1,y1) or (px,py)==(x2,y2):
            # Case 1: star at endpoint
            counts.append(cells_touched(x1,y1,x2,y2,px,py))
        else:
            # Case 2: star inside line, count both directions
            counts.append(cells_touched(x1,y1,x2,y2,px,py))
            counts.append(cells_touched(x2,y2,x1,y1,px,py))
    return min(counts) if counts else 0

# ---------------- MAIN ----------------
data = sys.stdin.read().strip().split()
if not data: sys.exit(0)

N = int(data[0])
lines = []
idx=1
for i in range(N):
    x1,y1,x2,y2 = map(int, data[idx:idx+4]); idx+=4
    lines.append((x1,y1,x2,y2))
K = int(data[idx])

# Find all intersection points
star_points = defaultdict(list)
for (i,j) in combinations(range(N),2):
    p = line_intersection(lines[i], lines[j])
    if p:
        star_points[p].append(lines[i])
        star_points[p].append(lines[j])

# Count intensity for required K-stars
total_intensity=0
for point, involved in star_points.items():
    uniq_lines = list({tuple(l) for l in involved})
    if len(uniq_lines)==K:
        intensity = star_intensity(lines, point, uniq_lines)
        total_intensity += intensity

print(total_intensity)

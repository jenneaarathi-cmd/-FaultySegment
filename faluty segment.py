import sys

# 7-segment dictionary: symbol -> 3x3 representation
SEGMENTS = {
    "0": [" _ ",
          "| |",
          "|_|"],
    "1": ["   ",
          "  |",
          "  |"],
    "2": [" _ ",
          " _|",
          "|_ "],
    "3": [" _ ",
          " _|",
          " _|"],
    "4": ["   ",
          "|_|",
          "  |"],
    "5": [" _ ",
          "|_ ",
          " _|"],
    "6": [" _ ",
          "|_ ",
          "|_|"],
    "7": [" _ ",
          "  |",
          "  |"],
    "8": [" _ ",
          "|_|",
          "|_|"],
    "9": [" _ ",
          "|_|",
          " _|"],
    "+": ["   ",
          " | ",
          " | "],
    "-": ["   ",
          " _ ",
          "   "],
    "*": ["   ",
          " * ",
          "   "],   # Simplified placeholder
    "%": ["   ",
          "%  ",
          "  %"],
    "=": ["   ",
          " _ ",
          " _ "]
}

# Reverse lookup dictionary
PATTERN_TO_CHAR = {"\n".join(v): k for k, v in SEGMENTS.items()}

# Function to decode a 3x3 block into symbol
def decode_block(block):
    return PATTERN_TO_CHAR.get("\n".join(block), "?")

# Evaluate expression left to right
def eval_expr(tokens):
    total = int(tokens[0])
    i = 1
    while i < len(tokens) and tokens[i] != "=":
        op = tokens[i]
        val = int(tokens[i+1])
        if op == "+": total += val
        elif op == "-": total -= val
        elif op == "*": total *= val
        elif op == "%": total %= val
        i += 2
    rhs = int(tokens[i+1]) if i+1 < len(tokens) else None
    return total, rhs

# ---------------- MAIN ----------------
lines = [line.rstrip("\n") for line in sys.stdin.read().splitlines()]
N = int(lines[0])
grid = lines[1:4]

# Extract characters
chars = []
for k in range(N):
    block = [row[k*3:(k+1)*3] for row in grid]
    chars.append(block)

# Decode all chars
decoded = [decode_block(block) for block in chars]

# Check correctness
lhs, rhs = eval_expr(decoded)
if lhs == rhs:
    print(-1)   # already correct
    sys.exit(0)

# Try toggling one LED
for idx, block in enumerate(chars):
    for r in range(3):
        for c in range(3):
            orig = block[r][c]
            # toggle between " " and segment chars
            for toggle in [" ", "_", "|"]:
                if toggle == orig:
                    continue
                new_block = [list(row) for row in block]
                new_block[r][c] = toggle
                new_block = ["".join(row) for row in new_block]
                sym = decode_block(new_block)
                if sym != "?":
                    trial = decoded[:]
                    trial[idx] = sym
                    lhs, rhs = eval_expr(trial)
                    if lhs == rhs:
                        print(idx+1, end="")
                        sys.exit(0)

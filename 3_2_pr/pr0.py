# from pprint import pprint

f = open("input.txt", "r")
n = int(f.readline())
tree = {}
tree2 = {}
for _ in range(n-1):
    # name, parent_name = input().split()
    name, parent_name = f.readline().split()
    tree[name] = parent_name

for i in tree:
    depth = 1
    cur_name = i
    while True:
        parent_name = tree[cur_name]
        if parent_name not in tree:
            tree2[parent_name] = 0
            break
        depth += 1
        cur_name = parent_name
    tree2[i] = depth

for i in sorted(tree2):
    print(i, tree2[i])

# DZ: O(n2) -> O(n)
f.close()

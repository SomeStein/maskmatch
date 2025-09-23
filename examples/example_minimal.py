from maskmatch.core import groups_by_duplicates, precombine_groups, solve_disjoint

print("\nImports successful!")

lists = [
    [0b1100_0000, 0b0110_0000, 0b0011_0000],
    [0b0000_1000, 0b0000_0100, 0b0000_0010, 0b0000_0001],
    [0b0000_1000, 0b0000_0100, 0b0000_0010, 0b0000_0001],
]

n = 8

print("\nlists: ")
for l in lists:
    print([format(i, f"0{n}b") for i in l])

groups = groups_by_duplicates(lists)

print("\ngroups: ")
for _, group in enumerate(groups):
    print(f"   group{_} of multiplicity: {group[1]}")
    print("   ", [format(i, f"0{n}b") for i in group[0]], "\n")

precombined = precombine_groups(groups)

print("precombined masks: ")
for masks, mult in precombined:
    print([format(i, f"0{n}b") for i in masks])

result = solve_disjoint(precombined)

print("\ndisjoint masks: ")
print([format(i, f"0{n}b") for i in result])
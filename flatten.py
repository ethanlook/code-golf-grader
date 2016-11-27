def flatten(l, acc):
    if not l:
        return acc
    if len(l) == 1:
        if not isinstance(l, list):
            acc.append(l)
            return acc
    if isinstance(l[0], list):
        acc.extend(flatten(l[0], []))
    else:
        acc.append(l[0])
    return flatten(l[1:], acc)

print flatten([1, [1, 2]], [])

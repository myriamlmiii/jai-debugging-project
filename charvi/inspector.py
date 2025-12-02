# inspector.py

# DFS object inspector for debugging.
# Handles circular references + depth limiting.

def _is_basic(x):
    return isinstance(x, (int, float, str, bool, bytes, type(None)))

def inspect_dfs(obj, visited=None, max_depth=5, depth=0):
    if visited is None:
        visited = set()

    oid = id(obj)

    # circular reference check
    if oid in visited:
        return "<circular>"

    # avoid going too deep
    if depth > max_depth:
        return "<max_depth_reached>"

    # primitives: just return
    if _is_basic(obj):
        return obj

    visited.add(oid)

    # dict case
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            out[str(k)] = inspect_dfs(v, visited, max_depth, depth + 1)
        return {"type": "dict", "id": oid, "items": out}

    # list/tuple/set case
    if isinstance(obj, (list, tuple, set)):
        lst = []
        for item in obj:
            lst.append(inspect_dfs(item, visited, max_depth, depth + 1))
        return {"type": type(obj).__name__, "id": oid, "items": lst}

    # generic object: inspect non-private attributes
    attrs = {}
    for name in dir(obj):
        if name.startswith("_"):
            continue
        try:
            val = getattr(obj, name)
        except:
            continue

        if callable(val):
            continue

        attrs[name] = inspect_dfs(val, visited, max_depth, depth + 1)

    return {"type": type(obj).__name__, "id": oid, "attrs": attrs}

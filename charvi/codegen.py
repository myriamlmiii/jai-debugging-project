# codegen.py

# Simple template engine + memoized wrapper

_template_cache = {}

def expand_template(template, params):
    """
    Replace {{var}} in template using params dict.
    Complexity: O(n) in length of template.
    """
    i = 0
    res = []
    n = len(template)

    while i < n:
        # find {{
        if i + 1 < n and template[i] == "{" and template[i + 1] == "{":
            end = template.find("}}", i + 2)
            if end == -1:
                # malformed, just treat "{" as normal char
                res.append(template[i])
                i += 1
                continue

            var = template[i + 2:end].strip()
            res.append(str(params.get(var, "")))
            i = end + 2
        else:
            res.append(template[i])
            i += 1

    return "".join(res)


def generate_code(template, params):
    """
    Memoized code generator.
    First call for a given (template, params) is O(n).
    Repeated calls with same (template, params) are O(1) cache lookups.
    """
    key = (template, tuple(sorted(params.items())))

    if key in _template_cache:
        return _template_cache[key]

    out = expand_template(template, params)
    _template_cache[key] = out
    return out


def clear_cache():
    _template_cache.clear()

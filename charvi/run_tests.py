# run_tests.py

from registry import FastRegistry, SlowRegistry
from inspector import inspect_dfs
from codegen import expand_template, generate_code, clear_cache


def test_fast_registry():
    class A:
        x: int
        y: str

    reg = FastRegistry()
    reg.register_type(A)
    info = reg.get_type_info(A)

    assert info is not None
    assert info.name == "A"
    assert "x" in info.fields
    assert "y" in info.fields


def test_slow_registry():
    class B:
        z: float

    reg = SlowRegistry()
    reg.register_type(B)
    info = reg.get_type_info(B)

    assert info is not None
    assert info.name == "B"


def test_inspector_basic():
    out = inspect_dfs(10)
    assert out == 10


def test_inspector_circular():
    a = {}
    b = {"link": a}
    a["back"] = b   # circular

    out = inspect_dfs(a, max_depth=10)
    assert isinstance(out, dict)  # mostly just checking it doesn't crash


def test_template():
    t = "Hello {{name}}, score {{score}}"
    params = {"name": "Charvi", "score": 99}
    out = expand_template(t, params)

    assert "Charvi" in out
    assert "99" in out
    assert "{{" not in out  # no placeholders left


def test_memo():
    clear_cache()
    t = "Hi {{x}}"
    p = {"x": "A"}
    first = generate_code(t, p)
    second = generate_code(t, p)
    assert first == second   # second call should hit cache


if __name__ == "__main__":
    # run all tests manually
    test_fast_registry()
    test_slow_registry()
    test_inspector_basic()
    test_inspector_circular()
    test_template()
    test_memo()
    print("All tests passed.")




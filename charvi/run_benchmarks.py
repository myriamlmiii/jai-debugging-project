# run_benchmarks.py

import time
from registry import FastRegistry, SlowRegistry
from codegen import expand_template, generate_code, clear_cache


def benchmark_registry():
    print("\n=== FastRegistry (dict) vs SlowRegistry (list) ===")
    print("n, fast_lookup_time, slow_lookup_time")

    sizes = [10, 100, 1000, 5000]

    for n in sizes:
        # create n dummy classes
        classes = [type(f"C{i}", (), {}) for i in range(n)]

        fast = FastRegistry()
        slow = SlowRegistry()

        for c in classes:
            fast.register_type(c)
            slow.register_type(c)

        target = classes[-1]

        # measure fast lookup
        start = time.perf_counter()
        fast.get_type_info(target)
        fast_time = time.perf_counter() - start

        # measure slow lookup
        start = time.perf_counter()
        slow.get_type_info(target)
        slow_time = time.perf_counter() - start

        print(f"{n}, {fast_time:.8f}, {slow_time:.8f}")


def benchmark_codegen():
    print("\n=== Memoized vs Non-memoized Code Generation ===")

    template = "Hello {{name}}, score: {{score}}.\n" * 200
    params = {"name": "User", "score": 123}
    iterations = 800

    # non-memoized: call expand_template directly
    start = time.perf_counter()
    for _ in range(iterations):
        expand_template(template, params)
    t_no_memo = time.perf_counter() - start

    # memoized: clear cache and call generate_code repeatedly
    clear_cache()
    start = time.perf_counter()
    for _ in range(iterations):
        generate_code(template, params)
    t_memo = time.perf_counter() - start

    print(f"Non-memoized: {t_no_memo:.5f} s")
    print(f"Memoized:     {t_memo:.5f} s")


if __name__ == "__main__":
    benchmark_registry()
    benchmark_codegen()

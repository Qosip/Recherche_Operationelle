import time

def measure_time(func, *args, n_values, repetitions=5):
    times = {}

    for n in n_values:
        total_time = 0
        for _ in range(repetitions):
            start_time = time.perf_counter()
            for _ in range(n):
                func(*args)
            end_time = time.perf_counter()
            total_time += (end_time - start_time)
        avg_time_per_operation = total_time / (n * repetitions) if n > 0 else float('inf')
        times[n] = avg_time_per_operation

    return times

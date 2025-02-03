import time


def measure_execution_time(algorithm, graph):
    start_time = time.time_ns()
    result = algorithm.execute(graph)
    end_time = time.time_ns()
    execution_time = end_time - start_time
    return result, execution_time

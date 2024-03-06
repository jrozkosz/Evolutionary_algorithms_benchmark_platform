try:
    from algorithm import evolutionary_algorithm
except Exception as e:
    print('Module does not exist.')

fun_exec_count = 0

call_count = 0  # Global variable to store the call count

def count_calls(func):
    def wrapper(*args, **kwargs):
        global call_count
        print(f"Function {func.__name__} has been called {call_count} times.")
        call_count += 1
        if call_count > 5:
            raise Exception('Budget exhausted - limit of objective function calls reached.')
        return func(*args, **kwargs)
    return wrapper

@count_calls
def objective_function(x):
    # global fun_exec_count
    # print(fun_exec_count)
    # fun_exec_count += 1
    # if fun_exec_count > 5:
    #     raise Exception('Budget exhausted - limit of objective function calls reached.')
    return x**2

def ranking_calc():
    evolutionary_algorithm(objective_function)

try:
    ranking_calc()
except Exception as e:
    print(e.args[0])

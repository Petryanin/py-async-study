def coroutine(func):
    def wrapper(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return wrapper


class MyExcept(Exception):
    pass


def subgen():
    while True:
        try:
            message = yield
        except StopIteration:
            print('Exception caught!')
            break
        else:
            print('Subgen received:', message)

    return 'RESULT'


@coroutine
def delegator(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except MyExcept as e:
    #         g.throw(e)
    result = yield from g  # AWAIT
    print('Result from subgen has been received:', result)


@coroutine
def average():
    count = 0
    summ = 0
    average = None

    while True:
        try:
            x = yield average
        except StopIteration:
            print('Done!')
            break
        else:
            count += 1
            summ += x
            average = round(summ / count, 2)
    return average

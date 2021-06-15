def gen1(s):
    for i in s:
        yield i


def gen2(n):
    for i in range(n):
        yield i


g1 = gen1('petryanin')
g2 = gen2(8)

tasks = [g1, g2]

while tasks:
    task = tasks.pop(0)

    try:
        print(next(task))
        tasks.append(task)
    except StopIteration:
        pass

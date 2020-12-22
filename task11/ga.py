from random import randint

RESULT = 100
NUM_POP = 20
CHANCE_MUTATION = 0.5
max_random_num = {
    1: (-25, 25),
    2: (-20, 20),
    3: (-11, 11),
    4: (-50, 50),
    5: (-12, 12),
    6: (-10, 10),
}


def calc(x1, x2, x3, x4, x5, x6):
    return (
        4 * x1 + 5 * x2 + 9 * x3 + 2 * x4 + 8 * x5 + 10 * x6
    )


def mutation(pops):
    new_pops = []
    for i in range(len(pops)):
        r = randint(0, 100)
        if r < 100 * CHANCE_MUTATION:
            index = int(r // 100 * NUM_POP)
            random_index = randint(1, 6)
            pops[i][index] = randint(
                *max_random_num[random_index])
        new_pops.append(pops[i])
    return new_pops


def reverse_results(results):
    results = [1 / abs(RESULT - result) for result in results]
    sum_result = sum(results)
    return [
        result / sum_result for result in results
    ]


def calc_all_pops(pops):
    results = []
    for pop in pops:
        result = calc(*pop)
        results.append(result)
    return results


def get_result(pops):
    for pop in pops:
        if calc(*pop) == RESULT:
            return pop
    return False


def get_next_pop(pops):
    results = calc_all_pops(pops)
    coef = reverse_results(results)
    fitnes = sum(coef)
    results = dict(zip(range(0, len(pops)), coef))
    results = [
        k for k, _ in sorted(results.items(),
                             key=lambda item: item[1], reverse=True)
    ]
    new_pops = []
    for i in range(len(pops) // 2):
        new_pops.extend(select(
            pops[results[2 * i]],
            pops[results[2 * i + 1]]
        ))
    if get_result(new_pops):
        return new_pops
    new_fitnes = sum(reverse_results(calc_all_pops(new_pops)))
    if fitnes > new_fitnes:
        print('Мутация')
        pops = mutation(pops)
    else:
        print('Селекция')
        pops = new_pops
    return pops


def select(pop1, pop2):
    random_slice = randint(1, len(pop1) - 2)
    return (
        pop1[:random_slice] + pop2[random_slice:],
        pop2[:random_slice] + pop1[random_slice:]
    )


def get_best_result(results):
    best_result = None
    for result in results:
        if (best_result is None or
                abs(best_result - RESULT) > abs(result - RESULT)):
            best_result = result
    return best_result


def main():
    # Уравнение 4x1 + 5x2 + 9x3 + 2x4 + 8x5 + 10x6 = 100
    pops = []

    # Первая популяция
    for i in range(NUM_POP):
        xs = []
        for j in range(len(max_random_num)):
            xs.append(
                randint(*max_random_num[j + 1])
            )
        pops.append(
            xs
        )

    index = 1
    while not get_result(pops):
        print(f'Популяция №{index}')
        pops = get_next_pop(pops)
        results = calc_all_pops(pops)
        best_result = get_best_result(results)
        print(f'Лучший результат популяции: {best_result}')
        index += 1

    print(f'Лучший представитель {get_result(pops)}')


if __name__ == '__main__':
    main()

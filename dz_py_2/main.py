from typing import Set


# matr = [[1, 0], [0, 0]]
# matr = [[1, 0], [1, 1]]
# matr = [[1, 0], [0, 1]]
# matr = [[1, 1, 1, 1, 1], [0, 0, 0, 0, 0], [0, 0, 1, 1, 0], [1, 0, 1, 1, 0]]
# matr = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
# matr = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]


def check_around_elements(mtrx: list, i_j_of_elements: set) -> set:
    """Проверяет у элементов mtrx[i][j] наличие соседей = 1, где (i,j) пары индексов из i_j_of_elements."""

    def check_element_and_add(i: int, j: int) -> None:
        if mtrx[i][j] == 1 and (i, j) not in i_j_of_elements:
            elements_for_check.add((i, j))

    elements_for_check: Set[tuple] = set([])
    i_n = len(mtrx) - 1
    j_n = len(mtrx[1]) - 1
    for z in i_j_of_elements:
        i, j = z[0], z[1]
        if j > 0:
            check_element_and_add(i, j - 1)
        if j < j_n:
            check_element_and_add(i, j + 1)
        if i > 0:
            check_element_and_add(i - 1, j)
            """if j < j_n:
                check_element_and_add(i - 1, j + 1)
            if j > 0:
                check_element_and_add(i - 1, j - 1) # в случае, если соприкосновения по углам тоже считать"""
        if i < i_n:
            check_element_and_add(i + 1, j)
            """if j < j_n:
                check_element_and_add(i + 1, j + 1)
            if j > 0:
                check_element_and_add(i + 1, j - 1) # в случае, если соприкосновения по углам тоже считать"""
        mtrx[i][j] = 0
    return elements_for_check


def calculate(mtrx: list) -> int:
    """Вычисляет количество пятен из 1 в матрице на фоне из 0."""
    i_n = len(mtrx)
    j_n = len(mtrx[1])
    count_rang = 0
    for i in range(0, i_n):
        for j in range(0, j_n):
            if mtrx[i][j] == 1:
                count_rang += 1
                elements_for_check = set()
                elements_for_check.add((i, j))
                while len(elements_for_check) > 0:
                    elements_for_check = check_around_elements(mtrx, elements_for_check)
    return count_rang


if __name__ == "__main__":
    matr = []
    with open("moon.txt", "rt") as m_file:
        for line in m_file:
            matr.append(list(map(lambda x: int(x), list(line.strip()))))
    print(matr)
    print(calculate(matr))

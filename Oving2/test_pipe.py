def sort_list(A):
    # NOTICE: The sorted list must be returned.
    len_A = len(A)
    modulus = 10
    div = 1
    while True:
        new_list = [[] for i in range(len_A)]
        for value in A:
            least_digit = value % modulus
            least_digit //= div
         #   print("least_digit: ",least_digit,"//=","div: ",div)
            new_list[least_digit].append(value)
        modulus = modulus * 10
        div = div * 10

        if len(new_list[0]) == len_A:
           # print("FERDIG!")
            return new_list[0]

        A = []
        # print("Print2:",A)
        list_append = A.append
        for x in new_list:
            for y in x:
               # print("x:", x, "y:", y, "\n")
                list_append(y)
               # print("Print3:", A)


print(sort_list([13,9,8,7,6,5,4,3,2,1,10000000,9999999]))

def binary_search(A, t):
    lower = 0
    upper = len(A) - 1
    while lower < upper:  # use < instead of <=
        mid = lower + (upper - lower) // 2
        value = A[mid]
        if t == value:
            return mid
        elif t > value:
            if lower == mid:  # this two are the actual lines
                break  # you're looking for
            lower = mid
        elif t < value:
            upper = mid
    return mid

#print(binary_search([1,2,3,4,5,6,7,8,9],4))

def binsok(A, verdi):
    l = 0
    r = len(A) - 1
    while l <= r:
        m = (l + r) // 2
        if verdi == A[m]:
            break
        elif verdi < A[m]:
            r = m - 1
        else:
            l = m + 1

    return m

#print(binsok([1,2,3,4,5,6,7,8,9],4))
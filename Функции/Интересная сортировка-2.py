def sum_digits(num_str):
    k = 0
    for ch in num_str:
        k += int(ch)
    return k


def sort_key(num_str):
    return (sum_digits(num_str), int(num_str))


numbers = input().split()
sorted_numbers = sorted(numbers, key=sort_key)
print(*sorted_numbers)
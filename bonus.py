def salaryCalc(longevity, current):
    if longevity > 5:
        salary = current + (current * 0.05)
    else:
        salary = current
    return salary


def main():
    longevity = int(input("How many years have you worked here?"))
    current = int(input("What is your current salary?"))
    final = salaryCalc(longevity, current)
    print("salary is", int(round(final)))


main()
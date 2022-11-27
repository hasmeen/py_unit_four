# hihi

def absolute(number):
    absNum = abs(number)
    return absNum


def main():
    number = int(input("Enter a number please"))

    print("The absolute value of", number, "is", absolute(number))


if __name__ == '__main__':
    main()

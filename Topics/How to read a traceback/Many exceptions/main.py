import math

def find_sqrt(number):
    try:
        print(math.sqrt(number))
    except TypeError:
        if number.isdigit():
            print(math.sqrt(int(number)))
        else:
            print('Please pass a number like "5" or 5')

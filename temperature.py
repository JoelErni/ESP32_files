import random
import sys

def get_celcius(raw_data):
    return raw_data * -0.00208 + 88

if __name__ == "__main__":
    try:
        test_value = int(sys.argv[1])
        print(get_celcius(test_value))
    except Exception:
        print("no TestData")

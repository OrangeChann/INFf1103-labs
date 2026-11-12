"""Lab 9, section 5.1: ask again until the user gives a valid value.

float()/int() raise ValueError for text such as "abc" (exception handling),
and each helper also checks the value against its rule (validation). The
program never continues with a bad value; it keeps asking instead.
"""
import math


def get_positive_float(prompt: str) -> float:
    """The lab sheet's helper: keep asking until the value is a number > 0."""
    while True:
        try:
            value = float(input(prompt))
            # float() also accepts "nan" and "inf"; nan <= 0 is False, so
            # without this check "nan" would be returned as a valid price.
            if not math.isfinite(value):
                raise ValueError("not a finite number")
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_whole_number(prompt: str, minimum: int) -> int:
    """Keep asking until the value is a whole number of at least minimum."""
    while True:
        try:
            value = int(input(prompt))
            if value < minimum:
                print(f"Please enter a whole number of {minimum} or more.")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 5")


def get_non_negative_int(prompt: str) -> int:
    """For stock quantities: 0 or more."""
    return get_whole_number(prompt, 0)


def get_positive_int(prompt: str) -> int:
    """For order quantities and subscription months: 1 or more."""
    return get_whole_number(prompt, 1)

import decimal
from decimal import Decimal

import numpy


def get_number_suffix(number: str) -> str:
    if not number:
        raise ValueError("The number must have at least 1 digit.")
    int(number)  # The number must not have any commas, periods, etc.
    digit_count = len(number)
    if digit_count > 15:
        raise NotImplementedError
    if digit_count >= 13:
        return "T"
    if digit_count >= 10:
        return "B"
    if digit_count >= 7:
        return "M"
    if digit_count >= 4:
        return "k"
    return ""


def round_(number: str | float | numpy.float64) -> str:
    """Rounds a number and appends a suffix if the amount is large enough.

    Examples:
    379 -> 379
    182.5 -> 182.50
    1.445 -> 1.45
    2.675 -> 2.68
    1.995 -> 2
    1072 -> 1.07k
    10072 -> 10.07k
    7485275 -> 7.49M
    74852750 -> 74.85M
    748527500 -> 748.53M
    """
    number = str(number)
    if not number:
        raise ValueError("The input must not be empty.")
    whole, *remaining = number.split(".")
    if len(remaining) > 1:
        raise ValueError("Too many decimal points.")
    if len(whole) > 3:
        number = whole
    if "." not in number:
        if len(number) <= 3:
            return number
        i = len(number) % 3 or 3
        decimal_number = Decimal(number) / pow(Decimal(10), Decimal(len(number) - i))
        return str(decimal_number.quantize(Decimal("1.00"))) + get_number_suffix(number)
    decimal.getcontext().rounding = decimal.ROUND_HALF_UP
    number = str(Decimal(number).quantize(Decimal("1.00")))
    whole, fraction = number.split(".")
    if int(fraction) == 0:
        return whole
    return number

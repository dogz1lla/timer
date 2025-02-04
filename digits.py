ZERO = r"""  #####
 ##   ##
##     ##
##     ##
##     ##
 ##   ##
  #####"""

ONE = r"""   ##
 ####
   ##
   ##
   ##
   ##
 ######"""

TWO = r""" #######
##     ##
       ##
 #######
##
##
#########"""

THREE = r""" #######
##     ##
       ##
 #######
       ##
##     ##
 #######"""

FOUR = r"""##
##    ##
##    ##
##    ##
#########
      ##
      ##"""

FIVE = r"""########
##
##
#######
      ##
##    ##
 ######"""

SIX = r""" #######
##     ##
##
########
##     ##
##     ##
 #######"""

SEVEN = r"""########
##    ##
    ##
   ##
  ##
  ##
  ##"""

EIGHT = r""" #######
##     ##
##     ##
 #######
##     ##
##     ##
 #######"""

NINE = r""" #######
##     ##
##     ##
 ########
       ##
##     ##
 #######"""


SEPARATOR = r""" 
 
#
 
#
 
 """

DIGITS = {
    "0": ZERO,
    "1": ONE,
    "2": TWO,
    "3": THREE,
    "4": FOUR,
    "5": FIVE,
    "6": SIX,
    "7": SEVEN,
    "8": EIGHT,
    "9": NINE,
}

MAX_WIDTH = max([max([len(s) for s in d.split("\n")]) for d in DIGITS.values()])


def pad_digit(digit: str, width: int) -> str:
    """Pad the string representation of a digit with spaces to make it rectangular."""
    d_inline: list[str] = digit.split('\n')
    max_width = max([len(s) for s in d_inline])
    padded = list()
    for s in d_inline:
        if len(s) < max_width:
            s += " " * (max_width - len(s))
        padded.append(s)
    return "\n".join([s for s in padded])


def combine_digits(d1: str, d2: str, max_width: int) -> str:
    """Take two digits and make them one two digit number."""
    # pad every line with " " till max_width
    d1 = pad_digit(d1, max_width)
    d2 = pad_digit(d2, max_width)
    d1_inline: list[str] = d1.split('\n')
    d2_inline: list[str] = d2.split('\n')
    assert len(d1_inline) == len(d2_inline), "numbers are screwed"
    combined = "\n".join([l1 + "  " + l2 for l1, l2 in zip(d1_inline, d2_inline)])
    return combined


def concat_number_list(number_list: list[str], separator: str) -> str:
    """Combine minutes string and seconds string with a separator in between."""
    nums: list[list[str]] = [num.split('\n') for num in number_list]
    se: list[str] = separator.split('\n')
    se = [" " + c + " " for c in se]
    assert all([len(x) == len(nums[0]) for x in nums])
    assert len(nums[0]) == len(se)
    result = list()
    for line_idx in range(len(nums[0])):
        result.append(se[line_idx].join([num[line_idx] for num in nums]))
    return "\n".join(result)


def get_hours_minutes_seconds_string(h1: str, h2: str, m1: str, m2: str, s1: str, s2: str) -> str:
    hours   = combine_digits(DIGITS[h1], DIGITS[h2], MAX_WIDTH)
    minutes = combine_digits(DIGITS[m1], DIGITS[m2], MAX_WIDTH)
    seconds = combine_digits(DIGITS[s1], DIGITS[s2], MAX_WIDTH)
    return concat_number_list([hours, minutes, seconds], SEPARATOR)


def get_time_digits_now() -> tuple[str, str, str, str, str, str]:
    from datetime import datetime as dt
    from datetime import timezone as tz
    now = dt.now(tz.utc).time().strftime("%H:%M:%S")
    hour, minute, second = now.split(":")
    h1, h2 = hour
    m1, m2 = minute
    s1, s2 = second
    return (h1, h2, m1, m2, s1, s2)


def print_clock() -> None:
    import time
    try:
        while True:
            time_str = get_hours_minutes_seconds_string(*get_time_digits_now())
            print(time_str)
            print("\n\n")
            time.sleep(1)
    except KeyboardInterrupt:
        exit()


def print_countdown(n: int = 90) -> None:
    assert n < 360000, "the program cant handle timers of 100h or more"
    hours = n // 3600
    n -= hours * 3600
    minutes = n // 60
    seconds = n % 60
    h1, h2 = f'{hours:02}'
    m1, m2 = f'{minutes:02}'
    s1, s2 = f'{seconds:02}'
    time_str = get_hours_minutes_seconds_string(h1, h2, m1, m2, s1, s2)
    print(time_str)


if __name__ == "__main__":
    #print_clock()
    print_countdown(359999)

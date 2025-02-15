import urwid
from digits import get_hours_minutes_seconds_string


def exit_on_q(key: str) -> None:
    if key in {"q", "Q"}:
        raise urwid.ExitMainLoop()

def on_exit_clicked(_: urwid.Button) -> None:
    raise urwid.ExitMainLoop()


def unhandled_input(key: str) -> None:
    if key == 'q':
        raise urwid.ExitMainLoop()
    

def main(n: int) -> None:
    """credit goes to https://python-forum.io/thread-8693.html"""
    red_fg = urwid.AttrSpec('dark red', 'default')
    default_bg = urwid.AttrSpec('default', 'default')

    def get_color(n: int) -> urwid.AttrSpec:
        if n < 10 and n % 2 == 1:
            return red_fg
        else:
            return default_bg

    def refresh(_loop, _n) -> None:
        """_n here is the number of seconds left on the timer"""
        assert isinstance(_n, int)
        # calculate the minutes/seconds left
        n = max(_n, 0)
        assert n < 360000, "the program cant handle timers of 100h or more"
        hours = n // 3600
        n -= hours * 3600
        minutes = n // 60
        seconds = n % 60
        # get the timer string
        h1, h2 = f'{hours:02}'
        m1, m2 = f'{minutes:02}'
        s1, s2 = f'{seconds:02}'
        timer_str = get_hours_minutes_seconds_string(h1, h2, m1, m2, s1, s2)
        # render the new timer string on screen
        # NOTE: need to pass _n and not n because this will make the color blink even after n < 0
        color = get_color(_n)
        txt.set_text((color, timer_str))
        # recur
        _loop.set_alarm_in(1, refresh, _n - 1)
    
    txt  = urwid.Text("")
    fill = urwid.LineBox(urwid.Padding(urwid.Filler(txt, valign='middle'), align=urwid.CENTER, width=75))
    loop = urwid.MainLoop(fill, unhandled_input=unhandled_input)
    loop.set_alarm_in(0, refresh, n)
    loop.run()


if __name__ == "__main__":
    import argparse

    def _validate_nseconds(nseconds: str):
        """see https://stackoverflow.com/a/14117511"""
        nseconds = int(nseconds)
        if nseconds >= 360000:
            raise argparse.ArgumentTypeError("must be less than 360000 (i.e. 100 hours)")
        return nseconds

    parser = argparse.ArgumentParser(
        prog="main.py",
        description="CLI countdown",
    )
    parser.add_argument("nseconds", help="Number of seconds to count down", type=_validate_nseconds)
    args = parser.parse_args()
    main(args.nseconds)

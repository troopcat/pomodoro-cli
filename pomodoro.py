import curses
from datetime import datetime
from sys import argv
from time import sleep

def after(hour, min, sec) -> datetime:
	now = datetime.now()

	_min = now.minute + min
	_hour = now.hour + hour
	_sec = now.second + sec
	_day = now.day

	while _min >= 60:
		_min -= 60
		_hour += 1
	
	while _hour >= 24:
		_hour -= 1
		_day += 1
	
	while _sec >= 60:
		_sec -= 60
		_min += 1

	after = datetime(now.year, now.month, _day, _hour, _min, _sec, now.microsecond)

	return after

SLEEP = 0.05 # refresh rate

if len(argv) > 2:
	work_time = argv[1].split(":")
	break_time = argv[2].split(":")

	aft = after(int(work_time[0]), int(work_time[1]), int(work_time[2]))

else:
	work_time = [0, 25, 0]
	aft = after(work_time[0], work_time[1], work_time[2])
	break_time = [0, 5, 0]

def main() -> None:
	global aft, work_time

	stdscr = curses.initscr()
	curses.noecho()
	stdscr.nodelay(1)

	while True:
		stdscr.clear()

		left = aft - datetime.now()

		if left.seconds <= 0:
			stdscr.addstr(0, 0, "It's break time. To enter it press any key.")

			while not stdscr.getch() >= 0:
				print("\a") # bell

			aft_break = after(int(break_time[0]), int(break_time[1]), int(break_time[2]))
			while True:

				stdscr.clear()

				left = aft_break - datetime.now()

				if left.seconds <= 0:
					stdscr.addstr(0, 0, "It's work time. To enter it press any key.")

					while not stdscr.getch() >= 0:
						print("\a") # bell
					
					aft = after(int(work_time[0]), int(work_time[1]), int(work_time[2]))
					break

				stdscr.addstr(0, 0, str(left))
				stdscr.refresh()
				sleep(SLEEP)

				if stdscr.getch() == 27: # ESC
					curses.endwin()
					exit()


		stdscr.addstr(0, 0, str(left))
		stdscr.refresh()
		sleep(SLEEP)

		if stdscr.getch() == 27: # ESC
			curses.endwin()
			exit()

if __name__ == "__main__":
	main()
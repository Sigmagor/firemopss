from screeninfo import get_monitors

monitors = get_monitors()
primary_monitor = monitors[0]

WIDTH = primary_monitor.width
WIDTH -= WIDTH * 0.5

HEIGHT = primary_monitor.height
HEIGHT -= HEIGHT * 0.4

user = None
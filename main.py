import sys
import signal

from ui.app_main import AppMain

# apparently we need this stupid hack to make Ctrl+C actually kill the process
# i tried running it a couple times and there were bugs, but when I ctrl+c'ed nothing
# happened... and Ctrl + Z "paused" it but the processes were still hanging out in the
# background. its things like this that turn me off from python every time i try using
# it >:|
signal.signal(signal.SIGINT, signal.SIG_DFL)

# copied this verbatim out of https://developer.gnome.org/gnome-devel-demos/stable/GtkApplicationWindow.py.html
app = AppMain()
exit_status = app.run (sys.argv)
sys.exit (exit_status)

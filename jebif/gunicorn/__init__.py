import os
import sys

paths = [
    '/home/jebif/.local/lib64/python2.7/site-packages',
    '/home/jebif/apps/jebif-ng'
]
for p in paths :
	if p not in sys.path :
		sys.path.append(p)

proc_name = "jebifng"

os.environ["DJANGO_SETTINGS_MODULE"] = "jebif.settings"

bind = "unix:/var/run/gunicorn/jebif/ng-sock"
pidfile = "/var/run/gunicorn/jebif/ng-pid"
max_requests = 500
umask = 0o007
workers = 5

def when_ready( server ) :
	from jebif.gunicorn import monitor
	monitor.start(interval=5.0)
	monitor.track(os.path.join(os.path.dirname(__file__), 'touch_to_restart'))


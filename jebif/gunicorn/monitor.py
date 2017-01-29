import os
import sys
import time
import signal
import threading
import atexit
from queue import Queue

_interval = 1.0
_times = {}
_files = []

_running = False
_queue = Queue()
_lock = threading.Lock()

def _restart(path):
    _queue.put(True)
    prefix = 'monitor (pid=%d):' % os.getpid()
#    print('%s Change detected to \'%s\'.' % (prefix, path), file=sys.stderr)
#    print('%s Triggering process restart.' % prefix, file=sys.stderr)
    os.kill(os.getpid(), signal.SIGINT)


def _modified(path):
    try:
        # Check for when file last modified.
        mtime = os.stat(path).st_mtime
        if path not in _times:
            _times[path] = mtime

        # Force restart when modification time has changed, even
        # if time now older, as that could indicate older file
        # has been restored.
        if mtime != _times[path]:
            return True
    except:
        pass

    return False


def _monitor():
    while 1:
        # Check modification times on files which have
        # specifically been registered for monitoring.
        for path in _files:
            if _modified(path):
                return _restart(path)

        # Go to sleep for specified interval.
        try:
            return _queue.get(timeout=_interval)
        except:
            pass

_thread = threading.Thread(target=_monitor)
_thread.setDaemon(True)

def _exiting():
    try:
        _queue.put_nowait(True)
    except:
        pass
#    _thread.join()

atexit.register(_exiting)

def track(path):
    print(path)
    if not path in _files:
        _files.append(path)

def start(interval=1.0):
    global _interval
    _interval = interval

    global _running
    _lock.acquire()
    if not _running:
        prefix = 'monitor (pid=%d):' % os.getpid()
#        print('%s Starting change monitor.' % prefix, file=sys.stderr)
        _running = True
        _thread.start()
    _lock.release()


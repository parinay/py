import threading
import signal
import random

# The Event class is provided in the threading module of the Python standard library.
# You can create an event object by instantiating the class.
# the idea is to set the event at the time when the thread needs to exit.
exit_event = threading.Event()


def bg_thread():
    """
        background thread printing an int range.
        Run 'Ctrl+c' once you run the programe.

        The problem is that Python has some logic that runs right
        before the process exits that is dedicated to wait for any
        background threads that are not configured as daemon threads
        to end before actually returning control to the operating system.

        1. Ctrl+c
        2. Before process exits it waits for background thread to end.
    """
    for i in range(1, 30):
        print(f"{i} of 30 iterations...")
        if exit_event.wait(timeout=random.random()):
            break

    print(f"{i} iteration completed before exiting.")


def signal_handler(signnum, frame):
    exit_event.set()


def main():
    """
        function demonstrating pthread and killing pthread.
        - with 'th.daeom = False' (default) you need to run 'Ctrl+c' twice.
          The wait mechanism that Python uses during exit has a provision
          to abort when a second interrupt signal is received. This is why
          a second Ctrl-C ends the process immediately
        - with 'th.daemon = True', with single 'Ctrl+c', the thread ceases
          to exists, killing the process as well.
        - python events -
    """
    signal.signal(signal.SIGINT, signal_handler)
    # Constructor with argument.
    # target is the callable object to be invoked by the run()
    th = threading.Thread(target=bg_thread)
    # How do you make a thread be a daemon thread? All thread objects
    # have a daemon property. You can set this property to True before
    # starting the thread, and then that thread will be considered a
    # daemon thread.
    th.daemon = True
    # start the thread's activity.
    # must be called once per thread object's run() method
    th.start()
    # wait until the thread terminates.
    # blocks the calling thread until the thread whose join()
    # method either normally or through unhandled exception - or
    # until the optional timeout occurs.
    th.join()


if __name__ == "__main__":
    main()

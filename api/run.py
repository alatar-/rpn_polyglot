import threading

from app import main, helpers

if __name__ == '__main__':
    # Configure loggers
    helpers.configure_loggers()

    # Start sink thread
    thread = threading.Thread(target=main.sink_thread)
    thread.start()

    # Start API thread
    main.api_thread()

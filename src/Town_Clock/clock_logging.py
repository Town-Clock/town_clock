import logging
import logging.config
import logging.handlers
import os
from multiprocessing import Event, Process, Queue, current_process
import queue
import time
from Town_Clock.clock_enums_exceptions import Clock, Log_Level


# Constants
log_folder = os.path.join(os.path.dirname(__file__),'clock_log')
pulse_log_name = 'pulse.log'
pulse_log_path = os.path.join(log_folder,pulse_log_name)

def get_or_create_output_folder() -> str:
        if not os.path.exists(log_folder):
            os.mkdir(log_folder)
        if not os.path.exists(pulse_log_path):
            with open(pulse_log_path, mode = 'x') as _:
                pass
        return log_folder


# The main process gets a simple configuration which prints to the console.
class Setup_Log:
    def __init__(self, name:str = 'Setup'):    
        self.config_initial = {
                            'version': 1,
                            'formatters': {
                                'simple': {
                                    'class': 'logging.Formatter',
                                    'format': '%(name)-15s %(levelname)-8s %(processName)-26s %(process)d %(message)s'
                                }},
                            'handlers': {
                                'console': {
                                    'class': 'logging.StreamHandler',
                                    'level': 'DEBUG',
                                    'formatter': 'simple'
                                }
                            },
                            'root': {
                                'handlers': ['console'],
                                'level': 'DEBUG'
                            }
                        }
        self.name = name
        self.folder_path = folder_path
        self.log('debug', self.folder_path)

    def log(self, level: Log_Level, msg: str, name: str = None) -> None:
        if name is None: name = self.name
        if isinstance(level, Log_Level): level = level.value
        elif isinstance(level, str): level = Log_Level[level.upper()].value
        elif not isinstance(level, int): 
            msg = f"LOG ERROR: UNKNOWN VALUE {level}, {msg = }"
            level = Log_Level.ERROR.value

        logging.config.dictConfig(self.config_initial)
        self.logger = logging.getLogger(self.name)
        self.logger.log(level = level, msg = msg)


class Listener:
    def __init__(self, name: str = 'Listener'):
        # The listener process configuration shows that the full flexibility of
        # logging configuration is available to dispatch events to handlers however
        # you want.
        # We disable existing loggers to disable the "setup" logger used in the
        # parent process. This is needed on POSIX because the logger will
        # be there in the child following a fork().
        self.config_listener = {
            'version': 1,
            'disable_existing_loggers': True,
            'formatters': {
                'detailed': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s.%(msecs)03d %(name)-15s %(levelname)-8s %(processName)-10s %(process)d %(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
                'pulse': {
                    'class': 'logging.Formatter',
                    'format': '%(asctime)s.%(msecs)03d;%(levelname)-8s;%(name)-9s;%(processName)s;%(process)d;%(message)s',
                    'datefmt': '%Y-%m-%d %H:%M:%S'
                },
                'simple': {
                    'class': 'logging.Formatter',
                    'format': '%(name)-15s %(levelname)-8s %(processName)-26s %(process)d %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                    'level': 'INFO'
                },
                'file':{
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': f'{log_folder}/clock.log',
                    'mode': 'a',
                    'maxBytes': 1073741824, 
                    'backupCount': 7,
                    'formatter': 'pulse'
                },
                'errors': {
                    'class': 'logging.FileHandler',
                    'filename': f'{log_folder}/clock-errors.log',
                    'mode': 'a',
                    'formatter': 'detailed',
                    'level': 'ERROR'
                },
                'pulserotate':{
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': f'{pulse_log_path}',
                    'mode': 'a',
                    'maxBytes': 129600, 
                    'backupCount': 7,
                    'formatter': 'pulse'
                },
            },
            'loggers': {
                'Pulse': {'handlers': ['pulserotate']}
            },
            'root': {
                'handlers': ['console', 'file', 'errors'],
                'level': 'DEBUG'
            }
        }
        self.name = name
        self.stop_event = Event()
        self.stop_event.clear()
        self.lp = Process(target = self.listener_process, 
                          name = self.name,
                          args = (log_queue,),
                          daemon = False
                          )
        self.lp.start()
        self.logger: Worker = Worker(name = self.name, clock = None)

    def listener_process(self, q):
        """
        This could be done in the main process, but is just done in a separate
        process for illustrative purposes.

        This initialises logging according to the specified configuration,
        starts the listener and waits for the main process to signal completion
        via the event. The listener is then stopped, and the process exits.
        """
        try:
            logging.config.dictConfig(self.config_listener)
            listener = logging.handlers.QueueListener(q, MyHandler())
            listener.start()
            self.stop_event.wait()
            listener.stop()
        except KeyboardInterrupt:
            self.stop_event.wait()
            listener.stop()


class MyHandler:
    """
    A simple handler for logging events. It runs in the listener process and
    dispatches events to loggers based on the name in the received record,
    which then get dispatched, by the logging system, to the handlers
    configured for those loggers.
    """
    def handle(self, record):
        if record.name == "root":
            logger = logging.getLogger()
        else:
            logger = logging.getLogger(record.name)

        if logger.isEnabledFor(record.levelno):
            # The process name is transformed just to show that it's the listener
            # doing the logging to files and console
            record.processName = '%s (for %s)' % (current_process().name, record.processName)
            logger.handle(record)


class Worker:
    def __init__(self, name: str, clock: Clock):
        # The worker process configuration is just a QueueHandler attached to the
        # root logger, which allows all messages to be sent to the queue.
        # We disable existing loggers to disable the "setup" logger used in the
        # parent process. This is needed on POSIX because the logger will
        # be there in the child following a fork().
        self.worker_config = {  
                              'version': 1,
                              'disable_existing_loggers': False,
                              'handlers': {
                                  'queue': {
                                      'class': 'logging.handlers.QueueHandler',
                                      'queue': log_queue
                                      }
                                  },
                              'root': {
                                  'handlers': ['queue'],
                                  'level': 'DEBUG'
                                  }
                              }
        self.name = name
        self.clock = clock
        self.q = log_queue
    
    def log(self, level: int, msg: str, name: str = None) -> None:
        if name is None: name = self.name
        
        if isinstance(level, Log_Level): level = level.value
        elif isinstance(level, str): level = Log_Level[level.upper()].value
        elif not isinstance(level, int): 
            msg = f"LOG ERROR: UNKNOWN VALUE {level}, {msg = }"
            level = Log_Level.ERROR.value
            
        logging.config.dictConfig(self.worker_config)
        self.logger = logging.getLogger(self.name)
        self.logger.log(level = level, msg = msg)
        

    # def worker_process(self):
    #     """
    #     A number of these are spawned for the purpose of illustration. In
    #     practice, they could be a heterogeneous bunch of processes rather than
    #     ones which are identical to each other.

    #     This initialises logging according to the specified configuration,
    #     and logs a hundred messages with random levels to randomly selected
    #     loggers.

    #     A small sleep is added to allow other processes a chance to run. This
    #     is not strictly needed, but it mixes the output from the different
    #     processes a bit more than if it's left out.
    #     """
    #     logging.config.dictConfig(self.worker_config)
    #     levels = [logging.DEBUG, logging.INFO, logging.WARNING, 
    #             logging.ERROR, logging.CRITICAL]
    #     loggers = ['Pulse', 'Pulse.one', 'Pulse.two']


def main():
    pass


def destroy():
    pass


main()
log_queue = Queue()
folder_path = get_or_create_output_folder()
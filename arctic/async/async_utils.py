import os
import time
import uuid
from enum import Enum


ARCTIC_ASYNC_NTHREADS = os.environ.get('ARCTIC_ASYNC_NTHREADS', 4)
USE_ASYNC_MONGO_WRITES = bool(os.environ.get('USE_ASYNC_MONGO_WRITES'))

class AsyncRequestType(Enum):
    MODIFIER = 'modifier'
    ACCESSOR = 'accessor'


class AsyncRequest(object):
    def __init__(self, kind, library, fun, *args, **kwargs):
        self.id = uuid.uuid4()

        # Request library call spec
        self.fun = fun
        self.args = args
        self.kwargs = kwargs

        # Request meta
        self.kind = kind
        self.library = library
        self.symbol = kwargs.get('symbol')

        # Request's state
        self.future = None
        self.data = None
        self.exception = None
        self.is_running = False
        self.is_completed = False

        # Timekeeping
        self.start_time = None
        self.end_time = None
        self.create_time = time.time()

        self.mongo_retry = bool(kwargs.get('mongo_retry'))

    @property
    def execution_duration(self):
        return self.end_time - self.start_time if self.end_time is not None else -1

    @property
    def schedule_delay(self):
        return self.start_time - self.create_time if self.start_time is not None else -1

    @property
    def total_time(self):
        return self.end_time - self.create_time if self.end_time is not None else -1
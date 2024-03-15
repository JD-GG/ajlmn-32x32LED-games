"""
## Core of thread

```py
class Thread: ...
class ParallelProcessing: ...
```

Documentation: https://thread.ngjx.org/docs/v1.0.0
"""

import sys
import time
import ctypes
import signal
import threading
from functools import wraps

from . import exceptions
from .utils.config import Settings
from .utils.algorithm import chunk_split

from ._types import (
    ThreadStatus,
    Data_In,
    Data_Out,
    Overflow_In,
    TargetFunction,
    _Target_P,
    _Target_T,
    DatasetFunction,
    _Dataset_T,
    HookFunction,
)
from typing_extensions import Generic, ParamSpec
from typing import List, Optional, Union, Mapping, Sequence, Tuple, Generator


Threads: set['Thread'] = set()


class Thread(threading.Thread, Generic[_Target_P, _Target_T]):
    """
    Wraps python's `threading.Thread` class
    ---------------------------------------

    Type-Safe and provides more functionality on top
    """

    status: ThreadStatus
    hooks: List[HookFunction]
    _returned_value: Data_Out

    errors: List[Exception]
    ignore_errors: Sequence[type[Exception]]
    suppress_errors: bool

    # threading.Thread stuff
    _initialized: bool

    def __init__(
        self,
        target: TargetFunction[_Target_P, _Target_T],
        args: Sequence[Data_In] = (),
        kwargs: Mapping[str, Data_In] = {},
        ignore_errors: Sequence[type[Exception]] = (),
        suppress_errors: bool = False,
        name: Optional[str] = None,
        daemon: bool = False,
        group=None,
        *overflow_args: Overflow_In,
        **overflow_kwargs: Overflow_In,
    ) -> None:
        """
        Initializes a thread

        Parameters
        ----------
        :param target: This should be a function that takes in anything and returns anything
        :param args: This should be an interable sequence of arguments parsed to the `target` function (e.g. tuple('foo', 'bar'))
        :param kwargs: This should be the kwargs parsed to the `target` function (e.g. dict(foo = 'bar'))
        :param ignore_errors: This should be an interable sequence of all exceptions to ignore. To ignore all exceptions, parse tuple(Exception)
        :param suppress_errors: This should be a boolean indicating whether exceptions will be raised, else will only write to internal `errors` property
        :param name: This is an argument parsed to `threading.Thread`
        :param daemon: This is an argument parsed to `threading.Thread`
        :param group: This does nothing right now, but should be left as None
        :param *: These are arguments parsed to `threading.Thread`
        :param **: These are arguments parsed to `thread.Thread`
        """
        _target = self._wrap_target(target)
        self._returned_value = None
        self.status = 'Idle'
        self.hooks = []

        self.errors = []
        self.ignore_errors = ignore_errors
        self.suppress_errors = suppress_errors

        super().__init__(
            target=_target,
            args=args,
            kwargs=kwargs,
            name=name,
            daemon=daemon,
            group=group,
            *overflow_args,
            **overflow_kwargs,
        )

    def _wrap_target(
        self, target: TargetFunction[_Target_P, _Target_T]
    ) -> TargetFunction[_Target_P, Union[_Target_T, None]]:
        """Wraps the target function"""

        @wraps(target)
        def wrapper(
            *args: _Target_P.args, **kwargs: _Target_P.kwargs
        ) -> Union[_Target_T, None]:
            try:
                self.status = 'Running'

                global Threads
                Threads.add(self)

                try:
                    self._returned_value = target(*args, **kwargs)
                except Exception as e:
                    if not any(isinstance(e, ignore) for ignore in self.ignore_errors):
                        self.status = 'Errored'
                        self.errors.append(e)
                        return

                self.status = 'Invoking hooks'
                self._invoke_hooks()
                Threads.remove(self)
                self.status = 'Completed'

            except SystemExit:
                self.status = 'Killed'
                if Settings.VERBOSITY > 'quiet':
                    print('KILLED ident: %s' % self.ident)
                return

        return wrapper

    def _invoke_hooks(self) -> None:
        """Invokes hooks in the thread"""
        errors: List[Tuple[Exception, str]] = []
        for hook in self.hooks:
            try:
                hook(self._returned_value)
            except Exception as e:
                if not any(isinstance(e, ignore) for ignore in self.ignore_errors):
                    errors.append((e, hook.__name__))

        if len(errors) > 0:
            self.errors.append(exceptions.HookRuntimeError(None, errors))

    def _handle_exceptions(self) -> None:
        """Raises exceptions if not suppressed in the main thread"""
        if self.suppress_errors:
            return

        for e in self.errors:
            raise e

    @property
    def result(self) -> _Target_T:
        """
        The return value of the thread

        Raises
        ------
        ThreadNotInitializedError: If the thread is not initialized
        ThreadNotRunningError: If the thread is not running
        ThreadStillRunningError: If the thread is still running
        """
        if not self._initialized:
            raise exceptions.ThreadNotInitializedError()
        if self.status in ['Idle', 'Killed']:
            raise exceptions.ThreadNotRunningError()

        self._handle_exceptions()
        if self.status in ['Invoking hooks', 'Completed']:
            return self._returned_value
        else:
            raise exceptions.ThreadStillRunningError()

    def is_alive(self) -> bool:
        """
        See if thread is still alive

        Raises
        ------
        ThreadNotInitializedError: If the thread is not initialized
        """
        if not self._initialized:
            raise exceptions.ThreadNotInitializedError()
        return super().is_alive()

    def add_hook(self, hook: HookFunction[_Target_T]) -> None:
        """
        Adds a hook to the thread
        -------------------------
        Hooks are executed automatically after a successful thread execution.
        The returned value is parsed directly into the hook

        Parameters
        ----------
        :param hook: This should be a function which takes the output value of `target` and should return None
        """
        self.hooks.append(hook)

    def join(self, timeout: Optional[float] = None) -> bool:
        """
        Halts the current thread execution until a thread completes or exceeds the timeout

        Parameters
        ----------
        :param timeout: The maximum time allowed to halt the thread

        Returns
        -------
        :returns bool: True if the thread is no-longer alive

        Raises
        ------
        ThreadNotInitializedError: If the thread is not initialized
        ThreadNotRunningError: If the thread is not running
        """
        if not self._initialized:
            raise exceptions.ThreadNotInitializedError()

        if self.status == ['Idle', 'Killed']:
            raise exceptions.ThreadNotRunningError()

        super().join(timeout)
        self._handle_exceptions()
        return not self.is_alive()

    def get_return_value(self) -> _Target_T:
        """
        Halts the current thread execution until the thread completes

        Returns
        -------
        :returns Any: The return value of the target function
        """
        self.join()
        return self.result

    def kill(self, yielding: bool = False, timeout: float = 5) -> bool:
        """
        Schedules a thread to be killed

        Parameters
        ----------
        :param yielding: If true, halts the current thread execution until the thread is killed
        :param timeout: The maximum number of seconds to wait before exiting

        Returns
        -------
        :returns bool: False if the it exceeded the timeout without being killed

        Raises
        ------
        ValueError: If the thread ident does not exist
        ThreadNotInitializedError: If the thread is not initialized
        ThreadNotRunningError: If the thread is not running
        """
        if not self.is_alive():
            raise exceptions.ThreadNotRunningError()

        self.status = 'Kill Scheduled'

        res: int = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(self.ident), ctypes.py_object(SystemExit)
        )

        if res == 0:
            raise ValueError('Thread IDENT does not exist')
        elif res > 1:
            # Unexpected behaviour, something seriously went wrong
            # https://docs.python.org/3/c-api/init.html#c.PyThreadState_SetAsyncExc
            ctypes.pythonapi.PyThreadState_SetAsyncExc(self.ident, None)
            raise SystemError(
                f'Killing thread with ident [{self.ident}] failed!\nPyThreadState_SetAsyncExc returned: {res}'
            )

        if not yielding:
            return True

        start = time.perf_counter()
        while self.status != 'Killed':
            time.sleep(0.01)
            if (time.perf_counter() - start) >= timeout:
                return False

        return True

    def start(self) -> None:
        """
        Starts the thread

        Raises
        ------
        ThreadNotInitializedError: If the thread is not initialized
        ThreadStillRunningError: If there already is a running thread
        """
        if self.is_alive():
            raise exceptions.ThreadStillRunningError()

        super().start()


_P = ParamSpec('_P')


class _ThreadWorker:
    progress: float
    thread: Thread

    def __init__(self, thread: Thread, progress: float = 0) -> None:
        self.thread = thread
        self.progress = progress


class ParallelProcessing(Generic[_Target_P, _Target_T, _Dataset_T]):
    """
    Multi-Threaded Parallel Processing
    ---------------------------------------

    Type-Safe and provides more functionality on top
    """

    _threads: List[_ThreadWorker]
    _completed: int

    status: ThreadStatus
    function: TargetFunction
    dataset: Sequence[Data_In]
    max_threads: int

    overflow_args: Sequence[Overflow_In]
    overflow_kwargs: Mapping[str, Overflow_In]

    def __init__(
        self,
        function: DatasetFunction[_Dataset_T, _Target_P, _Target_T],
        dataset: Sequence[_Dataset_T],
        max_threads: int = 8,
        *overflow_args: Overflow_In,
        **overflow_kwargs: Overflow_In,
    ) -> None:
        """
        Initializes a new Multi-Threaded Pool\n
        Best for data processing

        Splits a dataset as evenly as it can among the threads and run them in parallel

        Parameters
        ----------
        :param function: This should be the function to validate each data entry in the `dataset`, the first argument parsed will be a value of the dataset
        :param dataset: This should be an iterable sequence of data entries
        :param max_threads: This should be an integer value of the max threads allowed
        :param *: These are arguments parsed to `threading.Thread` and `Thread`
        :param **: These are arguments parsed to `thread.Thread` and `Thread`

        Raises
        ------
        AssertionError: invalid `max_threads`
        """
        assert 0 <= max_threads, 'Cannot run a thread pool with max threads set to 0'

        self._threads = []
        self._completed = 0

        self.status = 'Idle'
        self.function = self._wrap_function(function)
        self.dataset = dataset
        self.max_threads = max_threads

        self.overflow_args = overflow_args
        self.overflow_kwargs = overflow_kwargs

    def _wrap_function(self, function: TargetFunction) -> TargetFunction:
        @wraps(function)
        def wrapper(
            index: int,
            length: int,
            data_chunk: Generator[_Dataset_T, None, None],
            *args: _Target_P.args,
            **kwargs: _Target_P.kwargs,
        ) -> List[_Target_T]:
            computed: List[Data_Out] = []

            i = 0
            for data_entry in data_chunk:
                v = function(data_entry, *args, **kwargs)
                computed.append(v)
                self._threads[index].progress = round((i + 1) / length, 5)
                i += 1

            self._completed += 1
            if self._completed == len(self._threads):
                self.status = 'Completed'

            return computed

        return wrapper

    @property
    def results(self) -> List[_Dataset_T]:
        """
        The return value of the threads if completed

        Raises
        ------
        ThreadNotInitializedError: If the threads are not initialized
        ThreadNotRunningError: If the threads are not running
        ThreadStillRunningError: If the threads are still running
        """
        if len(self._threads) == 0:
            raise exceptions.ThreadNotInitializedError()

        results: List[Data_Out] = []
        for entry in self._threads:
            results += entry.thread.result
        return results

    def is_alive(self) -> bool:
        """
        See if any threads are still alive

        Raises
        ------
        ThreadNotInitializedError: If the thread is not initialized
        """
        if len(self._threads) == 0:
            raise exceptions.ThreadNotInitializedError()
        return any(entry.thread.is_alive() for entry in self._threads)

    def get_return_values(self) -> List[_Dataset_T]:
        """
        Halts the current thread execution until the thread completes

        Returns
        -------
        :returns Any: The return value of the target function
        """
        results: List[Data_Out] = []
        for entry in self._threads:
            entry.thread.join()
            results += entry.thread.result
        return results

    def join(self) -> bool:
        """
        Halts the current thread execution until a thread completes or exceeds the timeout

        Returns
        -------
        :returns bool: True if the thread is no-longer alive

        Raises
        ------
        ThreadNotInitializedError: If the thread is not initialized
        ThreadNotRunningError: If the thread is not running
        """
        if len(self._threads) == 0:
            raise exceptions.ThreadNotInitializedError()

        if self.status == 'Idle':
            raise exceptions.ThreadNotRunningError()

        for entry in self._threads:
            entry.thread.join()
        return True

    def kill(self) -> None:
        """
        Kills the threads

        Raises
        ------
        ThreadNotInitializedError: If the thread is not initialized
        ThreadNotRunningError: If the thread is not running
        """
        for entry in self._threads:
            entry.thread.kill()

    def start(self) -> None:
        """
        Starts the threads

        Raises
        ------
        ThreadStillRunningError: If there already is a running thread
        """
        if self.status == 'Running':
            raise exceptions.ThreadStillRunningError()

        self.status = 'Running'
        max_threads = min(self.max_threads, len(self.dataset))

        parsed_args = self.overflow_kwargs.get('args', [])
        name_format = (
            self.overflow_kwargs.get('name') and self.overflow_kwargs['name'] + '%s'
        )
        self.overflow_kwargs = {
            i: v for i, v in self.overflow_kwargs.items() if i != 'name' and i != 'args'
        }

        i = 0
        for chunkStart, chunkEnd in chunk_split(len(self.dataset), max_threads):
            chunk_thread = Thread(
                target=self.function,
                args=[
                    i,
                    chunkEnd - chunkStart,
                    (self.dataset[x] for x in range(chunkStart, chunkEnd)),
                    *parsed_args,
                    *self.overflow_args,
                ],
                name=name_format and name_format % i or None,
                **self.overflow_kwargs,
            )
            self._threads.append(_ThreadWorker(chunk_thread, 0))
            chunk_thread.start()
            i += 1


# Handle abrupt exit
def service_shutdown(signum, frame):
    if Settings.GRACEFUL_EXIT_ENABLED:
        if Settings.VERBOSITY > 'quiet':
            print('\nCaught signal %d' % signum)
            print('Gracefully killing active threads')

        for thread in Threads:
            if isinstance(thread, Thread):
                try:
                    thread.kill()
                except (
                    exceptions.ThreadNotRunningError,
                    exceptions.ThreadNotInitializedError,
                ):
                    pass
                except Exception:
                    if Settings.VERBOSITY > 'quiet':
                        print('Failed to kill ident: %d' % thread.ident or 0)
        sys.exit(0)


# Register the signal handlers
signal.signal(signal.SIGTERM, service_shutdown)
signal.signal(signal.SIGINT, service_shutdown)

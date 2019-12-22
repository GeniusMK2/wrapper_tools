import functools
import os
import pickle
from datetime import datetime


def chronograph(func):
    """
    A decorator to test execution time for invocation functions or methods..
    :param func: function to be invocated.
    :return: func
    """

    _template_ = '\033[32;0mChronograph click:{0}\033[0m'
    _delta_template_ = '"\033[32;0m{0}" COSTS:{1}s.\033[0m'

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = datetime.utcnow()
        print(_template_.format(start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]))
        ret = func(*args, **kwargs)
        end_time = datetime.utcnow()
        print(_template_.format(end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]))
        print(_delta_template_.format(func.__name__, (end_time - start_time).total_seconds()))
        return ret

    return functools.update_wrapper(wrapper, func)


def save_return(path='.'):
    _file_name_template_ = '.~tmp-{0}-return.pkl'

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            _file_ = open(os.path.join(path, _file_name_template_.format(func.__name__)), 'wb')
            pickle.dump(ret, _file_)
            return ret
        return functools.update_wrapper(wrapper, func)

    return decorator


def load_return(path='.'):
    _file_name_template_ = '.~tmp-{0}-return.pkl'

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # ret = func(*args, **kwargs)
            _file_ = open(os.path.join(path, _file_name_template_.format(func.__name__)), 'rb')
            return pickle.load(_file_)
        return functools.update_wrapper(wrapper, func)

    return decorator


@chronograph
@load_return()
def test_demo():
    """
    A function that costs some time.
    :return:
    """
    for _ in range(1, 1000):
        print(test_demo.__name__)
        return 1


if __name__ == '__main__':
    print(test_demo())

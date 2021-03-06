import gzip
from functools import wraps

import floto.specs
import floto.specs.task

ACTIVITY_FUNCTIONS = {}
COMPRESS_GENERATOR_RESULT = False


def activity(*, domain, name, version):
    """Decorator that registers a function to `ACTIVITY_FUNCTIONS`
    """
    def function_wrapper(func):
        identifier = '{}:{}:{}'.format(name, version, domain)
        ACTIVITY_FUNCTIONS[identifier] = func

    return function_wrapper


def compress_generator_result(result):
    serializable = [t.serializable() for t in result]
    if result and COMPRESS_GENERATOR_RESULT:
        j = floto.specs.JSONEncoder.dump_object(serializable)
        z = gzip.compress(j.encode())
        z = 'x'.join([format(c, 'x') for c in z])
        return z
    else:
        return serializable


def check_type_generator_output(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        message = 'Generators must return list(<floto.spec.Task>)'
        if not isinstance(result, list):
            raise ValueError(message)
        if not [isinstance(t, floto.specs.task.Task) for t in result]:
            raise ValueError(message)
        return compress_generator_result(result)

    return wrapper


def generator(*, domain, name, version):
    """Decorator that registers a generator function to `ACTIVITY_FUNCTIONS`
    """
    def function_wrapper(func):
        identifier = '{}:{}:{}'.format(name, version, domain)
        ACTIVITY_FUNCTIONS[identifier] = check_type_generator_output(func)

    return function_wrapper


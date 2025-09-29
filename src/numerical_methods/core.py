__all__ = []

POS_INF = float('inf')
NEG_INF = float('-inf')


def _check_bounds(bounds):
    if len(bounds) != 2 or bounds[0] > bounds[1]:
        assert 'invalid bounds'


def _function_wrapper(func, value, args = (), details = False):
    if not isinstance(args, tuple):
        args = (args,)

    res = 0
    message = ''

    try:
        res = func(value, *args)
    except ValueError as e:
        message = e
        res = 0
    except ZeroDivisionError as e:
        message = e
        res = 0

    if details:
        print(message)

    return res 
#   finally:
#       print('Calculation Error!')


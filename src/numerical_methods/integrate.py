__all__ = ['Simpson', 'Trapezoid']


from .core import (_function_wrapper, _check_bounds, NEG_INF, POS_INF)
import math


# TODO: Для интегрирования по бесконечным пределам нужно ввести неравномерную сетку, 
# шаги которой нарастают при стремлении к бесконечности, либо можно сделать такую замену 
# переменных в интеграле, после которой пределы будут конечны. Аналогичным образом можно поступить, 
# если функция особая на концах отрезка интегрирования.

def Simpson(func, args=(), bounds=(), n:int=100, inf:int=0, eps:float=10e-06, iterations_count:int=50, details:bool=False) -> float:

    _check_bounds(bounds=bounds)
    
    if inf == 0:
        
        res = _simpson_rule(func=func, args=args, bounds=bounds, n=n, details=details)

    elif inf == -1:

        right = bounds[1]
        left = right - 100

        approx = _simpson_rule(func=func, args=args, bounds=(left, right), n=n, details=details)
        buffer = 0
        counter = 0

        while(abs(approx - buffer) > eps and counter < iterations_count):
            left -= 100
            right -= 100
            buffer = approx
            approx += _simpson_rule(func=func, args=args, bounds=(left, right), n=n, details=details)
            counter += 1

        if abs(approx - buffer) > eps:
            print('WARNING: bad convergence')

        res = approx

    elif inf == 1:

        left = bounds[0]
        right = left + 100

        approx = _simpson_rule(func=func, args=args, bounds=(left, right), n=n, details=details)
        buffer = 0
        counter = 0

        while(abs(approx - buffer) > eps and counter < iterations_count):
            left += 100
            right += 100
            buffer = approx
            approx += _simpson_rule(func=func, args=args, bounds=(left, right), n=n, details=details)
            counter += 1

        if abs(approx - buffer) > eps:
            print('WARNING: bad convergence')

        res = approx

    elif inf == 2:
        left, right = -50, 50
        approx = _simpson_rule(func=func, args=args, bounds=(left, right), n=n, details=details)
        buffer = 0
        counter = 0        

        while(abs(approx - buffer) > eps and counter < iterations_count):
            buffer = approx
            approx += _simpson_rule(func=func, args=args, bounds=(left-100, left), n=n, details=details)
            approx += -_simpson_rule(func=func, args=args, bounds=(right, right+100), n=n, details=details)

        if abs(approx - buffer) > eps:
            print('WARNING: bad convergence')

        res = approx


    else:
        assert 'uknown integration range'


    return res

# TODO: Модифицировать Trapezoid для работы с несобственными интеграллами

def Trapezoid(func, args=(), bounds=(), n:int=100, inf:int=0, eps:float=1e-05, details:bool=False) -> float:

    _check_bounds(bounds=bounds)

    res = _trapezoid_rule(func=func, args=args, bounds=bounds, n=n, details=details)

    return res


def _trapezoid_rule(func, args=(), bounds=(), n = 100, details = False) -> float:
    a,b = bounds

    res: float = 0
    h = (b-a) / n

    for i in range(1, n):
        res += _function_wrapper(func = func, value = a + i * h, args = args, details = details)

    f0 = _function_wrapper(func = func, value = a, args = args, details = details)
    fN = _function_wrapper(func = func, value = b, args = args, details = details)

    res += (f0 + fN) / 2
    res *= h

    return res


def _simpson_rule(func, args=(), bounds=(), n=100, details = False) -> float:

    a,b = bounds
    res: float = 0

    f0 = _function_wrapper(func = func, value = a, args = args, details = details)
    fN = _function_wrapper(func = func, value = b, args = args, details = details)

    h = (b-a) / 2 / n 

    s1, s2 = 0, 0

    for j in range(1, n):
        xj = a + 2*j*h
        xj1 = a + (2*j - 1)*h
        s1 += _function_wrapper(func = func, value = xj, args = args, details = details)
        s2 += _function_wrapper(func = func, value = xj1, args = args, details = details)

    s2 += _function_wrapper(func = func, value = a + (2*n-1)*h, args = args, details = details)

    res = f0 + 2*s1 + 4*s2 + fN 
    res *= h / 3

    return res

   

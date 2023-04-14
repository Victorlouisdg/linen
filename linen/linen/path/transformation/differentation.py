import numdifftools as nd

from linen.path.path import Path


def differentiated(path, n=1):
    # TODO: can we take one-sided derivatives at the start and end?
    def function(t):
        return nd.Derivative(path, n=n)(t)

    return Path(function, start_time=path.start_time, end_time=path.end_time)

import scipy.integrate as integrate

from linen.path.path import Path


def integrated(path):
    def function(t):
        return integrate.quad(path, path.start_time, path.start_time + t)[0]

    return Path(function, start_time=path.start_time, end_time=path.end_time)

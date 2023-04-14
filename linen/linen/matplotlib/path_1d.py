import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

from linen.matplotlib.path_2d import plot_path_2d
from linen.path.path import Path


def make_2d(path_1d: Path):
    def path_2d(t: float) -> np.ndarray:
        return np.array([t, path_1d(t)])

    return Path(path_2d, start_time=path_1d.start_time, end_time=path_1d.end_time)


def plot_path_1d(
    path: Path,
    xlabel: str = "x",
    ylabel: str = "y",
    xlim: np.ndarray = None,
    ylim: np.ndarray = None,
    padding: float = 0.1,
    cmap: ListedColormap = None,
    grid: bool = True,
    ax: plt.Axes = None,
) -> plt.Axes:
    path_2d = make_2d(path)
    return plot_path_2d(
        path_2d,
        xlabel=xlabel,
        ylabel=ylabel,
        xlim=xlim,
        ylim=ylim,
        padding=padding,
        cmap=cmap,
        grid=grid,
        ax=ax,
    )

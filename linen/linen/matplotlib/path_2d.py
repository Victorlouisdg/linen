import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap

from linen.path.path import Path


# From: https://nbviewer.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
def make_segments(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    TODO ensure correctness

    Create list of line segments from x and y coordinates, in the correct format for LineCollection:
    an array of the form   numlines x (points per line) x 2 (x and y) array

    Args:
        x: x coordinates
        y: y coordinates

    Returns:
        segments

    """

    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    return segments


# From: https://nbviewer.org/github/dpsanders/matplotlib-examples/blob/master/colorline.ipynb
def colorline(
    ax, x, y, z=None, cmap=plt.get_cmap("hsv"), norm=plt.Normalize(0.0, 1.0), linewidth=3, alpha=1.0
) -> LineCollection:
    """
    TODO ensure correctness

    Plot a colored line with coordinates x and y
    Optionally specify colors in the array z
    Optionally specify a colormap, a norm function and a line width

    Args:
        ax: axes to plot on
        x: x coordinates
        y: y coordinates
        z: colors?
        cmap: colormap
        norm: normalization function
        linewidth: line width
        alpha: alpha value

    Returns:
        line collection
    """

    # Default colors equally spaced on [0,1]:
    if z is None:
        z = np.linspace(0.0, 1.0, len(x))

    # Special case if a single number:
    if not hasattr(z, "__iter__"):  # to check for numerical input -- this is a hack
        z = np.array([z])

    z = np.asarray(z)

    segments = make_segments(x, y)
    lc = LineCollection(segments, array=z, cmap=cmap, norm=norm, linewidth=linewidth, alpha=alpha)

    # ax = plt.gca()
    ax.add_collection(lc)

    return lc


def calculate_path_2d_limits(path: Path, num_path_samples: int = 100):
    x_min = np.inf
    x_max = -np.inf
    y_min = np.inf
    y_max = -np.inf

    t_range = np.linspace(path.start_time, path.end_time, num_path_samples)

    for t in t_range:
        x, y = path(t)
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)

    xlim = np.array([x_min, x_max])
    ylim = np.array([y_min, y_max])
    return xlim, ylim


def pad_limit(lim: np.ndarray, padding: float) -> np.ndarray:
    low, high = lim
    delta = high - low
    low -= delta * padding
    high += delta * padding
    return np.array([low, high])


def plot_path_2d(
    path: Path,
    xlabel: str = "x",
    ylabel: str = "y",
    xlim: np.ndarray = None,
    ylim: np.ndarray = None,
    padding: float = 0.1,
    cmap: ListedColormap = plt.get_cmap("hsv"),
    grid: bool = True,
    ax: plt.Axes = None,
):

    if xlim is None or ylim is None:
        xlim_auto, ylim_auto = calculate_path_2d_limits(path)
        if xlim is None:
            xlim = xlim_auto
        if ylim is None:
            ylim = ylim_auto

    xlim = pad_limit(xlim, padding)
    ylim = pad_limit(ylim, padding)

    if ax is None:
        _, ax = plt.subplots()

    ax.set_autoscale_on(False)
    ax.set_aspect("equal")

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(*tuple(xlim))
    ax.set_ylim(*tuple(ylim))

    if grid:
        ax.grid()

    points = [path(t) for t in np.linspace(0, path.duration, 100)]
    xs, ys = np.array(points).T

    colorline(ax, xs, ys, cmap=cmap)

    return ax


def animate_path_2d(path: Path, fps: float = 24.0):
    fig, ax = plt.subplots()

    ax = plot_path_2d(path, ax=ax)
    point_artist = ax.plot([], [], "o", color="red")[0]

    plt.close()

    def update(frame):
        point = path(frame)
        point_artist.set_data(*point)
        ax.set_title(f"t = {frame:.2f}")

    num_frames = int(fps * path.duration)
    interval_in_milliseconds = 1000 * path.duration / num_frames
    times = np.linspace(0, path.duration, num_frames)

    animation = FuncAnimation(fig, update, frames=times, interval=interval_in_milliseconds)
    return animation

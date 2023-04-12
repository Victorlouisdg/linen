import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

from linen.path.path import Path


def pad_limit(lim: np.ndarray, padding: float) -> np.ndarray:
    low, high = lim
    delta = high - low
    low -= delta * padding
    high += delta * padding
    return np.array([low, high])


def auto_limits(values, min_range=0.5):
    vmin = np.min(values)
    vmax = np.max(values)
    vrange = vmax - vmin
    if vrange < min_range:
        vcenter = (vmin + vmax) / 2
        vmin = vcenter - min_range / 2
        vmax = vcenter + min_range / 2
    return np.array([vmin, vmax])


def plot_path_3d(
    path: Path,
    xlabel: str = "x",
    ylabel: str = "y",
    zlabel: str = "z",
    xlim: np.ndarray = None,
    ylim: np.ndarray = None,
    zlim: np.ndarray = None,
    padding: float = 0.1,
    grid: bool = True,
    ax: plt.Axes = None,
):
    points = [path(t) for t in np.linspace(0, path.duration, 100)]
    xs, ys, zs = np.array(points).T

    if ax is None:
        _, ax = plt.subplots(subplot_kw={"projection": "3d"})

    ax.set_aspect("equal")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

    if grid:
        ax.grid()

    if xlim is None:
        xlim = auto_limits(xs)
    if ylim is None:
        ylim = auto_limits(ys)
    if zlim is None:
        zlim = auto_limits(zs)

    xlim = pad_limit(xlim, padding)
    ylim = pad_limit(ylim, padding)
    zlim = pad_limit(zlim, padding)

    xrange = xlim[1] - xlim[0]
    yrange = ylim[1] - ylim[0]
    zrange = zlim[1] - zlim[0]
    ax.set_box_aspect((xrange, yrange, zrange))

    ax.plot(xs, ys, zs)
    return ax


def animate_path_3d(path: Path, fps: float = 24.0):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    ax = plot_path_3d(path, ax=ax)
    point_artist = ax.plot([], [], "o", color="red")[0]

    plt.close()

    def update(frame):
        point = path(frame)
        point_artist.set_data(point[:2])
        point_artist.set_3d_properties(point[2])
        ax.set_title(f"t = {frame:.2f}")

    num_frames = int(fps * path.duration)
    interval_in_milliseconds = 1000 * path.duration / num_frames
    times = np.linspace(0, path.duration, num_frames)

    animation = FuncAnimation(fig, update, frames=times, interval=interval_in_milliseconds)
    return animation

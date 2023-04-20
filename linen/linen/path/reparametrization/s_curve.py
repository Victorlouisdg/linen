import numpy as np

from linen.path.path import Path


def s_position_path(maximum_velocity_phase_duration=0.5) -> Path:
    acceleration_phase_duration = (1.0 - maximum_velocity_phase_duration) / 2

    acceleration_phase_end = acceleration_phase_duration
    acceleration_phase_end + maximum_velocity_phase_duration

    q0 = 0.0
    alim = 1.0
    vlim = vmax = 1.0
    v0 = 0.0
    Ta = acceleration_phase_duration
    jmax = 6.0
    jmin = -jmax

    Tj1 = np.sqrt((vmax - v0) / jmax)

    print("Tj1", Tj1)

    def function(t):
        if t < 0.0:
            return q0
        if t < Tj1:
            return q0 + v0 * t + jmax * t**3 / 6.0
        if t < Ta - Tj1:
            return q0 + v0 * t + alim / 6.0 * (3 * t * t - 3 * Tj1 * t + Tj1 * Tj1)
        if t < Ta:
            return q0 + (vlim + v0) * Ta / 2.0 + vlim * (t - Ta) - jmin * (t - Ta) ** 3 / 6.0

        return q0 + (vlim + v0) * Ta / 2.0 + vlim * (t - Ta)

    return Path(function, 0.0, 1.0)

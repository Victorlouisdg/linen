from linen.path.path import Path
from linen.path.transformation.integration import integrated


def s_acceleration_path() -> Path:
    """Acceleration profile that looks like this with two trapezoidal parts.

    Returns:
        Path: The acceleration profile.
    """
    zero_acceleration_duration = 0.5
    constant_accleration_duration = 0.1
    remaining = 1.0 - zero_acceleration_duration - 2 * constant_accleration_duration
    changing_acceleration_duration = remaining / 4

    phase_1_end = changing_acceleration_duration
    phase_2_end = phase_1_end + constant_accleration_duration
    phase_3_end = phase_2_end + changing_acceleration_duration
    phase_4_end = phase_3_end + zero_acceleration_duration
    phase_5_end = phase_4_end + changing_acceleration_duration
    phase_6_end = phase_5_end + constant_accleration_duration

    def function(t):
        if t < phase_1_end:
            return t / changing_acceleration_duration
        if t < phase_2_end:
            return 1.0
        if t < phase_3_end:
            return 1.0 - (t - phase_2_end) / changing_acceleration_duration
        if t < phase_4_end:
            return 0.0
        if t < phase_5_end:
            return -(t - phase_4_end) / changing_acceleration_duration
        if t < phase_6_end:
            return -1.0
        if t < 1.0:
            return -1.0 + (t - phase_6_end) / changing_acceleration_duration
        return 0.0

    return Path(function, 0.0, 1.0)


def s_velocity_path() -> Path:
    return integrated(s_acceleration_path())


def s_position_path() -> Path:
    return integrated(s_velocity_path())

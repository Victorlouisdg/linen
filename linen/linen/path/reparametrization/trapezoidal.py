from linen.path.path import Path

# def trapezoidal_acceleration_path(high_fraction: float = 0.5):
#     high_fraction = 0.5
#     rise_end = (1.0 - high_fraction) / 2
#     fall_start = rise_end + high_fraction

#     def function(t):
#         if t < rise_end:
#             return t / rise_end
#         if t < fall_start:
#             return 1.0
#         if t < 1.0:
#             return (1.0 - t) / (1.0 - fall_start)
#         return 0.0

#     return Path(function, 0.0, 1.0)


def trapezoidal_coefficients(acceleration_phase_duration: float = 0.25):
    q0 = 0.0
    q1 = 1.0
    t0 = 0.0
    t1 = 1.0
    Ta = acceleration_phase_duration
    vv = (q1 - q0) / (t1 - t0 - Ta)

    a0 = q0
    a1 = 0.0
    a2 = vv / (2.0 * Ta)

    b0 = q0 - vv * Ta / 2.0
    b1 = vv

    c0 = q1 - vv * t1 * t1 / (2.0 * Ta)
    c1 = vv * t1 / Ta
    c2 = -vv / (2.0 * Ta)

    return a0, a1, a2, b0, b1, c0, c1, c2


def trapezoidal_acceleration_path(constant_velocity_phase_duration=0.5):
    acceleration_phase_duration = (1.0 - constant_velocity_phase_duration) / 2

    acceleration_phase_end = acceleration_phase_duration
    constant_velocity_phase_end = acceleration_phase_end + constant_velocity_phase_duration

    def function(t):
        if t < 0.0:
            return 0.0
        if t < acceleration_phase_duration:
            return 1.0
        if t < constant_velocity_phase_end:
            return 0.0
        if t <= 1.0:
            return -1.0
        return 0.0

    return Path(function, 0.0, 1.0)


def trapezoidal_velocity_path(constant_velocity_phase_duration=0.5):
    acceleration_phase_duration = (1.0 - constant_velocity_phase_duration) / 2

    acceleration_phase_end = acceleration_phase_duration
    constant_velocity_phase_end = acceleration_phase_end + constant_velocity_phase_duration

    slope = 1.0 / acceleration_phase_duration

    def function(t):
        if t < 0.0:
            return 0.0
        if t < acceleration_phase_duration:
            return slope * t
        if t < constant_velocity_phase_end:
            return 1.0
        if t <= 1.0:
            return 1.0 - slope * (t - constant_velocity_phase_end)
        return 0.0

    return Path(function, 0.0, 1.0)


def trapezoidal_position_path(constant_velocity_phase_duration=0.5):
    acceleration_phase_duration = (1.0 - constant_velocity_phase_duration) / 2

    acceleration_phase_end = acceleration_phase_duration
    constant_velocity_phase_end = acceleration_phase_end + constant_velocity_phase_duration

    # From Section 3.2 Linear Trajectory with Parabolic Blends (Trapezoidal)
    # Trajectory Planning for Automatic Machines and Robots
    a0, a1, a2, b0, b1, c0, c1, c2 = trapezoidal_coefficients(acceleration_phase_duration)

    def function(t):
        if t < 0.0:
            return 0.0
        if t < acceleration_phase_duration:
            return a0 + a1 * t + a2 * t * t
        if t < constant_velocity_phase_end:
            return b0 + b1 * t
        if t <= 1.0:
            return c0 + c1 * t + c2 * t * t
        return 0.0

    return Path(function, 0.0, 1.0)

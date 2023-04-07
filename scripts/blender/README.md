# Trajectory Visualizations
Blender scripts that showcase the main cloth manipulation trajectories from Linen.
In the subdirectories you can find additional visualizations that clarify details.

> :information_source: Requires [airo-blender](https://github.com/airo-ugent/airo-blender) and the URDFs from [urdf-workshop](https://github.com/Victorlouisdg/urdf-workshop).

## Gallery

### 01 - [Slide grasp](01_slide_grasp.py)

![Slide grasp](https://i.imgur.com/qpCIPgA.gif)

An L-shaped grasp trajectory with a constant pitched orientation to slide underneath the a piece of cloth.

### 02 - [Circular arc fold](02_circular_arc_fold.py)

![Circular arc fold](https://i.imgur.com/WO6ndw3.gif)

A circular folding path that start and end with a choosable pitched orientation.

### 03 - [Lift and twist](03_lift_and_twist.py)
![Lift and twist](https://i.imgur.com/Bmm5Scd.gif)

A motion where the gripper move up in a straight line, but at the same time rotates 180 degress.
This could be used e.g. after grasping the lowest point of a towel.
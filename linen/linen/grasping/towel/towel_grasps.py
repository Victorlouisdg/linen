from linen.grasping.edge_grasps import orthogonal_insetted_edge_grasps


def towel_aligned_grasps(ordered_keypoints, grasp_depth=0.05, inset=0.05):
    # Do we need to grasp other edges of the towel?
    edge_start = ordered_keypoints[0]
    edge_end = ordered_keypoints[1]
    return orthogonal_insetted_edge_grasps(edge_start, edge_end, grasp_depth, inset)


# def towel_opposing_grasps(ordered_keypoints, parallel_near_edge=(0, 1)):
#     """TODO: implement

#       1------->0
#       |        |
#     ---->x  x<----
#       |        |
#       |        |
#       |        |
#       2------->3
#     """

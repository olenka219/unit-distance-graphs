from math import cos, sin, pi, acos, sqrt
from graph import Point, Graph

def create_segment_points(angle):
    length = 1
    angle_rad = angle * pi / 180
    p1 = Point(0, 0)
    p2 = Point(length * cos(angle_rad), length * sin(angle_rad))
    return [p1, p2]

segment1_points = create_segment_points(0)
segment2_points = create_segment_points(60)

segment1_graph = Graph(segment1_points)
segment2_graph = Graph(segment2_points)

# First segment
segment1_graph.plot()

# Second segment
segment2_graph.plot()

# Minkowski sum of the two segments
minkowski_sum_graph = segment1_graph.minkowski_sum(segment2_graph)
minkowski_sum_graph.plot()

rotation_angle = 2 * (90 - acos(1 / (2 * sqrt(3))) * 180 / pi)

# Rotate that Minkowski sum
rotated_minkowski_sum_graph = minkowski_sum_graph.rotate(rotation_angle)
rotated_minkowski_sum_graph.plot()

# Moser's spindle which is a union of the original Minkowski sum and the rotated Minkowski sum
union_graph = minkowski_sum_graph.union(rotated_minkowski_sum_graph)
union_graph.plot()

# Coloring the Moser's spindle
union_graph.plot(use_colors=True)

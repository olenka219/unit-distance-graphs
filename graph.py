import numpy as np
import matplotlib.pyplot as plt
from math import cos, sin, sqrt, pi

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

class Graph:
    def __init__(self, points):
        self.points = points
        self.edges = self.create_edges()
        self.color_map = self.greedy_coloring()

    def create_edges(self):
        edges = []
        for i, p1 in enumerate(self.points):
            for j, p2 in enumerate(self.points):
                if i < j and abs(p1.distance_to(p2) - 1) < 1e-15:
                    edges.append((i, j))
        return edges

    def union(self, other):
        new_points = self.points + other.points
        return Graph(new_points)

    def minkowski_sum(self, other):
        new_points = [Point(p1.x + p2.x, p1.y + p2.y) for p1 in self.points for p2 in other.points]
        return Graph(new_points)

    def rotate(self, angle):
        angle_rad = angle * pi / 180
        new_points = [
            Point(p.x * cos(angle_rad) - p.y * sin(angle_rad),
                  p.x * sin(angle_rad) + p.y * cos(angle_rad))
            for p in self.points
        ]
        return Graph(new_points)

    def plot(self, use_colors=False):
        plt.figure()
        for edge in self.edges:
            p1, p2 = self.points[edge[0]], self.points[edge[1]]
            plt.plot([p1.x, p2.x], [p1.y, p2.y], 'bo-')
        if use_colors:
            for i, p in enumerate(self.points):
                plt.plot(p.x, p.y, 'o', color=plt.cm.Set1(self.color_map[i]))
            color_count = max(self.color_map.values()) + 1
            plt.title(f"Graph Coloring: {color_count} colors needed")
        plt.axis('equal')
        plt.show()

    def greedy_coloring(self):
        color_map = {}
        for node in range(len(self.points)):
            available_colors = [True] * len(self.points)
            for edge in self.edges:
                if edge[0] == node and edge[1] in color_map:
                    color = color_map[edge[1]]
                    available_colors[color] = False
                elif edge[1] == node and edge[0] in color_map:
                    color = color_map[edge[0]]
                    available_colors[color] = False

            for color, available in enumerate(available_colors):
                if available:
                    color_map[node] = color
                    break
        return color_map

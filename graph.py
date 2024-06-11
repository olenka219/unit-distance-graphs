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
        self.adj_list = self.create_adj_list()
        self.color_map = self.color_graph()

    def create_edges(self):
        edges = []
        for i, p1 in enumerate(self.points):
            for j, p2 in enumerate(self.points):
                if i < j and abs(p1.distance_to(p2) - 1) < 1e-15:
                    edges.append((i, j))
        return edges

    def create_adj_list(self):
        adj_list = {i: [] for i in range(len(self.points))}
        for u, v in self.edges:
            adj_list[u].append(v)
            adj_list[v].append(u)
        return adj_list

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

        plt.axis('equal')
        plt.axhline(y=0, color='lightgrey', linewidth=0.5)
        plt.axvline(x=0, color='lightgrey', linewidth=0.5)
        plt.xticks([0, 1], labels=['0', '1'])
        plt.yticks([0, 1], labels=['0', '1'])
        plt.grid(True, which='both', linestyle='--', linewidth=0.5, color='lightgrey')
        
        for edge in self.edges:
            p1, p2 = self.points[edge[0]], self.points[edge[1]]
            plt.plot([p1.x, p2.x], [p1.y, p2.y], 'bo-')
        
        if use_colors:
            for i, p in enumerate(self.points):
                plt.plot(p.x, p.y, 'o', color=plt.cm.Set1(self.color_map[i] / 7.0))
            color_count = max(self.color_map.values()) + 1
            plt.title(f"At least {color_count} colors needed")
        
        plt.show()

    def color_graph(self):
        n = len(self.points)
        color_map = [-1] * n

        def is_valid(vertex, color):
            return all(color_map[neighbor] != color for neighbor in self.adj_list[vertex])

        def recursive_color(vertex, m):
            if vertex == n:
                return True

            for color in range(m):
                if is_valid(vertex, color):
                    color_map[vertex] = color
                    if recursive_color(vertex + 1, m):
                        return True
                    color_map[vertex] = -1

            return False

        for m in range(1, 8):
            if recursive_color(0, m):
                return {i: color_map[i] for i in range(n)}

        return {i: color_map[i] for i in range(n)}

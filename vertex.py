# vertex.py
# Author: Rahee
# CS1 LAB 4

from cs1lib import *

# Constants for drawing
CIRCLE_SIZE = 5    # Increased size for better visibility
LINE_WIDTH = 2      # Reduced thickness to reduce clutter

# Define the Vertex class to hold information about each point
# Source: Learned structure from Dartmouth CS10 notes: https://www.cs.dartmouth.edu/~cs10/notes16.html
class Vertex:
    def __init__(self, point_name, x_pos, y_pos):
        # Initialize vertex properties
        self.point_name = point_name    # Name of the location
        self.x_pos = int(x_pos)         # X position on the map
        self.y_pos = int(y_pos)         # Y position on the map
        self.neighbors = []             # List to store nearby points

    # Add a nearby point to the list if not already present
    def add_neighbor(self, nearby_point):
        found = False
        for neighbor in self.neighbors:
            if neighbor == nearby_point:
                found = True
                break
        if not found:
            self.neighbors.append(nearby_point)

    # Draw a circle for this vertex with the given color
    def draw_vertex(self, red, green, blue):
        set_fill_color(red, green, blue)    # Set fill color
        set_stroke_color(red, green, blue)  # Set outline color
        draw_circle(self.x_pos, self.y_pos, CIRCLE_SIZE)  # Draw the circle

    # Draw a line to another vertex with the given color
    def draw_edge(self, other_point, red, green, blue):
        set_stroke_color(red, green, blue)  # Set line color
        set_stroke_width(LINE_WIDTH)        # Set line thickness
        draw_line(self.x_pos, self.y_pos, other_point.x_pos, other_point.y_pos)

    # Draw lines to all nearby vertices
    def draw_all_edges(self, red, green, blue, exclude_path):
        for neighbor in self.neighbors:
            # Skip drawing edges if both vertices are in the path
            if exclude_path and (self in exclude_path and neighbor in exclude_path):
                continue
            self.draw_edge(neighbor, red, green, blue)  # Draw straight line to each neighbor

    # Check if the mouse is near this vertex
    # Source: Mouse checking idea from Dartmouth CS10 slides: https://www.cs.dartmouth.edu/~cs10/slides/Day16.pdf
    def is_on_vertex(self, mouse_x, mouse_y):
        # Check if mouse is within a square around the vertex
        return (abs(self.x_pos - mouse_x) <= CIRCLE_SIZE and
                abs(self.y_pos - mouse_y) <= CIRCLE_SIZE)

    # Return a string representation of the vertex
    def __str__(self):
        nearby_points = ""
        first_time = True
        for v in self.neighbors:
            if not first_time:
                nearby_points = nearby_points + ", " + v.point_name
            else:
                nearby_points = v.point_name
                first_time = False
        return (self.point_name + "; Location: " + str(self.x_pos) + ", " +
                str(self.y_pos) + "; Adjacent vertices: " + nearby_points)
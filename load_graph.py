# load_graph.py
# Author: Rahee
# CS1 LAB 4

from vertex import Vertex

def create_vertex_dictionary(file_name):
    points_dict = {}

    # Open the file and read
    lines = open(file_name, "r").readlines()

    # First pass: Create a Vertex for each line
    for line in lines:
        parts = line.strip().split(";")
        point_name = parts[0].strip()
        coords = parts[2].split(",")
        x = int(coords[0])
        y = int(coords[1])
        # Ensuring coordinates are within window bounds
        x = min(max(x, 0), 1012)  # limit x to window width
        y = min(max(y, 0), 811)   # limiting y to window height
        points_dict[point_name] = Vertex(point_name, x, y)

    # Second pass
    for line in lines:
        parts = line.strip().split(";")
        point_name = parts[0].strip()
        nearby_part = parts[1]
        nearby_names = []
        if nearby_part:
            current_name = ""
            for char in nearby_part:
                if char == ",":
                    if current_name:
                        nearby_names.append(current_name.strip())
                    current_name = ""
                else:
                    current_name = current_name + char
            if current_name:
                nearby_names.append(current_name.strip())
        current_point = points_dict[point_name]
        for nearby_name in nearby_names:
            if nearby_name in points_dict:
                neighbor = points_dict[nearby_name]
                current_point.add_neighbor(neighbor)
                neighbor.add_neighbor(current_point)  # Make graph undirected
            else:
                print("Warning: " + nearby_name + " not found in points_dict for " + point_name)

    return points_dict
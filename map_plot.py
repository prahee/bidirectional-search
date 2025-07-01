# map_plot.py
# Author: Rahee
# CS1 LAB 4

from cs1lib import *
from load_graph import create_vertex_dictionary
from bidirectional_bfs import bidirectional_bfs

# Window and map settings
WINDOW_WIDTH = 1012
WINDOW_HEIGHT = 811
MAP_IMAGE_FILE = "dartmouth_map.png"

graph = create_vertex_dictionary("dartmouth_graph.txt")
map_img = load_image(MAP_IMAGE_FILE)

# Print to check loading
print("Map image: " + str(map_img))
print("Number of points: " + str(len(graph)))

start_points = []
path = []
start_visited = {}
goal_visited = []
all_visited = []
ctrl_pressed = False
drawn_edges = []
ARROW_SIZE = 5
ANGLE = 0.5

def draw():
    clear()
    draw_image(map_img, 0, 0)

    global drawn_edges
    drawn_edges = []

    for point in graph.values():
        point.draw_all_edges(0, 0, 1, path)

    for point in graph.values():
        if point in start_points:
            point.draw_vertex(0, 1, 0)  # Green -- start points
        elif point in path and not (point in start_points):
            point.draw_vertex(1, 0, 0)  # Red -- path
        elif point in start_visited:
            distance = start_visited[point][1]
            if distance == 0:
                point.draw_vertex(0, 1, 0)  # Green
            elif distance == 1:
                point.draw_vertex(1, 1, 0)  # Yellow
            elif distance == 2:
                point.draw_vertex(1, 0.5, 0)  # Orange
            else:
                point.draw_vertex(1, 0, 0)  # Red for 3+
        elif point in goal_visited:
            point.draw_vertex(0.5, 0.5, 0)  # Olive -- goal visited
        elif point in all_visited:
            point.draw_vertex(0, 1, 1)  # Cyan -- frontier
        else:
            point.draw_vertex(0, 0, 1)  # Blue -- unvisited

    # Draw the path with arrows if it exists :)
    if path and len(path) > 1:
        i = 0
        while i < len(path) - 1:
            # Draw the path segment
            path[i].draw_edge(path[i + 1], 1, 0, 0)  # Draw path in red
            # Draw arrow for direction, skip if last segment loops back to start
            if i == len(path) - 2 and path[i + 1] == path[0]:
                i = i + 1
                continue
            x1 = path[i].x_pos
            y1 = path[i].y_pos
            x2 = path[i + 1].x_pos
            y2 = path[i + 1].y_pos
            # Calculate direction vector
            dx = x2 - x1
            dy = y2 - y1
            # Normalize direction vector
            length = (dx * dx + dy * dy) ** 0.5
            if length == 0:  # Avoid division by zero
                i = i + 1
                continue
            dx = dx / length
            dy = dy / length
            # Calculate perpendicular vector for arrowhead
            perp_x = -dy
            perp_y = dx
            # Calculate arrowhead points
            arrow_base_x = x2 - dx * 10  # Move back along the path
            arrow_base_y = y2 - dy * 10
            arrow_tip1_x = arrow_base_x + perp_x * ARROW_SIZE
            arrow_tip1_y = arrow_base_y + perp_y * ARROW_SIZE
            arrow_tip2_x = arrow_base_x - perp_x * ARROW_SIZE
            arrow_tip2_y = arrow_base_y - perp_y * ARROW_SIZE
            set_stroke_color(1, 0, 0)  # Red arrows
            draw_line(int(x2), int(y2), int(arrow_tip1_x), int(arrow_tip1_y))
            draw_line(int(x2), int(y2), int(arrow_tip2_x), int(arrow_tip2_y))
            i = i + 1

        # Displaying start and goal names
        set_stroke_color(1, 0.2, 0.6)  # pink text
        draw_text(start_points[0].point_name, start_points[0].x_pos - 10, start_points[0].y_pos - 20)
        draw_text(path[len(path) - 1].point_name, path[len(path) - 1].x_pos - 10, path[len(path) - 1].y_pos - 20)

        # Display path length
        path_length = str(len(path) - 1)
        draw_text("Length: " + path_length, path[len(path) - 1].x_pos - 20, path[len(path) - 1].y_pos - 40)

# Find a vertex at the given mouse position
def find_vertex(mouse_x, mouse_y):
    for point in graph.values():
        if point.is_on_vertex(mouse_x, mouse_y):
            return point
    return None

# key press events
def key_press(key):
    global ctrl_pressed, start_points, path, start_visited, goal_visited, all_visited
    if key == "r":  # Reset -- 'r' key
        start_points = []
        path = []
        start_visited = {}
        goal_visited = []
        all_visited = []
    elif key == "control":
        ctrl_pressed = True

# key release events
def key_release(key):
    global ctrl_pressed
    if key == "control":
        ctrl_pressed = False

# mouse press events
def mouse_press(mouse_x, mouse_y):
    global start_points, path, start_visited, goal_visited, all_visited
    vertex = find_vertex(mouse_x, mouse_y)
    if vertex and ctrl_pressed:
        found = False
        for sp in start_points:
            if sp == vertex:
                found = True
                break
        if not found:
            start_points.append(vertex)
        path, start_visited, goal_visited, all_visited = bidirectional_bfs(start_points, None)
    elif vertex:
        start_points = [vertex]
        path, start_visited, goal_visited, all_visited = bidirectional_bfs(start_points, None)

# mouse move events
def mouse_move(mouse_x, mouse_y):
    global path, start_visited, goal_visited, all_visited
    if start_points != [] : # Check if start_points is not empty
        goal_vertex = find_vertex(mouse_x, mouse_y)
        if goal_vertex:
            path, start_visited, goal_visited, all_visited = bidirectional_bfs(start_points, goal_vertex)
        else:
            path, start_visited, goal_visited, all_visited = bidirectional_bfs(start_points, None)

start_graphics(draw, width=WINDOW_WIDTH, height=WINDOW_HEIGHT,
               mouse_press=mouse_press, mouse_move=mouse_move,
               key_press=key_press, key_release=key_release)
# bidirectional_bfs.py
# Author: Rahee
# CS1 LAB 4

from collections import deque

def bidirectional_bfs(start_points, goal_point):
    if not start_points or not goal_point:
        return [], {}, [], []

    # closest start point
    CLOSEST_DISTANCE = 1000000  # large number for infinity
    closest_start = None
    all_start_visited = {}
    all_start_frontier = []
    for start in start_points:
        queue = deque([start])
        visited = {start: [None, 0]}  # [parent, distance]
        frontier = [start]
        while queue:
            current = queue.popleft()
            i = 0
            while i < len(frontier):
                if frontier[i] == current:
                    frontier.pop(i)
                    break
                i = i + 1
            for neighbor in current.neighbors:
                if neighbor not in visited:
                    visited[neighbor] = [current, visited[current][1] + 1]
                    queue.append(neighbor)
                    found = False
                    for f in frontier:
                        if f == neighbor:
                            found = True
                    if not found:
                        frontier.append(neighbor)
        all_start_visited[start] = visited
        for f in frontier:
            all_start_frontier.append(f)
        if goal_point in visited:
            distance = visited[goal_point][1]
            if distance < CLOSEST_DISTANCE:
                CLOSEST_DISTANCE = distance
                closest_start = start

    if closest_start is None:
        return [], {}, [], []

    # The cases where start and goal are the same
    if closest_start == goal_point:
        return [closest_start], {closest_start: [None, 0]}, [], all_start_visited.keys()

    # Run bidirectional BFS from closest start
    start = closest_start
    start_queue = deque([start])
    goal_queue = deque([goal_point])
    start_visited = {start: [None, 0]}
    goal_visited = {goal_point: [None, 0]}
    start_frontier = [start]
    goal_frontier = [goal_point]

    while start_queue and goal_queue:
        current_start = start_queue.popleft()
        i = 0
        while i < len(start_frontier):
            if start_frontier[i] == current_start:
                start_frontier.pop(i)
                break
            i = i + 1
        for neighbor in current_start.neighbors:
            if neighbor not in start_visited:
                start_visited[neighbor] = [current_start, start_visited[current_start][1] + 1]
                start_queue.append(neighbor)
                if neighbor in goal_visited:
                    path = []
                    current = neighbor
                    while current is not None and current != start:
                        path.append(current)
                        parent = start_visited[current][0]
                        current = parent
                    if current == start:
                        path.append(start)
                    # Reverse the path
                    reversed_path = []
                    i = len(path) - 1
                    while i >= 0:
                        reversed_path.append(path[i])
                        i = i - 1
                    path = reversed_path
                    # Path from meeting point to goal
                    current = goal_visited[neighbor][0]
                    while current is not None and current != goal_point:
                        found = False
                        for p in path:
                            if p == current:
                                found = True
                        if not found:
                            path.append(current)
                        parent = goal_visited[current][0]
                        current = parent
                    if goal_point not in path:
                        path.append(goal_point)
                    return path, start_visited, goal_visited.keys(), all_start_visited.keys()
                found = False
                for f in start_frontier:
                    if f == neighbor:
                        found = True
                if not found:
                    start_frontier.append(neighbor)

        # Search from goal
        current_goal = goal_queue.popleft()
        i = 0
        while i < len(goal_frontier):
            if goal_frontier[i] == current_goal:
                goal_frontier.pop(i)
                break
            i = i + 1
        for neighbor in current_goal.neighbors:
            if neighbor not in goal_visited:
                goal_visited[neighbor] = [current_goal, goal_visited[current_goal][1] + 1]
                goal_queue.append(neighbor)
                if neighbor in start_visited:
                    path = []
                    # Path from meeting point to start
                    current = neighbor
                    while current is not None and current != start:
                        path.append(current)
                        parent = start_visited[current][0]
                        current = parent
                    if current == start:
                        path.append(start)
                    # Reverse the path
                    reversed_path = []
                    i = len(path) - 1
                    while i >= 0:
                        reversed_path.append(path[i])
                        i = i - 1
                    path = reversed_path
                    # Path from meeting point to goal
                    current = goal_visited[neighbor][0]
                    while current is not None and current != goal_point:
                        found = False
                        for p in path:
                            if p == current:
                                found = True
                        if not found:
                            path.append(current)
                        parent = goal_visited[current][0]
                        current = parent
                    if goal_point not in path:
                        path.append(goal_point)
                    return path, start_visited, goal_visited.keys(), all_start_visited.keys()
                found = False
                for f in goal_frontier:
                    if f == neighbor:
                        found = True
                if not found:
                    goal_frontier.append(neighbor)

    return [], start_visited, goal_visited.keys(), all_start_visited.keys()
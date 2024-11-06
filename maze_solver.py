import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import random

# Load the maze image
maze_img = mpimg.imread('maze-2.png')

# Convert the image to a binary maze (0 for paths, 1 for walls)
maze = (np.mean(maze_img, axis=2) < 0.5).astype(int)  # Adjust threshold if necessary

# Display the maze
plt.imshow(maze, cmap='gray_r') # Use 'gray_r' to invert colors for display
plt.title('Maze')
plt.show()


def solve_maze_backtracking(maze):
    rows, cols = maze.shape
    solution = np.zeros((rows, cols), dtype=int)
    path = []

    def is_safe(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[x, y] == 0 and solution[x, y] == 0

    def backtrack(x, y):
        print(f"Visiting: ({x}, {y})") # Debug statement
        if x == rows - 1:  # Exit found
            solution[x, y] = 1
            path.append((x, y))
            print("Exit found!") # Debug statement
            return True
        if is_safe(x, y):
            solution[x, y] = 1
            path.append((x, y))
            if backtrack(x + 1, y) or backtrack(x, y + 1) or backtrack(x - 1, y) or backtrack(x, y - 1):
                return True
            solution[x, y] = 0
            path.pop()
            print(f"Backtracking from: ({x}, {y})") # Debug statement
        return False

    if not backtrack(0, 0):
        print("No solution found")
    return solution, path

def solve_maze_las_vegas(maze):
    rows, cols = maze.shape
    solution = np.zeros((rows, cols), dtype=int)
    path = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    x, y = 0, 0
    steps = 0
    while steps < 400 and not (x == rows - 1):
        if maze[x, y] == 0 and solution[x, y] == 0:
            solution[x, y] = 1
            path.append((x, y))
            print(f"Visiting: ({x}, {y}), Steps: {steps}") # Debug statement
            if x == rows - 1:
                print("Exit found!") # Debug statement
                break
            random.shuffle(directions)
            for dx, dy in directions:
                if 0 <= x + dx < rows and 0 <= y + dy < cols and maze[x + dx, y + dy] == 0 and solution[x + dx, y + dy] == 0:
                    x, y = x + dx, y + dy
                    break
        steps += 1

    if x != rows - 1:
        print("No solution found in 400 steps")
    return solution, path

# Ask the user for the approach
approach = input("Choose an approach (Backtracking or Las Vegas): ").strip().lower()

if approach == "backtracking":
    solution, path = solve_maze_backtracking(maze)
elif approach == "las vegas":
    solution, path = solve_maze_las_vegas(maze)
else:
    print("Invalid approach selected")


# Visualize visited squares in both successful and unsuccessful attempts
def visualize_path(maze, path, title): 
    # Make a copy of the maze so we don't change the original
    maze_copy = maze.copy()
    # Mark the squares we visited on the path
    for x, y in path:
        maze_copy[x, y] = 0.5 # 0.5 makes the path show up in black
    # Display the maze with the path
    plt.imshow(maze_copy, cmap='gray_r')
    plt.title(title)
    plt.show()

visualize_path(maze, path, f"{approach.capitalize()} Path")


# Calculate success rates
def calculate_success_rate(solver_func, maze, runs):
    success_count = 0
    for _ in range(runs):
        _, path = solver_func(maze)
        if path and path[-1][0] == maze.shape[0] - 1:
            success_count += 1
    return success_count / runs

backtracking_success_rate = calculate_success_rate(solve_maze_backtracking, maze, 10000)
las_vegas_success_rate = calculate_success_rate(solve_maze_las_vegas, maze, 10000)

# Print success rates
print(f"Backtracking Success Rate: {backtracking_success_rate * 100:.2f}%")
print(f"Las Vegas Success Rate: {las_vegas_success_rate * 100:.2f}%")

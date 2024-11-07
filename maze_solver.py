import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import random

# Load the maze image
maze_img = mpimg.imread('maze-2.png')

# Convert the image to a binary maze (0 for paths, 1 for walls)
maze = (np.mean(maze_img, axis=2) < 0.5).astype(int)  # Adjust threshold if necessary

# Find the bounding box manually
rows = np.any(maze, axis=1)
cols = np.any(maze, axis=0)
min_row, max_row = np.where(rows)[0][0], np.where(rows)[0][-1] + 1
min_col, max_col = np.where(cols)[0][0], np.where(cols)[0][-1] + 1

# Crop the maze using the bounding box coordinates
cropped_maze = maze[min_row:max_row, min_col:max_col]

# Resize the cropped maze to 21x21 using interpolation
resized_maze = np.zeros((21, 21), dtype=int)
scale_y, scale_x = cropped_maze.shape[0] / 21, cropped_maze.shape[1] / 21

for y in range(21):
    for x in range(21):
        orig_y, orig_x = int(y * scale_y), int(x * scale_x)
        resized_maze[y, x] = cropped_maze[orig_y, orig_x]

# Display the resized maze
plt.imshow(resized_maze, cmap='gray_r')
plt.axis('off')  # Hide the axes
plt.title('Maze')
plt.show()


def solve_maze_backtracking(maze):
    rows, cols = maze.shape
    solution = np.zeros((rows, cols), dtype=int)
    path = []

    def is_safe(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[y, x] == 0 and solution[y, x] == 0

    def backtrack(x, y):
        print(f"Visiting: ({x}, {y})") # Debug statement
        if (x == cols - 1 or y == rows - 1) and maze[y, x] == 0:
            solution[y, x] = 1
            path.append((x, y))
            print("Exit found!") # Debug statement
            return True
        if is_safe(x, y):
            solution[y, x] = 1
            path.append((x, y))
            if backtrack(x + 1, y) or backtrack(x, y + 1) or backtrack(x - 1, y) or backtrack(x, y - 1):
                return True
            solution[y, x] = 0
            path.pop()
            print(f"Backtracking from: ({x}, {y})") # Debug statement
        return False

    if not backtrack(9, 0):
        print("No solution found")
    return solution, path

def solve_maze_las_vegas(maze):
    rows, cols = maze.shape
    solution = np.zeros((rows, cols), dtype=int)
    path = []
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    x, y = 9, 0
    steps = 0
    while steps < 400 and not (x == rows - 1):
        if maze[y, x] == 0 and solution[y, x] == 0:
            solution[y, x] = 1
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
    solution, path = solve_maze_backtracking(resized_maze)
elif approach == "las vegas":
    solution, path = solve_maze_las_vegas(resized_maze)
else:
    print("Invalid approach selected")


# Visualize visited squares in both successful and unsuccessful attempts
def visualize_path(maze, path, title): 
    # Make a copy of the maze so we don't change the original
    maze_copy = maze.copy()
    # Mark the squares we visited on the path
    for x, y in path:
        maze_copy[y, x] = 0.5 # 0.5 makes the path show up in black
    # Display the maze with the path
    plt.imshow(maze_copy, cmap='gray_r')
    plt.title(title)
    plt.show()

visualize_path(resized_maze, path, f"{approach.capitalize()} Path")

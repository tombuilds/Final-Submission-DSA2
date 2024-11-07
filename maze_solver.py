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

    x, y = 9, 0  # Starting position
    steps = 0
    exit_found = False
    while steps < 400:
        if maze[y, x] == 0 and solution[y, x] == 0:
            solution[y, x] = 1
            path.append((x, y))
            print(f"Visiting: ({x}, {y}), Steps: {steps}")  # Debug statement
            if (x == cols - 1 or y == rows - 1):
                print("Exit found!")  # Debug statement
                exit_found = True
                break
            random.shuffle(directions)
            move_found = False
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < cols and 0 <= new_y < rows and maze[new_y, new_x] == 0 and solution[new_y, new_x] == 0:
                    x, y = new_x, new_y
                    move_found = True
                    break
            if not move_found:
                # If no valid move is found, restart from a random location
                x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
        else:
            # If the current position is invalid, restart from a random location
            x, y = random.randint(0, rows - 1), random.randint(0, cols - 1)
        steps += 1

    if not exit_found and steps >= 400:
        print("Reached maximum steps without finding an exit")
    return solution, path

# Ask the user for the approach
approach = input("Choose an approach (1 for Backtracking, 2 for Las Vegas): ").strip()

if approach == "1":
    solution, path = solve_maze_backtracking(resized_maze)
elif approach == "2":
    solution, path = solve_maze_las_vegas(resized_maze)
else:
    print("Invalid approach selected")


# Visualize visited squares in both successful and unsuccessful attempts
def visualize_path(maze, path, title): 
    # Convert the maze to a floating-point array to handle all values correctly
    maze_copy = maze.astype(float).copy()
    # Mark the squares we visited on the path
    for x, y in path:
        maze_copy[y, x] = 0.5 # 0.5 makes the path show up in black
    # Display the maze with the path
    plt.imshow(maze_copy, cmap='gray_r', vmin=0, vmax=1)
    plt.title(title)
    plt.show()

visualize_path(resized_maze, path, f"{approach.capitalize()} Path")

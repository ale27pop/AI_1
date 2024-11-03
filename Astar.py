import pygame
from queue import PriorityQueue

# Initialize Pygame
pygame.init()

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Pastel Colors
PASTEL_WHITE = (255, 240, 245) 
PASTEL_BLACK = (189, 189, 189) 
PASTEL_ORANGE = (255, 204, 204)  
PASTEL_TURQUOISE = (173, 216, 230) 
PASTEL_PURPLE = (200, 162, 200)  
PASTEL_GREY = (200, 200, 200)  
PASTEL_RED = (255, 182, 193)  
PASTEL_GREEN = (152, 251, 152)  
BRIGHT_PINK = (255, 105, 180)  # Path

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = PASTEL_WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == PASTEL_RED

    def is_open(self):
        return self.color == PASTEL_GREEN

    def is_barrier(self):
        return self.color == PASTEL_BLACK

    def reset(self):
        self.color = PASTEL_WHITE

    def make_start(self):
        self.color = PASTEL_ORANGE

    def make_closed(self):
        self.color = PASTEL_RED

    def make_open(self):
        self.color = PASTEL_GREEN

    def make_barrier(self):
        self.color = PASTEL_BLACK

    def make_end(self):
        self.color = PASTEL_TURQUOISE

    def make_path(self):
        self.color = BRIGHT_PINK  

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # Right
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

def h(p1, p2):
    # Heuristic function for A*
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    path = []
    while current in came_from:
        path.append(current.get_pos())  # Append each coordinate to path list
        current = came_from[current]
        current.make_path()
        draw()
    
    # Since we trace the path from end to start, reverse it to display from start to end
    path.reverse()
    print_path(path)

def print_path(path):
    print("Path")
    print("Start:")
    for coord in path:
        print(f"  {coord},")
    print("Goal")
    print(f"Length: {len(path)} steps")

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True  # Path found

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    show_message("Impossible")  #no path is found
    return False

def show_message(message):
    font = pygame.font.Font(None, 50)
    text_surface = font.render(message, True, (255, 0, 0))  # Red color text
    text_rect = text_surface.get_rect(center=(WIDTH // 2, WIDTH // 2))
    
    # Display the message for 2 seconds
    WIN.blit(text_surface, text_rect)
    pygame.display.update()
    pygame.time.delay(2000) 

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, PASTEL_GREY, (0, i * gap), (width, i * gap))  # Horizontal lines
        for j in range(rows):
            pygame.draw.line(win, PASTEL_GREY, (j * gap, 0), (j * gap, width))  # Vertical lines

def draw(win, grid, rows, width):
    win.fill(PASTEL_WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]

                if not start and spot != end:
                    start = spot
                    start.make_start()

                elif not end and spot != start:
                    end = spot
                    end.make_end()

                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:  # Clear the grid
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)

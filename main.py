import pygame
import sys
import random

pygame.init()

# Window icon
icon_surface = pygame.Surface((32, 32))
icon_surface.fill((25, 25, 25))
glider_cells = [(16, 4), (24, 12), (8, 20), (16, 20), (24, 20)]
for cx, cy in glider_cells:
    pygame.draw.rect(icon_surface, (220, 220, 220), (cx, cy, 7, 7), border_radius=2)
pygame.display.set_icon(icon_surface)

# Set up the window
width = 1500  # Needs to be a multiplication of 15
height = 825  # Needs to be a multiplication of 15
background_color = (15, 15, 18)
window_size = (width, height)

# Set up the sidebar
sidebar_width = 150
sidebar_color = (20, 20, 22)
sidebar_rect = pygame.Rect(width, 0, sidebar_width, height)

# Buttons
button_start_color = (55, 160, 95)
button_stop_color = (200, 80, 80)
button_default_color = (65, 65, 70)
button_random_color = (80, 70, 120)

font = pygame.font.SysFont("Arial", 13, bold=True)
font_color = (245, 245, 245)
start_text = font.render("START", True, font_color)
stop_text = font.render("STOP", True, font_color)
restart_text = font.render("RESTART", True, font_color)
random_text = font.render("RANDOM", True, font_color)

buttons_width = 110
button_height = 32
button_margin = (sidebar_width - buttons_width) // 2

start_y = 30
spacing = 10        
group_spacing = 40  

start_button_rect = pygame.Rect(width + button_margin, start_y, buttons_width, button_height)
stop_button_rect = pygame.Rect(width + button_margin, start_button_rect.bottom + spacing, buttons_width, button_height)
restart_button_rect = pygame.Rect(width + button_margin, stop_button_rect.bottom + spacing, buttons_width, button_height)

# Patterns
pat_glider = [(-1, 0), (0, 1), (1, -1), (1, 0), (1, 1)]
pat_pulsar = []
for i in [-6, -1, 1, 6]:
    for j in [-4, -3, -2, 2, 3, 4]:
        pat_pulsar.append((i, j))
        pat_pulsar.append((j, i))
        
pat_spaceship = [
    (-1, -1), (-1, 2),
    (0, -2),
    (1, -2), (1, 2),
    (2, -2), (2, -1), (2, 0), (2, 1)
]

gun_raw = [
    (0, 24), (1, 22), (1, 24), 
    (2, 12), (2, 13), (2, 20), (2, 21), (2, 34), (2, 35),
    (3, 11), (3, 15), (3, 20), (3, 21), (3, 34), (3, 35),
    (4, 0), (4, 1), (4, 10), (4, 16), (4, 20), (4, 21),
    (5, 0), (5, 1), (5, 10), (5, 14), (5, 16), (5, 17), (5, 22), (5, 24),
    (6, 10), (6, 16), (6, 24),
    (7, 11), (7, 15),
    (8, 12), (8, 13)
]
pat_generator = [(r - 4, c - 17) for r, c in gun_raw]

upward_gun_raw = [
    (0, 24), (-1, 22), (-1, 24), 
    (-2, 12), (-2, 13), (-2, 20), (-2, 21), (-2, 34), (-2, 35),
    (-3, 11), (-3, 15), (-3, 20), (-3, 21), (-3, 34), (-3, 35),
    (-4, 0), (-4, 1), (-4, 10), (-4, 16), (-4, 20), (-4, 21),
    (-5, 0), (-5, 1), (-5, 10), (-5, 14), (-5, 16), (-5, 17), (-5, 22), (-5, 24),
    (-6, 10), (-6, 16), (-6, 24),
    (-7, 11), (-7, 15),
    (-8, 12), (-8, 13)
]
pat_rocket = [(r + 4, c - 17) for r, c in upward_gun_raw]

patterns_label = font.render("PATTERNS:", True, (150, 150, 160))
glider_text = font.render("GLIDER", True, font_color)
pulsar_text = font.render("PULSAR", True, font_color)
spaceship_text = font.render("SPACESHIP", True, font_color)
generator_text = font.render("GOSPER GUN", True, font_color)
rocket_text = font.render("UPWARD GUN", True, font_color)

patterns_label_y = restart_button_rect.bottom + group_spacing
glider_btn_rect = pygame.Rect(width + button_margin, patterns_label_y + 25, buttons_width, button_height)
pulsar_btn_rect = pygame.Rect(width + button_margin, glider_btn_rect.bottom + spacing, buttons_width, button_height)
spaceship_btn_rect = pygame.Rect(width + button_margin, pulsar_btn_rect.bottom + spacing, buttons_width, button_height)
generator_btn_rect = pygame.Rect(width + button_margin, spaceship_btn_rect.bottom + spacing, buttons_width, button_height)
rocket_btn_rect = pygame.Rect(width + button_margin, generator_btn_rect.bottom + spacing, buttons_width, button_height)

# Przesunięta sekcja z Random i Sliderem
random_btn_y = rocket_btn_rect.bottom + group_spacing
random_button_rect = pygame.Rect(width + button_margin, random_btn_y, buttons_width, button_height)

slider_val = 0.5
is_dragging_slider = False
slider_label_y = random_button_rect.bottom + 20
slider_rect = pygame.Rect(width + button_margin, slider_label_y + 22, buttons_width, 6)
slider_hitbox = pygame.Rect(width + button_margin, slider_rect.y - 10, buttons_width, 26)

# Changable cell size (15, 5, 3, 1)
cell_size = 5

grid_width = int(width / cell_size)
grid_height = int(height / cell_size)

print(grid_width, grid_height)

# Initialize
screen = pygame.display.set_mode((width + sidebar_width, height))
pygame.display.set_caption("Game Of Life")

grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
is_playing = False
clock = pygame.time.Clock()
fps = 15
alive_cell_color = (235, 235, 240)

draw_start_pos = None
locked_axis = None
draw_val = 1 
selected_pattern = None

def count_neighbors(grid, row, col):
    live_neighbors = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            r, c = row + i, col + j
            if 0 <= r < grid_height and 0 <= c < grid_width:
                live_neighbors += grid[r][c]
    return live_neighbors

def update_grid(current_grid):
    new_grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    for row in range(grid_height):
        for col in range(grid_width):
            live_neighbors = count_neighbors(current_grid, row, col)
            if current_grid[row][col] == 1:
                if live_neighbors in (2, 3):
                    new_grid[row][col] = 1
            else:
                if live_neighbors == 3:
                    new_grid[row][col] = 1
                    
    for col in range(grid_width):
        new_grid[0][col] = 0
        new_grid[grid_height - 1][col] = 0
    for row in range(grid_height):
        new_grid[row][0] = 0
        new_grid[row][grid_width - 1] = 0
        
    return new_grid

running = True
while running:
    mouse = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    is_shift_pressed = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if start_button_rect.collidepoint(mouse):
                    is_playing = True
                elif stop_button_rect.collidepoint(mouse):
                    is_playing = False
                elif restart_button_rect.collidepoint(mouse):
                    is_playing = False
                    grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
                elif random_button_rect.collidepoint(mouse):
                    grid = [[1 if random.random() < slider_val else 0 for _ in range(grid_width)] for _ in range(grid_height)]
                elif glider_btn_rect.collidepoint(mouse):
                    selected_pattern = pat_glider if selected_pattern != pat_glider else None
                elif pulsar_btn_rect.collidepoint(mouse):
                    selected_pattern = pat_pulsar if selected_pattern != pat_pulsar else None
                elif spaceship_btn_rect.collidepoint(mouse):
                    selected_pattern = pat_spaceship if selected_pattern != pat_spaceship else None
                elif generator_btn_rect.collidepoint(mouse):
                    selected_pattern = pat_generator if selected_pattern != pat_generator else None
                elif rocket_btn_rect.collidepoint(mouse):
                    selected_pattern = pat_rocket if selected_pattern != pat_rocket else None
                elif slider_hitbox.collidepoint(mouse):
                    is_dragging_slider = True
                elif mouse[0] < width: 
                    col = mouse[0] // cell_size
                    row = mouse[1] // cell_size
                    if selected_pattern:
                        for dr, dc in selected_pattern:
                            r, c = row + dr, col + dc
                            if 0 <= r < grid_height and 0 <= c < grid_width:
                                grid[r][c] = 1
                    else:
                        grid[row][col] = 1
                        draw_start_pos = (col, row)
                        locked_axis = None
                        draw_val = 1
                    
            elif event.button == 3:
                if selected_pattern:
                    selected_pattern = None
                elif mouse[0] < width:
                    col = mouse[0] // cell_size
                    row = mouse[1] // cell_size
                    grid[row][col] = 0
                    draw_start_pos = (col, row)
                    locked_axis = None
                    draw_val = 0
                    
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                draw_start_pos = None
                locked_axis = None
                is_dragging_slider = False
            elif event.button == 3:
                draw_start_pos = None
                locked_axis = None
                
        elif event.type == pygame.MOUSEMOTION:
            if is_dragging_slider:
                rel_x = mouse[0] - slider_rect.x
                slider_val = max(0.0, min(1.0, rel_x / slider_rect.width))
                
            is_drawing = pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]
            
            if is_drawing and mouse[0] < width and not is_dragging_slider and not selected_pattern:
                col = mouse[0] // cell_size
                row = mouse[1] // cell_size
                
                if is_shift_pressed and draw_start_pos:
                    if locked_axis is None:
                        if col != draw_start_pos[0] or row != draw_start_pos[1]:
                            if abs(col - draw_start_pos[0]) > abs(row - draw_start_pos[1]):
                                locked_axis = 'horizontal'
                            else:
                                locked_axis = 'vertical'
                                
                    if locked_axis == 'horizontal':
                        row = draw_start_pos[1]
                    elif locked_axis == 'vertical':
                        col = draw_start_pos[0]
                        
                grid[row][col] = draw_val

    if is_playing:
        grid = update_grid(grid)
        clock.tick(fps)
    else:
        clock.tick(60)

    screen.fill(background_color)

    for row in range(grid_height):
        for col in range(grid_width):
            if grid[row][col] == 1:
                cell_rect = pygame.Rect(col * cell_size + 1, row * cell_size + 1, cell_size - 2, cell_size - 2)
                pygame.draw.rect(screen, alive_cell_color, cell_rect, border_radius=3)

    pygame.draw.rect(screen, sidebar_color, sidebar_rect)
    pygame.draw.line(screen, (30, 30, 35), (width, 0), (width, height), 1)

    start_color = (70, 180, 110) if start_button_rect.collidepoint(mouse) or is_playing else button_start_color
    stop_color = (220, 100, 100) if stop_button_rect.collidepoint(mouse) or not is_playing else button_stop_color
    restart_color = (85, 85, 90) if restart_button_rect.collidepoint(mouse) else button_default_color
    random_color = (100, 90, 150) if random_button_rect.collidepoint(mouse) else button_random_color

    pygame.draw.rect(screen, start_color, start_button_rect, border_radius=4)
    pygame.draw.rect(screen, stop_color, stop_button_rect, border_radius=4)
    pygame.draw.rect(screen, restart_color, restart_button_rect, border_radius=4)
    pygame.draw.rect(screen, random_color, random_button_rect, border_radius=4)

    screen.blit(start_text, (start_button_rect.x + (start_button_rect.width - start_text.get_width()) // 2,
                             start_button_rect.y + (start_button_rect.height - start_text.get_height()) // 2))
    screen.blit(stop_text, (stop_button_rect.x + (stop_button_rect.width - stop_text.get_width()) // 2,
                            stop_button_rect.y + (stop_button_rect.height - stop_text.get_height()) // 2))
    screen.blit(restart_text, (restart_button_rect.x + (restart_button_rect.width - restart_text.get_width()) // 2,
                               restart_button_rect.y + (restart_button_rect.height - restart_text.get_height()) // 2))
    screen.blit(random_text, (random_button_rect.x + (random_button_rect.width - random_text.get_width()) // 2,
                               random_button_rect.y + (random_button_rect.height - random_text.get_height()) // 2))

    patterns_x = width + (sidebar_width - patterns_label.get_width()) // 2
    screen.blit(patterns_label, (patterns_x, patterns_label_y))
    
    pat_base = (45, 80, 110)
    pat_hover = (60, 100, 130)
    pat_active = (80, 140, 180)
    
    def get_pat_color(rect, pat):
        if selected_pattern == pat: return pat_active
        if rect.collidepoint(mouse): return pat_hover
        return pat_base

    pygame.draw.rect(screen, get_pat_color(glider_btn_rect, pat_glider), glider_btn_rect, border_radius=4)
    pygame.draw.rect(screen, get_pat_color(pulsar_btn_rect, pat_pulsar), pulsar_btn_rect, border_radius=4)
    pygame.draw.rect(screen, get_pat_color(spaceship_btn_rect, pat_spaceship), spaceship_btn_rect, border_radius=4)
    pygame.draw.rect(screen, get_pat_color(generator_btn_rect, pat_generator), generator_btn_rect, border_radius=4)
    pygame.draw.rect(screen, get_pat_color(rocket_btn_rect, pat_rocket), rocket_btn_rect, border_radius=4)

    screen.blit(glider_text, (glider_btn_rect.x + (glider_btn_rect.width - glider_text.get_width()) // 2,
                              glider_btn_rect.y + (glider_btn_rect.height - glider_text.get_height()) // 2))
    screen.blit(pulsar_text, (pulsar_btn_rect.x + (pulsar_btn_rect.width - pulsar_text.get_width()) // 2,
                              pulsar_btn_rect.y + (pulsar_btn_rect.height - pulsar_text.get_height()) // 2))
    screen.blit(spaceship_text, (spaceship_btn_rect.x + (spaceship_btn_rect.width - spaceship_text.get_width()) // 2,
                           spaceship_btn_rect.y + (spaceship_btn_rect.height - spaceship_text.get_height()) // 2))
    screen.blit(generator_text, (generator_btn_rect.x + (generator_btn_rect.width - generator_text.get_width()) // 2,
                           generator_btn_rect.y + (generator_btn_rect.height - generator_text.get_height()) // 2))
    screen.blit(rocket_text, (rocket_btn_rect.x + (rocket_btn_rect.width - rocket_text.get_width()) // 2,
                           rocket_btn_rect.y + (rocket_btn_rect.height - rocket_text.get_height()) // 2))

    slider_label = font.render(f"DENSITY: {int(slider_val * 100)}%", True, font_color)
    slider_label_x = width + (sidebar_width - slider_label.get_width()) // 2
    screen.blit(slider_label, (slider_label_x, slider_label_y))
    
    pygame.draw.rect(screen, (50, 50, 55), slider_rect, border_radius=3)
    
    active_width = int(slider_val * slider_rect.width)
    if active_width > 0:
        pygame.draw.rect(screen, (100, 90, 150), (slider_rect.x, slider_rect.y, active_width, slider_rect.height), border_radius=3)
        
    knob_x = slider_rect.x + active_width
    knob_y = slider_rect.y + slider_rect.height // 2
    pygame.draw.circle(screen, (245, 245, 245), (knob_x, knob_y), 6)

    pygame.display.flip()

pygame.quit()
sys.exit()
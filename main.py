import pygame
import sys

pygame.init()


# Set up the window
width = 1500  # Needs to be a multiplication of 15
height = 825  # Needs to be a multiplication of 15
background_color = (0, 0, 0)
window_size = (width, height)

# Set up the sidebar
sidebar_width = 150
sidebar_color = (6, 6, 6)
sidebar_rect = (pygame.Rect(width, 0, sidebar_width, height))

# Buttons
button_start_color = (5,101,23)
button_stop_color = (191,16,41)
button_default_color = (27, 27, 27)

font = pygame.font.SysFont("Arial Black", 14)
font_color = (255, 255, 255)
start_text = font.render("Start", True, font_color)
stop_text = font.render("Stop", True, font_color)
restart_text = font.render("Restart", True, font_color)

buttons_width = 110
button_height = 25
button_margin = (sidebar_width - buttons_width) / 2

start_button_rect = pygame.Rect((sidebar_width / 2 - buttons_width / 2) + width,
                                button_margin, buttons_width, button_height)

stop_button_rect = pygame.Rect((sidebar_width / 2 - buttons_width / 2) + width,
                               button_height + 2 * button_margin, buttons_width, button_height)

restart_button_rect = pygame.Rect((sidebar_width / 2 - buttons_width / 2) + width,
                                  2 * button_height + 3 * button_margin, buttons_width, button_height)


cell_size = 15

grid_width = width / cell_size
grid_height = height / cell_size

print(grid_width, grid_height)

# Initialize
screen = pygame.display.set_mode((width + sidebar_width, height))
screen.fill(background_color)
pygame.draw.rect(screen, sidebar_color, sidebar_rect)
pygame.draw.rect(screen, button_start_color, start_button_rect)
pygame.draw.rect(screen, button_stop_color, stop_button_rect)
pygame.draw.rect(screen, button_default_color, restart_button_rect)
pygame.display.set_caption("Game Of Life")

screen.blit(start_text, (start_button_rect.x + (start_button_rect.width - start_text.get_width()) / 2,
                         start_button_rect.y + (start_button_rect.height - start_text.get_height()) / 2))

screen.blit(stop_text, (stop_button_rect.x + (stop_button_rect.width - stop_text.get_width()) / 2,
                        stop_button_rect.y + (stop_button_rect.height - stop_text.get_height()) / 2))

screen.blit(restart_text, (restart_button_rect.x + (restart_button_rect.width - restart_text.get_width()) / 2,
                           restart_button_rect.y + (restart_button_rect.height - restart_text.get_height()) / 2))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse.get_pos()
    pygame.display.flip()

import pygame
import sys
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Ball Bouncing Inside a Spinning Hexagon')

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the clock
clock = pygame.time.Clock()
FPS = 60

# Hexagon properties
hexagon_radius = 200
hexagon_center = (WIDTH // 2, HEIGHT // 2)
hexagon_rotation = 0
rotation_speed = 0.5  # degrees per frame

# Function to calculate hexagon vertices
def get_hexagon_vertices(center, radius, rotation_angle):
    vertices = []
    for i in range(6):
        angle_deg = rotation_angle + i * 60
        angle_rad = math.radians(angle_deg)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        vertices.append((x, y))
    return vertices

# Ball properties
ball_radius = 15
ball_color = RED
ball_pos = [WIDTH // 2, HEIGHT // 2 - 80]  # Starting off-center
ball_velocity = [3, 4]

# Function to check if ball hits a line segment
def distance_point_to_line(point, line_start, line_end):
    # Vector from line_start to line_end
    line_vec = (line_end[0] - line_start[0], line_end[1] - line_start[1])
    # Vector from line_start to point
    point_vec = (point[0] - line_start[0], point[1] - line_start[1])
    # Length of line
    line_len = math.sqrt(line_vec[0]**2 + line_vec[1]**2)
    # Normalize line_vec
    line_unit_vec = (line_vec[0] / line_len, line_vec[1] / line_len)
    # Project point_vec onto line_unit_vec
    projection_length = point_vec[0] * line_unit_vec[0] + point_vec[1] * line_unit_vec[1]
    # Clamp projection_length to line segment
    if projection_length < 0:
        closest_point = line_start
    elif projection_length > line_len:
        closest_point = line_end
    else:
        closest_point = (
            line_start[0] + line_unit_vec[0] * projection_length,
            line_start[1] + line_unit_vec[1] * projection_length
        )
    
    # Calculate distance from point to closest_point
    distance = math.sqrt(
        (point[0] - closest_point[0])**2 + 
        (point[1] - closest_point[1])**2
    )
    
    return distance, closest_point

def reflect_velocity(velocity, normal):
    # Normalize normal vector
    norm_length = math.sqrt(normal[0]**2 + normal[1]**2)
    unit_normal = (normal[0] / norm_length, normal[1] / norm_length)
    
    # Calculate dot product of velocity and unit normal
    dot_product = velocity[0] * unit_normal[0] + velocity[1] * unit_normal[1]
    
    # Calculate reflection
    reflected_velocity = [
        velocity[0] - 2 * dot_product * unit_normal[0],
        velocity[1] - 2 * dot_product * unit_normal[1]
    ]
    
    return reflected_velocity

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Update hexagon rotation
    hexagon_rotation += rotation_speed
    if hexagon_rotation >= 360:
        hexagon_rotation -= 360
    
    # Get current hexagon vertices
    vertices = get_hexagon_vertices(hexagon_center, hexagon_radius, hexagon_rotation)
    
    # Draw the hexagon
    pygame.draw.polygon(screen, BLUE, vertices, 2)
    
    # Update ball position
    next_pos = [ball_pos[0] + ball_velocity[0], ball_pos[1] + ball_velocity[1]]
    
    # Check for collisions with hexagon sides
    collision_detected = False
    for i in range(6):
        start_vertex = vertices[i]
        end_vertex = vertices[(i + 1) % 6]
        
        distance, closest_point = distance_point_to_line(next_pos, start_vertex, end_vertex)
        
        if distance <= ball_radius:
            # Calculate normal vector (perpendicular to the line)
            line_vec = (end_vertex[0] - start_vertex[0], end_vertex[1] - start_vertex[1])
            normal = (-line_vec[1], line_vec[0])  # Perpendicular
            
            # Reflect ball velocity
            ball_velocity = reflect_velocity(ball_velocity, normal)
            
            # Adjust position to avoid getting stuck
            collision_detected = True
            break
    
    # Update ball position
    if not collision_detected:
        ball_pos = next_pos
    
    # Draw the ball
    pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

# Quit
pygame.quit()
sys.exit()
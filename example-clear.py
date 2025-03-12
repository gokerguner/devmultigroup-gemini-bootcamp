import pygame
import math
import sys
import numpy as np

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Physics parameters
FPS = 60
GRAVITY = 0.5
FRICTION = 0.98
BALL_RESTITUTION = 0.8  # Bounce energy retention

# Ball properties
ball_radius = 15
ball_pos = np.array([WIDTH/2, HEIGHT/2], dtype=float)
ball_vel = np.array([0.0, 0.0], dtype=float)

# Hexagon properties
hex_radius = 200
hex_center = np.array([WIDTH/2, HEIGHT/2])
hex_rotation = 0
hex_rotation_speed = 0.01  # radians per frame

def get_hexagon_vertices(center, radius, rotation):
    vertices = []
    for i in range(6):
        angle = rotation + i * (2 * math.pi / 6)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

def get_hexagon_edges(vertices):
    edges = []
    for i in range(6):
        edges.append((vertices[i], vertices[(i+1) % 6]))
    return edges

def distance_point_to_line(point, line_start, line_end):
    """Calculate the shortest distance from point to line segment."""
    line_vec = np.array(line_end) - np.array(line_start)
    point_vec = np.array(point) - np.array(line_start)
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len if line_len > 0 else np.array([0, 0])
    
    # Project point onto line vector
    projection_length = np.dot(point_vec, line_unitvec)
    
    # If projection is outside the line segment, use distance to nearest endpoint
    if projection_length < 0:
        return np.linalg.norm(point_vec), line_start, -line_unitvec
    elif projection_length > line_len:
        return np.linalg.norm(np.array(point) - np.array(line_end)), line_end, line_unitvec
    else:
        # Find closest point on line
        closest_point = np.array(line_start) + projection_length * line_unitvec
        # Calculate normalized distance vector (perpendicular to line)
        dist_vec = np.array(point) - closest_point
        dist = np.linalg.norm(dist_vec)
        normal = dist_vec / dist if dist > 0 else np.array([0, 0])
        return dist, closest_point, normal

def reflect_velocity(velocity, normal):
    """Reflect velocity vector across normal vector."""
    normal = np.array(normal)
    velocity = np.array(velocity)
    # Calculate the reflection: v - 2(v·n)n
    return velocity - 2 * np.dot(velocity, normal) * normal

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                # Give the ball a random initial push when space is pressed
                ball_vel = np.array([np.random.uniform(-10, 10), np.random.uniform(-10, 10)])
    
    # Update hexagon rotation
    hex_rotation += hex_rotation_speed
    
    # Apply gravity to ball velocity
    ball_vel[1] += GRAVITY
    
    # Update ball position based on velocity
    ball_pos += ball_vel
    
    # Get hexagon vertices and edges
    hex_vertices = get_hexagon_vertices(hex_center, hex_radius, hex_rotation)
    hex_edges = get_hexagon_edges(hex_vertices)
    
    # Check for collisions with hexagon edges
    for edge in hex_edges:
        distance, closest_point, normal = distance_point_to_line(ball_pos, edge[0], edge[1])
        
        if distance <= ball_radius:
            # Move ball outside the edge
            penetration = ball_radius - distance
            ball_pos += penetration * normal
            
            # Reflect velocity with energy loss
            ball_vel = reflect_velocity(ball_vel, normal) * BALL_RESTITUTION
            
            # Apply friction to the component parallel to the edge
            edge_vector = np.array(edge[1]) - np.array(edge[0])
            edge_unit = edge_vector / np.linalg.norm(edge_vector)
            parallel_component = np.dot(ball_vel, edge_unit) * edge_unit
            perpendicular_component = ball_vel - parallel_component
            
            # Apply friction only to parallel component
            parallel_component *= FRICTION
            
            # Recombine components
            ball_vel = parallel_component + perpendicular_component
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hex_vertices, 2)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    # Draw velocity vector (for visualization)
    line_end = (int(ball_pos[0] + ball_vel[0] * 3), int(ball_pos[1] + ball_vel[1] * 3))
    pygame.draw.line(screen, BLUE, (int(ball_pos[0]), int(ball_pos[1])), line_end, 2)
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()
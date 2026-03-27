import pygame
import sys
import random
import math

# 1. Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Barkpocalypse Now: Unified Input Fix")

# Colors
BACKGROUND_COLOR = (50, 50, 50)
STREET_COLOR = (70, 70, 70)         
DASHBOARD_COLOR = (30, 30, 30)      
GERTRUDE_COLOR = (200, 150, 100)
ROOMBA_COLOR = (200, 50, 50)        
STAMINA_BG_COLOR = (150, 0, 0)      
STAMINA_FG_COLOR = (0, 200, 50)     
EXHAUSTED_COLOR = (200, 200, 0)     
JOYSTICK_BASE_COLOR = (100, 100, 100)
JOYSTICK_STICK_COLOR = (180, 180, 180)

# Gertrude's Stats
gertrude_width = 40
gertrude_height = 30
gertrude_x = 200 
gertrude_y = 150

# Physics Variables
velocity_x = 0.0
velocity_y = 0.0
acceleration = 0.4      
friction = 0.2          
max_forward_speed = 8.0         
max_reverse_speed = 3.5    
max_speed_y = 5.0          

# Boundaries
DASHBOARD_HEIGHT = 140
STREET_TOP = 20
STREET_BOTTOM = HEIGHT - DASHBOARD_HEIGHT - gertrude_height 

# Stamina Variables
max_stamina = 200
current_stamina = max_stamina
depletion_rate = 0.5       
recovery_rate = 3          
is_exhausted = False     
recovery_threshold = 15    

# Roomba Variables
roombas = []             
roomba_speed = 4
spawn_timer = 0
spawn_rate = 60          

# --- FLOATING JOYSTICK VARIABLES ---
DEFAULT_JOY_X = 120
DEFAULT_JOY_Y = HEIGHT - (DASHBOARD_HEIGHT // 2)
joy_radius = 50
stick_radius = 25

joy_base_x = DEFAULT_JOY_X
joy_base_y = DEFAULT_JOY_Y
stick_x = joy_base_x
stick_y = joy_base_y
joystick_active = False

clock = pygame.time.Clock()
touch_x, touch_y = 0, 0

# 2. The Game Loop
running = True
while running:
    # --- A. CLEAN EVENT LOOP (No FINGER events) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            tx, ty = event.pos
            # Activate if touched in the left dashboard area
            if ty >= (HEIGHT - DASHBOARD_HEIGHT) and tx <= WIDTH // 2:
                joystick_active = True
                joy_base_x, joy_base_y = tx, ty
                touch_x, touch_y = tx, ty
                
        elif event.type == pygame.MOUSEBUTTONUP:
            joystick_active = False
            joy_base_x, joy_base_y = DEFAULT_JOY_X, DEFAULT_JOY_Y
            stick_x, stick_y = DEFAULT_JOY_X, DEFAULT_JOY_Y
            
        elif event.type == pygame.MOUSEMOTION:
            if joystick_active:
                touch_x, touch_y = event.pos

    # B. Update State
    is_pedaling = False
    keys = pygame.key.get_pressed()

    if is_exhausted and current_stamina >= recovery_threshold:
        is_exhausted = False 

    if not is_exhausted and current_stamina > 0:
        
        # --- 1. JOYSTICK MOVEMENT (Clean Vector Math) ---
        if joystick_active:
            dx = touch_x - joy_base_x
            dy = touch_y - joy_base_y
            
            # Avoid division by zero
            if dx != 0 or dy != 0:
                input_x = dx / joy_radius
                input_y = dy / joy_radius
                
                # Normalize vector to ensure speed is consistent in all directions
                input_length = math.hypot(input_x, input_y)
                if input_length > 1.0:
                    input_x /= input_length
                    input_y /= input_length
                    
                # Update visual stick position
                stick_x = joy_base_x + (input_x * joy_radius)
                stick_y = joy_base_y + (input_y * joy_radius)
                
                # Apply a small deadzone (0.1) so slight jitters don't trigger movement
                if input_length > 0.1:
                    is_pedaling = True
                    
                    # Map input ratios to our maximum speeds
                    if input_x > 0:
                        target_vel_x = input_x * max_forward_speed
                    else:
                        target_vel_x = input_x * max_reverse_speed
                        
                    target_vel_y = input_y * max_speed_y
                    
                    # Smoothly accelerate toward the target velocity
                    if velocity_x < target_vel_x:
                        velocity_x = min(velocity_x + acceleration, target_vel_x)
                    elif velocity_x > target_vel_x:
                        velocity_x = max(velocity_x - acceleration, target_vel_x)
                        
                    if velocity_y < target_vel_y:
                        velocity_y = min(velocity_y + acceleration, target_vel_y)
                    elif velocity_y > target_vel_y:
                        velocity_y = max(velocity_y - acceleration, target_vel_y)

        # --- 2. KEYBOARD FALLBACK (WASD / Arrows) ---
        elif not joystick_active:
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                velocity_x = min(velocity_x + acceleration, max_forward_speed)
                is_pedaling = True
            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                velocity_x = max(velocity_x - acceleration, -max_reverse_speed)
                is_pedaling = True

            if keys[pygame.K_UP] or keys[pygame.K_w]:
                velocity_y = max(velocity_y - acceleration, -max_speed_y)
                is_pedaling = True
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                velocity_y = min(velocity_y + acceleration, max_speed_y)
                is_pedaling = True

        # Drain Stamina if moving
        if is_pedaling:
            current_stamina -= depletion_rate
            if current_stamina <= 0:
                current_stamina = 0
                is_exhausted = True

    # --- FRICTION & RECOVERY ---
    if not is_pedaling:
        current_stamina += recovery_rate
        if current_stamina > max_stamina: current_stamina = max_stamina
        
        # Apply friction to coast to a stop
        if velocity_x > 0:
            velocity_x = max(velocity_x - friction, 0)
        elif velocity_x < 0:
            velocity_x = min(velocity_x + friction, 0)
            
        if velocity_y > 0:
            velocity_y = max(velocity_y - friction, 0)
        elif velocity_y < 0:
            velocity_y = min(velocity_y + friction, 0)

    # Apply final calculated velocity to position
    gertrude_x += velocity_x
    gertrude_y += velocity_y

    # Screen Boundaries
    if gertrude_x < 0:
        gertrude_x = 0
        velocity_x = 0
    if gertrude_x > WIDTH - gertrude_width:
        gertrude_x = WIDTH - gertrude_width
        velocity_x = 0
        
    if gertrude_y < STREET_TOP:
        gertrude_y = STREET_TOP
        velocity_y = 0
    if gertrude_y > STREET_BOTTOM:
        gertrude_y = STREET_BOTTOM
        velocity_y = 0

    # --- ENEMIES ---
    spawn_timer += 1
    if spawn_timer >= spawn_rate:
        spawn_y = random.randint(STREET_TOP, STREET_BOTTOM)
        new_roomba = pygame.Rect(WIDTH, spawn_y, 20, 20) 
        roombas.append(new_roomba)
        spawn_timer = 0
        spawn_rate = random.randint(30, 80)

    for roomba in roombas[:]: 
        roomba.x -= roomba_speed
        if roomba.x < -20:
            roombas.remove(roomba)

    # --- COLLISION ---
    gertrude_rect = pygame.Rect(gertrude_x, gertrude_y, gertrude_width, gertrude_height)
    for roomba in roombas[:]:
        if gertrude_rect.colliderect(roomba):
            current_stamina -= 50  
            velocity_x = -5        
            joystick_active = False
            joy_base_x, joy_base_y = DEFAULT_JOY_X, DEFAULT_JOY_Y
            stick_x, stick_y = DEFAULT_JOY_X, DEFAULT_JOY_Y
            roombas.remove(roomba) 
            if current_stamina <= 0:
                current_stamina = 0
                is_exhausted = True

    # C. Draw Graphics
    screen.fill(BACKGROUND_COLOR)
    
    pygame.draw.rect(screen, STREET_COLOR, (0, STREET_TOP, WIDTH, HEIGHT - DASHBOARD_HEIGHT - STREET_TOP))
    pygame.draw.rect(screen, DASHBOARD_COLOR, (0, HEIGHT - DASHBOARD_HEIGHT, WIDTH, DASHBOARD_HEIGHT))
    
    for roomba in roombas:
        pygame.draw.rect(screen, ROOMBA_COLOR, roomba)
        
    pygame.draw.rect(screen, GERTRUDE_COLOR, gertrude_rect)
    
    stamina_y_pos = HEIGHT - (DASHBOARD_HEIGHT // 2) - 10
    pygame.draw.rect(screen, STAMINA_BG_COLOR, (WIDTH - 250, stamina_y_pos, max_stamina, 20))
    current_bar_color = EXHAUSTED_COLOR if is_exhausted else STAMINA_FG_COLOR
    if current_stamina > 0:
        pygame.draw.rect(screen, current_bar_color, (WIDTH - 250, stamina_y_pos, int(current_stamina), 20))
        
    if joystick_active:
        pygame.draw.circle(screen, JOYSTICK_BASE_COLOR, (int(joy_base_x), int(joy_base_y)), joy_radius, 3) 
        pygame.draw.circle(screen, JOYSTICK_STICK_COLOR, (int(stick_x), int(stick_y)), stick_radius)
    else:
        pygame.draw.circle(screen, (70, 70, 70), (DEFAULT_JOY_X, DEFAULT_JOY_Y), joy_radius, 2)
        pygame.draw.circle(screen, (90, 90, 90), (DEFAULT_JOY_X, DEFAULT_JOY_Y), stick_radius)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

import pygame, sys, os, random

# Trong pygame di chuyển đi xuống là tăng y ,di chuyển sang phải là tăng x


# Tạo hàm cho trò chơi
def draw_floor():
    screen.blit(floor, (floor_x_pos, 650))
    # Tạo thêm 1 sàn để cho 2 sàn di chuyển liên tục
    screen.blit(floor, (floor_x_pos + 432, 650))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(500, random_pipe_pos - 650))
    return bottom_pipe, top_pipe


def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


# Xử lí va chạm
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -75 or bird_rect.bottom >= 650:
        return False
    return True


pygame.init()
#  Tạo khung hình
screen = pygame.display.set_mode((432, 768))
# FPS
clock = pygame.time.Clock()

# Tạo các biến cho trò chơi
gravity = 0.25
bird_movement = 0
game_active = True


# Đường dẫn đến thư mục hiện tại (chứa tệp my_pygame.py)
current_dir = os.path.dirname(__file__)
#  Chèn background


# Tải hình nền
bg_path = os.path.join(current_dir, "assets", "background-night.png")
bg = pygame.image.load(bg_path)
bg = pygame.transform.scale2x(bg)

# Cho sàn nhà
floor_path = os.path.join(current_dir, "assets", "floor.png")
floor = pygame.image.load(floor_path)
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# Tạo chim
bird_path = os.path.join(current_dir, "assets", "yellowbird-midflap.png")
bird = pygame.image.load(bird_path)
bird = pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100, 384))

# Tạo ống
pipe_surface_path = os.path.join(current_dir, "assets", "pipe-green.png")
pipe_surface = pygame.image.load(pipe_surface_path)
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# Tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200, 300, 400]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement = -11
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 384)
                bird_movement = 0
        if event.type == spawnpipe:
            # append những ống mới vào list
            pipe_list.extend(create_pipe())
    # Background
    screen.blit(bg, (0, 0))
    if game_active:
        # Của chim
        bird_movement += gravity
        bird_rect.centery += bird_movement
        screen.blit(bird, bird_rect)
        game_active = check_collision(pipe_list)
        # Ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
    # Sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    # Điều chỉnh FPS của game
    clock.tick(120)

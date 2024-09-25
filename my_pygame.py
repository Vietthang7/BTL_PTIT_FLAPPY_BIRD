import pygame, sys, os, random

# Đường dẫn đến thư mục hiện tại (chứa tệp my_pygame.py)
current_dir = os.path.dirname(__file__)
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


# End xử lí va chạm


# Xử lí đập cánh chim
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


#  Xoay chim
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement * 3, 1)
    return new_bird


#  Tính điểm
def score_display(game_state):
    if game_state == "main game":
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)
    if game_state == "game_over":
        score_surface = game_font.render(f"Score: {int(score)}", True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(216, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(
            f" High Score: {int(high_score)}", True, (255, 255, 255)
        )
        high_score_rect = high_score_surface.get_rect(center=(216, 630))
        screen.blit(high_score_surface, high_score_rect)


# High_score
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


pygame.init()
#  Tạo khung hình
screen = pygame.display.set_mode((432, 768))
# FPS
clock = pygame.time.Clock()
game_font = pygame.font.Font(os.path.join(current_dir, "04B_19.TTF"), 40)
# Tạo các biến cho trò chơi
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0


#  Chèn background


# Tải hình nền
bg_path = os.path.join(current_dir, "assets", "background-night.png")
bg = pygame.image.load(bg_path).convert()
bg = pygame.transform.scale2x(bg)

# Cho sàn nhà
floor_path = os.path.join(current_dir, "assets", "floor.png")
floor = pygame.image.load(floor_path).convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0

# Tạo chim

bird_path_down = os.path.join(current_dir, "assets", "yellowbird-downflap.png")
bird_down = pygame.image.load(bird_path_down).convert_alpha()
bird_down = pygame.transform.scale2x(bird_down)

bird_path_mid = os.path.join(current_dir, "assets", "yellowbird-midflap.png")
bird_mid = pygame.image.load(bird_path_mid).convert_alpha()
bird_mid = pygame.transform.scale2x(bird_mid)

bird_path_up = os.path.join(current_dir, "assets", "yellowbird-upflap.png")
bird_up = pygame.image.load(bird_path_up).convert_alpha()
bird_up = pygame.transform.scale2x(bird_up)

#  Trạng thái đập cánh
bird_list = [bird_down, bird_mid, bird_up]  # 0,1,2
bird_index = 0
bird = bird_list[bird_index]
bird_rect = bird.get_rect(center=(100, 384))

# Tạo timer cho bird
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 200)
# Tạo ống
pipe_surface_path = os.path.join(current_dir, "assets", "pipe-green.png")
pipe_surface = pygame.image.load(pipe_surface_path)
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

# Tạo timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1200)
pipe_height = [200, 300, 400]

# Tạo màn hình kết thúc
game_over_surface_path = pipe_surface_path = os.path.join(
    current_dir, "assets", "message.png"
)
game_over_surface = pygame.image.load(game_over_surface_path).convert_alpha()
game_over_surface = pygame.transform.scale2x(game_over_surface)
game_over_rect = game_over_surface.get_rect(center=(216, 384))
# While loop của trò chơi
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
                score = 0
        if event.type == spawnpipe:
            # append những ống mới vào list
            pipe_list.extend(create_pipe())
        if event.type == birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird, bird_rect = bird_animation()
    # Background
    screen.blit(bg, (0, 0))
    if game_active:
        # Của chim
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)
        # Ống
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        score_display("main game")
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score, high_score)
        score_display("game_over")
    # Sàn
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos = 0

    pygame.display.update()
    # Điều chỉnh FPS của game
    clock.tick(120)

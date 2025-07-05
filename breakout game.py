import pygame
pygame.init()


WIDTH = 700
HEIGHT = 700
FPS = 120
COLS = 10
ROWS = 6

#Color...
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#DISPLAY...
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")
clock = pygame.time.Clock()

#brick class
class brick():
    def __init__(self):
        self.width = int(WIDTH / COLS)
        self.height = 30
    def creat_bricks(self):
        self.bricks = []
        for row in range(ROWS):
            bricks_row = []
            for col in range(COLS):
                bricks_x = col * self.width
                bricks_y = row * self.height
                br = pygame.Rect(bricks_x, bricks_y, self.width, self.height)
                bricks_row.append(br)
            self.bricks.append(bricks_row)

    def draw_bricks(self):
        for row in self.bricks:
            for br in row:
                pygame.draw.rect(sc,GREEN , br)
                pygame.draw.rect(sc,BLACK , br,2)



#paddle class...
class paddle():
    def __init__(self):
        self.width = int(WIDTH / COLS)
        self.height = 20
        self.x = int(WIDTH / 2) - int(self.width / 2)
        self.y = int(HEIGHT - 40)
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    def draw(self):
        pygame.draw.rect(sc,(255,255,255), self.rect)

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if key[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

#ball class
class ball():
    def __init__(self,x,y):
        self.radius = 10
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)
        self.dx = 3
        self.dy = -3
        self.game_status = 0
    def draw_ball(self):
        pygame.draw.circle(sc,RED,(self.x,self.y),self.radius)
    def move_ball(self,paddle):
        #wall collision
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.dx *= -1
        if self.rect.top < 0:
            self.dy *= -1
        if self.rect.bottom > HEIGHT:
            self.game_status = -1
        #paddle collision
        if self.rect.colliderect(paddle.rect) and self.dy > 0:
            self.dy *= -1

        self.x += self.dx
        self.y += self.dy


        #brick collision
        all_done = True
        row_num = 0
        for row in bw.bricks:
            col_num = 0
            for br in row:
                if self.rect.colliderect(br):
                    if abs(self.rect.bottom - br.top) < 5 and self.dy > 0:
                        self.dy *= -1
                    if abs(self.rect.top - br.bottom) < 5 and self.dy < 0:
                        self.dy *= -1
                    if abs(self.rect.left - br.right) < 5 and self.dx < 0:
                        self.dx *= -1
                    if abs(self.rect.right - br.left) < 5 and self.dy > 0:
                        self.dx *= -1
                    bw.bricks[row_num][col_num] = (0,0,0,0)
                if bw.bricks[row_num][col_num] != (0,0,0,0):
                    all_done = False
                col_num += 1
            row_num += 1
        if all_done:
            self.game_status = 1



        #update rect position
        self.rect.x = self.x
        self.rect.y = self.y
        return self.game_status



p = paddle()
b = ball(p.x + int(p.width / 2), p.y -10)
bw = brick()
bw.creat_bricks()

run = True

while run:
    clock.tick(FPS)
    sc.fill(BLACK)
    p.draw()
    p.move()
    b.draw_ball()
    bw.draw_bricks()
    game_status = b.move_ball(p)
    if game_status == -1:
        sc.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render("Game Over", True, YELLOW)
        text_rect = text.get_rect(centerx=WIDTH/2, centery=HEIGHT/2)
        sc.blit(text, text_rect)
    if game_status == 1:
        sc.fill(BLACK)
        font = pygame.font.SysFont(None, 50)
        text = font.render("YOU WIN", True, BLUE)
        text_rect = text.get_rect(centerx=WIDTH/2, centery=HEIGHT/2)
        sc.blit(text, text_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()



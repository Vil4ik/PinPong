from pygame import *

class GamePlayer(sprite.Sprite):
    def __init__(self, img, width, height, x, y, step):
        super().__init__()
        self.image = transform.scale(
            image.load(img),
            (width, height)
            )
        self.height = height
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.step = step

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class LeftPlayer(GamePlayer):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.step
        elif keys[K_s] and self.rect.y < 500 - self.height:
            self.rect.y += self.step

class RightPlayer(GamePlayer):
    def update(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.step
        elif keys[K_DOWN] and self.rect.y < 500 - self.height:
            self.rect.y += self.step


class Score():
    def __init__(self, text, size, x, y, width, height, color=(255, 255, 255)):
        font.init()
        self.rect = Rect(x, y, width, height)
        self.size = size
        self.color = color
        self.image = font.SysFont('verbana', size).render(
            text, True, (255, 255, 255))

    def draw(self, shift_x = 0, shift_y = 0):
        window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

    def changeText(self, text):
        self.image = font.SysFont('verbana', self.size).render(
            text, True, self.color)

score_1 = 0
score_2 = 0
player_score_1 = Score(str(score_1), 40, 330, 3, 40, 40)
player_score_2 = Score(str(score_2), 40, 450, 3, 40, 40)

window = display.set_mode((800, 500))
background = transform.scale(
    image.load('pin pong.jpg'),
    (800, 500)
)
fps = 60
clock = time.Clock()
game = True
player_1 = LeftPlayer('teni.png', 10, 65, 40, 215, 10)
player_2 = RightPlayer('teni.png', 10, 65, 750, 215, 10)
player_2.image = transform.rotate(player_2.image, 180)
ball = GamePlayer('tennis.png', 20, 20, 400, 250, 20)
dx = 3
dy = 3
pending = 0
finish = False
win_1 = Score('Left player win!', 50, 100, 50, 700, 500, (0, 255, 0))
win_2 = Score('Right player win!', 50, 100, 50, 700, 500, (0, 255, 0))

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        window.blit(background, (0, 0))
        if score_1 >= 2:
            win_1.draw(165, 180)
            finish = True
        if score_2 >= 5:
            win_2.draw(165, 180)
            finish = True
        if pending == 0:
            if ball.rect.x > 800: 
                score_1 += 1
                player_score_1.changeText(str(score_1))
                pending = 60
                dx = 3
                dy = 3
            if ball.rect.x < 0:
                score_2 += 1
                player_score_2.changeText(str(score_2))
                pending = 60
                dx = 3
                dy = 3
            if ball.rect.y >= 480 or ball.rect.y <= 0:
                dy *= -1
            if ball.rect.colliderect(player_1.rect) or ball.rect.colliderect(player_2.rect):
                dx += -1
                if dx < 0:
                    dx -= 0.2
                else:
                    dx += 0.2
            ball.rect.x += dx
            ball.rect.y += dy

            ball.reset()
        else:
            pending -= 1
            ball.rect.x = 390 
            ball.rect.y = 240 
        player_1.update()
        player_1.reset()
        player_2.update()
        player_2.reset()
        player_score_1.draw()
        player_score_2.draw()
    display.update()
    clock.tick(fps)
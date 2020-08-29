import pygame

pygame.init()

SC_WIDTH = 500
SC_HEIGHT = 480
# 윈도우 창 크기 설정
win = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT))

# 게임 창에 뜨는 제목 설정
pygame.display.set_caption("Yacht Dice Game")

# 게임에 사용될 이미지 불러오기
walkRight = [pygame.image.load('img/R%s.png' % frame) for frame in range(1, 10)]
walkLeft = [pygame.image.load('img/L%s.png' % frame) for frame in range(1, 10)]
bg = pygame.image.load('img/bg.jpg')
char = pygame.image.load('img/standing.png')

# 프레임설정
clock = pygame.time.Clock()


class player(object):
    def __init__(self, x, y, width, height):
        # 캐릭터의 시작위치
        self.x = x
        self.y = y
        # 캐릭터의 크기
        self.width = width
        self.height = height
        # 캐릭터가 움직이는 속도
        self.vel = 5
        # 캐릭터 점프 관련
        self.isJump = False
        self.jumpCount = 10
        # 캐릭터 이동방향 관련
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True

    def draw(self, win):
        # 이미지9개에 각 3프레임으로 할꺼니까 27까지로 설정
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))


class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.facing = facing  # 캐릭터가 보고있는 방향
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('img/R%sE.png' % frame) for frame in range(1, 12)]
    walkLeft = [pygame.image.load('img/L%sE.png' % frame) for frame in range(1, 12)]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = (self.x, self.end)
        self.walkCount = 0
        self.vel = 3

    def draw(self, win):
        self.move()
        if self.walkCount + 1 >= 33:
            self.walkCount = 0

        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
            self.walkCount += 1


    def move(self):
        # 오른쪽으로 이동
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1   # 경계 도달시 방향전환
                self.walkCount = 0
        # 왼쪽 이동
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1  # 경계 도달시 방향전환
                self.walkCount = 0

def redrawGameWindow():
    # 메인 루프안에 draw를 쓰는것은 좋지않다. 함수를만들어쓰자.
    global walkCount

    win.blit(bg, (0, 0))  # 백그라운드 이미지와 위 치를 넣는다
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()  # 이걸 해줘야 내가 설정한 그림들이 나옴


# main loop
man = player(100, 410, 64, 64)
goblin = enemy(100, 410, 64, 64, 450)
bullets = []
run = True
while run:
    clock.tick(27)  # 밀리초단위다 프레임 설정!
    # 이벤트 체크(유저에게 일어나는 모든일 ex.마우스클릭)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            # 총알이 경계선에 닿으면 사라지게 한다.
            bullets.remove(bullet)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5: # 쏠 수 있는 탄환을 5개로 제한
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height //2), 6, (0, 0, 0), facing))

    # 방향키 누르는것에 따라 이동하면서, 경계를 넘어가지 않게함
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < SC_WIDTH - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0

    if not (man.isJump):
        if keys[pygame.K_UP ]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1  # neg는 y축 이동방향을 결정! 점프하면 위로 올라갔다 내려가니까
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1  # 점프하면 빠르게 점프후 점점 느려지는것을 구현
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()

pygame.QUIT()

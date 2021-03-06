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

# 음악 파일 불러오기
bulletSound = pygame.mixer.Sound('music/bullet.wav')
hitSound = pygame.mixer.Sound('music/hit.wav')

music = pygame.mixer.music.load('music/music.mp3') # 배경음은 방식이 조금 다름에 유의
pygame.mixer.music.play(-1) # -1은 무한루프 재생을 뜻함

# 점수 설정
score = 0

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
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

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
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        # 텍스트를 정중앙에 배치하는법
        # 전체 길이 / 2 - 텍스트 길이 / 2
        win.blit(text, (250 - (text.get_width()/2), 200))
        pygame.display.update()
        # 텍스트를 화면에 잠깐 머물게 하는 법
        i = 0
        while i < 150:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 151
                    pygame.quit()

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
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        # 체력이 없으면 안보이게 설정하기 위함
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            # HP 바 구현
            pygame.draw.rect(win,(255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            # 맞을때마다 피가 깎여서 초록색 바가 줄어드는 것을 구현
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)


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

    def hit(self):
        if self.health > 0:
            self.health -= 1
        else :
            self.visible = False

def redrawGameWindow():
    # 메인 루프안에 draw를 쓰는것은 좋지않다. 함수를만들어쓰자.
    win.blit(bg, (0, 0))  # 백그라운드 이미지와 위치를 넣는다

    # 점수 판 작성
    text = font.render('Score : ' + str(score), 1, (0, 0, 0))
    win.blit(text,(350,10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()  # 이걸 해줘야 내가 설정한 그림들이 나옴


# main loop
# 폰트 설정
font = pygame.font.SysFont('comicsans', 30, True)
man = player(100, 410, 64, 64)
goblin = enemy(200, 410, 64, 64, 450)
shootloop = 0
bullets = []
run = True
while run:
    clock.tick(27)  # 밀리초단위다 프레임 설정!
    if goblin.visible == True:
            # 사람이 고블린 히트박스에 맞았는지 여부 판단
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

    if shootloop > 0:
        shootloop += 1
    if shootloop > 3:
        shootloop = 0
    # 이벤트 체크(유저에게 일어나는 모든일 ex.마우스클릭)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        # 총알이 고블린 히트박스에 맞았는지 여부 판단
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            if bullet.x - bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                if goblin.visible:
                    hitSound.play()
                    goblin.hit()
                    score += 1
                    bullets.remove(bullet)

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            # 총알이 경계선에 닿으면 사라지게 한다.
            bullets.remove(bullet)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootloop == 0:
        bulletSound.play()
        if man.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 5: # 쏠 수 있는 탄환을 5개로 제한
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height //2), 6, (0, 0, 0), facing))
        shootloop = 1

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

import pygame
pygame.init()

SC_WIDTH = 500
SC_HEIGHT = 500
#윈도우 창 크기 설정
win = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT))

#게임 창에 뜨는 제목 설정
pygame.display.set_caption("Yacht Dice Game")

#캐릭터의 시작위치
x = 50
y = 50
#캐릭터의 크기
width = 40
height = 60
#캐릭터가 움직이는 속도
vel = 5

isJump = False
jumpCount = 10

run = True
while run:
    pygame.time.delay(50) #밀리초단위다
    #이벤트 체크(유저에게 일어나는 모든일 ex.마우스클릭)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    #방향키 누르는것에 따라 이동하면서, 경계를 넘어가지 않게함
    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT] and x < SC_WIDTH - width - vel:
        x += vel
    #점프했을때 허공에서 y축 이동 방지
    if not(isJump):
        if keys[pygame.K_UP] and y > vel:
            y -= vel
        if keys[pygame.K_DOWN] and y < SC_HEIGHT - height - vel:
            y += vel
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            y -= (jumpCount ** 2) * 0.5
            jumpCount -= 1  #점프하면 빠르게 점프후 점점 느려지는것을 구현
        else:
            isJump = False
            jumpCount = 10

    win.fill((0,0,0))
    pygame.draw.rect(win, (87, 81, 81), (x, y, width, height))
    pygame.display.update() #이걸 해줘야 내가 설정한 그림들이 나옴


pygame.QUIT()



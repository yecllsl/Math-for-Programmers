import pygame
import sys
import random

# 初始化pygame
pygame.init()

# 设置屏幕大小和标题
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Runner Game")

# 设置颜色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# 设置字体
font = pygame.font.Font(None, 36)

# 设置玩家和敌人
player_size = 50
player_speed = 5
player_pos = [screen_width // 2, screen_height - player_size]

enemy_size = 20
enemy_speed = 3
enemy_pos = [random.randint(0, screen_width - enemy_size), 0]

# 游戏循环
while True:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()

       if event.type == pygame.KEYDOWN:
           if event.key == pygame.K_LEFT:
               player_pos[0] -= player_speed
           if event.key == pygame.K_RIGHT:
               player_pos[0] += player_speed
           if event.key == pygame.K_UP:
               player_pos[1] -= player_speed
           if event.key == pygame.K_DOWN:
               player_pos[1] += player_speed

   # 更新敌人位置
   enemy_pos[1] += enemy_speed

   # 检查玩家和敌人是否发生碰撞
   if (player_pos[0] < enemy_pos[0] + enemy_size and
           player_pos[0] + player_size > enemy_pos[0] and
           player_pos[1] < enemy_pos[1] + enemy_size and
           player_pos[1] + player_size > enemy_pos[1]):
       pygame.quit()
       sys.exit()

   # 绘制玩家和敌人
   screen.fill(black)
   pygame.draw.rect(screen, white, (player_pos[0], player_pos[1], player_size, player_size))
   pygame.draw.rect(screen, red, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

   # 更新屏幕
   pygame.display.flip()
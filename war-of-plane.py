import pygame
from pygame.locals import *
import time
import random

# 全局变量 表示爆炸
bomb_flag = 0  # 0 表示没有爆炸，1表示爆炸

class Base(object):
    def __init__(self, screen_temp, x, y, image_name, image_name1):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)
        self.image1 = pygame.image.load(image_name1)


class BasePlane(Base):
    def __init__(self, screen_temp, x, y, image_name, image_name1):
        Base.__init__(self, screen_temp, x, y, image_name, image_name1)
        self.bullet_list = []  # 存储发射出去的子弹对象引用

"""英雄机类"""
class HeroPlane(BasePlane):
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 210, 700, "./feiji/hero1.png", "./feiji/hero2.png")  # super().__init__()
        self.direction = "right"  # 用来存储飞机默认的显示方向
        self.destroy_images = []  # 存放毁灭时的图片
        #英雄机采用第一种加载爆炸图片方式，敌机采用第二种加载图片方式
        self.destroy_images.extend([pygame.image.load("./feiji/hero_blowup_n1.png").convert_alpha(), pygame.image.load("./feiji/hero_blowup_n2.png").convert_alpha(), \
                                    pygame.image.load("./feiji/hero_blowup_n3.png").convert_alpha(), pygame.image.load("./feiji/hero_blowup_n4.png").convert_alpha()])
        self.image_length = len(self.destroy_images)
        #第二种加载爆炸图片方式
        #self.__get_bomb_image()  # 加载爆炸图片
        self.isbomb = False  # false没有爆炸，True爆炸
        self.image_num = 0  # 显示过的图片数
        self.image_index = 0  # 显示图片的下标变化

    def display(self):
        if self.isbomb:
            bom_image = self.destroy_images[self.image_index]
            self.screen.blit(bom_image, (self.x, self.y))
            self.image_num += 1
            if self.image_num == (self.image_length + 1):
                self.image_num = 0
                self.image_index += 1

                if self.image_index > (self.image_length - 1):
                    self.image_index = 5
                    time.sleep(2)
                    exit()
        else:
            random_num = random.randint(0, 1)
            if (random_num == 0):
                self.screen.blit(self.image, (self.x, self.y))
            elif (random_num == 1):
                self.screen.blit(self.image1, (self.x, self.y))

            for bullet in self.bullet_list:
                bullet.display()
                bullet.move()
                # 判断当前子弹是否击中飞机
                if bullet.judge_jizhong(self.enemy):
                    self.enemy.bomb(True)

                if bullet.judge():  # 判断子弹是否越界
                    self.bullet_list.remove(bullet)

    def bomb(self, isBomb):
        self.isbomb = isBomb

    # 加载爆炸图片
    def __get_bomb_image(self):
        for i in range(1, 4):
            im_path = './feiji/hero_blowup_n' + str(i) + '.png'
            self.destroy_images.append(pygame.image.load(im_path))
        # 总数有多少张
        self.image_length = len(self.destroy_images)

    def move_up(self):
        self.y -= 5

    def move_down(self):
        self.y += 5

    def move_left(self):
        self.x -= 5

    def move_right(self):
        self.x += 5

    def fire(self, enemy):
        self.enemy = enemy
        self.bullet_list.append(Bullet(self.screen, self.x, self.y))

"""敌机的类"""
class EnemyPlane(BasePlane):
    def __init__(self, screen_temp):
        BasePlane.__init__(self, screen_temp, 0, 0, "./feiji/enemy0.png", "./feiji/enemy0.png")
        self.direction = "right"  # 用来存储飞机默认的显示方向
        self.destroy_images = []  # 存放毁灭时的图片
        # self.destroy_images.extend([pygame.image.load("./feiji/enemy0_down1.png").convert_alpha(), pygame.image.load("./feiji/enemy0_down2.png").convert_alpha(),\
        #                             pygame.image.load("./feiji/enemy0_down3.png").convert_alpha(), pygame.image.load("./feiji/enemy0_down4.png").convert_alpha()])
        self.__get_bomb_image()  # 加载爆炸图片
        self.isbomb = False  # false没有爆炸，True爆炸
        self.image_num = 0  # 显示过的图片数
        self.image_index = 0  # 显示图片的下标变化

    def display(self):
        if self.isbomb:
            bomb_image = self.destroy_images[self.image_index]
            self.screen.blit(bomb_image, (self.x, self.y))
            self.image_num += 1
            if self.image_num == (self.image_length+1):
                self.image_num = 0
                self.image_index += 1

                if self.image_index > (self.image_length - 1):
                    self.image_index = 5
                    time.sleep(2)
                    exit()
        else:
            random_num = random.randint(0, 1)
            if random_num == 0:
                self.screen.blit(self.image, (self.x, self.y))
            elif random_num == 1:
                self.screen.blit(self.image1, (self.x, self.y))

            for bullet in self.bullet_list:
                bullet.display()
                bullet.move()
                # 判断当前子弹是否击中飞机
                if bullet.judge_jizhong(self.hero):
                    self.hero.bomb(True)

                if bullet.judge():  # 判断子弹是否越界
                    self.bullet_list.remove(bullet)

    def __get_bomb_image(self):
        for i in range(1,4):
            im_path = "./feiji/enemy0_down"+str(i)+".png"
            self.destroy_images.append(pygame.image.load(im_path))
        self.image_length = len(self.destroy_images)

    def bomb(self, isBomb):
        self.isbomb = isBomb

    def move(self):

        if self.direction == "right":
            self.x += 5
        elif self.direction == "left":
            self.x -= 5

        if self.x > 480 - 50:
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"

    def fire(self, hero):
        self.hero = hero
        random_num = random.randint(1, 100)
        if random_num == 8 or random_num == 20:
            self.bullet_list.append(EnemyBullet(self.screen, self.x, self.y))


class BaseBullet(object):
    def __init__(self, screen_temp, x, y, image_name):
        self.x = x
        self.y = y
        self.screen = screen_temp
        self.image = pygame.image.load(image_name)

    def display(self):
        self.screen.blit(self.image, (self.x, self.y))

"""英雄机子弹类"""
class Bullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x + 40, y - 20, "./feiji/bullet.png")

    def judge_jizhong(self, enemy):
        if self.x > enemy.x and self.x < enemy.x + 56:
            if self.y > enemy.y and self.y < enemy.y + 31:
                print('击中敌机')
                return True
        else:
            return False

    def move(self):
        self.y -= 20

    def judge(self):
        if self.y < 0:
            return True
        else:
            return False

"""敌机子弹类"""
class EnemyBullet(BaseBullet):
    def __init__(self, screen_temp, x, y):
        BaseBullet.__init__(self, screen_temp, x + 25, y + 40, "./feiji/bullet1.png")

    def judge_jizhong(self, hero):
        if self.x > hero.x and self.x < hero.x + 80:
            if self.y > hero.y and self.y < hero.y + 20:
                print('英雄死亡')
                return True
        else:
            return False

    def move(self):
        self.y += 5

    def judge(self):
        if self.y > 852:
            return True
        else:
            return False

class PlaneWarGame(object):

    """键盘控制"""
    def key_control(self):
        # 获取事件
        for event in pygame.event.get():
            # 判断是否点击了退出按钮
            if event.type == QUIT:
                print("exit")
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                # 检测按键是否是a或者left
                if event.key == K_a or event.key == K_LEFT:
                    print("left")
                    self.hero.move_left()
                # 检测按键是否是d或者right
                elif event.key == K_d or event.key == K_RIGHT:
                    print("right")
                    self.hero.move_right()
                # 检测按键是否是w或者up
                elif event.key == K_w or event.key == K_UP:
                    print("up")
                    self.hero.move_up()
                # 检测按键是否是s或者down
                elif event.key == K_s or event.key == K_DOWN:
                    print("down")
                    self.hero.move_down()
                # 检测是否按了空格键或return键 发射子弹
                elif event.key == K_SPACE or event.key == K_RETURN:
                    print("space")
                    self.hero.fire(self.enemy)
                # 检测是否按了R键 敌机全部爆炸
                elif event.key == K_r:
                    self.enemy.isbomb = True

    def main(self):
        pygame.init()
        # 1. 创建窗口
        self.screen = pygame.display.set_mode((480, 852), 0, 32)

        # 2. 创建一个背景图片
        self.background = pygame.image.load("./feiji/background.png")

        # 3. 创建一个飞机对象
        self.hero = HeroPlane(self.screen)

        # 4. 创建一个敌机
        self.enemy = EnemyPlane(self.screen)

        while True:
            # 键盘控制
            self.key_control()
            self.screen.blit(self.background, (0, 0))
            self.hero.display()
            self.enemy.display()
            self.enemy.move()  # 调用敌机的移动方法
            self.enemy.fire(self.hero)  # 敌机开火
            # 更新窗口重新绘制
            pygame.display.update()
            # 让cpu休息一会会
            time.sleep(0.01)


if __name__ == "__main__":
    PlaneWarGame().main()

import pygame
import weapon
from pygame.locals import *
import sys

class Player:
    def __init__(self):
        self.hp = 100
        self.x = 100
        self.y = 500
        self.speed = 0
        self.weapon = None
        self.state = "stop"  # stop , walk , dash.
        self.ystate = "nutral" # fall , nutral , jump.

        self.img_animation = [0,0,0,0,0,0] # 0 stop, 1 walk , 2 dash, 3 fall , 4 nutral, 5 jumpの順番.
        self.img_animation_flame = [3,4,3,2,0,1] #アニメーションのフレーム数
        self.img_animation_rate_basic = [10,3,3,2,5,5] #アニメーションレートはこれによって定まる.
        self.img_animation_rate = 0 #rateは、画像を何秒ごとに変更するか.

        self.chr_img_stop_1 = pygame.image.load("./character/sor_ba.png")

        self.dash_img = [0,0,0,0]
        self.walk_img = [0,0,0,0,0]
        self.stop_img = [0,0,0,0]
        self.fall_img = [0,0,0]
        self.jump_img = pygame.image.load("./character/04_jump1.png")

        for i in range(3):
            self.fall_img[i] = pygame.image.load("./character/05_fall"+str(i+1)+".png")
        for i in range(4):
            self.stop_img[i] = pygame.image.load("./character/03_stop"+str(i+1)+".png")

        self.walk_img[0] = pygame.image.load("./character/02_walk1.png")
        self.walk_img[1] = pygame.image.load("./character/02_walk2.png")
        self.walk_img[2] = pygame.image.load("./character/02_walk3.png")
        self.walk_img[3] = pygame.image.load("./character/02_walk4.png")
        self.walk_img[4] = pygame.image.load("./character/02_walk5.png")

        self.dash_img[0] = pygame.image.load("./character/01_run1.png")
        self.dash_img[1] = pygame.image.load("./character/01_run2.png")
        self.dash_img[2] = pygame.image.load("./character/01_run3.png")
        self.dash_img[3] = pygame.image.load("./character/01_run4.png")

    
    def state_change_flag(self): #状態が変わるときに戻しておきたいパラメータ。
        self.img_animation[3] = 0

    
    def img_change(self,number): #画像のアニメーションを変化させる。 numberは状態種類.
        if self.img_animation_rate_basic[number] < self.img_animation_rate:
            self.img_animation_rate = 0

        if self.img_animation_rate_basic[number] == self.img_animation_rate:
            self.img_animation_rate = 0  #アニメーションレートを0にして、次も画像が切り替わるように.
            self.img_animation[number] += 1 #対象のアニメーション番号を加算する.
            if self.img_animation[number] == self.img_animation_flame[number] + 1  and number == 3:
                self.img_animation[number] -= 1
                
            elif self.img_animation[number] == self.img_animation_flame[number] and number !=3: #最大フレーム数に達したら最初の画像に変異.
                self.img_animation[number] = 0
        

            

        self.img_animation_rate += 1
    


    def jump(self):
        self.ystate = "jump"
    
    def fall(self):
        self.ystate = "fall"

    def back(self):
        self.state = "back"
        self.speed = -15

    def dash(self):
        self.state = "dash"
        self.speed = 25

    def walk(self):
        self.state = "walk"
        self.speed += 1
        if self.speed > 5:
            self.speed = 5
    
    def stop(self):
        self.state = "stop"
        self.speed = 0

    def change_weapon(self,weapon):
        self.weapon = weapon

    def now_weapon(self):
        print(self.weapon.name)
        return self.weapon.name

    
    def gameover_flag(self):
        if self.y >= 1500:
            return 1

        else:
            return 0

#player = Player()

#hg = weapon.handgun()

#player.change_weapon(hg)

#player.now_weapon()
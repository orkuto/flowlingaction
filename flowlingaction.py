import pygame
from pygame.locals import *
import player
import weapon
import stage_generate

import random

clock = pygame.time.Clock()
FPS = 160

class Maingame:
    def __init__(self):
        pygame.init()
        self.prog =  -1 
        self.score = 0
        self.screen_x = 2400
        self.screen_y = 1080
        self.character_max_x = 750
        self.ground_size = 150
        self.screen = pygame.display.set_mode((self.screen_x,self.screen_y))
        pygame.display.set_caption("gun_shooting")

        #self.bg_normal = pygame.image.load("./screen/shadowver.png")
        #self.bg_reverse = pygame.image.load("./screen/shadowverrev.png")
        
        self.button = pygame.image.load("./mobile/button.png")
        self.bg_normal = pygame.image.load("./screen/bg2.png")
        self.bg_normal=pygame.transform. scale(self.bg_normal,(self.screen_x*2,self.screen_y))
        self.bg_reverse = pygame.transform. scale(self.bg_normal,(self.screen_x*2,self.screen_y))
       

        self.img_gd = pygame.image.load("./screen/gd2.png")

        self.opening_img = pygame.image.load("./screen/opening_mobile.png")
        self.gameover_img = pygame.image.load("./screen/gameover_mobile.png")

        self.player = player.Player()
        



        self.generate_stage = stage_generate.stage_generation()

        #self.generate_stage.stage_course_generate()
        self.generate_stage.read_start()
        
        self.ground_data = [0] #地面のデータを格納しておく場所。多分1300個のリストになる。ピクセルを合わせたブロック単位で減少可能.

        for i in range(self.screen_x-1):
            self.ground_data.append(0)
        
        for i in range(len(self.ground_data)):  #初期地面をロードスル。
            self.ground_data[i] = self.generate_stage.read_stage_data() #i ってのはx座標の事で、その中に入っているものがy座標.
        

        self.gd = 550 #当たり判定の地面。

        self.scflow1 = 0
        self.scflow2 = self.screen_x*2

        self.accel = 0 #落下時の加速度。
        self.max_jp = 2

    def score_paste(self,screen,x,y,width,height,text,text_color,font_size,bg = None):
        rect = pygame.Rect(x,y,width,height)

        if bg != None:
            pygame.draw.rect(screen,bg,rect)

        font = pygame.font.SysFont(None,font_size)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        screen.blit(text_surface, text_rect)


    
    def take_ground(self): #地面データを取得してリストに格納する。これを1/60秒間に1300回数行う。 displayerで描画する.
        self.gd = int(self.ground_data[self.player.x+97])

    def ground_flow(self):
        if self.player.x >= self.character_max_x:
            #print(self.ground_data)

            for i in range(self.player.speed,self.screen_x):
                self.ground_data[i-self.player.speed] = self.ground_data[i]
            
            for i in range(self.player.speed ):
                self.ground_data[self.screen_x-self.player.speed + i] = self.generate_stage.read_stage_data()
    
    def player_score(self):
        if self.player.state == "dash":
            self.score += 2
        elif self.player.state == "walk":
            self.score += 1 
        
    def player_jp_and_fall(self): #ジャンプしたり落下したりの処理をします。
        character_gd = 199 #キャラクターの位置調整。

        if self.player.ystate == "jump":
            self.player.y += -self.accel
            self.accel -= 3
            if self.accel < 0:
                self.player.state_change_flag()
                self.player.ystate = "fall"
        
        if self.player.ystate == "nutral":
            if self.player.y < self.gd - character_gd or self.player.y - (self.gd - character_gd) >=  100:
                self.player.state_change_flag()
                self.accel = 2
                self.player.ystate = "fall"

        if self.player.ystate == "fall":
            self.player.y += self.accel
            self.accel += 3
            if self.player.y - (self.gd - character_gd) <  100 and self.player.y - (self.gd - character_gd) > 0:
                self.player.ystate = "nutral"
                self.max_jp = 2
        
        #ここの100を変更すると、下方向の猶予が無くなる。
        if self.player.y - (self.gd - character_gd) <  100 and self.player.y - (self.gd - character_gd) > 0:
            self.player.y = self.gd - character_gd
            

    def jump(self):
        if self.max_jp > 0:
            self.max_jp -= 1
            self.player.jump()
            self.accel = 35
                

    def mouse_ctl(self):
        self.mouse_pos = pygame.mouse.get_pos()
        #print(self.mouse_pos)
    
    def paste_disp(self,screen,x,y,width,height,image): #画像を貼り付ける。
        rect = pygame.Rect(x,y,width,height)
        image = pygame.transform.scale(image,(width,height))
        screen.blit(image,rect)
    
    def displayer(self): # 0 stop, 1 walk , 2 dash, 3 fall , 4 nutral, 5 jumpの順番.
        self.player_size = 200
        if self.player.ystate == "jump":
            self.paste_disp(self.screen,self.player.x,self.player.y,self.player_size,self.player_size,self.player.jump_img)
            self.player.img_change(5)
        elif self.player.ystate == "fall":
            self.paste_disp(self.screen,self.player.x,self.player.y,self.player_size,self.player_size,self.player.fall_img[self.player.img_animation[3]])
            self.player.img_change(3)
        elif self.player.state == "stop":
            self.paste_disp(self.screen,self.player.x,self.player.y,self.player_size,self.player_size,self.player.stop_img[self.player.img_animation[0]])
            self.player.img_change(0)
        elif self.player.state == "walk":
            self.paste_disp(self.screen,self.player.x,self.player.y,self.player_size,self.player_size,self.player.walk_img[self.player.img_animation[1]])
            self.player.img_change(1)
        elif self.player.state == "dash":
            self.paste_disp(self.screen,self.player.x,self.player.y,self.player_size,self.player_size,self.player.dash_img[self.player.img_animation[2]])
            self.player.img_change(2)
        elif self.player.state == "back":
            self.paste_disp(self.screen,self.player.x,self.player.y,self.player_size,self.player_size,self.player.walk_img[self.player.img_animation[1]])
            self.player.img_change(1)
        
    def displayer_menu_bar(self):
        #self.score_paste(self.screen,0,0,self.screen_x,70,"",(0,0,0),font_size=50,bg=(100,100,100))
        self.score_paste(self.screen,400,0,100,70,str(self.score)+"m",(255,255,255),font_size=70)

    def displayer_ground(self):
        for i in range(len(self.ground_data)):
            if self.ground_data[i] != 1999:
                self.paste_disp(self.screen,i,self.ground_data[i],1,self.ground_size,self.img_gd)
    
    def displayer_bullet(self):
        for i in range(self.player_bullet_counter):
            self.paste_disp(self.screen,self.player_bullet[i].bullarray[0],self.player_bullet[i].bullarray[1],10,5,self.player_bullet[i].bullet_img)


    
    def displayer_gun(self):
        
        size = 50 #銃の大きさ。
        ofset = 50 #銃のx軸の相対位置.

        if self.player.weapon.name == "handgun":
            #self.handgun.gun_img = pygame.transform.rotate(self.handgun.gun_img,90) #回転させてマウスカーソルに追尾させたいよね。
            self.paste_disp(self.screen,self.player.x+ofset,self.player.y+15,size,size,self.handgun.gun_img)
        
        if self.player.weapon.name == "ar":
            self.paste_disp(self.screen,self.player.x+ofset, self.player.y+15,size,size,self.ar.gun_img)
        
        if self.player.weapon.name == "smg":
            self.paste_disp(self.screen,self.player.x+ofset,self.player.y+15,size,size,self.smg.gun_img)
        
        if self.player.weapon.name == "magic" :
            self.paste_disp(self.screen,self.player.x+77 ,self.player.y+15,size,size,self.magic.gun_img)

        
        
    def bullet_move_collition(self):
        for i in range(self.player_bullet_counter):
            self.player_bullet[i].bullet_line(1)
            if self.player_bullet[i].bullarray[0] > 1299: 
                self.player_bullet.pop(i)
                self.player_bullet_counter += -1
                self.bullet_move_collition()
                break
            if self.player_bullet[i].bullarray[1] > self.ground_data[self.player_bullet[i].bullarray[0]] :
                self.player_bullet.pop(i)
                self.player_bullet_counter += -1
                self.bullet_move_collition()
                break

    def screen_flow(self):
        self.screen.blit(self.bg_normal,(self.scflow1,0))
        self.screen.blit(self.bg_reverse,(self.scflow2,0))
        if self.player.x >= self.character_max_x and self.player.speed >=0: 
            self.scflow1 = self.scflow1 - self.player.speed #playerのスピードに合わせて進む 後ろには下がれない。
            self.scflow2 = self.scflow2 - self.player.speed 
        if self.scflow1 <= -(self.screen_x*2):
            self.scflow1 = (self.screen_x*2)
        if self.scflow2 <= -(self.screen_x*2):
            self.scflow2 = (self.screen_x*2)

    
    def player_move(self):
        if self.player.x <= self.character_max_x:
            self.player.x +=  self.player.speed

        if self.player.x > self.character_max_x:
            self.player.x = self.character_max_x
        
        if self.player.x < 0 :
            self.player.x = 0

    def mainloop(self):
        while True:
            if self.prog == -1:
                self.screen_flow()
                action = random.randint(0,100)

                if action == 0:
                    self.player.walk()
                if action == 1:
                    self.player.dash()
                
                self.player_move()
                self.displayer()
                self.paste_disp(self.screen,0,0,self.screen_x,self.screen_y,self.opening_img)


            if self.prog == 0:
                self.player.dash()
                self.player_jp_and_fall()
                self.player_move()
                self.screen_flow()
                self.take_ground()
                self.ground_flow()
                self.displayer()
                self.displayer_ground()
                self.displayer_menu_bar()
                self.player_score()

                if self.player.gameover_flag() == 1:
                    self.prog = 1
                    
                    
            
            pygame.display.update() #ここで、画面更新

            if self.prog == 1:
                self.paste_disp(self.screen,0,0,self.screen_x,self.screen_y,self.gameover_img)
                self.score_paste(self.screen,500,500,700,400,"RESULT SCORE:"+str(self.score)+"m",(150,150,165),80)

            for event in pygame.event.get():
                if event.type == pygame.FINGERDOWN:
                    if self.prog == -1:
                        self.prog = 0
                    if self.prog == 0:
                        self.jump()
                    if self.prog == 1:
                        self.generate_stage.read_fin()
                        self = Maingame()
                        self.mainloop()
                
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.prog == -1:
                        self.prog = 0
                        self.player.x = 100
                        self.player.y = 100

                    if event.key == pygame.K_ESCAPE and (self.prog == 0 or self.prog == 1):
                        self.generate_stage.read_fin()
                        self = Maingame()
                        self.mainloop()

                    if event.key == pygame.K_SPACE and self.prog == 0:
                        self.jump()


                if event.type == QUIT:
                    self.generate_stage.read_fin()
                    pygame.QUIT()
            clock.tick(FPS)

#main = Maingame()


#main.mainloop()

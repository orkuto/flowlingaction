import csv
import random

class stage_generation:
    def __init__(self):  #平地、上り坂、下り坂、あな。

        self.file =  None
        self.data_write = None

        self.max = 300
        self.min = 800 
        self.base_gd = 650 #スタート時の底面。
        self.freq = 200 #地面の処理が何ピクセル続くか。
        self.course_length = 500
        self.select_pattern = 0 #0 平地、1　上り坂、2 下り坂、 3　あな。

    def data_generate(self):
        self.data_write.writerow("5")
        
    
    def flat_data_generate(self):
        for i in range(self.freq):
            self.data_write.writerow([str(self.base_gd)])
    
    def uphill_data_generate(self):
        for i in range(self.freq):
            self.base_gd -= 1
            self.data_write.writerow([str(self.base_gd)])

            if self.base_gd < self.max:
                break
    
    def downhill_data_generate(self):
        for i in range(self.freq):
            self.data_write.writerow([str(self.base_gd)])
            self.base_gd += 1

            if self.base_gd > self.min:
                break
    
    def hole_data_generate(self):
        for i in range(self.freq):
            self.data_write.writerow(["1999"])

    def wall_generate(self):
        a = 0
        up_or_down = random.randint(0,2)
        if up_or_down == 0: #上に上がる
            up_or_down = 1

        else: #下に下がる
            up_or_down = -1 
        for i in range(self.freq):
            a += up_or_down
            if  self.base_gd - a < self.max or self.base_gd - a > self.min:
                break
        
        self.base_gd = self.base_gd - a
        self.data_write.writerow([str(self.base_gd)])
        self.flat_data_generate()

    def stage_course_generate(self): #0 平地、1　上り坂、2 下り坂、 3　あな。4 崖
        
        self.file =  open("stage_data.csv","w",newline="")
        self.data_write = csv.writer(self.file)

        for i in range(self.course_length):
            self.select_pattern = random.randint(0,5)
            if self.select_pattern == 0:
                self.freq = random.randint(100,500)
                self.flat_data_generate()
            if self.select_pattern == 1:
                self.freq = random.randint(50,90)
                self.flat_data_generate()
                self.freq = random.randint(100,700)
                self.uphill_data_generate()
            if self.select_pattern == 2:
                self.freq = random.randint(50,90)
                self.flat_data_generate()
                self.freq = random.randint(100,700)
                self.downhill_data_generate()
            if self.select_pattern == 3:
                self.freq = random.randint(50,90)
                self.flat_data_generate()
                self.freq = random.randint(200,700)
                self.hole_data_generate()
            if self.select_pattern == 4:
                self.freq = random.randint(50,90)
                self.flat_data_generate()
                self.freq = random.randint(100,600)
                self.wall_generate()
        
        self.file.close()
    
    def read_stage_data(self): 
        output =  next(self.data_write)
        output =int(output[0])
        return output

    def read_start(self):
        self.file = open("stage_data.csv","r")
        self.data_write = csv.reader(self.file)
        

    def read_fin(self):
        self.file.close()
        self.file = None
        self.data_write = None

    
        

            
            



#a = stage_generation()

#a.stage_course_generate()

#a.read_start()

#for i in range(2000):
#   print(a.read_stage_data())
#a.read_fin()
import sys
import time
import pygame
import random
from collections import OrderedDict
from PIL import Image
 
#常量定义
FPS=60
size=3
margin=10
qizi_size=100
size=min(max(size,3),5)
photo_height=250
photo_width=250
screen_height=qizi_size*size+300#+margin+photo_height#+margin*(size+1)
screen_width=qizi_size*size+margin+photo_width+300#+margin*(size+1)
 
 
#定义时间变量
game_start=0
start_time=None
elapsed_time=0#使用时间
over_time=size*size*20-60#截止时间
'''
#输入框变量
font_text=pygame.font.Font(None, 36)
input_rect=pygame.Rect(200,250,140,32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = 'Please input n'
input_surface = font_text.render(text, True, color)
width = max(200, input_surface.get_width()+10)
'''
 
global color_active ,color_inactive,width,color
color_active= pygame.Color('dodgerblue2')
color_inactive = pygame.Color('lightskyblue3')
color = color_inactive
 
#重新定义图片大小
# 替换为指定的图片路径
img_path = r"E:\计算机概论\识物探趣课题材料\识物探趣课题材料\识物探趣小程序\archi_python_backend-main\archi_python_backend-main\static\image\f742d170-60c6-40e1-b724-3e8266083803.png"

# 重新定义图片大小，使用固定的图片路径
img = Image.open(img_path)
img = img.resize((photo_width, photo_height))
img.save("image/custom_image.jpg")  # 将图片保存到指定目录

 
#img.save('photo/future.jpg')
 
#背景颜色
background="white"
BACKGROUND_QIZI_COLOR="#9e948a"
#background_qizi_color="#9e948a"
 
# 设置图片切割
img = Image.open("image/custom_image.jpg")
img_width = img.width
img_height = img.height
img_we = img_width / size
img_he = img_height / size
 
# 创建切片元组
img_list = []
count = 1
for i in range(size):
    for j in range(size):
        leftup_y = i * img_he
        leftup_x = j * img_we
        rightdown_y = (i + 1) * img_he
        rightdown_x = (j + 1) * img_we
        tmp_s = (leftup_x, leftup_y, rightdown_x, rightdown_y)
        tmp_img = img.crop(tmp_s)
        tmp_img = tmp_img.resize((qizi_size, qizi_size))
        img_list.append(tmp_img)
        tmp_img.save(f'image/img{count}.jpg')
        count += 1
 
#定义元组相加
def addtu(tuple1,tuple2):
    tmp=(tuple1[0]+tuple2[0],tuple1[1]+tuple2[1])
    return tmp
 
#定义输出文本函数
def print_text(screen, font, x, y, text, fcolor=(255, 255, 255)):
    #print(x)
    #print(y)
    imgText = font.render(text, True, fcolor)
    screen.blit(imgText, (x, y))
 
#定义棋盘的类
class Qipan:
    def __init__(self,size=4):
        #随机方向
        self.position=[
            [1,0],#下
            [-1,0],#上
            [0,1],#右
            [0,-1]#左
        ]
        
        #棋盘大小
        self.size=size
 
        #棋盘点击坐标字典
        self.click_react={'x':{},'y':{}}
 
        #pos（有序字典）记录每个xy坐标
        self.pos=OrderedDict()
 
        #初始化数字化棋盘
        num=1
        for i in range(size):#i是行j是列
            for j in range(size):
                posxy=tuple([i,j])
                self.pos[posxy]=num
                num+=1
        
        #保证是随机棋盘，从正确的棋盘移动至随机棋盘，移动1e5
        for i in range(100000):
            positions=random.choice(self.position)
            change_op=addtu(posxy,positions)#相加移动
            if change_op in self.pos:
                tmp=self.pos[change_op]
                self.pos[change_op]=size*size
                self.pos[posxy]=tmp
                posxy=change_op
        
        #将点击区域与坐标相挂钩（xy）
        for y in range(self.size):
            for x in range(self.size):
                #x
                x0=x*qizi_size+margin
                x1=(x+1)*qizi_size+margin
                click_x=(x0,x1)################################
                self.click_react['x'][click_x]=x
 
                #y
                y0=y*qizi_size+150
                y1=(y+1)*qizi_size+150
                click_y=(y0,y1)
                self.click_react['y'][click_y]=y
    
    #实现移动棋子
    def move(self,x,y):
        #判断对应的是第几行第几列
        xnum=-1
        for i,j in self.click_react['x'].items():
            if i[0]<=x<i[1]:
                xnum=j
                break
        if xnum ==-1:
            return False
        
        ynum=-1
        for i,j in self.click_react['y'].items():
            if i[0]<=y<i[1]:
                ynum=j
                break
        if ynum==-1:
            return False
        #
 
        #判断该棋子周围是否可以移动
        for i in self.position:
            change_op=addtu((ynum,xnum),i)
 
            if change_op in self.pos:
                if self.pos[change_op]==self.size*self.size:
                    self.pos[change_op],self.pos[(ynum,xnum)]=self.pos[(ynum,xnum)],self.pos[change_op]
                    break
    
    #判断移动之后是否已经赢了
    def win(self):
        #return True
        number=1
        for i in range(self.size):
            for j in range(self.size):
                if self.pos[(i,j)]==number:
                    number+=1
                    continue
                else:
                    #print("1\n")
                    return False
        #print("2\n")
        return True
#
 
#初始化游戏界面
def game_init():
    pygame.init()
    screen=pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("拼图小游戏")
    return screen###################
 
#开始绘画拼图
def draw_img(qipan,screen):
    for i in range(qipan.size):
        for j in range(qipan.size):
            temp=qipan.pos[(i,j)]
            if temp == qipan.size*qipan.size:
                color=pygame.Color(BACKGROUND_QIZI_COLOR)
                x=qizi_size*j+10
                y=qizi_size*i+150
                pygame.draw.rect(screen,color,(x,y,qizi_size,qizi_size))
            else:
                #插入图片
                ################################
                #for k in range(qipan.size*qipan.size):
                    #if temp-1 == k:
                        #temp_img=img_list[k-1]
                img=pygame.image.load("image/img{}.jpg".format(temp)).convert()
                screen.blit(img,(j*qizi_size+10,i*qizi_size+150))
                '''color=pygame.Color(BACKGROUND_QIZI_COLOR)
                x=qizi_size*j
                y=qizi_size*i
                pygame.draw.rect(screen,color,(x,y,qizi_size,qizi_size))
                font_size=int(qizi_size/1.3)
                font = pygame.font.SysFont('arialBlod', font_size)
                font_width, font_height = font.size(str(temp))
                screen.blit(font.render(str(temp), True, (255, 255, 255)),
                            (x + (qizi_size - font_width) / 2, y +
                             (qizi_size - font_height) / 2 + 5))'''
    global rand_photo
    
    img=pygame.image.load('image/{}.jpg'.format(rand_photo)).convert()
    #img=pygame.image.load("photo/{}.jpg".format(rand_photo)).convert()
    screen.blit(img,(size*qizi_size+2*margin+150,margin+50))
#
 
#
def press(game_over,qipan,NOb,times):
    global game_start,start_time,elapsed_time
    for event in pygame.event.get():
        #设置定时器，记录完成时间
        if event.type ==NOb and not game_over:
            '''if game_start==0:
                game_start=1
                start_time = time.time()
                elapsed_time=0'''
            #else:
            
            times+=1
            #设置使用时间页面
        elif event.type==pygame.QUIT:#######
            pygame.quit()
            sys.exit()
        #鼠标点击之后的操作
        elif event.type==pygame.MOUSEBUTTONUP:
            if game_start==0:
                game_start=1
                start_time = time.time()
                elapsed_time=0
            if event.button == 1 and not game_over:
                x,y=event.pos
                if size*qizi_size+2*margin+150<=x<=size*qizi_size+2*margin+150+photo_width and  margin+50<=y<=margin+50+photo_height:
                    return -413
                #qipan.move(x,y)#移动棋盘
                xnum=-1
                for i,j in qipan.click_react['x'].items():
                    if i[0]<=x<i[1]:
                        xnum=j
                        break
                if xnum ==-1:
                    return False
        
                ynum=-1
                for i,j in qipan.click_react['y'].items():
                    if i[0]<=y<i[1]:
                        ynum=j
                        break
                if ynum==-1:
                    return False
        #
                #print(qipan.pos[(ynum,xnum)])
        #判断该棋子周围是否可以移动
                for i in qipan.position:
                    change_op=addtu((ynum,xnum),i)
 
                    if change_op in qipan.pos:
                        if qipan.pos[change_op]==qipan.size*qipan.size:
                            qipan.pos[change_op],qipan.pos[(ynum,xnum)]=qipan.pos[(ynum,xnum)],qipan.pos[change_op]
                            break
        #####需要修改
        elif event.type==pygame.KEYDOWN and event.key==13:
            return True
    if NOb:
        return times
#
 
#游戏结算画面
def game_over_win(screen,qipan,clock,size, text="win"):
    font =pygame.font.SysFont('Blod',int (100))
    font_width,font_height=font.size(str(text))
    while True:
        if press(True,qipan,None,None):
            break
        screen.fill(pygame.Color(background))#背景颜色，也可以改成图片
        #print(1)
        draw_img(qipan,screen)#绘画整个页面
        font1 = pygame.font.Font('photo/a.TTF', 20 * 2)
        tmp_time=size*size*20-60-elapsed_time
        print_text(screen,font1, 150, 0, '%03d' % tmp_time, (200,40,40))
        screen.blit(font.render(str(text), True, (0, 0, 0)),((screen_width - font_width) / 2,(screen_height - font_height) / 2+200))
        font2=pygame.font.SysFont('KaiTi',25)
        print_text(screen,font2,size*qizi_size+2*margin+100,margin+320,"可以点击图片进行更换拼图图片",(0,0,0))
        
        print_text(screen,font2,size*qizi_size+2*margin+80,margin+350,"如果完成拼图之后可以点击回车重新开始",(0,0,0))
        pygame.display.update()
        clock.tick(FPS)######
#
 
#输掉比赛
def game_over_lose(screen,q,clock,text="lose"):
    font =pygame.font.SysFont('Blod',int (100))
    font_width,font_height=font.size(str(text))
    while True:
        if press(True,q,None,None):
            break
        screen.fill(pygame.Color(background))#背景颜色，也可以改成图片
        #print(1)
        draw_img(q,screen)#绘画整个页面
        font1 = pygame.font.Font('photo/a.TTF', 20 * 2)
        print_text(screen,font1, 150, 0, '%03d' % 0, (200,40,40))#输出时间为0
        screen.blit(font.render(str(text), True, (0, 0, 0)),((screen_width - font_width) / 2,(screen_height - font_height) / 2+200))
        font2=pygame.font.SysFont('KaiTi',25)
        print_text(screen,font2,size*qizi_size+2*margin+100,margin+320,"可以点击图片进行更换拼图图片",(0,0,0))
        
        print_text(screen,font2,size*qizi_size+2*margin+80,margin+350,"如果完成拼图之后可以点击回车重新开始",(0,0,0))
        pygame.display.update()
        clock.tick(FPS)######
 
#
 
#输入数字n
def input_text(screen,active,size,font,input_rect,text):
    running=True
    global color,width,input_surface
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active=not active
                    if active==True:
                        a=1
                        text=''
                    else:
                        text='Please input n'
                else:
                    active=False
                color=color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key==pygame.K_RETURN:
                        size=eval(text)
                        size=min(max(size,3),5)
                        return size
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
                    width = max(200, font.render(text, True, color).get_width()+10)
                    input_surface = font.render(text, True, color)
        screen.fill((0,0,0))
        pygame.draw.rect(screen, color, input_rect, 2)
        input_rect.w = width
        screen.blit(input_surface, (input_rect.x+5, input_rect.y+5))
 
        pygame.display.flip()
                        
 
#
def main():
    screen=game_init()
    #定义字体 
    font1 = pygame.font.Font('E:\计算机概论\generative-models-main\COOPBL.TTF', 20 * 2)#需要先pygame.init()
 
    font_text=pygame.font.Font(None, 36)
    input_rect=pygame.Rect(200,250,140,32)
    
    global width,input_surface
    active = False
    text = 'Please input n'
    input_surface = font_text.render(text, True, color)
    width = max(200, input_surface.get_width()+10)
    tmp_size=input_text(screen,active,size,font_text,input_rect,'Please input n')
    
    #定义时间变量
    global game_start,start_time,elapsed_time
    game_start=0
    start_time=None
    elapsed_time=0#使用时间
    over_time=tmp_size*tmp_size*20-60
    
 
    clock=pygame.time.Clock()
    q=Qipan(tmp_size)
    NOb=pygame.USEREVENT+1 
    pygame.time.set_timer(NOb,1000)
    times=0
    active=False
    
    #if flag_text==False:
    rand_nob1 = random.randint(0,2)
    global rand_nob
    global rand_photo
    rand_nob=rand_nob1
    rand_photo = "custom_image"
    img=Image.open('image/{}.jpg'.format(rand_photo))
    #img=Image.open('photo/future.jpg')
    img=img.resize((photo_width,photo_height))
    img.save("image/{}.jpg".format(rand_photo))
    #重新分割图片
    img=Image.open('image/{}.jpg'.format(rand_photo))
    img_width=img.width
    img_height=img.height
    img_we=img_width/tmp_size
    img_he=img_height/tmp_size
    #创建切片元组
    img_list=[]
    count=1
    for i in range(tmp_size):
        for j in range(tmp_size):
            leftup_y=i*img_he
            leftup_x=j*img_we
            rightdown_y=(i+1)*img_he
            rightdown_x=(j+1)*img_we
            tmp_s=(leftup_x,leftup_y,rightdown_x,rightdown_y)
            tmp_img=img.crop(tmp_s)
            tmp_img=tmp_img.resize((qizi_size,qizi_size))
            img_list.append(tmp_img)
            tmp_img.save('image/img{}.jpg'.format(count))
            count+=1
        
    while True:
        if q.win():
            #font =pygame.font.SysFont('Blod',int (screen_width/4))
            #font_width,font_height=font.size(str("你赢了！！！"))
            #screen.blit(font.render(str("你赢了！！！"), True, (0, 0, 0)),((screen_width - font_width) / 2, (screen_height - font_height) / 2))
            break
        if elapsed_time==over_time:
            break
        if game_start==1:
            elapsed_time=int(time.time()-start_time)
        
        times=press(False,q,NOb,times)
        if times==-413:
            break
        screen.fill(pygame.Color(background))
        print_text(screen,font1, 150, 0, '%03d' % (over_time-elapsed_time), (200,40,40))
        #print_text(screen ,font1,0,0,"hello ",(200,40,40))
        draw_img(q,screen)
        font=pygame.font.SysFont('KaiTi',25)
        #game_over_win(screen,q,clock,text="you win!total:"+str(100)+"s")
        print_text(screen,font,tmp_size*qizi_size+2*margin+110,margin+320,"可以点击图片进行更换拼图图片",(0,0,0))
        
        print_text(screen,font,tmp_size*qizi_size+2*margin+120,margin+350,"如果完成拼图或超时失败之后",(0,0,0))
        print_text(screen,font,tmp_size*qizi_size+2*margin+170,margin+380,"可以点击回车重新开始",(0,0,0))
        pygame.display.update()
        clock.tick(FPS)
    elapsed_time=int(time.time()-start_time)
    if elapsed_time==over_time:
        game_over_lose(screen,q,clock,text="you lose!")
    if not times==-413:
        game_over_win(screen,q,clock,tmp_size,text="you win!total:"+str(elapsed_time)+"s")
    game_start=0
    start_time=None
    elapsed_time=0
    #重新随机选择图片
    rand_nob1 = random.randint(0,2)
    #global rand_nob
    #global rand_photo
    rand_nob=rand_nob1
    rand_photo = "custom_image"
    img=Image.open('photo/{}.jpg'.format(rand_photo))
    #img=Image.open('photo/future.jpg')
    img=img.resize((photo_width,photo_height))
    img.save("photo/{}.jpg".format(rand_photo))
    #重新分割图片
    img=Image.open('photo/{}.jpg'.format(rand_photo))
    img_width=img.width
    img_height=img.height
    img_we=img_width/tmp_size
    img_he=img_height/tmp_size
    #创建切片元组
    img_list=[]
    count=1
    for i in range(tmp_size):
        for j in range(tmp_size):
            leftup_y=i*img_he
            leftup_x=j*img_we
            rightdown_y=(i+1)*img_he
            rightdown_x=(j+1)*img_we
            tmp_s=(leftup_x,leftup_y,rightdown_x,rightdown_y)
            tmp_img=img.crop(tmp_s)
            tmp_img=tmp_img.resize((qizi_size,qizi_size))
            img_list.append(tmp_img)
            tmp_img.save('photo/img{}.jpg'.format(count))
            count+=1
#
 
#
if __name__=="__main__":
    while True:
        main()       

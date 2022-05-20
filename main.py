from pygame import *
from random import *
from sys import exit
init()
clock = time.Clock()

x_size,y_size = 800, 600

window = display.set_mode((x_size,y_size))

#настройки
debug = True
FPS = 70
razmer = 100
bg = transform.scale(image.load('les.png'), (x_size,y_size))
jump_power = 10
attack_reach = razmer*2
#переменные
vrags = []
'''фон'''
bg_zdvig = 0
bg_speed = 0
y_speed = 0
platforms_touched = []
f1 = font.Font(None, 130)
f2 = font.Font(None, 30)
text1 = f1.render('WIN', True,(255, 50, 50))
jumplist = []
timefast = False
lives = 3
#звуки
swing = mixer.Sound('swing.ogg')
arbuz = mixer.Sound('smachno.ogg')
ded0 = mixer.Sound('ded0.ogg')
ded1 = mixer.Sound('ded1.ogg')
vzriv = mixer.Sound('bom.ogg')
victory = mixer.Sound('victory.ogg')
madeinheaven = mixer.Sound('made_in_heaven.ogg')

sprites = []
class GameSprite(sprite.Sprite):
    def __init__(self,img,cord_x,cord_y,speed):
        sprite.Sprite.__init__(self)
        sprites.append(self)
        self.image = transform.scale(image.load(img),(razmer,razmer))
        self.rect = self.image.get_rect()
        self.rect.x = cord_x
        self.rect.y = cord_y
        self.speed = speed
    def draw(self,img,x,y):
        window.blit(img,(x,y))

flats = []
class Platforma(sprite.Sprite):
    def __init__(self, cord_x, cord_y, width, height):
        sprite.Sprite.__init__(self)
        sprites.append(self)
        flats.append(self)
        self.width = width
        self.height = height
        self.srfc = Surface((width,height))
        self.srfc.fill((50,255,50))
        self.rect = self.srfc.get_rect()
        self.rect.x = cord_x
        self.rect.y = cord_y
        self.stands_on_me = False
    def draw(self):
        window.blit(self.srfc,(self.rect.x,self.rect.y))
        draw.rect(window,(0,0,0),(self.rect.x,self.rect.y,self.width,self.height),3)

bombs = []
class Bomb(GameSprite):
    def __init__(self,img,cord_x,cord_y):
        GameSprite.__init__(self,img,cord_x,cord_y,0)
        self.startcoord = cord_x
        self.direction = cord_y
        bombs.append(self)
    def boom(self):
        active = False
        window.blit(transform.scale((image.load('blood.png')),(razmer+25,razmer+25)),(knight.rect.x-20,knight.rect.y-20))
        window.blit(transform.scale(image.load('boom.png'),(razmer+50,razmer+50)),(self.rect.x-40,self.rect.y-40))
        display.flip()
        mixer.Sound.play(vzriv)
        time.delay(1000)
        restart()

knights = []
class Player(GameSprite):
    def __init__(self,img,cord_x,cord_y,speed):
        GameSprite.__init__(self,img,cord_x,cord_y,speed)
        knights.append(self)
        self.allowjump = True
        self.y_speed = 0
    def update(self):
        #действие прыжка
        if move:
            knight.rect.y -= knight.y_speed
        #приколы со скоростью y
        if knight.allowjump:
                knight.y_speed = 0
        else:
            if (knight.y_speed > -10)and(not knight.allowjump):
                    knight.y_speed -= 0.5
        #дебаг платформ
        '''паста warning'''
        bx1, by1, bx2, by2 = [knight.rect.x+2, knight.rect.y+2, knight.rect.x+100-2, knight.rect.y+100-2]
        bx2 = bx1 + bx2
        by2 = by1 + by2
        for l in flats:
            if ((self.rect.y+125 <= l.rect.y)or(l.rect.y >= self.rect.y))and(l.rect.colliderect(self.rect)):
                #print(str(l)+'\nYes')
                l.stands_on_me = True
                #!до след комма пасчено!
                ax1, ay1, ax2, ay2 = [l.rect.x+2, l.rect.y+2, l.rect.x+l.width-2, l.rect.y+l.height-2]
                ax2 = ax1 + ax2
                ay2 = ay1 + ay2
                s1 = ( ax1>=bx1 and ax1<=bx2 ) or ( ax2>=bx1 and ax2<=bx2 )
                s2 = ( ay1>=by1 and ay1<=by2 ) or ( ay2>=by1 and ay2<=by2 )
                s3 = ( bx1>=ax1 and bx1<=ax2 ) or ( bx2>=ax1 and bx2<=ax2 )
                s4 = ( by1>=ay1 and by1<=ay2 ) or ( by2>=ay1 and by2<=ay2 )
                #движение на платформу
                if ((s1 and s2) or (s3 and s4)) or ((s1 and s4) or (s3 and s2)):
                    if self.rect.y >= l.rect.y-75:
                        global lives
                        global bg_zdvig
                        global timefast
                        while self.rect.y >= l.rect.y-99:
                            for e in event.get():
                                if e.type == QUIT:
                                    active = False
                                    exit()
                            self.y_speed = 0
                            self.rect.y -= 0.5
                            #эффекты усторения времени
                            if bg_zdvig <= -800:
                                bg_zdvig = 0
                            if timefast:
                                bg_zdvig += -50
                            window.blit(bg,(bg_zdvig,0))
                            vrag.update()
                            vrag0.update()
                            window.blit(f2.render('lives - '+str(lives), True,(255, 50, 50)),(25,25))
                            for i in sprites:
                                if i in flats or i in sticks:
                                    i.draw()
                                elif i in textures:
                                    i.draw(i.image,i.rect.x,i.rect.y)
                                    i.update()
                                else:
                                    i.draw(i.image,i.rect.x,i.rect.y)
                            #[debug]
                            if debug:
                                print('y_speed=('+str(knight.y_speed)+') | x,y='+str(knight.rect.x)+','+str(knight.rect.y)+' | bottomcord='+str(knight.rect.y+100)+' | bg_zdvig='+str(bg_zdvig)+' | FPS='+str(FPS))
                            display.flip()
                        else:
                            self.rect.y = l.rect.y-99
                    self.rect.y = l.rect.y-99
            elif not((l.rect.y >= self.rect.y)and(l.rect.colliderect(self.rect))):
                #print(str(l)+'\nNo')
                l.stands_on_me = False
        #движение на клавиши
        keys = key.get_pressed()
        if keys[K_a]:
            if self.rect.x > 0:
                #сдвиг игрока влево
                self.rect.x -= self.speed
                #изменение текстуры
                self.image = playertexture_l
        if keys[K_d]:
            if self.rect.x < (800-razmer):
                #сдвиг игрока вправо
                self.rect.x += self.speed
                #изменение текстуры
                self.image = playertexture_r
        if debug:
            if keys[K_w]:
                self.rect.y -= 1
            if keys[K_s]:
                self.rect.y += 1
            if keys[K_c]:
                self.stands_on = True
                self.y_speed = 0
        #прицел
        if self.image == playertexture_r:
            draw.aaline(window,(255,0,0),(self.rect.x+(razmer//2),self.rect.y+(razmer//2)),(self.rect.x+(razmer//2)+(razmer*2),self.rect.y+(razmer//2)),5)
        elif self.image == playertexture_l:
            draw.aaline(window,(255,0,0),(self.rect.x+(razmer//2),self.rect.y+(razmer//2)),(self.rect.x+(razmer//2)-(razmer*2),self.rect.y+(razmer//2)),5)
        else:
            pass
    #Прыжок
    def jump(self, y):
        self.rect.y -= 1
        self.y_speed = y
    #атака
    def attack(self):
        global attack_reach
        mixer.Sound.play(swing)
        if self.image == playertexture_r:
            for v in vrags:
                for a in range(self.rect.x+(razmer//2),self.rect.x+(razmer//2)+attack_reach):
                    if v.rect.x == a and v.rect.y in range(self.rect.y-50,self.rect.y+50):
                        sprites.remove(v)
                        vrags.remove(v)
                        mixer.Sound.play(ded1)
                        krov = texture('blood.png',v.rect.x,v.rect.y,150,False)
        elif self.image == playertexture_l:
            for v in vrags:
                for a in range(self.rect.x+(razmer//2)-(razmer*3),self.rect.x+attack_reach):
                    if v.rect.x == a and v.rect.y in range(self.rect.y-50,self.rect.y+50):
                        sprites.remove(v)
                        vrags.remove(v)
                        mixer.Sound.play(ded0)
                        krov = texture('blood.png',v.rect.x,v.rect.y,150,False)
        else:
            pass

finish = []
class Finish(GameSprite):
    def __init__(self,img,cord_x,cord_y):
        GameSprite.__init__(self,img,cord_x,cord_y,0)
        finish.append(self)

vrags = []
class Enemy(GameSprite):
    def __init__(self, img, cord_x, cord_y,speed):
        GameSprite.__init__(self,img,cord_x,cord_y,speed)
        vrags.append(self)
    def update(self):
        self.rect.x = randint(self.rect.x-self.speed,self.rect.x+self.speed)
        self.rect.y = randint(self.rect.y-self.speed,self.rect.y+self.speed)
        #plav = 2
        #if x1 < self.rect.x:
        #    for i in range(0,plav):
        #        self.rect.x -= (self.rect.x-x1)/plav
        #        for i in sticks:
        #            i.draw()
        #        for i in sprites:
        #            if i in flats:
        #                i.draw()
        #            elif not i in sticks:
        #                i.draw(i.image,i.rect.x,i.rect.y)
        #            else:
        #                pass
        #elif x1 > self.rect.x:
        #    for i in range(0,plav):
        #        self.rect.x += (x1-self.rect.x)/plav
        #        for i in sticks:
        #            i.draw()
        #        for i in sprites:
        #            if i in flats:
        #                i.draw()
        #            elif not i in sticks:
        #                i.draw(i.image,i.rect.x,i.rect.y)
        #            else:
        #                pass
        #else:
        #    pass
        #if y1 < self.rect.y:
        #    for i in range(0,plav):
        #        self.rect.y -= (self.rect.y-y1)/plav
        #        for i in sticks:
        #            i.draw()
        #        for i in sprites:
        #            if i in flats:
        #                i.draw()
        #            elif not i in sticks:
        #                i.draw(i.image,i.rect.x,i.rect.y)
        #            else:
        #                pass
        #elif y1 > self.rect.y:
        #    for i in range(0,plav):
        #        self.rect.y += (y1-self.rect.y)/plav
        #        for i in sticks:
        #            i.draw()
        #        for i in sprites:
        #            if i in flats:
        #                i.draw()
        #            elif not i in sticks:
        #                i.draw(i.image,i.rect.x,i.rect.y)
        #            else:
        #                pass
        #else:
        #    pass
    def murder(self):
        active = False
        window.blit(transform.scale((image.load('blood.png')),(razmer+25,razmer+25)),(knight.rect.x-20,knight.rect.y-20))
        window.blit(transform.scale((image.load('eye.png')),(razmer,razmer)),(self.rect.x,self.rect.y))
        display.flip()
        mixer.Sound.play(arbuz)
        time.delay(1000)
        restart()

sticks = []
class sled(sprite.Sprite):
    def __init__(self,cord_x,cord_y):
        sprite.Sprite.__init__(self)
        sprites.append(self)
        sticks.append(self)
        global ktick
        global razmer
        self.srfc = Surface((razmer//4,razmer//4))
        r0, r1, r2 = randint(20,200), randint(20,200), randint(20,200)
        self.srfc.fill((r0,r1,r2))
        self.srfc.set_alpha(0)
        if ktick:
            for s in sticks:
                s.srfc.set_alpha(255)
                s.srfc.fill((r0,r1,r2))
        self.srfc.set_alpha(255)
        self.rect = self.srfc.get_rect()
        self.rect.x = cord_x
        self.rect.y = cord_y
        self.timer = 255
    def draw(self):
        self.timer -= 5
        if self.timer > 0:
            self.srfc.set_alpha(self.timer)
            window.blit(self.srfc,(self.rect.x,self.rect.y))
            window.blit(knight.image,(knight.rect.x,knight.rect.y))
        else:
            sprites.remove(self)
            sticks.remove(self)

class dum(GameSprite):
    def __init__(self,cord_x,cord_y):
        GameSprite.__init__(self,'enemy.png',cord_x-(razmer//4),cord_y,0)
        vrags.append(self)
    def murder(self):
        pass

textures = []
class texture(sprite.Sprite):
    def __init__(self,img,cord_x,cord_y,timer,mirror):
        sprite.Sprite.__init__(self)
        sprites.append(self)
        textures.append(self)
        #приколы с изображением
        if mirror:
            self.image = transform.flip(transform.scale(image.load(img),(razmer,razmer)),True,False)
        else:
            self.image = transform.scale(image.load(img),(razmer,razmer))
        self.rect = self.image.get_rect()
        #корды
        self.rect.x = cord_x
        self.rect.y = cord_y
        #таймер исчезновения
        self.timer = timer
    def update(self):
        if self.timer != -1:
            self.timer -= 1
        if self.timer == 0:
            sprites.remove(self)
            textures.remove(self)
    def draw(self,img,x,y):
        window.blit(img,(x,y))

def win():
    move = False
    active = False
    active0 = True
    #звук победы
    mixer.Sound.play(victory)
    while active0:
        #тикрейт
        clock.tick(FPS)
        #выход на крестик
        for e in event.get():
            if e.type == QUIT:
                active0 = False
                exit()
        #выход на escape
        if key.get_pressed()[K_ESCAPE]:
            active0 = False
            exit()
        #заставка
        window.fill((255,150,150))
        window.blit(transform.scale(image.load('geroi.png'),(razmer,razmer)),(250,400))
        window.blit(transform.scale(image.load('heart.png'),(razmer,razmer)),(350,300))
        window.blit(transform.flip(transform.scale(image.load('princess.png'),(razmer,razmer)),True,False),(450,400))
        window.blit(text1,(300,50))
        #обовление окна
        display.flip()

def restart():
    global lives
    lives -= 1
    knight.rect.x,knight.rect.y=150,101
    for v in vrags:
        v.rect.x,v.rect.y = 1000,1000
        v.speed = 0
        sprites.remove(v)
        vrags.remove(v)
    vrag = Enemy('enemy.png',500,100,10)
    vrag0 = Enemy('enemy.png',350,450,10)
    if lives > 0:
        active = True
        move = True
    else:
        active = False
        move = False
        exit()

def kill(v):
    global attack_reach
    attack_reach = razmer
    txtr000 = knight.image
    x000, y000 = knight.rect.x, knight.rect.y
    knight.image = playertexture_r
    global bg_zdvig
    #выход на крестик
    for e in event.get():
        if e.type == QUIT:
            active = False
            exit()
    if bg_zdvig <= -800:
        bg_zdvig = 0
    if timefast:
        bg_zdvig += -50
    #обнуление скорости падения и тп к врагу
    knight.y_speed = 0
    knight.rect.x, knight.rect.y = v.rect.x-100, v.rect.y
    #отрисовка фона и жизней
    window.blit(bg,(0,0))
    window.blit(f2.render('lives - '+str(lives), True,(255, 50, 50)),(25,25))
    #обновление спрайтов
    for i in sprites:
        if i in flats or i in sticks:
            i.draw()
        elif i in textures:
            i.draw(i.image,i.rect.x,i.rect.y)
            i.update()
        else:
            i.draw(i.image,i.rect.x,i.rect.y)
    #[debug]
    if debug:
        print('y_speed=('+str(knight.y_speed)+') | x,y='+str(knight.rect.x)+','+str(knight.rect.y)+' | bottomcord='+str(knight.rect.y+100)+' | bg_zdvig='+str(bg_zdvig)+' | FPS='+str(FPS))
    display.flip()
    #атака
    for v in vrags:
        for a in range(knight.rect.x+(razmer//2),knight.rect.x+(razmer//2)+attack_reach):
            if v.rect.x == a and v.rect.y in range(knight.rect.y-50,knight.rect.y+50):
                sprites.remove(v)
                vrags.remove(v)
                mixer.Sound.play(ded1)
                krov = texture('blood.png',v.rect.x,v.rect.y,150,False)
    knight.image = txtr000
    knight.rect.x, knight.rect.y = x000, y000
    attack_reach = razmer*2

playertexture_l = transform.flip(transform.scale(image.load('geroi.png'),(razmer,razmer)),True,False)
playertexture_r = transform.scale(image.load('geroi.png'),(razmer,razmer))

flat0 = Platforma(0,550,1600,50)
flat1 = Platforma(0,425,200,25)
flat2 = Platforma(150,250,650,25)
knight = Player('geroi.png',150,150,5)
princess = Finish('princess.png',0,450)
bomb = Bomb('bomb.png',600,450)
bomb0 = Bomb('bomb.png',400,275)
vrag = Enemy('enemy.png',500,100,10)
vrag0 = Enemy('enemy.png',350,450,10)

knight.y_speed = 5

active = True
move = True
sectick = 1
ktick = False
#Главный цикл
while active:
    #тикрейт
    clock.tick(FPS)
    #каждый второй тик
    if sectick < 7:
        ktick = False
        sectick += 1
    elif sectick == 7:
        ktick = True
        sectick = 1
    #получение всех нажатых на данный тик клавиш
    keys = key.get_pressed()
    #выход на крестик
    for e in event.get():
        if e.type == QUIT:
            active = False
            exit()
        #ускорение времени
        if keys[K_b] and debug:
            if not timefast:
                for v in vrags:
                    v.speed //= 5
                timefast = True
                #mixer.Sound.play(madeinheaven)
            elif timefast:
                for v in vrags:
                    v.speed *= 5
                bg_zdvig = 0
                timefast = False
            else:
                pass
        #управление скоростью игры
        if keys[K_DELETE] and debug:
            FPS //= 2
        if keys[K_INSERT] and debug:
            FPS *= 2
        #спавн хлебушка
        if keys[K_x] and debug:
            loaf = dum(knight.rect.x,knight.rect.y)
        #спавн опасной булочки
        if keys[K_z] and debug:
            if knight.image == playertexture_r:
                bread = Enemy('enemy.png',knight.rect.x+150,knight.rect.y,10)
            elif knight.image == playertexture_l:
                bread = Enemy('enemy.png',knight.rect.x-150,knight.rect.y,10)
            else:
                pass
        #тп курсором
        if e.type == MOUSEBUTTONDOWN and debug:
            kx, ky = mouse.get_pos()
            knight.y_speed = 0
            knight.rect.x, knight.rect.y = kx-50, ky-50
        #атака
        if keys[K_v]:
            knight.attack()
        #резня
        if keys[K_q]:
            for k in vrags:
                while k in sprites and k in vrags and not(k.rect.x==1000 and k.rect.y==1000):
                    kill(k)
    #выход на escape
    if keys[K_ESCAPE]:
        active = False
        exit()
    #прыжок
    for t in flats:
        jumplist.append(t.stands_on_me)
    c = 0
    for r in jumplist:
        c+=1
        if r:
            jumplist = []
            knight.allowjump = True
            break
        if c == len(jumplist):
            knight.allowjump = False
    if keys[K_SPACE] and knight.allowjump:
        knight.jump(jump_power)
        knight.allowjump = False
    #эффекты ускорения времени
    if bg_zdvig <= -800:
        bg_zdvig = 0
    if timefast:
        bg_zdvig += randint(10,100)*(-1)
    window.blit(bg,(bg_zdvig,0))
    window.blit(bg,(bg_zdvig+800,0))
    if timefast:
        y00 = randint(0,800)
        draw.aaline(window,(255,255,255),(randint(0,600),y00),(randint(0,600),y00),50)
        y01 = randint(0,800)
        draw.aaline(window,(255,255,255),(randint(0,600),y01),(randint(0,600),y01),50)
    if timefast:
        palka = sled(knight.rect.x+((razmer//4)+(razmer//8)),knight.rect.y+((razmer//4)+(razmer//8)))
        #if knight.image == playertexture_r:
        #    r = texture('geroi.png',knight.rect.x,knight.rect.y,5,False)
        #elif knight.image == playertexture_l:
        #    r = texture('geroi.png',knight.rect.x,knight.rect.y,5,True)
        #else:
        #    pass
    else:
        for s in sticks:
            sprites.remove(s)
            sticks.remove(s)
    #обновление спрайтов
    for u in sprites:
        if u in textures:
            u.update()
            u.draw(u.image,u.rect.x,u.rect.y)
        elif u in vrags:
            if knight.rect.colliderect(u.rect) and not timefast:
                u.draw(u.image,u.rect.x,u.rect.y)
                u.murder()
            else:
                if move:
                    u.update()
            u.draw(u.image,u.rect.x,u.rect.y)
        elif u in bombs:
            if knight.rect.colliderect(u.rect) and not timefast:
                u.draw(u.image,u.rect.x,u.rect.y)
                u.boom()
            else:
                u.draw(u.image,u.rect.x,u.rect.y)
        elif u in finish:
            if knight.rect.colliderect(u.rect):
                win()
            u.draw(u.image,u.rect.x,u.rect.y)
        elif u in flats:
            u.draw()
        elif u in sticks:
            u.draw()
        elif u in knights:
            if move:
                u.update()
            u.draw(u.image,u.rect.x,u.rect.y)
        else:
            pass
    #счетчик жыз
    window.blit(f2.render('lives - '+str(lives), True,(255, 50, 50)),(25,25))
    #тп наверх при падении
    if knight.rect.y >= 600:
        knight.rect.y = -100
    #[debug]
    if debug:
        print('y_speed=('+str(knight.y_speed)+') | x,y='+str(knight.rect.x)+','+str(knight.rect.y)+' | bottomcord='+str(knight.rect.y+100)+' | bg_zdvig='+str(bg_zdvig)+' | FPS='+str(FPS))
    #обновление окна
    display.flip()
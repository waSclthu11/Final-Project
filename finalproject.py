"""
platformer.py
Author:waSclthu11
Credit:The example platformer program helped a lot, especially with subclasses, which I used for the terrain. Also Mr.Dennison helped with the collision detection setup.
Sprite credit link: https://goglilol.itch.io/cute-knight
Assignment:
Write and submit a program that implements the sandbox platformer game:
https://github.com/HHS-IntroProgramming/Platformer
"""
from ggame import App, Color, LineStyle, Sprite, RectangleAsset, CircleAsset, TextAsset, EllipseAsset, PolygonAsset, ImageAsset, Frame
x=510
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
blue = Color(0x2EFEC8, 1.0)
black = Color(0x000000, 1.0)
pink = Color(0xFF00FF, 1.0)
red = Color(0xFF5733, 1.0)
white = Color(0xFFFFFF, 1.0)
red = Color(0xff0000, 1.0)
green = Color(0x00ff00, 1.0)
blue = Color(0x0000ff, 1.0)
black = Color(0x000000, 1.0)
white = Color(0xffffff, 1.0)
grey = Color(0xC0C0C0, 1.0)

thinline = LineStyle(2, black)
blkline = LineStyle(1, black)
noline = LineStyle(0, white)
coolline = LineStyle(1, grey)
blueline = LineStyle(2, blue)
redline = LineStyle(1, red)
greenline = LineStyle(1, green)
gridline = LineStyle(1, grey)
grid=RectangleAsset(30,30,gridline,white)


from ggame import App, RectangleAsset, ImageAsset, Sprite, LineStyle, Color, Frame

class Player(Sprite):
    asset = ImageAsset("images/SpriteFinalproj1.png", Frame(0,36,64,28), 8, 'horizontal')
    asset.append("images/sheet_hero_walk.png", Frame(0,36,64,28), 3, 'horizontal')
    asset.append("images/sheet_hero_jump.png", Frame(0,26,64,38), 5, 'horizontal')
    asset.append("images/sheet_hero_stab.png", Frame(0,34,64,30), 5, 'horizontal')
    
    def __init__(self, position):
        super().__init__(Player.asset, position, CircleAsset(10))
        self.vx = 0
        self.vy = 0
        self.thrust = 0
        self.left=0
        self.right=0
        self.collidingwithsprites=0
        self.resting=0
        self.collidetop=Collide(position,12,5,green)
        self.collidebottom=Collide(position,8,5,blue)
        self.collideleft=Collide(position,5,15,red)
        self.collideright=Collide(position,5,15,pink)
        self.leftslide=False
        self.rightslide=False
        self.leftleap=False
        self.rightleap=False
        self.leap=False
        self.attack=False
        self.attackp=True
        self.thrustframe=1
        self.width=64
        SpaceGame.listenKeyEvent("keydown", "space", self.thrustOn)
        SpaceGame.listenKeyEvent("keyup", "space", self.thrustOff)
        SpaceGame.listenKeyEvent("keydown", "left arrow", self.lefton)
        SpaceGame.listenKeyEvent("keyup", "left arrow", self.leftoff)
        SpaceGame.listenKeyEvent("keydown", "right arrow", self.righton)
        SpaceGame.listenKeyEvent("keyup", "right arrow", self.rightoff)
        SpaceGame.listenKeyEvent("keydown", "down arrow", self.Leap)
        SpaceGame.listenKeyEvent("keyup", "down arrow", self.noLeap)
        SpaceGame.listenKeyEvent("keydown", "c", self.Attack)
        SpaceGame.listenKeyEvent("keyup", "c", self.noAttack)
        self.fxcenter = self.fycenter = 0.5
    def step(self):
        downcollide=self.collidebottom.collidingWithSprites(Variblock)
        #Jump Animation
        if not len(downcollide):
            if self.thrustframe<12:
                self.thrustframe=12
            self.setImage(self.thrustframe)
            self.thrustframe += .25
            if self.thrustframe==16:
                self.thrustframe=14  
        #Attack Animation
        elif self.attack==True and self.vy==0:
            self.attackp=False
            if self.thrustframe<16.5:
                self.thrustframe=16.5
            self.setImage(self.thrustframe)
            self.thrustframe += .125
            if self.thrustframe>=22:
                self.thrustframe=16.5
                self.attackp=False

        #Running Animation
        elif (self.left==1 or self.right==1) and self.vy==0:
            if self.thrustframe<9 or self.thrustframe>11:
                self.thrustframe=9
            """if self.left==1:
                self.width=-64
                print(self.width)
            if self.right==1:
                self.width=64"""
            self.setImage(self.thrustframe)
            self.thrustframe += .25 
            if self.thrustframe == 11:
                self.thrustframe = 9
        #Idle Animation
        elif self.vx==0 and self.resting==1:
            self.setImage(self.thrustframe)
            self.thrustframe += .25
            if self.thrustframe >= 8:
                self.thrustframe = 1

        self.x += self.vx
        self.y += self.vy
        self.collidetop.x = self.x
        self.collidetop.y = self.y-13
        self.collidebottom.x =self.x
        self.collidebottom.y =self.y+12
        self.collideright.x =self.x+7
        self.collideright.y =self.y-1
        self.collideleft.x =self.x-7
        self.collideleft.y =self.y-1
        upcollide=self.collidetop.collidingWithSprites(Variblock)
        downcollide=self.collidebottom.collidingWithSprites(Variblock)
        downcollidep=self.collidebottom.collidingWithSprites(Platform)
        downcollide.extend(downcollidep)
        downcollides=self.collidebottom.collidingWithSprites(sprong)
        if len(downcollides):
            self.vy=-15
        if len(downcollide):
             if self.vy>0:
                if self.vy>=3:
                    self.y=self.y-self.vy*0.3
                    self.vy=0
                    
                self.vy=0
                self.resting=1
        elif len(downcollide)==0:
            if self.rightslide==True and self.vy>1:
                self.vy=1
                self.leftleap=True
            if self.leftslide==True and self.vy>1:
                self.rightleap=True
                self.vy=1
            else:
                if self.vy<6:
                    self.vy=self.vy+.3
            self.resting=0
            if len(upcollide):
                self.y=self.y+3
                self.vy=self.vy*-.5
            
                
        leftcollide=self.collideleft.collidingWithSprites(Variblock)
        if len(leftcollide):
            #print("left")
            self.x=self.x-self.vx
            self.vx=0
        self.leftslide=True
        if not len(leftcollide):
            self.leftslide=False
            self.rightleap=False
        rightcollide=self.collideright.collidingWithSprites(Variblock)
        if len(rightcollide):
            #print("right")
            self.x=self.x-self.vx
            self.vx=0
            self.rightslide=True
        if not len(rightcollide):
            self.rightslide=False
            self.leftleap=False
        if self.left==1:
            if self.vx>0 and len(downcollide):
                self.vx=0
            if self.vx>=-4:
                self.vx=self.vx-.4
        else:
            if self.right==1:
                if self.vx<0 and len(downcollide):
                    self.vx=0
                if self.vx<=4:
                    self.vx=self.vx+.4
            else:
                if self.resting==1:
                    self.vx=0
        
        if self.thrust == 1:
            self.vy = -6
            self.thrust=0
        else:
            if self.y>=x:
                self.vy=0
        if self.leap==True:
            if self.rightleap==True:
                self.vx=6.5
                self.vy=-5
            if self.leftleap==True:
                self.vx=-6.5
                self.vy=-5
    def thrustOn(self, event):
        if self.resting==1:
            self.thrust = 1
    def thrustOff(self, event):
        self.thrust = 0
    def lefton(self, event):
        self.left=1
    def leftoff(self, event):
        self.left=0
    def righton(self, event):
        self.right=1
    def rightoff(self, event):
        self.right=0
    def Leap(self, event):
        self.leap=True
    def noLeap(self, event):
        self.leap=False
    def Attack(self, event):
        if self.attackp==True:
            self.attack=True
        else:
            self.attack==False
    def noAttack(self, event):
        self.attack=False
        self.attackp=True
class Snake(Sprite):
    asset = ImageAsset("images/sheet_snake_walk.png", Frame(0,40,64,24), 7, 'horizontal')
    def __init__(self,position):
        super().__init__(Snake.asset, position, CircleAsset(10))
        self.vx=0
        self.thrustframe=1
        self.rightdetect=Collide(position,5,15,green)
        self.leftdetect=Collide(position,5,15,red)
        self.fxcenter = self.fycenter = 0.5
    def step(self):
 
        self.x += self.vx
        self.rightdetect.x=self.x+10
        self.rightdetect.y=self.y
        self.leftdetect.x=self.x-10
        self.leftdetect.y=self.y
        leftdetect=self.leftdetect.collidingWithSprites(Variblock)
        ree=(self.leftdetect.collidingWithSprites(Player))
        leftdetect.extend(ree)
        if len(leftdetect):
            self.vx=1
        rightdetect=self.rightdetect.collidingWithSprites(Variblock)
        ros=(self.rightdetect.collidingWithSprites(Player))
        rightdetect.extend(ros)
        if len(rightdetect):
            self.vx=-1
        if self.thrustframe<7:
            self.thrustframe+=.25
            self.setImage(self.thrustframe)
        elif self.thrustframe<=7:
            self.thrustframe=1
       
class Collide(Sprite):
    def __init__(self, position,w,h,color):
        super().__init__(RectangleAsset(w,h,noline, color), position)
        self.fxcenter = 0.5
        self.fycenter = 0.5
        self.visible=True

class Wallblock(Sprite):
    def __init__(self, x, y, w, h, color):
        super().__init__(RectangleAsset(w-1,h-1,noline, color),
            (x, y))
        collideswith = self.collidingWithSprites(type(self))
        if len(collideswith):
            collideswith[0].destroy()
        Wallblock.fxcenter = Wallblock.fycenter = 0
class Platform(Wallblock):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 10, blue)
class Block(Wallblock):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 50, red)

class Variblock(Sprite):
    def __init__(self, w, h, x, y):
        super().__init__(RectangleAsset(w,h,noline,grey),(x,y))

class sprong(Wallblock):
    def __init__(self, x, y):
        super().__init__(x, y, 50, 10, pink)
class goal(Sprite):
    def __init__(self, w, h, x, y):
        super().__init__(RectangleAsset(w,h,noline,blue),(x,y))
class Spike(Sprite):
    def __init__(self, w, h, x, y):
        super().__init__(RectangleAsset(w,h,noline,red),(x,y))
class textbox(Sprite):
    def __init__(self, t, w, x, y):
        super().__init__(TextAsset(t, style="bold 40pt Arial", width=w, fill=blue),(x,y))
class SpaceGame(App):
    def __init__(self):
        super().__init__()
        # Background
        x=510
        beeg=50
        black = Color(0, 1)
        noline = LineStyle(0, black)
        TA= TextAsset("Press Enter to Begin", style="bold 40pt Arial", width=250, fill=black)
        self.Enter=Sprite(TA,(400,200))
        self.levelindex=.5
        self.listenMouseEvent("mousemove", self.Mouse)
        self.listenKeyEvent("keydown", "enter", self.newlevel)
        self.listenKeyEvent("keydown", "z", self.uplevel)
        self.listenKeyEvent("keydown", "x", self.downlevel)
        self.levelfinish=[]
        self.terrainlist=None
        self.p = None
        self.progress=False
        
    def Mouse(self, event):
        self.pos = (event.x, event.y)
    def uplevel(self, event):
        self.levelindex+=0.5
    def downlevel(self, event):
        self.levelindex-=0.5
    def newlevel(self,event):
        for s in self.getSpritesbyClass(Player):
            s.destroy()
        for s in self.getSpritesbyClass(Spike):
            s.destroy()
        for a in self.getSpritesbyClass(Variblock):
            a.destroy()
        for c in self.getSpritesbyClass(Collide):
            c.destroy()
        for s in self.getSpritesbyClass(sprong):
            s.destroy()
        for s in self.getSpritesbyClass(textbox):
                    s.destroy()
        for s in self.getSpritesbyClass(goal):
                    s.destroy()
        if self.Enter:
            self.Enter.destroy()
            self.Enter=None
        if self.levelindex==0.5:
            self.progress=True
            self.p=Player((60,350))
            Variblock(1050,300,0,0)
            Variblock(1050,300,0,400)
            Spike(10,100,0,300)
            goal(20,100,1000,300)
            Snake((200,390))
            textbox("Press 'Enter' when touching the blue goal to complete the level. The red 'Spikes' will send you back.",1000,10,10)
        if self.levelindex==1:
            self.progress=True
            self.p = Player((60,50))
            Variblock(50,800,0,0)
            Variblock(1050,50,0,500)
            Variblock(365,800,650,0)
            ###NonborderTerrain
            Variblock(230,400,50,150)
            Variblock(100,30,400,150)
            Variblock(30,130,400,150)
            Spike(120,10,280,250)
            Spike(10,100,430,180)
            
            Spike(200,10,450,400)
            goal(20,20,500,470)
        if self.levelindex==1.5 or self.levelindex==2.5:
            self.progress=True
            self.p=Player((60,350))
            Variblock(1050,300,0,0)
            Variblock(1050,300,0,400)
            Spike(10,100,0,300)
            goal(20,100,1000,300)
        if self.levelindex==2:
            self.progress=True
            
            self.p = Player((60,50))
            Variblock(50,800,0,0)
            Variblock(1050,50,0,500)
            Variblock(50,800,970,0)
            Variblock(50,250,400,250)
            sprong(350,500)
            goal(20,20,500,470)
        if self.levelindex==3:
            self.progress=True
            self.p=Player((60,50))
            goal(20,100,1000,300)
        if self.levelindex==4:
            self.progress=True
            self.p = Player((60,50))
            Variblock(50,800,0,0)
            Variblock(1050,50,0,500)
            Variblock(50,800,970,0)
            ###NonborderTerrain
            Variblock(200,30,50,150)
            Spike(200,10,50,145)
            
            Variblock(30,100,260,210)
            Spike(30,10,260,205)
            #Block 1
            Variblock(800,30,50,410)
            Spike(800,10,50,400)
            #Block 2
            Variblock(100,30,420,280)
            Spike(100,10,420,310)
            Spike(10,30,420,280)
            #Block 3
            Variblock(30,100,600,180)
            Spike(10,105,630,175)
            Spike(30,10,600,175)
            #Block 4
            Variblock(130,30,400,180)
            Variblock(30,100,400,90)
            Spike(130,10,400,200)
            Spike(10,120,400,90)
            #Block 5
            Variblock(100,30,700,300)
            
            goal(20,20,500,470)
    def step(self):
        if self.p:
            self.levelfinish=self.p.collidingWithSprites(goal)
            self.playerhurt=self.p.collidingWithSprites(Spike)
            if len(self.levelfinish):
                if self.progress==True:
                    print(self.levelindex)
                    self.levelindex=self.levelindex+.5
                    print(self.levelindex)
                    self.progress=False
            if len(self.playerhurt):
                for s in self.getSpritesbyClass(Player):
                    s.destroy()
                for q in self.getSpritesbyClass(Spike):
                    q.destroy()
                for a in self.getSpritesbyClass(Variblock):
                    a.destroy()
                for c in self.getSpritesbyClass(Collide):
                    c.destroy()
                for s in self.getSpritesbyClass(sprong):
                    s.destroy()
                for s in self.getSpritesbyClass(textbox):
                    s.destroy()
                if self.levelindex>.5:
                    self.levelindex-=.5
  
        for ship in self.getSpritesbyClass(Player):
            ship.step()
        for ip in self.getSpritesbyClass(Snake):
            ip.step()
print("use the left and right arrows to move , space bar to jump, and down arrow when sliding on a wall to wall")        
myapp = SpaceGame()
myapp.run()
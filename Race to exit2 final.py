# Simple race to the exit game J Joubert 28 November 2019
# This is based on the last game in the book Python for Kids by Jason R Briggs
# Tkinter is used in the book
# I think this version in Python 3 and Turtle may be a bit easier
# (But not as elegant)
# Written in IDLE on mac osX (may need some adjustments in windows)

import turtle
import random
#import time # and time.sleep(0.017) windows??


win = turtle.Screen()
win.title('Race to exit')
win.bgpic('back1.gif')
win.setup(800,700)
win.tracer(0)
win.listen()
shape_list = ['door1.gif', 'door2.gif', 'stick-L1.gif', 'stick-L2.gif', 'stick-L3.gif', 'stick-R1.gif', 'stick-R2.gif',
              'stick-R3.gif']


# Register gif files as shapes
for i in  shape_list:
    win.register_shape(i)

   
# Place the platforms    
platforms = []

class Platform(turtle.Turtle):
    def __init__(self, xpos, ypos):
        super().__init__(shape='square')
        self.shapesize(0.5,30) 
        self.color('red')
        self.up()
        self.xpos = xpos
        self.ypos = ypos
        self.goto(self.xpos, self.ypos)
        self.deg = 0

x_list = [-30, 30, -50, 30, -30]
y_list = [-300, -170, -60, 70, 200]

switch = 0
for i in range(5):
    platform = Platform(x_list[i],y_list[i])
    if switch%2 == 0:
        platform.rt(6)
        platform.slope = 'down'
    else:
        platform.lt(6)
        platform.slope = 'up'
    platforms.append(platform)
    switch += 1



class Door(turtle.Turtle):
    def __init__(self):
        super().__init__(shape='door1.gif')
        self.up()
        self.goto(-280,300)
        self.color('red')



class Ball(turtle.Turtle):
    def __init__(self, platforms):
        super().__init__(shape='circle')
        self.up()
        self.color('blue')
        self.goto(-240, 380)
        self.platforms = platforms
        self.point = 270 # prevents too many collision checks while within the platform y
        self.state = 'falling' # will use to fall off platform
        self.dx = 0
        self.xpoint = self.xcor()
        self.age = 'new'
      

    def move(self):
        self.fd(1)
        
        if self.ycor()< -320:
            self.sety(-320)
            self.dy = 0
            self.setheading(0)
            self.state = 'rolling'
            
        if self.state == 'falling':
            self.fall()

        for i in self.platforms:
            if within_platform(self,i) and i.slope == 'up' and self.point-self.ycor() > 31.5:
                #print('up')
                self.state = 'rolling'
                self.point = i.ycor() # wait until below platform before check
                self.xpoint = i.xcor()
                if self.xcor() < i.xcor():
                    self.sety(i.ycor()+10 - self.distance(i)*0.11) # sin 6 deg
                elif self.xcor() >= i.xcor():
                    self.sety(i.ycor()+10 + self.distance(i)*0.11)
                    
                self.setheading(186) # down to the left
                self.dx = -1

            if within_platform(self,i) and i.slope == 'down' and self.point-self.ycor() > 31.5:
                #print('down')
                self.state = 'rolling'
                self.point = i.ycor()
                self.xpoint = i.xcor()
                if self.xcor()< i.xcor():
                    self.sety(i.ycor()+10 + self.distance(i)*0.11)
                elif self.xcor()>=i.xcor():
                    self.sety(i.ycor()+10 - self.distance(i)*0.11)
                    
                self.setheading(-6)# down to the right
                self.dx = 1

            #Falling off the platform - tried several ways....not working well yet
            if self.state == 'rolling' and (self.xcor()-self.xpoint>300 or self.xcor()-self.xpoint<-300):
                #print('fall')
                self.point = self.ycor()
                self.xpoint = self.xcor()
                self.state = 'falling'

    def fall(self):
        self.dy = -5
        self.goto(self.xcor()+self.dx, self.ycor()+self.dy)
            
        if self.ycor() <= -320: # Stop at ground after jump
            self.sety(-320)
            self.state = 'rolling'
            self.dy = 0

        
                
class Player(turtle.Turtle):
    def __init__(self, platforms):
        super().__init__(shape='circle')
        self.up()
        self.s = 'stick-R1.gif'
        self.shape(self.s)
        self.color('blue')
        self.goto(300, -320)
        self.platforms = platforms
        self.deg = 0
        self.dx = 1
        self.dy = -6
        self.jump = 'stop'
        self.counter = 0
        self.move_dir = 'right'
        
        self.point = self.xcor() # Used to fall off the platforms
        
        

    def move_right(self):
        
        self.dx = 1
        self.move_dir = 'right'
        self.s = 'stick-R1.gif'

    def move_left(self):
        self.move_dir = 'left'
        self.dx = -1
        self.s = 'stick-L1.gif'
        

    def jump_up(self):
        if self.jump == 'stop':
            self.jump = 'up'

    def animate(self):
        if self.move_dir == 'left':
            if self.s == 'stick-L1.gif' and counter%10 == 0: #  Every 10th time in the loop
                self.s = 'stick-L2.gif'
                self.shape(self.s)
            elif self.s == 'stick-L2.gif' and counter%10 == 0:
                self.s = 'stick-L3.gif'
                self.shape(self.s)
            elif self.s == 'stick-L3.gif' and counter%10 == 0:
                self.s = 'stick-L1.gif'
                self.shape(self.s)

        elif self.move_dir == 'right':
            if self.s == 'stick-R1.gif' and counter%10 == 0:
                self.s = 'stick-R2.gif'
                self.shape(self.s)
            elif self.s == 'stick-R2.gif' and counter%10 == 0:
                self.s = 'stick-R3.gif'
                self.shape(self.s)
            elif self.s == 'stick-R3.gif' and counter%10 == 0:
                self.s = 'stick-R1.gif'
                self.shape(self.s)
            

    def move(self):
        # Move forward (right) or back(left)
        if self.move_dir == 'right':
            self.fd(1)
        else:
            self.bk(1)

        if self.ycor()< -320:
            self.sety(-320)
            self.dy = 0
            self.setheading(0)
            
        
        # Change direction at the sides
        if self.xcor() <= -380:
            self.move_right()
        elif self.xcor()>= 380:
            self.move_left()

        # Jump
        if self.jump == 'up':
            self.dy = 7 # Adjust this for height 
            
            # Ajust dx*3 for distance
            self.goto(self.xcor()+self.dx*3, self.ycor()+self.dy)
            self.counter += 1
            if self.counter == 10:
                self.jump = 'down'
                
        elif self.jump == 'down':
            self.fall()
            
            
                
        for i in platforms:
            # Landing on platform:
            if within_platform(self,i) and player.dy < 0 and i.slope == 'up':
                #print('up')
                self.point = i.xcor()
                #print(self.point)
                if self.xcor() < i.xcor():
                    self.sety(i.ycor()+20 - self.distance(i)*0.11) # sin 6deg
                elif self.xcor() >= i.xcor():
                    self.sety(i.ycor()+20 + self.distance(i)*0.11)
                    
                self.setheading(6)
                self.jump = 'stop'
                self.counter = 0
                self.dy = 0
              
               

            if within_platform(self,i) and player.dy < 0 and i.slope == 'down':
                #print('down')
                self.point = i.xcor()
                #print(self.point)
                if self.xcor()<= i.xcor():
                    self.sety(i.ycor()+20 + self.distance(i)*0.11)
                elif self.xcor()>i.xcor():
                    self.sety(i.ycor()+20 - self.distance(i)*0.11)
                self.setheading(-6)
                self.jump = 'stop'
                self.counter = 0
                self.dy = 0

            # Falling off the platform 
            if self.jump == 'stop' and (self.xcor()-self.point>300 or self.xcor()-self.point<-300):
                #print('fall')
                self.point = self.xcor()
                self.jump = 'down'
                

    def fall(self):
        self.dy = -12
        self.goto(self.xcor()+self.dx*2, self.ycor()+self.dy)
            
        if self.ycor() <= -320: # Stop at ground after jump
            self.sety(-320)
            player.jump = 'stop'
            self.counter = 0
            self.dy = 0
            
            
                       
            
def within_platform(player, platform): 
    if platform.xcor()-300 <= player.xcor() <= platform.xcor()+300:
        if platform.ycor()-31.5 <= player.ycor() <= platform.ycor()+ 31.5: # Not strictly correct but working best so far
            return True


def within_platform_x(player,platform):
    if platform.xcor()-300 <= player.xcor() <= platform.xcor()+300:
        return True


ball_list = []
player = Player(platforms)
door = Door()
ball = Ball(platforms)

ball_list.append(ball)

win.onkey(player.move_right, 'Right')
win.onkey(player.move_left, 'Left')
win.onkey(player.jump_up, 'space')

game_over = False
counter = 0

while not game_over:
    #time.sleep(0.017) # windows??
    
    counter += 1
    win.update()
    player.move()
    player.animate()
    delay = random.random()
    
    for i in ball_list:
        i.move()
    
        if i.distance(door) > 200 and i.age == 'new' and delay <0.005:
            ball = Ball(platforms)
            ball_list.append(ball)
            i.age = 'old'

        if i.xcor() > 420:
            ball_list.remove(i)
            #print(len(ball_list))
           

        if player.distance(i)<18:
            game_over = True
        
    
    if player.distance(door)<20:
        door.shape('door2.gif')
        game_over = True

   

win.bgcolor('yellow')
win.update()

# Simple race to the exit game J Joubert 27 December 2019
# This is based on the last game in the book Python for Kids by Jason R Briggs
# Tkinter is used in the book
# I think this version in Python 3 and Turtle may be a bit easier
# (But not as elegant)
# Written in IDLE on mac osX (may need some adjustments in windows)

# Having a game class allows simple start/game over screen/restart game

import turtle
import random


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
        self.platforms = game.platforms
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
        self.platforms = game.platforms
        self.deg = 0
        self.dx = 1
        self.dy = -6
        self.jump = 'stop'
        self.counter = 0 # Timing of jumps
        self.animate_counter = 0
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
            if self.s == 'stick-L1.gif' and self.animate_counter%10 == 0: #  Every 10th time in the loop
                self.s = 'stick-L2.gif'
                self.shape(self.s)
            elif self.s == 'stick-L2.gif' and self.animate_counter%10 == 0:
                self.s = 'stick-L3.gif'
                self.shape(self.s)
            elif self.s == 'stick-L3.gif' and self.animate_counter%10 == 0:
                self.s = 'stick-L1.gif'
                self.shape(self.s)

        elif self.move_dir == 'right':
            if self.s == 'stick-R1.gif' and self.animate_counter%10 == 0:
                self.s = 'stick-R2.gif'
                self.shape(self.s)
            elif self.s == 'stick-R2.gif' and self.animate_counter%10 == 0:
                self.s = 'stick-R3.gif'
                self.shape(self.s)
            elif self.s == 'stick-R3.gif' and self.animate_counter%10 == 0:
                self.s = 'stick-R1.gif'
                self.shape(self.s)
        self.animate_counter += 1
            

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
            
            
                
        for i in self.platforms:
            # Landing on platform:
            if within_platform(self,i) and self.dy < 0 and i.slope == 'up':
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
              
               

            if within_platform(self,i) and self.dy < 0 and i.slope == 'down':
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
            self.jump = 'stop'
            self.counter = 0
            self.dy = 0
            
            
                       
            
def within_platform(player, platform): 
    if platform.xcor()-300 <= player.xcor() <= platform.xcor()+300:
        if platform.ycor()-31.5 <= player.ycor() <= platform.ycor()+ 31.5: # Not strictly correct but working best so far
            return True


def within_platform_x(player,platform):
    if platform.xcor()-300 <= player.xcor() <= platform.xcor()+300:
        return True


class Pen(turtle.Turtle):
    def __init__(self):
        super().__init__(shape='square')
        self.up()
        self.color('blue')
        self.hideturtle()

class Game():
    def __init__(self):
        self.win = turtle.Screen()
        self.win.title('Race to exit')
        self.win.bgcolor('lightblue')
        self.win.setup(800,700)
        self.win.tracer(0)
        self.win.listen()
        self.shape_list = ['door1.gif', 'door2.gif', 'stick-L1.gif', 'stick-L2.gif', 'stick-L3.gif', 'stick-R1.gif', 'stick-R2.gif',
              'stick-R3.gif']

        self.pen = Pen()


        # Register gif files as shapes
        for i in  self.shape_list:
            self.win.register_shape(i)

   
        # Place the platforms    
        self.platforms = []

        self.x_list = [-30, 30, -50, 30, -30]
        self.y_list = [-300, -170, -60, 70, 200]

        switch = 0
        for i in range(5):
            self.platform = Platform(self.x_list[i],self.y_list[i])
            if switch%2 == 0:
                self.platform.rt(6)
                self.platform.slope = 'down'
            else:
                self.platform.lt(6)
                self.platform.slope = 'up'
            self.platforms.append(self.platform)
            switch += 1

    def new_game(self):
        
            
        self.win.bgcolor('lightblue')
        self.counter = 0
        self.ball_list = []
        self.player = Player(self.platforms)
        self.door = Door()
        self.ball = Ball(self.platforms)

        self.ball_list.append(self.ball)
        self.pen.clear()

        self.run()

    def run(self):
        self.playing = True

        while self.playing:
            self.events()
            self.update()

    def events(self):
        self.win.onkey(self.player.move_right, 'Right')
        self.win.onkey(self.player.move_left, 'Left')
        self.win.onkey(self.player.jump_up, 'space')

    def update(self):
        self.counter += 1
        self.win.update()
        self.player.move()
        self.player.animate()
        self.delay = random.random()
    
        for i in self.ball_list:
            i.move()

            # New ball only if latest(new) ball is more than 200 pixels from door
            if i.distance(self.door) > 200 and i.age == 'new' and self.delay <0.005:
                self.ball = Ball(self.platforms)
                self.ball_list.append(self.ball)
                i.age = 'old' # Don't look at this ball anymore to create new ball

            if i.xcor() > 420:
                self.ball_list.remove(i)
           

            # Game over if hit by ball
            if self.player.distance(i) <= 18:
                self.win.bgcolor('yellow')
                self.win.update()
                self.playing = False
               
        
        # Game over if at the door
        if self.player.distance(self.door)<20:
            self.door.shape('door2.gif')
            self.win.bgcolor('yellow')
            self.win.update()
            self.playing = False
            
            


    def show_start_screen(self):
        self.waiting = True
        self.pen.goto(0, 0)
        self.win.onkey(self.wait_for_keypress, 'space')
        
        while self.waiting:
            self.win.bgcolor('yellow')
            self.pen.write('Race to the exit using Python 3 and Turtle\n\n Press the "space" key to continue',
                      align='center', font=('Courier', 18, 'normal'))
            
        


    def show_game_over_screen(self):
        self.waiting = True
        self.pen.goto(0, 0)
        self.win.onkey(self.wait_for_keypress, 'space')
        
        while self.waiting:
            self.pen.write('\t   Game Over \n\n Press the "space" key for new game',
                      align='center', font=('Courier', 18, 'normal'))

        self.player.goto(1000,1000)
        for i in self.ball_list:
            i.goto(1000,1000)
            

            

    def wait_for_keypress(self):
        self.waiting = False




game = Game()
game.show_start_screen()


while True:
    game.new_game()
    game.show_game_over_screen()
    

   



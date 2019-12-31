# Simple race to the exit game J Joubert 28 November 2019
# This is the last game in the book Python for Kids by Jason R Briggs
# Tkinter is used in the book
# I think this version in Python 3 and Turtle may be a bit easier
# (But not as elegant)
# Written in IDLE on mac osX (may need some adjustments in windows)

# Adding a game class gives little bit more control for start/game over screen
# or for adding levels

import turtle
import random
#import time # and time.sleep(0.017) windows??

class Door(turtle.Turtle):
    def __init__(self):
        super().__init__(shape='door1.gif')
        self.up()
        self.goto(-220,190)
        self.color('red')

class Player(turtle.Turtle):
    def __init__(self, platforms):
        super().__init__(shape='square')
        self.up()
        self.color('blue')
        self.s = 'stick-R1.gif'
        self.shape(self.s)
        self.goto(100, -220)
        self.platforms = platforms
        self.dx = 0
        self.dy = -6
        self.jump = 'stop'
        self.counter = 0
        
                                         
    def move_right(self):
        self.dx = 1
        self.s = 'stick-R1.gif'


    def move_left(self):
        self.dx = -1
        self.s = 'stick-L1.gif'


    def jump_up(self):
        if self.jump == 'stop': # cannot jump in the air
            self.jump = 'up'


    def animate(self):
        counter = game.gifcounter
        
        if self.dx<0:
            if self.s == 'stick-L1.gif' and counter%10 == 0:
                self.s = 'stick-L2.gif'
                self.shape(self.s)
            elif self.s == 'stick-L2.gif' and counter%10 == 0:
                self.s = 'stick-L3.gif'
                self.shape(self.s)
            elif self.s == 'stick-L3.gif' and counter%10 == 0:
                self.s = 'stick-L1.gif'
                self.shape(self.s)

        elif self.dx > 0:
            if self.s == 'stick-R1.gif' and counter%10 == 0:
                self.s = 'stick-R2.gif'
                self.shape(self.s)
            elif self.s == 'stick-R2.gif' and counter%10 == 0:
                self.s = 'stick-R3.gif'
                self.shape(self.s)
            elif self.s == 'stick-R3.gif' and counter%10 == 0:
                self.s = 'stick-R1.gif'
                self.shape(self.s)


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
        self.win.setup(500,500)
        self.win.tracer(0)
        self.win.listen()
        
        
        self.gifcounter = 0
        self.counter = 0
        self.shape_list = ['door1.gif', 'door2.gif', 'stick-L1.gif', 'stick-L2.gif', 'stick-L3.gif', 'stick-R1.gif', 'stick-R2.gif', 'stick-R3.gif',
              'platform1.gif', 'platform2.gif', 'platform3.gif', 'background.gif']
        

        

        # Register gif files as shapes
        for i in  self.shape_list:
            self.win.register_shape(i)

        self.pen = Pen()

        # Place background gif 5 in a row in x and y
        self.bg_x = [-200,-100,0,100,200]
        self.bg_y = [-200,-100,0,100,200]

        for i in self.bg_x:
            for j in self.bg_y:
                self.background = turtle.Turtle()
                self.background.up()
                self.background.shape('background.gif')
                self.background.goto(i,j)
   
     
        


    def new_game(self):
        self.level_number = 1
        # Place the platforms    
        self.platforms = []
        # y, x, gif (from bottom to top - y first)
        self.pf = [
            [-220,-200, 'platform1.gif'],
            [-180,-80, 'platform1.gif'],
            [-150,100, 'platform1.gif'],
            [-100,-50, 'platform2.gif'],
            [-50,-200, 'platform2.gif'],
            [-10,-80, 'platform3.gif'],
            [40,20, 'platform3.gif'],
            [80,130, 'platform1.gif'],
            [140,-40, 'platform2.gif'],
            [170, -200, 'platform2.gif']
            ]

        for i in self.pf:
            self.platform = turtle.Turtle()
            self.platform.up()
            self.platform.goto(i[1], i[0])
            self.platform.shape(i[2])
            if i[2] == 'platform1.gif':
                self.platform.width = 50
                self.platform.height = 10
            elif i[2] == 'platform2.gif':
                self.platform.width = 33
                self.platform.height = 10
            elif i[2] == 'platform3.gif':
                self.platform.width = 16
                self.platform.height = 10
            self.platforms.append(self.platform)

        self.counter = 0
        self.player = Player(self.platforms)
        self.door = Door()
        self.door.shape('door1.gif')
        self.pen.clear()

        self.win.update()

        
        

        self.run()

    def level_2(self):
        self.level = True
        self.level_number = 2
        self.pf = [
            [-220,-100, 'platform1.gif'],
            [-180,-200, 'platform1.gif'],
            [-150,-100, 'platform1.gif'],
            [-100,-200, 'platform2.gif'],
            [-50,-100, 'platform2.gif'],
            [-10,-30, 'platform1.gif'],
            [40,120, 'platform1.gif'],
            [80,0, 'platform1.gif'],
            [140,-100, 'platform2.gif'],
            [170, -200, 'platform2.gif']
            ]
        for i in self.pf:
            self.platform = turtle.Turtle()
            self.platform.up()
            self.platform.goto(i[1], i[0])
            self.platform.shape(i[2])
            if i[2] == 'platform1.gif':
                self.platform.width = 50
                self.platform.height = 10
            elif i[2] == 'platform2.gif':
                self.platform.width = 33
                self.platform.height = 10
            elif i[2] == 'platform3.gif':
                self.platform.width = 16
                self.platform.height = 10
            self.platforms.append(self.platform)

        self.player.goto(100, -220)
            
        
            

    def run(self):
        self.playing = True
        self.level = True

        # Level 1
        while self.playing and self.level:
            self.events()
            self.update()

        # Level 2
        self.level_number = 2
        self.level_2()
        
        while self.playing and self.level:
            self.events()
            self.update()

    def events(self):
        self.win.onkey(self.player.move_right, 'Right')
        self.win.onkey(self.player.move_left, 'Left')
        self.win.onkey(self.player.jump_up, 'space')


    def update(self):
        #time.sleep(0.017) # windows??
        
        self.gifcounter += 1
        self.win.update()
        self.player.animate()

        # Game over at the door
        if self.player.distance(self.door)<30:
            self.door.shape('door2.gif')
            self.win.update()
            self.level = False
            for i in self.platforms:
                i.goto(1000,1000)
            if self.level_number == 2:
                self.playing = False
            
            


        # Move left and right
        self.player.goto(self.player.xcor()+self.player.dx, self.player.ycor()+self.player.dy)

        # Don't drop off the bottom of the screen
        if self.player.ycor()<=-220:
            self.player.goto(self.player.xcor(), -220)
            self.player.dy = 0
            

        # Stop at the edges
        if self.player.xcor()>230 or self.player.xcor()<-230:
            self.player.dx *= 0
            

        # After pressing spacebar - jump
        if self.player.jump == 'up':
            self.player.dy = 5
           
            self.player.goto(self.player.xcor()+self.player.dx*7, self.player.ycor()+self.player.dy)
            self.counter += 1
            if self.counter == 10:
                self.player.jump = 'down'
                
        elif self.player.jump == 'down':
            self.player.dy = -12
            self.player.goto(self.player.xcor()+self.player.dx*7, self.player.ycor()+self.player.dy)
            if self.player.ycor() <= -220:
                self.player.jump = 'stop'
                self.counter = 0
                self.player.dy = -6
        
        for i in self.platforms:     
            # Landing/falling on platform working
            if within_platform(self.player, i) and self.player.dy<0:
                self.player.sety(i.ycor()+20)
                self.player.dy = 0
                self.player.jump = 'stop'
                self.counter = 0


            # fall off platform
            if not within_platform_x(self.player,i) and self.player.ycor() == i.ycor()+20:
                self.player.dy = -6
                
            # Stop at the side of the platform
            if within_platform(self.player, i) and i.ycor()-5 <= self.player.ycor()<= i.ycor()+5:
                self.player.dx =0

            # Jumping into a platform from below
            if within_platform(self.player,i) and self.player.dy >0 and self.player.ycor()<i.ycor()+10:
                self.player.sety(i.ycor()-20)
                self.player.jump = 'down'
                self.player.dy = -6
                

    def show_start_screen(self):
        self.waiting = True
        self.pen.goto(0, 0)
        self.win.onkey(self.wait_for_keypress, 'space')
        
        while self.waiting:
            self.win.bgcolor('black')
            self.pen.write('Race to the door using Python 3 and Turtle\n\n Press the "space" key to continue',
                      align='center', font=('Courier', 18, 'normal'))

    def show_game_over_screen(self):
        self.waiting = True
        self.level_number = 1
        self.playing = True
        self.pen.goto(0, 0)
        self.player.goto(1000,1000)
        for i in self.platforms:
            i.goto(1000,1000)
        self.win.onkey(self.wait_for_keypress, 'space')
        
        while self.waiting:
            self.win.bgcolor('black')
            self.pen.write('\t   Game Over \n\n Press the "space" key for new game',
                      align='center', font=('Courier', 18, 'normal'))
            

    def wait_for_keypress(self):
        self.waiting = False



# Functions to assess basic collisions:
def within_platform(player, platform): 
    if platform.xcor()-platform.width <= player.xcor() <= platform.xcor()+platform.width:
        if platform.ycor()-12 <= player.ycor() <= platform.ycor()+12:
            return True
    
def within_platform_x(player,platform):
    if platform.xcor()-platform.width <= player.xcor() <= platform.xcor()+ platform.width:
        return True
                    




game = Game()
game.show_start_screen()
    

while True:
    game.new_game()
    game.show_game_over_screen()
  






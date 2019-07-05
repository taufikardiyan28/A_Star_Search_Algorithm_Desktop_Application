import tkinter as tk
from tkinter import *
import random
import time
from astar import *
from PIL import Image, ImageTk


#  CONSTANTS
TIME = 0.05
CELL_SIZE = 35
NUMBER_OF_OBSTACLES = 30
SIZE = 10

STATE_OBSTACLE = 0
STATE_START = 1
STATE_END = 2

STATE_NO_DIAGONAL = 0
STATE_DIAGONAL = 1

class App(tk.Tk):    
    def __init__(self, obstacles, current_state, diagonal_state, start, end):
        tk.Tk.__init__(self)
        self.astar = AStar()    
        self.obstacles = obstacles
        self.current_state = current_state
        self.diagonal_state = diagonal_state
        self.start = start
        self.end = end
        self.title("Final Project - A* Algorithm")
        
        #Size Of the Window
        self.wm_geometry("725x880")
        # Gets the requested values of the height and widht.
        windowWidth = self.winfo_reqwidth()
        windowHeight = self.winfo_reqheight()

        # Gets both half the screen width/height and window width/height
        positionRight = int(self.winfo_screenwidth() / 3 - windowWidth / 2)
        positionDown = int(self.winfo_screenheight() / 6 - windowHeight / 2)

        # Positions the window in the center of the page.
        self.geometry("+{}+{}".format(positionRight, positionDown))

        self.configure(bd=10)
        
        self.logo_image = PhotoImage(file="images/banner.png")
        self.background_label = Label(self, image=self.logo_image, justify=CENTER, height=213, width=700)
        self.background_label.place(x=0, y=-100, relwidth=1, relheight=1)
        self.background_label.grid(row=0, column=0, pady=5)

        #Information Grid for Actions info
        self.information_frame = LabelFrame(self, width=SIZE*CELL_SIZE*SIZE/5, height=55, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1)                
        self.information_frame.place(x=1, y=100, relwidth=1, relheight=1)
        self.information_frame.propagate(False)
        self.information_frame.grid(row=1, column=0, pady=5)

        #Grid for the 2D Map        
        self.grid_frame = Frame(self)        
        self.grid_frame.grid(row=2, column=0)
        self.grid_frame.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)

        #Buttons's Frame  
        self.button_frame = Frame(self)              
        self.button_frame.grid(row=3, column=0, pady=10)
        self.button_frame.config(background='#ff4a4a', bd=1, highlightbackground="black", highlightcolor="black", highlightthickness=1)

        #Information Frame Configuration        
        self.information = Label(self.information_frame, text="Click on the start button to create a path between 2 random positions")
        self.information.config(background='#ff4a4a', font=("Tahoma", 12, "bold"), fg='white')
        self.information.pack(expand=True, fill=BOTH)

        self.frame_start_button = Frame(self.button_frame, width=SIZE*CELL_SIZE//2, height=65)
        self.frame_start_button.propagate(False)
        self.frame_start_button.grid(row=0, column=0)
        self.buttonimg1 = PhotoImage(file='images/button_start.png')
        self.start_button = Button(self.frame_start_button, command=self.create_path, image=self.buttonimg1, bd=0, bg='#ff4a4a')
        self.start_button.pack(expand=True, fill=BOTH)
        self.frame_custom_button = Frame(self.button_frame, width=SIZE*CELL_SIZE//2, height=65)
        self.frame_custom_button.propagate(False)
        self.frame_custom_button.grid(row=0, column=1)
        self.buttonimg2 = PhotoImage(file='images/new_map.png')
        self.custom_button = Button(self.frame_custom_button, command=self.new_map, image=self.buttonimg2, bd=0, bg='#ff4a4a')
        self.custom_button.pack(expand=True, fill=BOTH)
        
        # Set Start Button
        self.frame_custom_button = Frame(self.button_frame, width=SIZE*CELL_SIZE, height=65)
        self.frame_custom_button.propagate(False)
        self.frame_custom_button.grid(row=1, column=0)
        self.buttonimg3 = PhotoImage(file='images/set_start.png')
        self.custom_button3 = Button(self.frame_custom_button, command=lambda:self.custom(STATE_START), image=self.buttonimg3, bg='#ff4a4a', bd=0)
        self.custom_button3.pack(expand=True, fill=BOTH)

        # Set End Button
        self.frame_custom_button = Frame(self.button_frame, width=SIZE*CELL_SIZE, height=65)
        self.frame_custom_button.propagate(False)
        self.frame_custom_button.grid(row=1, column=1)
        self.buttonimg4 = PhotoImage(file='images/set_end.png')
        self.custom_button4 = Button(self.frame_custom_button, command=lambda:self.custom(STATE_END), image=self.buttonimg4, bd=0, bg='#ff4a4a')
        self.custom_button4.pack(expand=True, fill=BOTH)

        # Set Diagonal Button
        self.frame_custom_button = Frame(self.button_frame, width=SIZE*CELL_SIZE, height=65)
        self.frame_custom_button.propagate(False)
        self.frame_custom_button.grid(row=2, column=0)
        self.buttonimg5 = PhotoImage(file='images/set_diagonal.png')
        self.custom_button1 = Button(self.frame_custom_button, command=lambda:self.diagonal_custom(STATE_NO_DIAGONAL), image=self.buttonimg5, bd=0, bg='#ff4a4a')
        self.custom_button1.grid(row=1, column=0)
        self.custom_button1.pack(expand=True, fill=BOTH)

        # Set Obstacles Button
        self.frame_custom_button = Frame(self.button_frame, width=SIZE*CELL_SIZE, height=65)
        self.frame_custom_button.propagate(False)
        self.frame_custom_button.grid(row=2, column=1)
        self.buttonimg6 = PhotoImage(file='images/set_obstacles.png')
        self.custom_button2 = Button(self.frame_custom_button, command=lambda:self.custom(STATE_OBSTACLE), image=self.buttonimg6, bd=0, bg='#ff4a4a')
        self.custom_button2.pack(expand=True, fill=BOTH)

        # 2D Map Frame Configuration
        self.grid = Canvas(self.grid_frame, width=SIZE*CELL_SIZE, height=SIZE*CELL_SIZE, bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.grid.bind("<Button-1>", self.click)
        self.grid.pack()

    def Run(self):                    

        # Creating the Cells at the 2D Grid
        for x in range(SIZE):
            self.grid.create_line(0, x*CELL_SIZE, SIZE*CELL_SIZE, x*CELL_SIZE)
            self.grid.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, SIZE*CELL_SIZE)

        # Creating the Obstacles
        for i in range(NUMBER_OF_OBSTACLES):
            x, y = random.randint(0, SIZE-1), random.randint(0, SIZE-1)
            self.obstacles.append((x, y))
            self.grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='black')

        # Start Of Buttons Configuration #
        # Start Button        
        
        # New Map Button
        

    # End Of Buttons Configuration #

        self.mainloop()

    def new_map(self):
        global NUMBER_OF_OBSTACLES, CELL_SIZE, SIZE #, start, end, diagonal_state

        #Cleaning the Obstacles list in order to randomize a new list
        self.obstacles.clear()

        for i in range(NUMBER_OF_OBSTACLES):
            x, y = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)
            self.obstacles.append((x, y))
            self.grid.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill='black')

        self.refresh_map()


    def refresh_map(self):
        #global obstacles, CELL_SIZE, SIZE, start, end

        #Delete the 2D Grid
        self.grid.delete(ALL)

        #Build the 2D Grid
        for x in range(SIZE):
            self.grid.create_line(0, x*CELL_SIZE, SIZE*CELL_SIZE, x*CELL_SIZE)
            self.grid.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, SIZE*CELL_SIZE)

        #Draw the Obstacles's cells in Black
        for self.obstacle in self.obstacles:
            x, y = self.obstacle
            self.grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='black')

        # Draw the Starting Point in Green
        if self.start:
            x1, y1 = self.start
            self.grid.create_rectangle(x1*CELL_SIZE, y1*CELL_SIZE, (x1+1)*CELL_SIZE, (y1+1)*CELL_SIZE, fill='green')

        # Draw the Ending Point in Red
        if self.end:
            x2, y2 = self.end
            self.grid.create_rectangle(x2*CELL_SIZE, y2*CELL_SIZE, (x2+1)*CELL_SIZE, (y2+1)*CELL_SIZE, fill='red')

        self.update()


    def get_random_positions(self):
        #global start, end

        # Randomize Starting/Ending Point
        self.start = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
        while self.start in self.obstacles:
            self.start = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
        self.end = self.start
        while self.end == self.start or self.end in self.obstacles:
            self.end = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))


    def create_path(self):
        global CELL_SIZE, SIZE #, current_state, start, end, diagonal_state,image_state

        # Randomize Starting\Ending Point if not exist or its the obstacles list
        if not self.start:
            self.start = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
            while self.start == self.end or self.start in self.obstacles:
                self.start = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))

        if not self.end:
            self.end = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
            while self.start == self.end or self.end in self.obstacles:
                self.end = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))

        self.current_state = None
        self.start_button.config(state=DISABLED)
        self.custom_button.config(state=DISABLED, command=self.new_map)
        self.custom_button1.config(state=DISABLED, command=lambda:self.diagonal_custom(STATE_NO_DIAGONAL))
        self.custom_button2.config(state=DISABLED, command=lambda:self.custom(STATE_OBSTACLE))
        self.custom_button3.config(state=DISABLED, command=lambda:self.custom(STATE_START))
        self.custom_button4.config(state=DISABLED, command=lambda:self.custom(STATE_END))
        self.information.config(text="Click on the start button to create a path between 2 random positions")
        self.refresh_map()

        print("path between", self.start, self.end)
        x1, y1 = self.start
        x2, y2 = self.end

        path, debug = self.astar.get_path(self.start, self.end, self.obstacles, SIZE, self.diagonal_state)
        print(path, debug)
        #Shows the calculation of the algorithm
        for cell in debug[1:]:
            x, y = cell
            self.grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='yellow')
            self.update()
            time.sleep(TIME)
            self.grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='#bbbbdd')

        if path:
            print("    length :", len(path))

            #Load the Robot Image
            load = Image.open("images/robot.png")
            render = ImageTk.PhotoImage(load)
            img = Label(image=render)
            img.image = render

            #Placing the Robot's image at the Starting Point
            img.place(x=int((x1 + 1) * CELL_SIZE - 2 + 4.125 * CELL_SIZE), y=int((y1+1) * CELL_SIZE + 259))

            # Placing the Robot's image at the current cell of the path
            for cell in path[:-1]:
                x, y = cell
                self.update()
                time.sleep(1)
                self.grid.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill='#ff4a4a')
                img.place(x=int((x + 1) * CELL_SIZE - 2 + 4.125 * CELL_SIZE), y=int((y+1) * CELL_SIZE + 259))
                self.update()

                # Placing the Robot's image at the cell which is 1 before the end
                img.place(x=int((x + 1) * CELL_SIZE - 2 + 4.125 * CELL_SIZE), y=int((y+1) * CELL_SIZE + 259))
                self.update()

            # Placing the Robot's image at the Ending Point
            time.sleep(1)
            img.place(x=int((x2 + 1) * CELL_SIZE - 2 + 4.125 * CELL_SIZE), y=int((y2+1) * CELL_SIZE + 259))
            self.update()
            percentage = round(len(path)*100/len(debug), 3)
            time.sleep(2)
            # Closing the Robot's image
            img.destroy()

        else:
            print("    length : no path")
            percentage = 0
        print("    {0} cells analyzed ({1}%)\n".format(len(debug), percentage))

        self.start_button.config(state=NORMAL)
        self.custom_button.config(state=NORMAL)
        self.custom_button1.config(state=NORMAL)
        self.custom_button2.config(state=NORMAL)
        self.custom_button3.config(state=NORMAL)
        self.custom_button4.config(state=NORMAL)
        self.start = None
        self.end = None

        self.refresh_map()
        self.update()


    def custom(self, state):
        #global obstacles, current_state

        if state == STATE_OBSTACLE:
            self.current_state = STATE_OBSTACLE
            self.information.config(text="Click on the grid to set/remove obstacles")
            self.custom_button2.config(text="set the start", command=lambda:self.custom(STATE_START))
            self.refresh_map()

        elif state == STATE_START:
            self.current_state = STATE_START
            self.information.config(text="Click on the grid to place the start position")
            self.custom_button2.config(text="set the end", command=lambda:self.custom(STATE_END))

        elif state == STATE_END:
            self.current_state = STATE_END
            self.information.config(text="Click on the grid to place the end position")
            self.custom_button2.config(text="set the obstacles", command=lambda:self.custom(STATE_OBSTACLE))


    def click(self, event):
        #global obstacles, current_state, start, end

        x, y = event.x//CELL_SIZE, event.y//CELL_SIZE

        #Update the Starting/Ending Point & Obstacles up to the User will

        if self.current_state == STATE_OBSTACLE:
            if (x, y) in self.obstacles:
                self.obstacles.remove((x, y))
            else:
                self.obstacles.append((x, y))
            self.refresh_map()

        elif self.current_state == STATE_START:
            if (x, y) not in self.obstacles:
                self.start = (x, y)
                self.refresh_map()

        elif self.current_state == STATE_END:
            if (x, y) not in self.obstacles and (x, y) != self.start:
                self.end = (x, y)
                self.refresh_map()


    def diagonal_custom(self, state2):
        #global diagonal_state

        #Capture the state of the Movement

        if state2 == STATE_NO_DIAGONAL:
            self.diagonal_state = STATE_NO_DIAGONAL
            self.information.config(text="Without Diagonal Movment")
            self.custom_button1.config(text="Without Diagonal", command=lambda: self.diagonal_custom(STATE_DIAGONAL))

        else:
            self.diagonal_state = STATE_DIAGONAL
            self.information.config(text="With Diagonal Movment")
            self.custom_button1.config(text="With Diagonal", command=lambda: self.diagonal_custom(STATE_NO_DIAGONAL))

        self.refresh_map()
        self.update()


if __name__ == "__main__":
    app = App([], None, 0, None, None)
    app.Run()
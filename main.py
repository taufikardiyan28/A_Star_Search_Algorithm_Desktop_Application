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

#  GLOBALS
obstacles = []
current_state = None
diagonal_state = 0
start = None
end = None


def new_map():
    global obstacles, NUMBER_OF_OBSTACLES, CELL_SIZE, SIZE, start, end, diagonal_state

    #Cleaning the Obstacles list in order to randomize a new list
    obstacles.clear()

    for i in range(NUMBER_OF_OBSTACLES):
        x, y = random.randint(0, SIZE - 1), random.randint(0, SIZE - 1)
        obstacles.append((x, y))
        grid.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill='black')

    refresh_map()


def refresh_map():
    global obstacles, CELL_SIZE, SIZE, start, end

    #Delete the 2D Grid
    grid.delete(ALL)

    #Build the 2D Grid
    for x in range(SIZE):
        grid.create_line(0, x*CELL_SIZE, SIZE*CELL_SIZE, x*CELL_SIZE)
        grid.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, SIZE*CELL_SIZE)

    #Draw the Obstacles's cells in Black
    for obstacle in obstacles:
        x, y = obstacle
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='black')

    # Draw the Starting Point in Green
    if start:
        x1, y1 = start
        grid.create_rectangle(x1*CELL_SIZE, y1*CELL_SIZE, (x1+1)*CELL_SIZE, (y1+1)*CELL_SIZE, fill='green')

    # Draw the Ending Point in Red
    if end:
        x2, y2 = end
        grid.create_rectangle(x2*CELL_SIZE, y2*CELL_SIZE, (x2+1)*CELL_SIZE, (y2+1)*CELL_SIZE, fill='red')

    root.update()


def get_random_positions():
    global start, end

    # Randomize Starting/Ending Point
    start = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
    while start in obstacles:
        start = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
    end = start
    while end == start or end in obstacles:
        end = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))


def create_path():
    global CELL_SIZE, SIZE, current_state, start, end, diagonal_state,image_state

    # Randomize Starting\Ending Point if not exist or its the obstacles list
    if not start:
        start = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
        while start == end or start in obstacles:
            start = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))

    if not end:
        end = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))
        while start == end or end in obstacles:
            end = (random.randint(0, SIZE-1), random.randint(0, SIZE-1))

    current_state = None
    start_button.config(state=DISABLED)
    custom_button.config(state=DISABLED, command=new_map)
    custom_button1.config(state=DISABLED, command=lambda:diagonal_custom(STATE_NO_DIAGONAL))
    custom_button2.config(state=DISABLED, command=lambda:custom(STATE_OBSTACLE))
    custom_button3.config(state=DISABLED, command=lambda: custom(STATE_START))
    custom_button4.config(state=DISABLED, command=lambda: custom(STATE_END))
    information.config(text="Click on the start button to create a path between 2 random positions")
    refresh_map()

    print("path between", start, end)
    x1, y1 = start
    x2, y2 = end

    path, debug = get_path(start, end, obstacles, SIZE, diagonal_state)

    #Shows the calculation of the algorithm
    for cell in debug[1:]:
        x, y = cell
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='yellow')
        root.update()
        time.sleep(TIME)
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='#bbbbdd')

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
            root.update()
            time.sleep(1)
            grid.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, (x + 1) * CELL_SIZE, (y + 1) * CELL_SIZE, fill='#ff4a4a')
            img.place(x=int((x + 1) * CELL_SIZE - 2 + 4.125 * CELL_SIZE), y=int((y+1) * CELL_SIZE + 259))
            root.update()

            # Placing the Robot's image at the cell which is 1 before the end
            img.place(x=int((x + 1) * CELL_SIZE - 2 + 4.125 * CELL_SIZE), y=int((y+1) * CELL_SIZE + 259))
            root.update()

        # Placing the Robot's image at the Ending Point
        time.sleep(1)
        img.place(x=int((x2 + 1) * CELL_SIZE - 2 + 4.125 * CELL_SIZE), y=int((y2+1) * CELL_SIZE + 259))
        root.update()
        percentage = round(len(path)*100/len(debug), 3)
        time.sleep(2)
        # Closing the Robot's image
        img.destroy()

    else:
        print("    length : no path")
        percentage = 0
    print("    {0} cells analyzed ({1}%)\n".format(len(debug), percentage))

    start_button.config(state=NORMAL)
    custom_button.config(state=NORMAL)
    custom_button1.config(state=NORMAL)
    custom_button2.config(state=NORMAL)
    custom_button3.config(state=NORMAL)
    custom_button4.config(state=NORMAL)
    start = None
    end = None

    refresh_map()
    root.update()


def custom(state):
    global obstacles, current_state

    if state == STATE_OBSTACLE:
        current_state = STATE_OBSTACLE
        information.config(text="Click on the grid to set/remove obstacles")
        custom_button2.config(text="set the start", command=lambda:custom(STATE_START))
        refresh_map()

    elif state == STATE_START:
        current_state = STATE_START
        information.config(text="Click on the grid to place the start position")
        custom_button2.config(text="set the end", command=lambda:custom(STATE_END))

    elif state == STATE_END:
        current_state = STATE_END
        information.config(text="Click on the grid to place the end position")
        custom_button2.config(text="set the obstacles", command=lambda:custom(STATE_OBSTACLE))


def click(event):
    global obstacles, current_state, start, end

    x, y = event.x//CELL_SIZE, event.y//CELL_SIZE

    #Update the Starting/Ending Point & Obstacles up to the User will

    if current_state == STATE_OBSTACLE:
        if (x, y) in obstacles:
            obstacles.remove((x, y))
        else:
            obstacles.append((x, y))
        refresh_map()

    elif current_state == STATE_START:
        if (x, y) not in obstacles:
            start = (x, y)
            refresh_map()

    elif current_state == STATE_END:
        if (x, y) not in obstacles and (x, y) != start:
            end = (x, y)
            refresh_map()


def diagonal_custom(state2):
    global diagonal_state

    #Capture the state of the Movement

    if state2 == STATE_NO_DIAGONAL:
        diagonal_state = STATE_NO_DIAGONAL
        information.config(text="Without Diagonal Movment")
        custom_button1.config(text="Without Diagonal", command=lambda: diagonal_custom(STATE_DIAGONAL))

    else:
        diagonal_state = STATE_DIAGONAL
        information.config(text="With Diagonal Movment")
        custom_button1.config(text="With Diagonal", command=lambda: diagonal_custom(STATE_NO_DIAGONAL))

    refresh_map()
    root.update()


if __name__ == '__main__':

    root = Tk()
    root.title("Final Project - A* Algorithm")
    #Size Of the Window
    root.wm_geometry("725x880")


#Centering Root Window on Screen

    # Gets the requested values of the height and widht.
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()

    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth() / 3 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 6 - windowHeight / 2)

    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(positionRight, positionDown))

    root.configure(bd=10)

    #Logo\Banner Image On Top
    logo_image = PhotoImage(file="images/banner.png")
    background_label = Label(root, image=logo_image, justify=CENTER, height=213, width=700)
    background_label.place(x=0, y=-100, relwidth=1, relheight=1)
    background_label.grid(row=0, column=0, pady=5)

    #Information Grid for Actions info
    information_frame = LabelFrame(root, width=SIZE*CELL_SIZE*SIZE/5, height=55, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=1)
    information_frame.place(x=1, y=100, relwidth=1, relheight=1)
    information_frame.propagate(False)
    information_frame.grid(row=1, column=0, pady=5)

    #Grid for the 2D Map
    grid_frame = Frame(root)
    grid_frame.grid(row=2, column=0)
    grid_frame.config(highlightbackground="black", highlightcolor="black", highlightthickness=1)

    #Buttons's Frame
    button_frame = Frame(root)
    button_frame.grid(row=3, column=0, pady=10)
    button_frame.config(background='#ff4a4a', bd=1, highlightbackground="black", highlightcolor="black", highlightthickness=1)

    #Information Frame Configuration
    information = Label(information_frame, text="Click on the start button to create a path between 2 random positions")
    information.config(background='#ff4a4a', font=("Tahoma", 12, "bold"), fg='white')
    information.pack(expand=True, fill=BOTH)

    # 2D Map Frame Configuration
    grid = Canvas(grid_frame, width=SIZE*CELL_SIZE, height=SIZE*CELL_SIZE, bg='white', highlightbackground="black", highlightcolor="black", highlightthickness=1)
    grid.bind("<Button-1>", click)
    grid.pack()

    # Creating the Cells at the 2D Grid
    for x in range(SIZE):
        grid.create_line(0, x*CELL_SIZE, SIZE*CELL_SIZE, x*CELL_SIZE)
        grid.create_line(x*CELL_SIZE, 0, x*CELL_SIZE, SIZE*CELL_SIZE)

    # Creating the Obstacles
    for i in range(NUMBER_OF_OBSTACLES):
        x, y = random.randint(0, SIZE-1), random.randint(0, SIZE-1)
        obstacles.append((x, y))
        grid.create_rectangle(x*CELL_SIZE, y*CELL_SIZE, (x+1)*CELL_SIZE, (y+1)*CELL_SIZE, fill='black')

    # Start Of Buttons Configuration #
    # Start Button
    frame_start_button = Frame(button_frame, width=SIZE*CELL_SIZE//2, height=65)
    frame_start_button.propagate(False)
    frame_start_button.grid(row=0, column=0)
    buttonimg1 = PhotoImage(file='images/button_start.png')
    start_button = Button(frame_start_button, command=create_path, image=buttonimg1, bd=0, bg='#ff4a4a')
    start_button.pack(expand=True, fill=BOTH)

    # New Map Button
    frame_custom_button = Frame(button_frame, width=SIZE*CELL_SIZE//2, height=65)
    frame_custom_button.propagate(False)
    frame_custom_button.grid(row=0, column=1)
    buttonimg2 = PhotoImage(file='images/new_map.png')
    custom_button = Button(frame_custom_button, command=new_map, image=buttonimg2, bd=0, bg='#ff4a4a')
    custom_button.pack(expand=True, fill=BOTH)

    # Set Start Button
    frame_custom_button = Frame(button_frame, width=SIZE*CELL_SIZE, height=65)
    frame_custom_button.propagate(False)
    frame_custom_button.grid(row=1, column=0)
    buttonimg3 = PhotoImage(file='images/set_start.png')
    custom_button3 = Button(frame_custom_button, command=lambda:custom(STATE_START), image=buttonimg3, bg='#ff4a4a', bd=0)
    custom_button3.pack(expand=True, fill=BOTH)

    # Set End Button
    frame_custom_button = Frame(button_frame, width=SIZE*CELL_SIZE, height=65)
    frame_custom_button.propagate(False)
    frame_custom_button.grid(row=1, column=1)
    buttonimg4 = PhotoImage(file='images/set_end.png')
    custom_button4 = Button(frame_custom_button, command=lambda:custom(STATE_END), image=buttonimg4, bd=0, bg='#ff4a4a')
    custom_button4.pack(expand=True, fill=BOTH)

    # Set Diagonal Button
    frame_custom_button = Frame(button_frame, width=SIZE*CELL_SIZE, height=65)
    frame_custom_button.propagate(False)
    frame_custom_button.grid(row=2, column=0)
    buttonimg5 = PhotoImage(file='images/set_diagonal.png')
    custom_button1 = Button(frame_custom_button, command=lambda:diagonal_custom(STATE_NO_DIAGONAL), image=buttonimg5, bd=0, bg='#ff4a4a')
    custom_button1.grid(row=1, column=0)
    custom_button1.pack(expand=True, fill=BOTH)

    # Set Obstacles Button
    frame_custom_button = Frame(button_frame, width=SIZE*CELL_SIZE, height=65)
    frame_custom_button.propagate(False)
    frame_custom_button.grid(row=2, column=1)
    buttonimg6 = PhotoImage(file='images/set_obstacles.png')
    custom_button2 = Button(frame_custom_button, command=lambda:custom(STATE_OBSTACLE), image=buttonimg6, bd=0, bg='#ff4a4a')
    custom_button2.pack(expand=True, fill=BOTH)

# End Of Buttons Configuration #

    root.mainloop()

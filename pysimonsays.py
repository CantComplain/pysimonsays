import tkinter as tk
from tkinter import Frame
from time import sleep
import random


class BaseProgram(tk.Tk):    # Our root window, that the program will run in
    def __init__(self) :    # This whole class is actually currently unessacary until I add menus and stuff ...
        tk.Tk.__init__(self)

        self.wm_title("SimonSays")       # Sets the Title of our window

        FrameMan = Frame(self,background="green") # Can set an outline or background color if want. it shouldn't really be seen.
        FrameMan.pack(fill="both",expand=1)    #Fill the slot its in. The window only have 1 slot
        
        # FrameMan = Frame Manager or the guy who decides which screen will show in the window

        FrameMan.grid_rowconfigure(0,weight=1)
        FrameMan.grid_columnconfigure(0,weight=1) # makes this frame adjust to the size of the window.

        self.pages = {} # a dic of all the pages in our program

        #TODO: Add Settings Page
        #TODO: Possibly add a "You Lost" page
        #TODO: Statistics Page?

        for page in (SimonSays,MainMenu,Lost,) : # must add new menus here...
            vpage = page(FrameMan,self)    # Calls and creates the page

            self.pages[page] = vpage        # Stores that page in the dict so it can be referenced again

            vpage.grid(row=0,column=0,sticky="nsew")  

        #self.Show_Page(MainMenu,)  # Starts the Game

        self.Show_Page(MainMenu)

    def Show_Page(self,page) : #We can change the page with this, just pass in name of Page
        shown = self.pages[page]
        shown.tkraise()   # Makes the frame show on TOP of the stack. Other windows are actually still there behind it
        if isinstance(shown,SimonSays) :
            shown.master.after(2000,shown.playgame)
        elif isinstance(shown,Lost) :
            var = "Highscore : "+str(self.Highscore)
            shown.Hs["text"] = var
            var = "Score : "+str(self.Score)
            shown.Ls["text"] = var


class SimonSays(Frame) :

    SPEED = 750  # class Var that decides how fast the  computer will run through it's turns

    #TODO: add speedup, every certain amount of turns the speed becomes faster by a certain amount

    def __init__(self,FrameManager,Program) :

        Frame.__init__(self,FrameManager) # Creates our Frame or "screen"  which will be managed by FrameManager
        
        self.Program = Program
        self.Program.Highscore = 0

        self.grid_rowconfigure(0,weight=1)       # Configure all the rows and columns
        self.grid_rowconfigure(1,weight=2)      # Inner rows have a bigger weight so they displace the outer spacer rows
        self.grid_rowconfigure(2,weight=2)
        self.grid_rowconfigure(3,weight=1)
       
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=2)
        self.grid_columnconfigure(2,weight=2)
        self.grid_columnconfigure(3,weight=1)

        # The Label self.Label will tell us about our game state... ie who is playing

        self.Label = tk.Label(self, text="Starting Game...",height=3,width=3,relief="ridge",borderwidth=10)
        self.Label.grid(row=0,column=1,sticky="nsew") 

        #the xspace labels are just blank frames that provides space around the main play area

        leftspace = tk.Label(self, text="",height=3,width=3,borderwidth=10)
        leftspace.grid(row = 0,column=0,rowspan=4,sticky="nsew")

        botspace = tk.Label(self, text="",height=3,width=3,borderwidth=10)
        botspace.grid(row = 4,column=1,columnspan=2,sticky="nsew")

        rightspace = tk.Label(self, text="",height=3,width=3,borderwidth=10)
        rightspace.grid(padx=4,row = 0,column=3,rowspan=4,sticky="nsew")

        # the label self.Display will show which button has been pressed last

        #TODO: Automate display changing

        self.Display = tk.Label(self,bg="white", text="",relief="ridge",borderwidth=4,height=3,width=3)
        self.Display.grid(row=0,column=2,sticky="nsew",padx=20,pady=20)


        #The self.Color buttons are the 4 main buttons that the game features. 

        self.Blue = tk.Button(self, state="disabled",disabledforeground="Black", text="Blue", bg="blue",height=10,width=20,borderwidth=8,command=lambda: self.buttonchosen(self.Blue))
        self.Blue.grid(row=2,column=1,sticky="nsew")

        self.Red = tk.Button(self,state="disabled",disabledforeground="Black", text="Red", bg="red",borderwidth=8,height=10,width=20,command=lambda: self.buttonchosen(self.Red))
        self.Red.grid(row=1,column=2,sticky="nsew")

        self.Green = tk.Button(self,state="disabled",disabledforeground="Black", text="Green", bg="green",borderwidth=8,height=10,width=20,command=lambda: self.buttonchosen(self.Green))
        self.Green.grid(row=1,column=1,sticky="nsew")

        self.Yellow = tk.Button(self,state="disabled",disabledforeground="Black", text="Yellow", bg="yellow",borderwidth=8,height=10,width=20,command=lambda: self.buttonchosen(self.Yellow))
        self.Yellow.grid(row=2,column=2,sticky="nsew")


        # self.buttons is a tuple for performing operations on all the buttons

        self.buttons = (self.Blue,self.Red,self.Green,self.Yellow,)



        #self.master.after(2000,self.playgame) # Gives us a short time to make sure window is loaded/ player is paying attention

    def playgame(self) :
        self.score = 0

        self.simonsaid = [] # Will Store the randomly selected sequence
        self.playerpressed = [] # Will Store what the player pressed

        self.Label["text"] = "Computer's Turn!"   
        self.master.after(1500,self.Computerturn) #gives you a little time before it starts flashing

    def Computerturn(self) :

        self.Label.config(text="Computer's Turn!")  # Make the Label show that it's the Computer's Turn

        self.simonsaid.append(random.choice(self.buttons)) # Select a random button each time it's the computer's turn
        

        for button in self.buttons :
            button["state"] = "disabled"   # Disable all of the buttons while it's the computer's turn!
        
        for num,buttonpressed in enumerate(self.simonsaid) :
            self.master.after(num*self.SPEED, self.flashbutton, buttonpressed)  #makes each button flash after each other

                            #We have to do the self.SPEED stuff because master.after actually doesn't stop the next buttons from flashing


            #After showing the sequence give the player a little bit of time before switching; less jarring
        self.master.after(len(self.simonsaid)*self.SPEED+500,self.playerturn)
            #Timing prob needs to be tweaked


    def flashbutton(self,buttonpressed) :  # Makes the button flash itself by changing color to white than changing back
        color = buttonpressed["bg"] #store button color
        self.Display["text"] = buttonpressed["text"] 
        self.Display["bg"] = color   # makes display show the button was pressed
        
        buttonpressed.config(bg="white") # Turn button white

        #after some time make it it's regular color again
        self.master.after(self.SPEED//2,lambda : buttonpressed.config(bg=color))
                # during each computer "turn" a button will spend half it's time white and half regular color

    def playerturn(self) :
        # Show that it's the player's turn
        self.Label.config(text="Player's Turn!")

        # Clear out the list of buttons that have been pressed
        self.playerpressed = []

        # Make all The buttons pressable again
        for button in self.buttons :
            button["state"] = "normal"

    def buttonchosen(self,button) :

        self.playerpressed.append(button)
        # Add the button to list of buttons the player pressed

        self.Display["text"] = button["text"]  # make display show this button was pressed
        self.Display["bg"] = button["bg"]

        if self.simonsaid[:len(self.playerpressed)] == self.playerpressed : #if player's pressed buttons so far matches what simon wants
            if len(self.simonsaid) == len(self.playerpressed) :  # pass unless player has pressed every button
                                                                 # if they have.
                self.Label["text"] = "Correct. Changing Turn..."  # Tell them they are right and turn is changing
                for b in self.buttons :                           # disable all the buttons
                    b["state"] = "disabled"
                self.score += 1

                self.master.after(1500,self.Computerturn)         # after a bit go back to computer's turn

        else :  #if the player pressed a button that isn't what simon wants
            self.lost() #they lost

    def lost(self) : # when a player loses
        #self.Label["text"] = "You Lost!"  #show they lost on label
        for button in self.buttons :     # disable all the buttons
            button["state"] = "disabled"
        self.Label["text"] = "Starting Game..."
        self.Display["bg"] = "white"
        self.Display["text"] = ""
        self.Program.Score = self.score
        if self.score > self.Program.Highscore :
            self.Program.Highscore = self.score

        self.Program.Show_Page(Lost)

        #TODO : add ability to retry


class MainMenu(Frame) :
    def __init__(self,FrameManager,Program) :

        Frame.__init__(self,FrameManager) # Creates our Frame or "screen"  which will be managed by FrameManager

        self.Program = Program
        
        self.Title = tk.Label(self,text="Simon Says",height=2,font=("", 44))
        self.Title.pack()

        self.Play = tk.Button(self, text="Play Game",bg="green",borderwidth=2,height=3,width=10,command=self.play)
        self.Play.pack()

    def play(self) :
        self.Program.Show_Page(SimonSays)
        

class Lost(Frame) :
    def __init__(self,FrameManager,Program) :

        Frame.__init__(self,FrameManager) # Creates our Frame or "screen"  which will be managed by FrameManager

        self.Program = Program
        
        self.Title = tk.Label(self,text="You Lost!",height=2,font=("", 44))
        self.Title.pack()

        self.Ls = tk.Label(self,font=("", 20))
        self.Ls.pack()

        self.Hs = tk.Label(self,font=("", 20),height=4)
        self.Hs.pack()

        self.PlayAgain = tk.Button(self, text="Play Again",bg="green",borderwidth=2,height=3,width=10,command=self.playagain)
        self.PlayAgain.pack()

    def playagain(self) :
        self.Program.Show_Page(SimonSays)


app = BaseProgram()
app.minsize(width=400,height=400)
app.geometry("600x500")
app.mainloop()

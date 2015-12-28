# -*- coding: utf-8 -*-
# Maja Svanberg & Bella Nikom
# CS111, final project
# 2015-04-27
# runGame.py

import Tkinter as tk
import random
import objectsAnimation
import animation

GAMETITLE = 'The ULTIMATE Frisbee Game'
LENGTHOFFIELD = 10
NUMANSWERS = 4
STARTPICLIST = ['teampic.gif', 'teampic2.gif', 'teampic3.gif', 'teampic4.gif', 'teampic5.gif', 'teampic6.gif', 'teampic7.gif', 'teampic8.gif']

class StartPage(tk.Frame):
    def __init__(self, root): #create variables necessary for startpage
        tk.Frame.__init__(self)
        # lets startpage recognize whether or not a game window or 
        # instructions window is running
        self.w_app = None
        self.w_inst = None
        self.w_tuts = None
        
        root.title(GAMETITLE)
        self.configure(bg='black')
        self.grid()
        
        self.createWidgets()
        
    def createWidgets(self):
        
        #Image
        pic = tk.PhotoImage(file=random.choice(STARTPICLIST))
        self.imageLabel = tk.Button(self, image=pic,borderwidth=0)
        self.imageLabel.pic = pic
        self.imageLabel.grid(row=0,column=0, columnspan=4)
        self.imageLabel.config(command=self.onImageClick)
        
        # game window-button
        self.startButton = tk.Button(self,text = 'Pull!', font='Steelfish 20', fg='gray', bg='black', command = self.onStartButtonClick)
        self.startButton.grid(row=1,column=0, sticky = tk.E+tk.W+tk.S)
        
        # instructions window-button
        instButton = tk.Button(self, text='Instructions', fg='gray', bg='black', font='Steelfish 20',
        command=self.onInstButtonClick)
        instButton.grid(row=1,column=1, sticky=tk.E+tk.W+tk.S)
        
        # tutorials-button        
        tutsButton = tk.Button(self, text='Tutorials', fg='gray', bg='black', font='Steelfish 20',\
        command=self.onTutsButtonClick)
        tutsButton.grid(row=1,column=2, sticky=tk.E+tk.W+tk.S)
        
        # quit-button        
        quitButton = tk.Button(self, text='Quit', fg='gray', bg='black', font='Steelfish 20',\
        command=self.onQuitButtonClick)
        quitButton.grid(row=1,column=3, sticky=tk.E+tk.W+tk.S)
        
    def onImageClick(self):
        newpic = tk.PhotoImage(file=random.choice(STARTPICLIST)) # create new PhotoImage
        self.imageLabel.configure(image=newpic) # change Label's image
        # store image, otherwise gets deleted when UI refreshes
        self.imageLabel.image = newpic 

    def onStartButtonClick(self):
        if self.w_app!=None: self.w_app.destroy() # if a window exists, detroy it
        if self.w_tuts!=None: self.w_tuts.destroy()
        self.w_app = GameApp() #opens new window with trivia game
        self.w_app.mainloop() #starts game
    
    def onQuitButtonClick(self):
        self.destroy() #destroys window
        root.destroy()
        
    def onInstButtonClick(self):
        if self.w_inst!=None: self.w_inst.destroy() # if a window exists, detroy it
        if self.w_tuts!=None: self.w_tuts.destroy()
        self.w_inst = Instructions() #opens new window with trivia game
        self.w_inst.mainloop() # runs instructions
        
    def onTutsButtonClick(self):
        if self.w_inst!=None: self.w_inst.destroy()
        if self.w_app!=None: self.w_app.destroy()
        self.w_tuts = Tutorials()
        self.w_tuts.mainloop()

class Instructions(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title(GAMETITLE + ' Instructions')
        root.config(bg='black')
        self.config(bg='black')
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        # photo to the right
        pic = tk.PhotoImage(file='lizard.gif')
        self.imageLabel = tk.Label(self, image=pic,borderwidth=0)
        self.imageLabel.pic = pic
        self.imageLabel.grid(row=1,column=1, rowspan=3)
        # opens the file with instructions
        instructionsList = open('instructions.txt').readlines()
        # sets header as larger, centered, with first line of instructions
        headerLabel = tk.Label(self, fg='white', bg='black', font=20, text=str(instructionsList[0]))
        headerLabel.grid(row=1,column=0, sticky=tk.S)
        # defines where instructions can be found in list and displays it
        instructionsString = reduce(lambda x, y: x+y, instructionsList[1:-1])
        instructLabel = tk.Label(self, fg='white', bg='black', text=str(instructionsString), justify='left')
        instructLabel.grid(row=2,column=0, ipadx=20)
        # "have fun" centered at the bottom
        funLabel = tk.Label(self, fg='white', bg='black', font = 14, text=str(instructionsList[-1]))
        funLabel.grid(row=3,column=0, sticky=tk.N)
        # return button
        returnButton = tk.Button(self, text='Close window and return to Start Page', fg='gray', bg='black', command=self.onReturnButtonClick)
        returnButton.grid(row=0,column=0, columnspan=2, sticky=tk.N+tk.E+tk.W+tk.S)
        
    def onReturnButtonClick(self):
        self.destroy()
        
class Tutorials(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.title('Ultimate Frisbee tutorials')
        root.config(bg='black')
        self.config(bg='black')
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        # title
        titleLabel = tk.Label(self, fg='white', bg='black', font = 40, text=str('Ultimate Frisbee Tutorials'))
        titleLabel.grid(row=0, column=0, columnspan=10, sticky=tk.N+tk.E+tk.W+tk.S)
        
        #Image and Title
        pic = tk.PhotoImage(file='field.gif')
        imageLabel = tk.Label(self, image=pic,borderwidth=0)
        imageLabel.pic = pic
        imageLabel.grid(row=1,column=0, rowspan=6)
        
        # return button
        returnButton = tk.Button(self, text='Main Menu', fg='gray', bg='black', command=self.destroy)
        returnButton.grid(row=5,column=7, sticky=tk.N+tk.E+tk.W+tk.S)

class QuestionsAndAnswers:
    '''reads the file containing definitions and terms and devides it into
    questions and answers'''
    def __init__(self, filename):
        lines = open(filename).readlines()
        self.QandA_list = []     # A list of question/answer tuples read in from file
        def readAndFormat(line):
            splitLine = line.strip().split('\t')  # Assumes tab-delimited file
            self.QandA_list.append((splitLine[0].strip(), splitLine[1].strip()))
        map(readAndFormat, lines)
        # Populate list of questions/answers with data from file

    def get_random_QandA_number(self):
        '''Every question/answer has a number associated with it, i.e., the index
        it occurs in the list. Return the number associated with a randmoly
        chosen question/answer.'''
        return random.randint(0, len(self.QandA_list)-1)

    def getQuestion(self, number):
        '''Returns the question associated with the given number.'''
        return self.QandA_list[number][1]

    def getAnswer(self, number):
        '''Returns the answer associated with the given number.'''
        return self.QandA_list[number][0]


class GameApp(tk.Toplevel):
    def __init__(self):
        tk.Toplevel.__init__(self)
        self.QA = QuestionsAndAnswers('terms_definitions.txt')
        root.title(GAMETITLE)
        root.config(bg='black')
        self.config(bg='black')
        self.grid()
        # Total number of questions = length of field
        self.lengthOfField = LENGTHOFFIELD 
        # Number of answer options
        self.numberOfAnswers = NUMANSWERS        
        # Current question number (increments with after each question)        
        self.currentPositionOnField = random.randint(1,4)   
         # Number/index of current question
        self.indexOfCurrentQuestion = self.QA.get_random_QandA_number() 
        # list of alreadyUsedIndices makes sure no questions gets repeated
        self.alreadyUsedIndices = [self.indexOfCurrentQuestion] 
        self.awaitingUserToSubmitAnswer = True  
        # if blue team has the disc
        self.inPossession = True
        # if previous answer was correct, determines the outcome of the animation
        self.previousAnswerCorrect = True
        # ends the game
        self.gameOver = False
        
        self.createWidgets()
        
        # list of players enables for quick removal of all players on the field
        self.players = []
        # creates a canvas for the animation, starting outside of screen for 
        # design purposes
        self.canvas = animation.AnimationCanvas(self, width = 305, height = 361)
        self.canvas.config(bg='darkgreen')
        self.canvas.place(x=-2, y=-2)        
        # starts the pull animation (initiates the ultimate game)
        self.startPullAnimation()
        

    def createWidgets(self):
        
        #Image and Title
        pic = tk.PhotoImage(file='field.gif')
        imageLabel = tk.Label(self, image=pic,borderwidth=0)
        imageLabel.pic = pic
        imageLabel.grid(row=0,column=0, rowspan=6)

        # Question
        self.question = tk.StringVar()
        questionLabel = tk.Label(self, fg='white', bg='black', \
        font='Times 14', textvariable=self.question,)
        questionLabel.grid(row=1,column=1, columnspan=5,\
        sticky=tk.N+tk.E+tk.W)
        self.setQuestion()  # Set text of question

        # Answers
        self.answerIndex = tk.IntVar()  # Index of selected button
        self.answerTexts = []  # List of StringVars, one for each button. 
        # Each list element allows getting/setting the text of a button.
        for i in range(0, self.numberOfAnswers):
            self.answerTexts.append(tk.StringVar())
        self.rbs = []                           # a list of our buttons
        for i in range(0, self.numberOfAnswers):  # Create buttons
            self.rb = tk.Radiobutton(self, indicatoron = 0, fg='black', bg='white', textvariable=self.answerTexts[i], \
            variable=self.answerIndex, value=i, command = self.onRadioButton)
            if i < 2:
                self.rb.grid(row=2+i, column=1, columnspan=2, sticky=tk.N+tk.E+tk.W+tk.S)
            else:
                self.rb.grid(row=i, column=3, columnspan=2, sticky=tk.N+tk.E+tk.W+tk.S)
            self.rbs.append(self.rb)
        self.setAnswers()  # Set text of radiobuttons

        # Progressbar, allows access to correct file
        pic = tk.PhotoImage(file='progressbar'+str(self.currentPositionOnField)+'.gif')
        self.progressLabel = tk.Label(self, image=pic,borderwidth=0)
        self.progressLabel.pic = pic
        self.progressLabel.grid(row=0,column=1, columnspan=4, padx = 10)
        
        # Status Label, explains state of the game to user
        self.results = tk.StringVar()
        self.resultsLabel = tk.Label(self, fg='white', bg='black', textvariable=self.results)
        self.resultsLabel.grid(row=4,column=1, columnspan = 2, sticky=tk.N+tk.E+tk.W+tk.S)

        # next Button, disabled until question is answered
        self.nextButton = tk.Button(self, text='Next', fg='gray', bg='black', \
        state='disabled', command=self.onNextButtonClick)
        self.nextButton.grid(row=4,column=3, sticky=tk.N+tk.E+tk.W+tk.S)
        
        # return button
        returnButton = tk.Button(self, text='Main Menu', fg='gray', bg='black', command=self.onReturnButtonClick)
        returnButton.grid(row=4,column=4, sticky=tk.N+tk.E+tk.W+tk.S)

    def setQuestion(self):
        self.question.set('What is: \n ' + str(self.QA.getQuestion(self.indexOfCurrentQuestion)))

    def setAnswers(self):
        '''Populates the answer radiobuttons in a random order 
        with the correct answer as well as random answers.'''
        self.answers = []  # List of possible answers
        self.answers.append(self.QA.getAnswer(self.indexOfCurrentQuestion))  
        # Add correct answer to list
        while len(self.answers) != self.numberOfAnswers:  
            # Add random answers to list. Ensure each random answer 
            #is not already in list, i.e., no duplicates.
            index = self.QA.get_random_QandA_number()  
            # Get random number/index
            if self.QA.getAnswer(index) not in self.answers:  
                # Ensure random answer is not already in answer list
                self.answers.append(self.QA.getAnswer(index))  
                # Add random answer to list
        random.shuffle(self.answers)  # Randomly shuffle answer list
        for i in range(0, len(self.answers)):  # Populate text of radiobuttons
            self.answerTexts[i].set(self.answers[i])
            self.rbs[i].deselect() # deselect the radiobuttons
            
    def onRadioButton(self):
        if self.awaitingUserToSubmitAnswer == True:
            # if the answer is correct
            if self.answers[self.answerIndex.get()] \
            ==self.QA.getAnswer(self.indexOfCurrentQuestion): 
                # if in possession or not, you will either advance or win disc
                #updates results label to display that the user was correct
                if self.inPossession:
                    self.results.set('Correct! \n Press next to watch your team move up the field')
                else:
                     self.results.set('Correct! \n Press next to watch your team get the disc back')
                self.previousAnswerCorrect = True
                self.currentPositionOnField += 1
            # if answer is incorrect
            else:
                # if in possession or not, either lose disc or opponents advance
                #updates results label to display that the user was incorrect
                if self.inPossession:
                    self.results.set('Incorrect: the correct answer is ' \
                + str(self.QA.getAnswer(self.indexOfCurrentQuestion) + \
                '\n Press next to watch your team lose the disc'))
                else:
                    self.results.set('Incorrect: the correct answer is ' \
                + str(self.QA.getAnswer(self.indexOfCurrentQuestion) + \
                '\n Press next to watch the opponents advance'))
                self.currentPositionOnField += -1
                self.previousAnswerCorrect = False
            # whether or not answer was incorrect
            self.updateProgressBar()
            self.awaitingUserToSubmitAnswer = False
            # remove old animation and start a new one with given conditions
            self.stopAnimation()
            self.startAnimation(self.inPossession, self.previousAnswerCorrect)
            # enable nextButton
            self.nextButton.config(state='normal')
            # updates in possession
            if self.previousAnswerCorrect == False:
                self.inPossession = False
            else:
                self.inPossession = True
        # if we're not awaiting an answer, and game is not over...
        else:
            if self.gameOver == False:
                self.results.set('You already answered this question!\nThe correct answer is  ' + str(self.QA.getAnswer(self.indexOfCurrentQuestion)) + '\n Press "Next" to continue')            
            
    def onNextButtonClick(self):
        # make selected animation move
        self.canvas.start()
        # if neither endzone has been reached
        if self.currentPositionOnField < self.lengthOfField and self.currentPositionOnField > 0:
            self.newQuestion()
        else:
            self.awaitingUserToSubmitAnswer = False
            self.nextButton.configure(state='disabled')
            self.gameOver = True
            if self.currentPositionOnField == 0:
                self.results.set('Game over! The opponent scored. \n Press Main Menu to return to Start Page\nand play again')
            else:
                self.results.set('You scored! Well done \n Press Main Menu to return to Start Page')

    def onReturnButtonClick(self):
        self.destroy()

    def updateProgressBar(self):
        # if within range of progressbar, update picture
        if self.currentPositionOnField < 11 and self.currentPositionOnField >=0:
            newpic = tk.PhotoImage(file='progressbar'+\
            str(self.currentPositionOnField)+'.gif') # create new PhotoImage
            self.progressLabel.configure(image=newpic) # change Label's image
            # store image, otherwise gets deleted when UI refreshes
            self.progressLabel.image = newpic 

    def newQuestion(self):
        # get a random question
        self.indexOfCurrentQuestion = self.QA.get_random_QandA_number()
        while self.indexOfCurrentQuestion in self.alreadyUsedIndices: #if it has already been asked...
            self.indexOfCurrentQuestion = self.QA.get_random_QandA_number() #generate a new question so there are no repeats
        self.alreadyUsedIndices.append(self.indexOfCurrentQuestion) #add to list once it has been asked
        self.setQuestion()
        self.setAnswers()
        self.results.set('')
        self.nextButton.configure(text='Next', state='disabled')
        self.awaitingUserToSubmitAnswer = True
        
    def stopAnimation(self):
        self.canvas.stop()
        for p in self.players:
            self.canvas.removeItem(p)
        self.players = []
    
    def startPullAnimation(self):
        self.canvas.addItem(Photo(self.canvas, 'field.gif', 0, 0))
        
        def addAndAppend(Object):
            self.players.append(Object)
            self.canvas.addItem(Object)
        # add players
        for i in range(7):
            addAndAppend(objectsAnimation.Players(self.canvas, 20+40*i, 320, 30, 0, 'blue'))
            addAndAppend(objectsAnimation.Players(self.canvas, 20+40*i, 20, 30, 0, 'red'))
        # add disc
        addAndAppend(objectsAnimation.BigDisc(self.canvas, 150, 0, 1.5, 'disc.gif'))
        self.canvas.start()
    
    #adding the animation to the GUI
    def startAnimation(self, inPossession, previousAnswerCorrect):
        # determines the colors of the different teams
        if inPossession:
            teams = ['blue', 'red']
        else:
            teams = ['red', 'blue']
        def addAndAppend(Object):
            self.players.append(Object)
            self.canvas.addItem(Object)
        # add stack
        for i in range(4):
            addAndAppend(objectsAnimation.Players(self.canvas, 240, 100+40*i, 30, 0, teams[0]))
            addAndAppend(objectsAnimation.Players(self.canvas, 200, 100+40*i, 30, 0, teams[1]))
        # add handlers
        addAndAppend(objectsAnimation.Players(self.canvas, 105, 310, 30, 0, teams[0]))
        addAndAppend(objectsAnimation.Players(self.canvas, 240, 310, 30, 0, teams[0]))
        # add marks on handlers
        addAndAppend(objectsAnimation.Players(self.canvas, 115, 280, 30, 0, teams[1]))
        addAndAppend(objectsAnimation.Players(self.canvas, 220, 290, 30, 0, teams[1]))
        # add good and bad first cutters depending on if answer is correct
        if previousAnswerCorrect and inPossession or not previousAnswerCorrect and not inPossession:
            addAndAppend(objectsAnimation.BadCutterD(self.canvas, 200, 60, 30, 0.5,teams[1]))
            addAndAppend(objectsAnimation.CutterO(self.canvas, 240, 60, 30, 0.5, teams[0]))
        else:
            addAndAppend(objectsAnimation.CutterD(self.canvas, 200, 60, 30, 0.5,teams[1]))
            addAndAppend(objectsAnimation.BadCutterO(self.canvas, 240, 60, 30, 0.5, teams[0]))
        # add disc
        addAndAppend(objectsAnimation.Disc(self.canvas, 90, 300,20, 0.25, 'white'))

#adds background image to the animation       
class Photo(animation.AnimatedObject):
    '''sets the background of the animation'''
    # Read in an image file
    def __init__(self,canvas,filename,x,y):
        self.canvas = canvas
        self.photo = tk.PhotoImage(file = filename)
        self.plusX = self.photo.width()/2
        self.plusY = self.photo.height()/2
        self.phototag = self.canvas.create_image(x + self.plusX,y + self.plusY, image=self.photo)
        
    def move(self):
        pass
        
root = tk.Tk()
app = StartPage(root)
app.mainloop()
from tkinter import *
from tkinter import ttk
from database import *




class Topic:
    '''
    class for topics in 0-100    
    '''

    def __init__(self,root,topic):
        self.root = root
        self.topic = topic
        self.titles = []
        self.toplvl = None
        self.dictionary = {}
        self.valDict = {}

        isDBempty = existsTable(conn,self.topic)
        if isDBempty != 0 :
            allTopicInfoDB = selectAll(conn, self.topic)
            if len(allTopicInfoDB)>0:
                for i in range(len(allTopicInfoDB)):
                    if allTopicInfoDB[i][0] not in self.titles:
                        self.titles.append(allTopicInfoDB[i][0])
                        self.valDict[allTopicInfoDB[i][0]] = float(allTopicInfoDB[i][1])
        
            print("ALLDATA FOR THIS TOPIC: ", self.titles)

    
    
    def createTopicWindow(self):

        topicWindow = Toplevel() # initialize window for topic
        self.toplvl = topicWindow
        self.toplvl.title(self.topic)






        newTitleLabel = ttk.Label(self.toplvl,text="Add a new title: ")
        newTitleLabel.grid(column=0,row=0)

        newTitleEntry = ttk.Entry(self.toplvl)
        newTitleEntry.grid(column=1,row=0)

        if len(self.dictionary)==0:
            dictionary = {} # create dict = {title1:scale1, title2:scale2, etc}
        else:
            dictionary = self.dictionary

        if len(self.titles)>0 :
            for i in range(len(self.titles)):
                name = ttk.Label(self.toplvl,text=self.titles[i])
                name.grid(column=0,row=i+2)
                
                nameScale = Scale(self.toplvl,orient=HORIZONTAL,resolution=0.1, length=250) # can also add label=self.titles[i] to get title above scale
                #nameScale.set(43)  # .set(int) presets value on initialization
                nameScale.grid(column=1,row=i+2)

                if self.titles[i] in self.valDict:
                    nameScale.set(self.valDict.get(str(self.titles[i])))

                dictionary[str(self.titles[i])] = (nameScale, nameScale.get())
                #print("TITLE: ", nameScale.location,nameScale.location(1,i+2),nameScale.get())

        newTitleButton = Button(self.toplvl, text="ADD", command=lambda: self.addTitle(newTitleEntry.get()))
        newTitleButton.grid(column=2,row=0)

        saveButton = Button(self.toplvl, text="SAVE", command=lambda: self.saveAll("a"))
        saveButton.grid(column=2, row=1)

        print("DICT: ", dictionary)
        self.dictionary =dictionary
        if len(self.titles)>0:
            for i in range(len(self.titles)):
                print(i, dictionary.get(str(self.titles[i]))[0].get())
        #print("asldfjasldfj", self.toplvl.grid_slaves(1,3))

    def saveAll(self,p):
            # IDEA:
            #   store title name & scaleValue in a dictionary, 
        print("ANYTHING",p, self.dictionary)
        #self.toplvl.destroy()
        if len(self.titles)>0:
            for i in range(len(self.titles)):
                keys = self.dictionary.keys()
                keys = list(keys)
                print("!!!!!!!!!!!",keys[i],self.dictionary.get(str(self.titles[i])),type(self.dictionary.get(str(self.titles[i]))),str(self.dictionary.get(str(self.titles[i]))),type(str(self.dictionary.get(str(self.titles[i])))))
                self.dictionary[self.titles[i]] = (self.dictionary.get(str(self.titles[i]))[0] ,self.dictionary.get(str(self.titles[i]))[0].get())

                addTitleDB(conn,self.topic, self.titles[i],self.dictionary.get(str(self.titles[i]))[0].get() )


    def addTitle(self, title):
        #print(title) # currently it gets the right title from entry box
        self.titles.append(title)
        self.toplvl.destroy()
        self.createTopicWindow()




###### TODO: Add a Save Button / Save Function functionality
######          This goes through titles and saves scale values to DB
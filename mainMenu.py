from tkinter import *
from tkinter import ttk

from requests import delete
from database import *





# why to use ttk instead of tkinter Frame
# https://stackoverflow.com/questions/19561727/what-is-the-difference-between-the-widgets-of-tkinter-and-tkinter-ttk-in-python


conn = mysql.connector.connect(host="localhost", port=3306, user="root", passwd="")


class mainMenu:
    '''
    main menu where to select existing topic or create new topic
    '''

    def __init__(self,root):
        self.root = root
        self.topics = allTopics




    def displayMainMenu(self): 
        # extracts db topics (if there are any)
        # creates main menu, allows creation of new topics and selection of existing topics

        menu = ttk.Frame(self.root)


        createTopicButton = ttk.Button(menu, text="New Topic",command=self.newTopic) #when implemented add ,command=self.newTopic)
        createTopicButton.grid(column=1,row=1)

        deleteTopicButton = ttk.Button(menu,text="Delete Topic", command=self.deleteTopic)
        deleteTopicButton.grid(column=1,row=2)

        if len(self.topics)>0:
            for i in range(len(self.topics)):
                button = ttk.Button(menu, text=str(self.topics[i]))
                button.grid(column=0,row=i+1)


        return menu



    def newTopic(self): 
        # creates button for a new topic onto the mainmenu

        topicCreation = Toplevel(self.root)
        topicCreation.title("New Topic Creation")

        titleText = ttk.Label(topicCreation, text="Enter Topic Name: ")
        titleText.grid(column=0,row=0)

        titleEntry = ttk.Entry(topicCreation)
        titleEntry.grid(column=1,row=0)


        

        topicEntered = ttk.Button(topicCreation, text="Continue", command=lambda: backToMain(topicCreation))
        topicEntered.grid(column=1,row=1)


        def backToMain(topicCreation):
            title = titleEntry.get()
            if title not in self.topics and len(title)>0:
                self.topics.append(title)
                createTable(conn, title)
            print(self.topics)
            topicCreation.destroy()

            for widget in self.root.grid_slaves():
                widget.grid_forget()
            
            self.displayMainMenu().grid(column=0,row=0)

    def deleteTopic(self):
        # new window use self.topics.remove(topicName) as command for buttons

        deleteWindow = Toplevel()


        if len(self.topics)>0:
            deleteText = ttk.Label(deleteWindow, text="What topic would you like to delete? ")
            deleteText.grid(column=0,row=0)

            deleteEntry = ttk.Entry(deleteWindow)
            deleteEntry.grid(column=1,row=0)

            
            topicDelete = ttk.Button(deleteWindow, text="DELETE", command=lambda: delete_topic(deleteWindow))
            topicDelete.grid(column=1,row=1)

        def delete_topic(deleteWindow): # deletes last added topic, not the proper one
            title = deleteEntry.get()
            print("TITLE: ", title)
            if title in self.topics:
                self.topics.remove(title)
                createDeleteTable(conn,title)
            deleteWindow.destroy()

            for widget in self.root.grid_slaves():
                widget.grid_forget()
            
            self.displayMainMenu().grid(column=0,row=0)






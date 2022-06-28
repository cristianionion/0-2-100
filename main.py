from tkinter import *
from mainMenu import *

'''
0-100 Structure Idea (no login, all local db/server)

Topic create/select/delete, 
add/delete title(s) to selected topic w/ Tkinter Scale for each title,
when topic is selected, open up a tkinter TopLevel


DB structure:
database = zeroto100
each table in zeroto100 is a different topic created in program
columns for each table need:
    title, (optional description), scale value

    # first implementation will not have description, might add later

    # could add option to customize scale from 0-100 to int1-int2 or float1-float2 later
    # in this case, table column "scale value" will become "scalestart, scaleend, scalevalue"

'''

topics2Delete = getDeleteTables(conn)
for i in range(len(topics2Delete)):
    deletedeleteBoard(conn,topics2Delete[i][0])


root = Tk()
root.title("0 to 100")
root.geometry("300x300")

mainMenu(root).displayMainMenu().grid(column=0,row=0)
#top = Toplevel()
#top.title('TopLevel 0-100')


# https://www.tutorialspoint.com/python/tk_scale.htm
# slider for tkinter 



'''   #THIS CREATES MULTIPLE TOPLEVELS labeled 1,2,3,4,5
temp = "top"
for i in range(5):
    t = temp+str(i+1)
    ti = Toplevel()
    ti.title(str(i+1))
    temp = 'top'
'''



mainloop()
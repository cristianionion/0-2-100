from pydoc_data.topics import topics
import mysql.connector



conn = mysql.connector.connect(host="localhost", port=3306, user="root", passwd="")

def createDatabase(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS zeroto100 DEFAULT CHARACTER SET utf8")
    cursor.close()
    conn.commit()

createDatabase(conn)

def createTable(conn, topic):
    conn.database = "zeroto100"
    cursor = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS "+ str(topic)+" (title VARCHAR(2000),scale_value VARCHAR(2000))"
    print("QUERY",query)
    cursor.execute(query)
    cursor.close()
    conn.commit()

#board = "FakeBoard"
#createTable(conn, board)


# deletes a whole topic from DB
def deleteTopicDB(conn,topic):
    conn.database = "zeroto100"
    cursor = conn.cursor()
    query = "DROP TABLE IF EXISTS "+str(topic).replace(" ","あ")
    cursor.execute(query)
    cursor.close()
    conn.commit()

# gets all tables inside zeroto100 DB
def getTables(conn):
    conn.database = "zeroto100"
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES FROM zeroto100")
    result = cursor.fetchall()
    cursor.close()
    return result



############################################################
# found way to delete saved table on next tkinter restart,
# have the delete from db for loop in BOTH database.py AND main.py 
############################################################

def tbd(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS tobedeleted DEFAULT CHARACTER SET utf8")
    cursor.close()
    conn.commit()


def createDeleteTable(conn, topic):
    conn.database = "tobedeleted"
    cursor = conn.cursor()
    query = "CREATE TABLE IF NOT EXISTS " + str(topic).replace(" ","あ") +" (title VARCHAR(2000))"
    #print("QUERY",query)
    cursor.execute(query)
    cursor.close()
    conn.commit()


def deletedeleteBoard(conn,topic):
    conn.database = "zeroto100"
    cursor = conn.cursor()
    query = "DROP TABLE IF EXISTS "+str(topic).replace(" ","あ")
    cursor.execute(query)
    cursor.close()
    conn.commit()


def getDeleteTables(conn):
    conn.database = "tobedeleted"
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES FROM tobedeleted")
    result = cursor.fetchall()
    cursor.close()
    return result

def deleteTopicfromdeleteDB(conn,topic):
    conn.database = "tobedeleted"
    cursor = conn.cursor()
    query = "DROP TABLE IF EXISTS "+str(topic).replace(" ","あ")
    cursor.execute(query)
    cursor.close()
    conn.commit()

print("GET TABLES THAT WILL BE DELETED: ", getDeleteTables(conn))
topics2Delete = getDeleteTables(conn)
for i in range(len(topics2Delete)):
    deletedeleteBoard(conn,topics2Delete[i][0])

for i in range(len(topics2Delete)):
    deleteTopicfromdeleteDB(conn,topics2Delete[i][0])


############################################################################################################
#  so far only above DB functions are specific for this project                                            #
############################################################################################################


def addCard(conn,query, info):
    binNum = info[0]
    name = info[1]
    desc = info[2]
    vals = [name, desc,True] 
    for i in range(binNum-1):
        vals.append(False)
    conn.database = "zeroto100"
    cursor = conn.cursor()
    #query = "INSERT INTO "+str(board)+ " (card,card_notes,cards_assignment) VALUES (%s,%s,%s)"
    #vals = (card, card_notes,cards_assignment)
    #print(query, vals)
    cursor.execute(query,vals)
    cursor.close()
    conn.commit()

def cardMoved(conn, board, cardTitle, oldLocation, newLocation):
    conn.database = "zeroto100"
    cursor = conn.cursor()
    # title and desc don't change, remaining are buckets on board
    # search for card title, make newLocation column True, rest false
    # need sum like UPDATE board SET oldLoc = False, newLoc = True WHERE title = cardTitle
    query = "UPDATE "+str(board).replace(" ","あ")+ " SET "+ str(oldLocation).replace(" ","あ")+" =%s, "+str(newLocation).replace(" ","あ")+" =%s WHERE title =%s "
    #print(query)
    vals = (False,True, str(cardTitle))
    cursor.execute(query,vals)
    cursor.close()
    conn.commit()

# returns all data for a specific board
def selectAll(conn,board):
    conn.database = "zeroto100"
    cursor = conn.cursor()
    query = "SELECT * FROM "+str(board)
    #print(query)
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result

# returns all data for a specific card
def selectOne(conn,board,card):
    conn.database = "zeroto100"
    cursor = conn.cursor()
    query = "SELECT * FROM "+str(board)+" WHERE card = %s"
    adr = (card,)
    cursor.execute(query,adr)
    result = cursor.fetchone()
    cursor.close()
    return result

# deletes specific card from DB
def deleteCard(conn,board,card):
    conn.database = "zeroto100"
    cursor = conn.cursor()
    query = "DELETE FROM "+str(board)+" WHERE card =%s"
    adr = (card,)
    cursor.execute(query,adr)
    cursor.close()
    conn.commit()



#https://www.geeksforgeeks.org/how-to-add-a-column-to-a-mysql-table-in-python/
# inserts new bin into DB for specific zeroto100 board
def addBin(conn,board, bin):
    conn.database = "zeroto100"
    cursor = conn.cursor()
    query = "ALTER TABLE "+str(board)+" ADD IF NOT EXISTS "+str(bin)+" VARCHAR(100)"
    cursor.execute(query)
    cursor.close()
    conn.commit()

# deletes a bin from a board in DB
def deleteBin(conn,board,bin):
    conn.database = "zeroto100"
    cursor = conn.cursor()
    query = "ALTER TABLE "+str(board)+" DROP COLUMN IF EXISTS "+str(bin)
    cursor.execute(query)
    cursor.close()
    conn.commit()



def getColumns(conn,board):
    conn.database = "zeroto100"
    cursor = conn.cursor()
    query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = 'zeroto100' AND TABLE_NAME = '"+str(board)+ "'"
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    return result    
    
allTopicsMessy = getTables(conn)
print("ALL TOPICS: ",allTopicsMessy)
allTopics = []
for i in range(len(allTopicsMessy)):
    print(allTopicsMessy[i][0], type(allTopicsMessy[i][0]))
    allTopics.append(allTopicsMessy[i][0])

print(allTopics, type(allTopics[0]))



allTopicsAndTables = []
for i in range(len(allTopics)):
    tempBoardTitle = allTopics[i][0]
    allTopicsAndTables.append(selectAll(conn,tempBoardTitle))
    #print("\n")

def getAllData():
    allData = []
    for i in range(len(allTopics)):
        allData.append([])
        allData[i].append((allTopics[i][0],),)
        cols = getColumns(conn,allTopics[i][0])
        for j in range(len(cols)):
            allData[i][0] = allData[i][0] + ((cols[j][0]),) 
            # at this point, each table has a list of one tuple containing boardTitle and colTitles
        for k in range(len(allTopicsAndTables[i])):
            allData[i].append(allTopicsAndTables[i][k])
    return allData




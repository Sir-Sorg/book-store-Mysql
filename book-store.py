import mysql.connector
from prettytable import PrettyTable
import re


def select2db():
    dbcursor.execute("SELECT * FROM book ORDER BY name")
    result = dbcursor.fetchall()
    t = PrettyTable(["Name", "Page Count", "Genre", "Score", "Author", "ISBN", "Price"])
    for thisBook in result:
        t.add_row(
            [
                thisBook[0] + " 📖",
                str(thisBook[1]) + " 📰",
                thisBook[2] + " 📆",
                str(thisBook[3]) + " 🏆",
                thisBook[4],
                thisBook[5] + " ©",
                str(thisBook[6]) + " 💲",
            ]
        )
    print(t)


def checkField(fNum, val):
    if fNum == 1:
        if val.isnumeric():
            return True
        else:
            print("page count must be Numeric (0-9)! (Error-4)")
            return False
    elif fNum == 2:
        if val.isalpha():
            return True
        else:
            print("genre must be alphabet letters (a-z) (Error-5)")
            return False
    elif fNum == 3:
        result = re.search(r"^\d\.*\d*$", val)
        if result and float(val) >= 0 and float(val) <= 5:
            return True
        else:
            print("score must be Float and between 0.0 to 5.0 (Error-6)")
            return False
    elif fNum == 6:
        result = re.search(r"^\d\.*\d*$", val)
        if result:
            return True
        else:
            print("price must be Float or Numeric (Error-7)")
            return False
    return True


def insert2db():
    sql = "INSERT INTO book (name,pageCount,genre,score,author,isbn,price) VALUES ('{0}',{1},'{2}',{3},'{4}','{5}',{6})"
    value = input(
        "Cool, Give those data in order :\n---------> Name - Page Count - Genre - Score (float between 0.0 to 5.0) - Author - ISBN - Price\n Separate them by '-' : "
    )
    value = value.strip()
    value = value.split("-")
    value = tuple(map(lambda this: this.strip(), value))
    if len(value) > 7:
        print("Too many Arguments! (Error-2)")
    elif len(value) < 7:
        print("All fields are required! (Error-3)")
    else:
        index = 0
        everythingisok = True
        while index <= 6:
            thisField = value[index]
            if not checkField(index, thisField):
                everythingisok = False
                break
            index += 1
        if everythingisok:
            dbcursor.execute(
                sql.format(
                    value[0],
                    value[1],
                    value[2],
                    value[3],
                    value[4],
                    value[5],
                    value[6],
                )
            )
            bookStoreDB.commit()
            print("The '%s' book successfully added to Database." % value[0])


def displayBasedOnId():
    dbcursor.execute("SELECT id,name FROM book ORDER BY id")
    result = dbcursor.fetchall()
    t = PrettyTable(["Id", "Name"])
    for thisBook in result:
        t.add_row([thisBook[0], thisBook[1] + " 📖"])
    print(t)
    return result


def update2db():
    result = displayBasedOnId()
    columnName = {
        "1": "name",
        "2": "pageCount",
        "3": "genre",
        "4": "score",
        "5": "author",
        "6": "isbn",
        "7": "price",
    }
    selectedBook = input("Which one will you update, enter its Id : ")
    sql = "UPDATE book SET %s = '%s' WHERE id = %s"
    SBName = [item[1] for item in result if str(item[0]) == selectedBook][0]
    column = input(
        "Which attribute will you change?\n1 - Name\n2 - Page Count\n3 - Genre\n4 - Score\n5 - Author\n6 - ISBN\n7 - Price\n: "
    )
    value = input("Enter its value : ")
    if checkField(int(column) - 1, value):
        dbcursor.execute(sql % (columnName[column], value, selectedBook))
        bookStoreDB.commit()
        print(
            "The '%s' book successfully updated on '%s' to value '%s' ."
            % (SBName, columnName[column].capitalize(), value)
        )


def delete2db():
    result = displayBasedOnId()
    selectedBook = input("Which one will you delete, Enter its Id : ")
    sql = "DELETE FROM book WHERE id = %s"
    SBName = [item[1] for item in result if str(item[0]) == selectedBook][0]
    dbcursor.execute(sql % selectedBook)
    bookStoreDB.commit()
    print("The '%s' book successfully removed from Database." % SBName)


def createTable():
    sql = "CREATE TABLE book (name varchar(100),pageCount smallint,genre varchar(30),score float,author varchar(50),isbn varchar(20),price float,id INT AUTO_INCREMENT PRIMARY KEY);"
    dbcursor.execute(sql)
    print("book store Table successfully created.")


# ====================================================================================================

try:
    bookStoreDB = mysql.connector.connect(
        host="localhost", user="bokstr", password="1234", database="bookstore"
    )
    dbcursor = bookStoreDB.cursor()
except:
    print("we cant connect to the Mysql on localhost@bokstr@1234@bookstore (Error-1)")

line = "========================================================================"
print("%s\n%s\n%s" % (line, "Welcome to Book Store 📚".center(len(line)), line))
while True:
    task = input(
        "what will do? (Press anything else to exit)\n1 - INSERT book 💾\n2 - DELETE book 🔥\n3 - UPDATE book 📎\n4 - SELECT (View) book 🔦\n5 - CREATE table 📂\n: "
    )
    if task == "1":
        insert2db()
    elif task == "2":
        delete2db()
    elif task == "3":
        update2db()
    elif task == "4":
        select2db()
        input("Press Enter to return to menu")
    elif task == "5":
        createTable()
    else:
        break

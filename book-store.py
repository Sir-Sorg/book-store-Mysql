import mysql.connector


def select2db():
    dbcursore.execute("SELECT * FROM book")
    result = dbcursore.fetchall()
    for thisBook in result:
        print(thisBook)


def insert2db():
    sql = "INSERT INTO book (name,pageCount,genre,score,author,isbn,price) VALUES ('{0}',{1},'{2}',{3},'{4}','{5}',{6})"
    value = input(
        "Cool, Give those data in order :\n---------> Name - Page Count - Genre - Score (float between 0 to 5) - Author - ISBN - Price\n Separate them by '-' : "
    )
    value = value.strip()
    value = value.split("-")
    value = tuple(map(lambda this: this.strip(), value))
    if len(value) > 7:
        print("too many arguments! (Error-2)")
    elif len(value) < 7:
        print("Please enter all information! (Error-3)")
    else:
        dbcursore.execute(
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
        print("The '%s' book Succesfully added to Database." % value[0])


def update2db():
    pass


def delete2db():
    pass


try:
    bookStoreDB = mysql.connector.connect(
        host="localhost", user="bokstr", password="1234", database="bookstore"
    )
except:
    print("we cant connect to the Mysql on localhost@bokstr@1234@bookstore (Error-1)")


dbcursore = bookStoreDB.cursor()
line = "========================================================================"
print("%s\n%s\n%s" % (line, "Welcome to Book Store".center(len(line)), line))
task = input(
    "what will do? (Press anything else to exit)\n1 - INSERT book\n2 - DELETE book\n3 - UPDATE book\n4 - SELECT (View) book\n: "
)
if task == "1":
    insert2db()
elif task == "2":
    delete2db()
elif task == "3":
    update2db()
elif task == "4":
    select2db()


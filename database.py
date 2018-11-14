import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "sqlhpc",
    database = "testdb"
)

mycursor = mydb.cursor()  #Object that communicates with the entire MySQL server

#mycursor.exucute("CREATE DATABASE testdb") --> Method that created the database

#mycursor.execute("CREATE TABLE ImagesTable (id VARCHAR(255), imagePath VARCHAR(255), Category VARCHAR(255))") #--> Created the table


# Function to add single image to db
def addImage(ID, imagePath, category):
    sqlFormula = "INSERT INTO ImagesTable (id, imagePath, Category) VALUES (%s, %s, %s)"
    image = (ID, imagePath, category)
    mycursor.execute(sqlFormula, image)
    mydb.commit()

# Function that takes an array of images and add them all to the db
def addImages(imagesArray):
    sqlFormula = "INSERT INTO ImagesTable (id, imagePath, Category) VALUES (%s, %s, %s)"
    mycursor.executemany(sqlFormula, imagesArray)
    mydb.commit()


# Block that search for a specific category
sql = "SELECT * FROM ImagesTable WHERE Category = 'Category3'"
mycursor.execute(sql)
result = mycursor.fetchall()
for r in result:
    print(r)


#Create images
#imagesArray = [("imageID1", "String1", "String2"),
 #              ("imageID2", "String1", "String2"),
  #             ("imageID3", "String1", "String2"),
   #            ("imageID4", "String1", "String2"),
    #           ("imageID5", "String1", "String2")]

#TODO Crear funcion para iniciar base de datos, a~adir elementos a la lista y conseguir elementos de acuerdo a la categoria

#mycursor.executemany(sqlFormula, imagesArray)    #Store the image in table

#mycursor.execute("SELECT id FROM images")

#myresult = mycursor.fetchall()

#for row in myresult:
#    print(row)

#mydb.commit()  #Make the change to the table to be seen in the database

import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "sqlhpc",
    database = "testdb"
)

mycursor = mydb.cursor()  #Object that communicates with the entire MySQL server

#mycursor.exucute("CREATE DATABASE testdb") --> Method that created the database

# mycursor.execute("CREATE TABLE ImagesTable (id INT AUTO_INCREMENT PRIMARY KEY, imagePath VARCHAR(255), Category VARCHAR(255))") #--> Created the table


# Function to add single image to db
def addImage(imagePath, category):
    sqlFormula = "INSERT INTO ImagesTable (imagePath, Category) VALUES (%s, %s)"
    image = (imagePath, category)
    mycursor.execute(sqlFormula, image)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

#Create images
# imagesArray = [("C:\home\GenImages\img1.jpg", "tennisball"),
#               ("C:\home\GenImages\img2.jpg", "baseballball"),
#               ("C:\home\GenImages\img3.jpg", "soccerball"),
#               ("C:\home\GenImages\img4.jpg", "volleyballball"),
#               ("C:\home\GenImages\img5.jpg", "golfball")]


# Function that takes an array of images and add them all to the db
def addImages(imagesArray):
    sqlFormula = "INSERT INTO ImagesTable (imagePath, Category) VALUES (%s, %s)"
    mycursor.executemany(sqlFormula, imagesArray)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")



# Search for a specific category
# sql = "SELECT * FROM ImagesTable WHERE Category = 'write category here'"
# mycursor.execute(sql)
# result = mycursor.fetchall()
# for r in result:
#     print(r)

#Delete from table
# sql = "DELETE FROM ImagesTable WHERE ID = 6"
# mycursor.execute(sql)
# mydb.commit()



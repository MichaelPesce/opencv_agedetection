import io
from time import sleep, time
import detect_age
import mysql.connector
import urllib.request

total = 0
unupdated = []
logfile = open("log.txt","a")

cnx = mysql.connector.connect(user='root', password='!',
                                  host='127.0.0.1', auth_plugin='mysql_native_password')
cursor = cnx.cursor()

def main():
    start_time = time()
    
    global cnx,cursor,total, unupdated, logfile
    logfile.write(str(start_time)+"\n")
    print("starting")
    currentPlace = 0
    query = "SELECT username,id FROM mikey.twitterbigjpg;"
    cursor.execute(query)
    results = cursor.fetchall()
    
    print(len(results))
    for each in results:
        userid = each[1]
        usernamewithat = each[0]
        username = usernamewithat[1:]
        username = "AbhiFour"
        ageBucket, confidence = detect_face_age(username, '.jpg')
        print(username)
        outputJson = {}
        outputJson["age"] = ageBucket
        outputJson["confidence"] = str(confidence)
        outputJson["user"] = username.replace(" ","")
        outputJson["id"] = userid
        if(ageBucket!=''):
            insert(outputJson)
        else:
            logfile.write("no age detected. not inserting for user: "+str(username)+"\n")
    
    elapsed_time = time() - start_time
    logfile.write("failures: \n")
    logfile.write(str(unupdated)+"\n")
    logfile.write('\nthis process took '+str(elapsed_time)+' seconds')
    logfile.close()
    print('\nthis process took '+str(elapsed_time)+' seconds')


#detect the age of input image name and extension type( jpg here)
def detect_face_age(user, extension):
    global logfile
    #"detect age of user"
    #currentDir: the directory where the detectage python file is locatied
    #image: the path to the image file
    # age : the name of the folder containing the age detecting python file
    # confidence: somehow connected to returned confidence, if set too low causes errors sometimes
    args = {"currentDir": "", "image":"images/"+user+extension, "age":"age_detector", "confidence": .20}
    ageBucket=''
    confidence=''
    try:
        detections = detect_age.start(args)
        #this will break out after the first returned detection (the one with the highest confidence)
        for key in detections:
            ageBucket = key
            confidence = detections[key]
            break
        #print("success")
        #print(detections)
        print(str(user)+ ": " +str(ageBucket),str(confidence))
        
    except Exception as e:
        print("an error occurred while detecting age")
        print(e)
    return ageBucket, confidence

def insert(outputJson):
    #print(outputJson)
    #return True
    #"insert user into mysql"
    return True
    global cursor, cnx, total, logfile
    query = "update mikey.twitterbigjpg set estimatedage = %s, confidence = %s where id = %s"
    attributes = (outputJson["age"], outputJson["confidence"], outputJson["id"])
    cursor.execute(query, attributes)
    cnx.commit()
    total += cursor.rowcount
    #print(cursor.rowcount)
    if cursor.rowcount == 1:
        logfile.write("success\n")
        logfile.write(str(outputJson)+"\n")
    else:
        unupdated.append(outputJson)
        logfile.write("failure")
        logfile.write(str(outputJson)+"\n")
    
    #print("succesfully inserted")
main()
import detect_age
from time import time
import os; 


def getUsers():
    usernames=[]
    f = open("images/twitterusers/usernames.txt","r")
    u = f.readline()
    while(len(u) > 0):
        length = len(u)
        username = u[0:length-1]
        usernames.append(username)
        u = f.readline()
    f.close()
    return usernames
def main():
    start_time = time()
    
    print("getting users")
    usernames = getUsers()
    success = 0
    total = 0

    # AGE_BUCKETS = ["(0-2)", "(4-6)", "(8-12)", "(15-20)", "(25-32)", "(38-43)", "(48-53)", "(60-100)"]    
    agegroups = {"(0-2)": 0, "(4-6)": 0, "(8-12)": 0, "(15-20)": 0, "(25-32)": 0, "(38-43)": 0, "(48-53)": 0, "(60-100)": 0}
    for user in usernames:
        total+=1
        args = {"image":"images/twitterusers/"+user, "age":"age_detector", "confidence": .20}
        try:
            detections = detect_age.start(args)
            for key in detections:
                curramt = agegroups[key]
                agegroups[key] = curramt+1
                success+=1
                break
            #print("success")
            #print(detections)
        except Exception as e: 
            print("unable to detect face in user: "+user)
            #print(e)
    print("success: "+str(success)+"\ntotal: "+str(total))
    for key in agegroups:
        print(key, agegroups[key])

    elapsed_time = time() - start_time
    print('this process took ' + str(elapsed_time) + ' seconds')


main()

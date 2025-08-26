import random as r
import time
import difflib

def accuracy(test, user):
    matcher = difflib.SequenceMatcher(None, test, user)
    return round(matcher.ratio() * 100, 2)

def mistake(test,user):
    test_words = test.split()
    user_words = user.split()
    error=0
    for i in range(len(test)):
        try:
            if test[i] !=user[i]:
                error=error+1
        except:
              error=error+1
    return error            

def speed_time(time_s,time_e,userinput):
    time_delay=time_e-time_s
    time_R= round(time_delay,2)
    if time_R == 0:
        return 0
    speed=len(userinput)/time_R
    return round(speed)

tests = [
    "Please take your dog, Cali, out for a walk – he really needs some exercise! What a beautiful day it is on the beach, here in beautiful and sunny Hawaii.",
    "Rex Quinfrey, a renowned scientist, created plans for an invisibility machine.",
    "Do you know why all those chemicals are so hazardous to the environment?",
    "You never did tell me how many copper pennies were in that jar; how come?",
    "Max Joykner sneakily drove his car around every corner looking for his dog."
]
test2=r.choice(tests)
print(test2)
print()
print()
time_1=time.time()
testinput=input("Enter:")
time_2= time.time()
print('speed:',speed_time(time_1,time_2,testinput),"w/sec")
print("ERROR:",mistake(test2,testinput))
print("Accuracy:", accuracy(test2, testinput), "%")
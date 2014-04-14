'''
Created on Apr 11, 2014

@author: The Oracle
'''
import json, time, operator
from pprint import pprint

month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6,
       "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

def convertMonthToNumber(month):
    return str(month_dict.get(month))

def convertToTime(messeduptime):
    return time.asctime(time.localtime(messeduptime))

def timeStruct(messeduptime):
    return time.localtime(messeduptime)


    '''
    everything.append((creator,message,peopleWhoLikedThePost,timeStamp,timeStampInSeconds,pictureURL,numberOfLikes))
    takes in buffer time in terms of seconds and returns a dictionary of 
    key: message,creator
    value: how many people who responded to that message within buffer time
    '''
def responseRate(everything,bufferTime):
    d={}
    for i in range(len(everything)):
        for j in range(i,len(everything)):
            if (everything[j][4]-everything[i][4]<bufferTime):
                message=everything[i][1]
                creator = everything[i][0]
                key=(message,creator)
                if key not in d:
                    d[key]=0
                d[key]+=1
    return d

def findMostPopularMessage(everything,topN):
    sortedList = sorted(everything,key=operator.itemgetter(6),reverse=True)
    return sortedList[:topN]

                
'''variables'''
allTheTimeStamps=[]#collects all the timestamps
allTheTimeStampsInSeconds=[]    
messageCount={}#collects the number of messages each person sent. 
allMembers=[]#name of all the people in the group. Probably need to check for name change
messagesPerDay={}
everything=[]

'''
===============================================================================================
'''
json_data=open('transcript-5511880.json')
data = json.load(json_data)
for eachMessage in data:
    print eachMessage[u'created_at']
    #timestamps
    timeStamp = convertToTime(eachMessage[u'created_at'])
    allTheTimeStamps.append(timeStamp)
    timeStampInSeconds=eachMessage[u'created_at']
    allTheTimeStampsInSeconds.append(timeStampInSeconds)
    temp =timeStamp.split(" ")
    yearMonthDay=temp[4]+"-"+convertMonthToNumber(temp[1])+"-"+temp[2]
    
    #messagesperday
    if yearMonthDay not in messagesPerDay:
        messagesPerDay[yearMonthDay]=0
    messagesPerDay[yearMonthDay]+=1
    
    pictureURL = eachMessage[u'picture_url']
    message =  eachMessage[u'text']
    creator = eachMessage[u'name']
    if str(creator) not in allMembers:
        allMembers.append(str(creator))
    if str(creator) not in messageCount:
        messageCount[str(creator)]=0
    messageCount[str(creator)]+=1
    peopleWhoLikedThePost = eachMessage[u'favorited_by']
    numberOfLikes = len(peopleWhoLikedThePost)
    everything.append((creator,message,peopleWhoLikedThePost,timeStamp,timeStampInSeconds,pictureURL,numberOfLikes))
json_data.close()

print "These are the names of all the members."
print allMembers
  
print "This is the sorted list of members - message count."
sortedMessageCount = sorted(messageCount.iteritems(),key=operator.itemgetter(1),reverse=True)
print sortedMessageCount
  
print "This is the list of all time stamps."
print allTheTimeStamps
print allTheTimeStampsInSeconds
#  
print "This is the sorted list of messages per day"
sortedMessagesPerDayByCount = sorted(messagesPerDay.iteritems(),key=operator.itemgetter(1),reverse=True)
sortedMessagesPerDayByDay = sorted(messagesPerDay.iteritems(),key=operator.itemgetter(0))
print sortedMessagesPerDayByDay
# print sortedMessagesPerDayByCount
# 
responseResult= responseRate(everything,120)
sortedResponseResult = sorted(responseResult.iteritems(),key=operator.itemgetter(1),reverse=True)
print sortedResponseResult

mostPopularMessages = findMostPopularMessage(everything,5)
print mostPopularMessages
# print everything





if __name__ == '__main__':
    pass
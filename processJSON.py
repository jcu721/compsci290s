'''
Created on Apr 11, 2014

@author: The Oracle
'''
import json, time, operator

month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6,
       "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

def convertMonthToNumber(month):
    return str(month_dict.get(month))

def convertToTime(messeduptime):
    return time.asctime(time.localtime(messeduptime))

def timeStruct(messeduptime):
    return time.localtime(messeduptime)

def responseRate(everything,bufferTime):
    d={}
    dictOfResponseCount={}
    for i in range(len(everything)):
        for j in range(i,len(everything)):
            if (everything[j][4]-everything[i][4]<bufferTime):
                message=str(everything[i][1])
                creator = str(everything[i][0])
                key=(message,creator)
                respondent=str(everything[j][0])
                if key not in d:
                    d[key]=0
                d[key]+=1
                if respondent not in dictOfResponseCount:
                    dictOfResponseCount[respondent]=0
                dictOfResponseCount[respondent]+=1
    return d,dictOfResponseCount

def findMostPopularMessage(everything,topN):
    sortedList = sorted(everything,key=operator.itemgetter(6),reverse=True)
    return sortedList[:topN]

'''((creator,message,peopleWhoLikedThePost,timeStamp,timeStampInSeconds,pictureURL,numberOfLikes))'''
def findMostLikes(everything):
    d={}
    for each_message in everything:
        creator = str(each_message[0])
        numLikes=each_message[6]
        if creator not in d:
            d[creator]=(0,0)
        tupz = d[creator]
        #tupz0 is the message count and tupz1 is the numlikes
        tupMessageCount=(tupz[0]+1)
        tupNumLikes=(tupz[1]+numLikes)
        d[creator]=(tupMessageCount,tupNumLikes)
    return d

def processMostLikes(d):
    lst=[]
    for creator,countLikesTup in d.iteritems():
        lst.append((creator,(1.0*countLikesTup[1]/countLikesTup[0]),countLikesTup[0]))
    return sorted(lst,key=operator.itemgetter(1),reverse=True)

def findResponseTimeOfEachPerson(threads):
    '''find how the time for each person to reply to messages
    ignores sequential messages
    finds participation rate in threads
    '''
    d={}            
    return d



def findWhoWillRespondToYou(threads):
    '''for every creator of the thread, this finds the people most likely to reply to you'''
    d={}
    return d


def findUsagePatterns(everything):
    '''finds the usage per day ie how many messages on Sunday compared to Monday
    finds usage patterns during certain times of the day'''
    d={}
    return d


'''((creator,message,peopleWhoLikedThePost,timeStamp,timeStampInSeconds,pictureURL,numberOfLikes))'''
def processMessagesToThreads(everything,bufferTime):
    '''converts the list of messages to a list of threads according to a bufferTime'''
    output=[]
    temp=[]
    for i in range(len(everything)):
        message=everything[i]
        if str(message[0])=='GroupMe':
            continue
        #corner case
        if i==0:
            temp.append(message)
            continue
        previousMessage=everything[i-1]
        if len(temp)==0:
            temp.append(message)
            continue
        if message[4]-previousMessage[4]<bufferTime:
            temp.append(message)
        else:
            output.append(temp)
            temp=[]
    return  output




                
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
json_data=open('transcript-5411880.json')
data = json.load(json_data)
for eachMessage in data:
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

'''
===============================================================================================
'''
print "These are the names of all the members."
print allMembers
print "This is the number of members.",len(allMembers)
 
print "This is the sorted list of members - message count."
sortedMessageCount = sorted(messageCount.iteritems(),key=operator.itemgetter(1),reverse=True)
print sortedMessageCount

'''
print "This is the list of all time stamps."
print allTheTimeStamps
print allTheTimeStampsInSeconds
'''

# print "This is the sorted list of messages per day"
# sortedMessagesPerDayByCount = sorted(messagesPerDay.iteritems(),key=operator.itemgetter(1),reverse=True)
# sortedMessagesPerDayByDay = sorted(messagesPerDay.iteritems(),key=operator.itemgetter(0))
# print sortedMessagesPerDayByDay
# print sortedMessagesPerDayByCount


responseResult= responseRate(everything,120)[0]
sortedResponseResult = sorted(responseResult.iteritems(),key=operator.itemgetter(1),reverse=True)
print "This is the list of messages: response count of messages which were responded within the buffer"
print sortedResponseResult

#print the list of the most responsive and least responsive people within the buffer
whoIsTheMostResponsive = responseRate(everything,2400)[1]
sortedwhoIsTheMostResponsive = sorted(whoIsTheMostResponsive.iteritems(),key=operator.itemgetter(1),reverse=True)
print "This is a list of people and the number of messages they respond to within the buffer time"
print sortedwhoIsTheMostResponsive

mostPopularMessages = findMostPopularMessage(everything,10)
print "This is the list of most popular messages"
print mostPopularMessages

mostLikes = findMostLikes(everything)
processedMostLikes = processMostLikes(mostLikes)
print "This is the list of creators, number of likes per messages, and number of messages sent"
print processedMostLikes

threads= processMessagesToThreads(everything, 12000)
for each in threads:
    print each


if __name__ == '__main__':
    pass
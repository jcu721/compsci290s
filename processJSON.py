'''
Created on Apr 11, 2014

@author: The Oracle
'''
import json, time, operator, nltk, numpy

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


'''((creator,message,peopleWhoLikedThePost,timeStamp,timeStampInSeconds,pictureURL,numberOfLikes))'''
def findParticipationRateInThreads(threads):
    '''find the rate of participation of all the members in threads
    find the people who are likely to respond to you'''
    d={}
    dictResponseTime={}
    for member in allMembers:
        d[member]=0

    for thread in threads:
        startTimeInSeconds = thread[0][4]
        creator = thread[0][0]
        alreadyResponded=set()
        for i in range(len(thread)):
            #calculate participation rate in threads
            respondent = thread[i][0]
            d[respondent]+=1
            #initialize the creator
            if i==0:
                if creator not in dictResponseTime:
                    temp={}
                    dictResponseTime[creator]=temp
                    if creator not in temp:
                        temp[creator]=[]
                    temp[creator].append(0)
                continue
            #for the rest of the respondents
            timeTakenToRespondInSeconds = thread[i][4] - startTimeInSeconds
            respondentName = thread[i][0]

            temp=dictResponseTime[creator]
            if respondentName not in temp:
                temp[respondentName]=[]
            if respondentName not in alreadyResponded:
                temp[respondentName].append(timeTakenToRespondInSeconds)
            alreadyResponded.add(respondentName)
    return d,dictResponseTime

def findUsagePatternsPerDay(eachMessage):
    '''finds the usage per day ie how many messages on Sunday compared to Monday
    finds usage patterns during certain times of the day'''
    day=convertToTime(eachMessage[u'created_at']).split(" ")[0]
    if day not in usagePatternsPerDay:
        usagePatternsPerDay[day]=0
    usagePatternsPerDay[day]+=1

def findUsagePatternsPerHour(timeStamp):
    hour=timeStamp.split(" ")[3].split(":")[0]
    if hour not in usagePatternsPerHour:
        usagePatternsPerHour[hour]=0
    usagePatternsPerHour[hour]+=1
    
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

def processDictResponseTime(dictResponseTime):
    for creator,val in dictResponseTime.iteritems():
        if len(val)==0: continue
        numThreadsCreated = len(val[creator])
        print "This is the number of threads",creator,"created:",numThreadsCreated
        
        for respondent,listOfTimes in val.iteritems():
            if respondent == creator:
                continue
            assert len(listOfTimes)>0
            print "\t",respondent,"has responded to",100.0*len(listOfTimes)/numThreadsCreated,"percent of the threads at an average of","{:.2f}".format(numpy.mean(listOfTimes)/60),"minutes"

def createIndex(someMembersList):
    lengthOfArray = len(someMembersList)
    sortedlist = sorted(someMembersList)
    matrix = numpy.zeros(shape=(lengthOfArray,lengthOfArray))
    indexDict = {}
    for i in range(len(sortedlist)):
        if someMembersList[i] not in indexDict:
            indexDict[sortedlist[i]]=i
        indexDict[sortedlist[i]]=i
        
    return matrix,indexDict

def populateMatrix(matrix,d):
    '''this is still not working
    =====================================================================================+++++++++++++++++++++++++++++++++
    '''
    for creator,val in d.iteritems():
        creatorIndex = indexDictionary[str(creator)]     
        for respondent,listOfTImes in val.iteritems():
            respondentIndex = indexDictionary[respondent]
            print "\t",creator,respondent
            matrix[creatorIndex][respondentIndex]+=1

'''variables'''
allTheTimeStamps=[]#collects all the timestamps
allTheTimeStampsInSeconds=[]    
messageCount={}#collects the number of messages each person sent. 
allMembers=[]#name of all the people in the group. Probably need to check for name change
messagesPerDay={}
everything=[]
wordCloudDict={}
usagePatternsPerDay={}
usagePatternsPerHour={}
'''
===============================================================================================
'''
json_data=open('transcript-5411880.json')
data = json.load(json_data)
for eachMessage in data:
    
    #timestamps
    timeStamp = convertToTime(eachMessage[u'created_at'])

    #manipulating day
    findUsagePatternsPerDay(eachMessage)
    findUsagePatternsPerHour(timeStamp)
    
    
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
    
    #uses nltk tokenizer REQUIRES NLTK MODULE
    tokens=nltk.word_tokenize(str(message))
    for token in tokens:
        if token not in wordCloudDict:
            wordCloudDict[token]=0
        wordCloudDict[token]+=1
    
    
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
print "\nThese are the names of all the members."
print allMembers
print "This is the number of members.",len(allMembers)
 
print "\nThis is the sorted list of members - message count."
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
print "\nThis is the list of messages: response count of messages which were responded within the buffer"
print sortedResponseResult

#print the list of the most responsive and least responsive people within the buffer
whoIsTheMostResponsive = responseRate(everything,2400)[1]
sortedwhoIsTheMostResponsive = sorted(whoIsTheMostResponsive.iteritems(),key=operator.itemgetter(1),reverse=True)
print "\nThis is a list of people and the number of messages they respond to within the buffer time"
print sortedwhoIsTheMostResponsive

mostPopularMessages = findMostPopularMessage(everything,10)
print "\nThis is the list of most popular messages"
print mostPopularMessages

mostLikes = findMostLikes(everything)
processedMostLikes = processMostLikes(mostLikes)
print "\nThis is the list of creators, number of likes per messages, and number of messages sent"
print processedMostLikes

sortedWordCloudDict = sorted(wordCloudDict.iteritems(),key=operator.itemgetter(1),reverse=True)
print "\nThis is a list of word / frequency -->use for word cloud."
print sortedWordCloudDict

print "\nThis shows the usage patterns per day / per hour"
print usagePatternsPerDay
print sorted(usagePatternsPerHour.iteritems(),key=operator.itemgetter(0))

print "\nThis shows the threads"
threads= processMessagesToThreads(everything, 7200) #set limit as 2 hours
# for each in threads:
#     print each


totalNumberOfThreads=len(threads)
print "\nThe total number of threads is:",totalNumberOfThreads
print "This shows the percentage and number of threads the participant has taken part in."
participationRate,dictResponseTime=findParticipationRateInThreads(threads)
processedParticipationRate = sorted([(k,1.0*val/totalNumberOfThreads,val) for k,val in participationRate.iteritems()],key=operator.itemgetter(0))
print processedParticipationRate

print "===================================================="
print participationRate

print "\nThis shows the response rate of the participants."
# print dictResponseTime
processedDictResponseTime = processDictResponseTime(dictResponseTime)



matrix,indexDictionary = createIndex(allMembers)
# print sorted(allMembers)
# print sorted(indexDictionary.iteritems(),key=operator.itemgetter(0))
populateMatrix(matrix,threads)
for row in matrix:
    print row
# print [(x,y) for x,y in indexDictionary.iteritems()]

if __name__ == '__main__':
    pass
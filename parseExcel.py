'''
Created on Apr 26, 2014

@author: The Oracle
'''
import csv
d={}
def createDict():
    with open('calendar of events.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            date=row[0]
            event=row[1]
            if date not in d:
                d[date]=event
            else:
                d[date]=event
    return d
        
        
        
        
        
if __name__ == '__main__':
    createDict()
    print d
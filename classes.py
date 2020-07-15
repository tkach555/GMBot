class newsContent:
    
    def __init__(self, masterPath):
        self.content = []
        self.msPath = masterPath
        self.fileName = 'lastlink.txt'
        
    def setContent(self, cont):
        self.content = cont
        
    def getData(self, keyw, index=0):
        if keyw == 'href':
            return self.msPath + self.content[index]['href']
        elif keyw == 'image':
            return self.content[index]['image']
        return self.content[index][str(keyw)].text
    
    # def getLink(self, index=0):
    #     return self.content[index]['href']
    
    # def writeLinkToFile(self):
    #     f = open(self.fileName, 'w')
    #     f.write(self.msPath + self.content['href'])
    #     f.close()

    def writeThisLinksToFile(self, links):	
        f = open(self.fileName, 'w')
        for line in links:
            f.write(line + '\n')
            # print(line)
        f.close()
        
    # def getLastLink(self):
    #     f = open(self.fileName, 'r')
    #     ln = f.readline()
    #     f.close()
    #     return ln

    def getAllLinksFromFile(self):
        with(open(self.fileName, 'r')) as f:
            ln = [line.rstrip() for line in f]
            return ln


    # def isEqualLinks(self, index=0):
    #     f = open(self.fileName, 'r')
    #     lastLink = f.readline()
    #     f.close()
    #     return lastLink == self.msPath + self.content[index]['href']
    
    def getStrData(self, index=0):
        fullLink = self.msPath + self.content[index]['href']
        return str('Заголовок:\n'+self.content[index]['header'].text+'\nОписание:\n'+self.content[index]['description'].text+'\nСсылка: '+fullLink)
        
import glob, os, re
from time import strptime

def initializeOutputFile(outputFileName):
    # Prep output file header
    outputFile = open('../' + outputFileName, "w")
    outputFile.write("Airline,Domestic,International,Month,Year\n")
    outputFile.close()

def parseFileYear(fileName):
    fileName = fileName.upper()
    fileName = fileName.replace("REGION", "")
    fileName = fileName.replace("REG", "")
    fileName = fileName.replace("_", "")
    fileName = fileName.replace("-", "")
    return re.search(r'\d{4}', fileName).group()

def parseFileMonth(fileName, fileYr):  
    fileName = fileName.upper()
    fileName = fileName.replace("REGION", "")
    fileName = fileName.replace("REG", "")
    fileName = fileName.replace("_", "")
    fileName = fileName.replace("-", "")
    fileName = fileName.replace(fileYr, "")
    wordMonth = re.search(r'\w{3}', fileName).group()
    return strptime(wordMonth,'%b').tm_mon # convert 3 letter month to integer

def prepareUsefulData(fileName):
    thisFile = open(fileName, "r")
    usefulData = thisFile.read()
    thisFile.close()
    if usefulData.find("Cum %") > 0 and usefulData.find("Tons") > 0:
        usefulData = usefulData[usefulData.find("Cum %")+5:usefulData.find("Tons")]
    else:
        raise Exception('Warning: Keyword Cum % or Tons not found!')
    # print("usefulData Length1: " + str(len(usefulData))) # debug output 
    # print("usefulData Length2: " + str(len(usefulData))) # debug output
    splitData = re.split('\n\n', usefulData) # split data by double newline, because of how pdf-to-text conversion went 
    ## Test if pdf-to-text conversion is imperfect
    testIndex = 0
    while re.search(r'[A-Z]{2,}', splitData[testIndex]) is None:
        testIndex=testIndex+1
        # print("testIndex: " + str(testIndex) + " splitData length: " + str(len(splitData))) # debug output
    splitData = splitData[testIndex-1:]
    try:
        splitData.remove("")
    except:
        pass
    try:
        splitData = splitData.remove(" ")
    except:
        pass
    for z in range(0, len(splitData)):
        if splitData[z].find("Freight") > 0:  
            splitData = splitData[:z]
            break
    return splitData

def checkForErrors(inputs, mode):
    if mode is 1:
        for z in inputs:
            if re.search(r'\d{3,}', z):
                raise Exception('Airlines list should not include numbers. A mixup occurred')
            if re.search(r'FEDERAL EXPRESS', z):
                raise Exception('FedEx is a freight carrier, not passenger carrier. A mixup occurred')
            if re.search(r'PARCEL', z):
                raise Exception('UPS is a freight carrier, not passenger carrier. A mixup occurred')
            if len(inputs) > 20:
                raise Exception('More than 20 values in the list of airlines. A mixup occurred')
    if mode is 2:
        for z in inputs:
            if re.search(r'\D{2,}', z):
                raise Exception('Number of passengers should not include alphabetic letters. A mixup occurred')
            if len(inputs) > 20:
                raise Exception('More than 20 values in the list of passengers carried. A mixup occurred')

# Initialize variables and data structures
os.chdir('./AirlinePDFs/')
outputFileName = "NYCAirlineData.txt"
initializeOutputFile(outputFileName)
columnsOfData = 6
airlineName = [] # list that stores all airline names
domesticPass = [] # list that stores all domestic passenger count
internationalPass = [] # list that stores all international passenger count

for file in glob.glob("*.txt"):
    # Specify which years of data to analyze. Still debugging to achieve general case...
    if (re.search('2010', file) is None) and (re.search('2011', file) is None) and (re.search('2012', file) is None) and (re.search('2013', file) is None) and (re.search('2014', file) is None)and (re.search('2015', file) is None)and (re.search('2016', file) is None) and (re.search('2017', file) is None):
        pass
    else:
        print(" ") # debug output
        print(file) # debug output
        splitData = prepareUsefulData(file)
        maxGroups = int(len(splitData)/columnsOfData) # there's 6 columns of data, but clumped together in groups

        # print("maxGroups: " + str(maxGroups)) # debug output
        # print("length of splitData: " + (str(len(splitData)))) # debug output
        # print(splitData) # debug output

        for x in range (0,maxGroups): 
            airlines = re.split('\n', splitData[(x*columnsOfData)+1])
            domestic = re.split('\n', splitData[(x*columnsOfData)+2])
            international = re.split('\n', splitData[(x*columnsOfData)+3])
            # print(airlines) # debug output
            # print(domestic) # debug output
            # print(international) # debug output
            for z in airlines:
                airlineName.append(z)
            for z in domestic:
                domesticPass.append(z.replace(',', ''))
            for z in international:
                internationalPass.append(z.replace(',', ''))
        
        checkForErrors(airlineName, 1)
        checkForErrors(domesticPass, 2)
        checkForErrors(internationalPass, 2)

        # Final case for 2015 files where an airline name is out of sequence in txt file after pdf-to-text parse
        if (len(domesticPass) > len(airlineName)) and (maxGroups*columnsOfData < len(splitData)):
            airlines = re.split('\n', splitData[len(splitData)-1])
            for z in airlines:
                airlineName.append(z)

        # print("Airlines:") # debug output
        # print(airlineName) # debug output
        # print("Dom Pass: ") # debug output
        # print(domesticPass) # debug output
        # print("Intl Pass: ") # debug output
        # print(internationalPass) # debug output

        fileYear = parseFileYear(file)
        fileMonth = parseFileMonth(file, fileYear)

        ### Add final processed data to output file
        outputFile = open('../' + outputFileName, "a") 
        for q in range(0, len(airlineName)):
            outputFile.write(airlineName[q]+','+domesticPass[q]+','+internationalPass[q]+','+str(fileMonth)+','+fileYear+'\n')

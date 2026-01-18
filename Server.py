import smtpd
import asyncore
import email
import struct
import os
import requests
import json
import time

# file which contains virus signatures, given in ESPL course
virusSignatureFileName = "signatures"

# file which contains words that are considered as spam (each word in the file is on new line)
spamWordsfilename = "spamWords"

# needed for using VirusTotal APIs
myApiKey = "25958e9090b5bcebf6669cb0bafd73b52d9bbe2b214ea8fa51a809bf56c25a27"

# reading the words from spamWords file and storing in list
def loadSpamWords():
    with open(spamWordsfilename) as file:
        spamWords = [line.rstrip() for line in file]
    file.close()
    return spamWords

# reading the viruses from signatures file and storing in list
def loadViruses():
    virusList = []
    with open(virusSignatureFileName, mode='rb') as signFile:

        # each virus data in the file is formatted this way:
        # < - little endian, H - unsigned short (signature length), 16s - 16-byte string (virus name)
        virus_format = '<H16s'

        # skip magic number (4 bytes)
        signFile.seek(4)

        # reading the block with signature length and virus name
        virus_data = signFile.read(18)

        while virus_data:

            # check if data was read successfully
            if len(virus_data) == 18:

                # unpack the data using the defined format
                sig_size, virus_name = struct.unpack(virus_format, virus_data)
        
                # allocate memory for the virus structure
                vir = {'SigSize': sig_size, 'virusName': virus_name, 'Sig': None}

                # read signature data
                vir['Sig'] = signFile.read(int(sig_size))

                virusList.append(vir)

                virus_data = signFile.read(18)  
            
    signFile.close()
    return virusList

# check if body contains spam words
def checkForSpam(body):
    foundSpam = False
    for word in SpamWords:
        if (word in body):
                print("\033[93mSpam word found: \033[00m", word)
                foundSpam = True
    
    if (foundSpam == False):
        print("\033[92mSpam words not found \033[00m")

# check if attachment contains virus from signatures
def checkForViruses(attachment):
    foundVirus = False
    for virus in VirusList:
        if (virus['Sig'] in attachment):
            print("\033[91mVirus found: \033[00m", virus['virusName'].decode("utf-8"))
            foundVirus = True
    
    if (foundVirus == False):
        print("\033[92mVirus from signatures not found \033[00m")

# check if attachment contains virus from VirusTotal
def checkVirusTotal(attachment, fileName):

    numOfTries = 5

    # creating directory "temp" to save there the attachment
    path = os.path.join(os.getcwd(),"Temp" )
    os.mkdir(path)
    filepath = os.path.join(path,fileName)
    
    # saving the attachment
    save_attach = open(filepath,"wb")
    save_attach.write(attachment)
    save_attach.close()

    # sending request to virustotal to scan the file
    command = "https://www.virustotal.com/vtapi/v2/file/scan"
    params = {'apikey': myApiKey}
    files = {'file': (fileName, open(filepath, "rb"))}
    response = requests.post(command, files=files, params=params)
    responseJson = json.loads(response.text)
                    
    print(responseJson)

    if (responseJson['response_code'] == 1):

        # come back after 60 sec to the response for scan request
        time.sleep(60)

        # sending the request for report 
        report = "https://www.virustotal.com/vtapi/v2/file/report"
        scan_id = responseJson["scan_id"]
        reportParams = {'apikey': myApiKey, 'resource': scan_id}
        reportResponse = requests.get(report, params=reportParams)
        reportResponseJson = json.loads(reportResponse.text)

        print(reportResponseJson)

        # scan finished successfully
        if(reportResponseJson['response_code'] == 1):
            if(reportResponseJson['positives'] == 0):
                print("\033[92m Virus not found by VirusTotal in: \033[00m", fileName)
            else:
                print("\033[91m Virus found by VirusTotal in: \033[00m", fileName)

        # response_code = -2, means need to wait and send again report request
        else:
            while (reportResponseJson['response_code'] == -2 and numOfTries > 0):
                time.sleep(60)      
                reportResponse = requests.get(report, params=reportParams)
                reportResponseJson = json.loads(reportResponse.text)
                print(" Send request ", numOfTries)
                print(reportResponseJson)
                numOfTries = numOfTries - 1  

            if(reportResponseJson['response_code'] == 1):
                if(reportResponseJson['positives'] == 0):
                    print("\033[92m Virus not found by VirusTotal in: \033[00m", fileName)
                else:
                    print("\033[91m Virus found by VirusTotal in: \033[00m", fileName)
            elif(reportResponseJson['response_code'] == -2):
                print("\033[94m sorry, site is unreachable at this moment. try again \033[00m")

    # deleting the file and the directory we created
    os.remove(filepath)
    os.rmdir(path)       

# loading the spam words and the signatures to the lists
SpamWords = loadSpamWords()
VirusList = loadViruses()

# define a SMTP server class inheriting from smtpd.SMTPServer
class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, mail_options=None,rcpt_options=None):
        print ('Receiving message from:', peer)
        print ('Message addressed from:', mailfrom)
        print ('Message addressed to  :', rcpttos)
        print ('Message length        :', len(data))

        # parse the incoming email message
        msg = email.message_from_string(data.decode("utf-8"))
        body = ""

        # check if the message is multipart (contains attachments)
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()

                # get the body
                if ctype == 'text/plain':

                    # decode
                    body = part.get_payload()

                    # check for spam in the body
                    checkForSpam(body)

                # get the attachment
                if ctype == 'application/octet-stream':

                    # decode
                    attach = part.get_payload(decode=True)  

                    # check for viruses from signatures in the attachment
                    checkForViruses(attach)                    

                    attachmentFileName = part.get_filename()

                    # check for viruses from virustotal in the attachment
                    checkVirusTotal(attach, attachmentFileName)

        # not multipart - no attachments
        else:
            print('NotMultipart')
            body = msg.get_payload(decode=True)
            checkForSpam(body)
        return

# create an instance of the custom SMTP server
server = CustomSMTPServer(('127.0.0.1', 1025), None)

# asyncore event loop to handle incoming connections
asyncore.loop()
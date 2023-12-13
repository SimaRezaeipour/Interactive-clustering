import pypff
import unicodecsv as csv
import os
import re
from datetime import datetime
from dateutil.parser import parse

def folderTraverse(base):
    for folder in base.sub_folders:
        if folder.number_of_sub_folders:
            folderTraverse(folder) # Call new folder to traverse:
        if folder.name == "CSRT - Listserv":
            checkForMessages(folder)

def checkForMessages(folder):
    message_list = []
    for message in folder.sub_messages:
        # getSenderName(message.get_transport_headers(), "name")
        message_dict = processMessage(message)
        message_list.append(message_dict)
    folderReport(message_list, folder.name)

def getSenderName(text, type):
    pattern = re.compile(r'From: (.*?>)')
    name = ""
    email = ""

    for matched in re.finditer(pattern, text):
        matched.group(1)
        name = matched.group(1)[0:matched.group(1).index('<')].replace('"','').strip()
        email = matched.group(1)[matched.group(1).index('<')+1:matched.group(1).index('>')]
        break

    if type == "name":
        return name

    if type == "email":
        return email

def getDate(text):
    """
    It is important to consider time dfferences as well: Fri, 10 Jul 2015 15:07:29 -0400
    :param text:
    :return:
    """
    date = text[text.index("Date: ")+6:text.index("Date: ") + 37]

    if date[len(date)-1] != '0':
        date = date.strip().replace('\r','').replace('\n','')
        date = date[:5] + "0" + date[5:]

    return date

def processMessage(message):
    return {
        "subject": message.subject,
        "to": message.sender_name,
        "body": message.plain_text_body,
        "sender_name": getSenderName(message.get_transport_headers(), "name"),
        "sender_email": getSenderName(message.get_transport_headers(), "email"),
        "delivery_time": getDate(message.get_transport_headers()),
        "attachment_count": message.number_of_attachments,
    }

def sortEmailsByDate(message_list):

    for i in range(0, len(message_list)):
        print(i)
        for j in range(i + 1, len(message_list)):
            # date1 = datetime.strptime(message_list[i]['delivery_time'], "%a, %d %b %Y %H:%M:%S %z")
            # date2 = datetime.strptime(message_list[j]['delivery_time'], "%a, %d %b %Y %H:%M:%S %z")
            date1 = parse(message_list[i]['delivery_time'])
            date2 = parse(message_list[j]['delivery_time'])

            if date1 > date2:
                temp = message_list[i]
                message_list[i] = message_list[j]
                message_list[j] = temp

def folderReport(message_list, folder_name):
    # CSV Report
    fout_path = makePath(folder_name + ".csv")
    fout = open(fout_path, 'wb')
    header = ['subject', 'to', 'body',
              'sender_name', 'sender_email', 'delivery_time', 'attachment_count']

    #sort rows by column
    sortEmailsByDate(message_list)

    csv_fout = csv.DictWriter(fout, fieldnames=header, extrasaction='ignore')
    csv_fout.writeheader()
    csv_fout.writerows(message_list)
    fout.close()

def makePath(file_name):
    return os.path.abspath(os.path.join("Resources", file_name))

pst = pypff.open("Resources/CSRT Data/CSRT_ListServ_Archive.pst")
root = pst.get_root_folder()
folderTraverse(root)


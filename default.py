'''

Created on 09.04.2013

@author: CRImier
'''

#import appuifw
#import appuifw2

import cryptdata
import time
import datetime

level = 0
data = []
password = ''
deleted = []

def load():
    global level
    global data
    global password
    data = False
    counter = 0
    while data == False: #Insert check and timer
        if counter != 0:
            print "Sorry, incorrect password. Wait "+str(counter*5)+" seconds"
            time.sleep(counter*5)
        password = raw_input('Your diary password:')
        data = cryptdata.decryptdiary(password)
        counter += 1
    if len(data) == 3 and data[2] == "ERROR!":
        print "Checksum error"
    level = data[1]
    data = data[0]
        
def setup():
    global level
    global password
    print "First launch!"
    password = raw_input('Your diary password:')
    print "Which level of encryption do you want? Select either 1, 2 or 3" #Insert disambiguation
    level = int(raw_input())
    if cryptdata.creatediary('[]', password, level):
        print "Diary created!"
    else:
        print "Error"
        
def add_entry():
    global data
    print "Express yourself"
    story = raw_input()
    now_time = datetime.datetime.now()
    header = now_time.strftime("%d.%m.%Y %H:%M")
    data += [[header, story]]
    return_to_menu()
    
def del_entry():
    global deleted
    global data
    if len(data) == 0:
        print "No entry to delete"
    else:
        number = select_entry("Select entry to delete", data)
        deleted += [[data[number], number]]
        del data[number]
        print "Entry deleted"
    return_to_menu()
    
def encrypt_entry():
    global data
    ennum = select_entry("Select entry to encrypt", data)
    password = raw_input("Enter password to encrypt this entry")
    data[ennum] = cryptdata.encryptentry(data[ennum], password)
    return_to_menu()

def decrypt_entry():
    global data
    ennum = select_entry("Select entry to decrypt", data)
    password = raw_input("Enter password to decrypt this entry")
    answer = cryptdata.decryptentry(data[ennum], password)
    if answer == 'notenc':
        print "Entry not encrypted."
    elif answer == False:
        print "Decryption failed"
    else:
        data[ennum] = answer
        
    return_to_menu()

def restore_entry():
    global deleted
    global data
    if len(deleted) == 0:
        print "No entry to restore"
    else:
        number = select_entry("Select entry to restore", array=[entry[0] for entry in deleted])
        entry = deleted[number]
        data += [entry[0]]
        del deleted[number]
        print "Restore successful"
    return_to_menu()

def delete_diary():
    print "It will delete the existing dictionary and checksum files. Continue? To continue, enter 'OK'."
    answer = raw_input()
    if answer == "OK":
        cryptdata.deletediary()
        exit()
    else:
        return_to_menu()

def import_data():
    global data
    filename = 'diary.dump'
    answer = cryptdata.importdata(filename)
    if isinstance(answer, list):
        data = answer
    else:
        print "Import failed - no file to import from or file corrupt."
    return_to_menu()
    
def export_data():
    filename = 'diary.dump'
    if cryptdata.exportdata(data, filename):
        pass
    else:
        print "Error exporting."
    return_to_menu()

def pexit():
    cryptdata.encryptdiary(data, password, level)
    print "Exiting"
    exit()
  
"""UI-related functions, mainly to make CLI menus"""  
view = 0 #Variable to save type of menu where user has been before selecting an option

def select_action(greeting, actlist):
    """This is function to use for menu generation and usage. 
    It takes greeting argument which is printed at the beginning and array of actions (like main_actions),
    then prints them out and allows to choose one option, and finally calls a callback."""
    print greeting
    for number in range(len(actlist)):
        action = actlist[number][1]
        print str(number)+" - "+action
    answer = -1
    while answer not in range(len(actlist)):
        try:
            answer = int(raw_input())
        except:
            answer = -1
    actlist[answer][0]()
    
def select_entry(greeting, array):
    """This is function to use for submenu generation and usage, 
    specified for submenus where one of array entries has to be selected.
    It takes greeting argument which is printed at the beginning and array of entries (like data),
    then prints this array out and allows to choose one entry, and finally returns index of entry."""
    print greeting
    if len(array) == 0:
        print "No entry to select"
        return 0
    for number in range(len(array)):
        entry = array[number]
        print str(number)+" - "+entry[0]
    answer = -1
    while answer not in range(len(array)):
        try:
            answer = int(raw_input())
        except:
            answer = -1
    return answer    
 
def main_view():
    """A function to show main menu"""
    global view
    view = 0
    select_action("Tasks:", main_actions)
    
def return_to_menu():
    if view == 0:
        main_view()
    else:
        list_entries()
    
def list_entries():
    """A function to list diary entries"""
    global view
    view = 1 #Setting return
    if len(data) != 0:
        for x in range(len(data)):
            entry = data[x]
            if len(entry) >= 3:
                print str(x)+" "+entry[0]+" encrypted"
            else:
                print str(x)+" "+entry[0]+": "+entry[1][:20]+"..."
    else:
        print "No entries yet."
    select_action("Tasks:", enlist_actions)
    
def diary_management():
    select_action("Tasks:", dicman_actions)
    
def pack_diary():
    pass
    return_to_menu()

def extract_diary():
    pass
    return_to_menu()

def display_entry():
    ennum = select_entry("Select entry to display:", data)
    if len(data[ennum]) >= 3:
        print ""
        print "Unable to display encrypted entry"
        print""
    else:
        print ""
        print data[ennum][0]
        print data[ennum][1]
        print ""
    return_to_menu()

"""Different menu items"""
main_actions = [[list_entries, "List entries"], [add_entry, "Add entry"], [diary_management, "Diary management"], [pexit, "Exit"]]
enlist_actions = [[add_entry, "Add entry"], [display_entry, "Display entry"], [del_entry, "Delete entry"], [encrypt_entry, "Encrypt entry"], [decrypt_entry, "Decrypt entry"], [restore_entry, "Restore entry"], [main_view, "Back to main menu"]]
dicman_actions = [[import_data, "Import data"], [export_data, "Export data"], [pack_diary, "Pack diary"], [extract_diary, "Extract diary"], [delete_diary, "Delete diary"], [main_view, "Back to main menu"]]

"""Main flow"""

first_launch = cryptdata.first_launch()
if first_launch:
    setup()
else:
    load()
main_view()

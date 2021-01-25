import cgi

import eel
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import nltk

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download("punkt", quiet= True)

train_data = pd.read_csv(r"data/Businessdata.csv")
train_data.head()

Names = train_data['Name']
Basic = train_data['Basic']
Advanced = train_data['Advance']
Address = train_data['Address']
Contact = train_data['Contact']

BasicItems = []
AdvancedItems = []

BasicSplit = [sub.split() for sub in Basic] 

LargeCorpus = Advanced.to_numpy().tolist()

def FindBusiness(user_input):
    user_input = user_input.lower()
    LargeCorpus.append(user_input)
    bot_response = ''

    
    
    #first get the basic things in order 
    get_basic(user_input)
    
    
    cm = CountVectorizer().fit_transform(LargeCorpus)
    simularity_score =  cosine_similarity(cm[-1], cm)
    similarity_score_list = simularity_score.flatten()
    index = index_sort(similarity_score_list)
    index = index[1:]
    response_flag = 0
    j = 0
    for i in range(len(index)):
        if (similarity_score_list[index[i]] > 0.0):
            indexOrder = index[i]
            response_flag = 1
            
            GlobalIndex = LargeCorpus.index(LargeCorpus[indexOrder])

            bot_response = bot_response + ' ' + Names[GlobalIndex] + '<div id = "InputDescription">'\
                           + Basic[GlobalIndex] + "</div>" + "<br>" + '<div id = "DetailsResult">'\
                           + Advanced[GlobalIndex] + "</div>" + "<br>" + '<div id = "Address">'\
                           + str(Address[GlobalIndex]) + "</div>" + '<div id = "Address">'\
                           + str(Contact[GlobalIndex]) + "</div>" + "<br><br>"
            j = j + 1
        if j > 8:
            break
    if response_flag == 0:
        bot_response = "Sorry, can't find anything"
    LargeCorpus.remove(user_input)

    return bot_response


def get_basic(user_input):
    BasicItems.clear()
    for index in range(len(BasicSplit)):
        for Keywords in BasicSplit[index]:
            if (user_input in Keywords and index not in BasicItems):
                BasicItems.append(index)

def index_sort (list_var):
    length = len(list_var)
    list_index = list(range(0,length))

    x = list_var
    for i in range(length):
        for j in range(length):
            if x[list_index[i]] > x[list_index[j]]:
                #Swap 
                temp = list_index[i]
                list_index[i] = list_index[j]
                list_index[j] = temp
    return list_index

#get input from the website
form = cgi.FieldStorage()
searchterm =  form.getvalue('searchbox')


#start the web
eel.init("static")


@eel.expose
def giveInput(user_input):

    #this was supposed to be used for a more advanced sorting system in the future, however time is short.
    print(Names[BasicItems])
    return FindBusiness(user_input)

@eel.expose
def getCatalog():
    bot_response = ''
    for x in range(len(Names)):
        bot_response = bot_response + ' ' + Names[x] + '<div id = "InputDescription">' \
                       + Basic[x] + "</div>" + "<br>" + '<div id = "DetailsResult">' \
                       + Advanced[x] + "</div>" + "<br>" + '<div id = "Address">' \
                       + str(Address[x]) + "</div>" + '<div id = "Address">' \
                       + str(Contact[x]) + "</div>" + "<br><br>"
    return bot_response

eel.start("index.html")

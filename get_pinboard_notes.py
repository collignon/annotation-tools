import os
from dotenv import load_dotenv, find_dotenv, set_key
load_dotenv() 

from dateutil.parser import parse

import pandas as pd
import json
import string

import pinboard

import secrets as se




pk = se.pinboard_key
pb = pinboard.Pinboard(pk)

out = pb.posts.all(parse_response=False)
out = json.loads(out.read().decode("utf-8"))

# pull last import date from .env file
pinboard_last_pull = os.getenv('pinboard_last_pull')
print("pinboard last date pulled: ", pinboard_last_pull)

# if None, set to 1990 
if pinboard_last_pull is None:
    pinboard_last_pull = "1990-01-01"

# filter bookmarks based on last pulled date
out = [i for i in out if parse(i['time'][:10])>=parse(pinboard_last_pull)]
print ("new notes: ", len(out))

assert len(out)>0

# update last pull in .env file
last_pull = pd.DataFrame(out).time.max()[:10]

dotenv_file = find_dotenv()
set_key(dotenv_file, "pinboard_last_pull", last_pull)

for pb_note in out:

    href = pb_note['href']
    title = pb_note['description']
    filename = title.translate(str.maketrans('', '', string.punctuation)).lower()
    filename = filename.replace(" ", "-")
    note = pb_note['extended']
    date = pb_note['time'][:10]
    tags = pb_note['tags']

    if pb_note['toread'] == 'yes':
        tags += ' to-read' 
    tags = " ".join(["#"+i for i in tags.split(" ")]) 

    with open("out/"+filename+'.md','w') as file:
            title_line= "# "+title+"\n\n"
            tag_line = "tags: "+ tags +"\n\n"
            uri_line = "uri: ["+title+"]("+href+")\n"
            date_line = "date: "+ date+"\n"
            if len(note)>0:
                note_line = "### note:\n"+note
            else:
                note_line = ""

            file.writelines([title_line,
                             date_line,
                            tag_line,
                            uri_line,
                            note_line])
        


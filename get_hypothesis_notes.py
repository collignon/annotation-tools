import os
from dotenv import load_dotenv, find_dotenv, set_key
load_dotenv() 

import json
import string

import numpy as np
import pandas as pd

from dateutil.parser import parse

ROOT = os.path.dirname(os.path.abspath(__file__))

with open('annotations.json', 'r', encoding='utf-8') as j:
     contents = json.loads(j.read())


# pull last import date from .env file
hypothesis_last_pull = os.getenv('hypothesis_last_pull')

print("hypothesis - Last date pulled: ", hypothesis_last_pull)

# if None, set to 1990 
if hypothesis_last_pull is None:
    hypothesis_last_pull = "1990-01-01"

# filter annotations based on last pulled date
contents['annotations'] = [i for i in contents['annotations'] if parse(i['updated'][:10])>=parse(hypothesis_last_pull)]

print("new notes: ", len(contents['annotations']))


all_notes =[]

# extract annotation info from each hypothesis document
for i in range(len(contents['annotations'])):

    anno = contents['annotations'][i]

    created = anno['updated']
    if len(anno['document'])==0:
        title = created[:10]+"-"+"no-title"
    else:
        title = anno['document']['title'][0]
        title = title.translate(str.maketrans('', '', string.punctuation)).lower()
        title = (created[:10]+"-"+title).replace(" ", "-")

    context_href = anno['links']['incontext']
    uri = anno['uri']
    tags = anno['tags']
    try:
        highlights = [i['exact'] for i in anno['target'][0]['selector'] if 'exact' in i.keys()][0]
    except:
        print(i)
        print(anno['target'])
    
    note = anno['text']
    
    n ={}
    
    date = created[:10]
    tags = "#"+' #'.join(tags)
    url = context_href
    title = title
    
    n['title'] = title
    n['tags'] = tags
    n['date'] = date
    n['url'] = url
    n['highlights'] = "> " +highlights +" s\n" +note 
    n['uri'] = uri
    
    all_notes.append(n)

# create dataframe and unify notes with same title / date pairs
df = pd.DataFrame(all_notes).groupby(["title","date","uri"])['highlights'].apply(list).reset_index(name='highlights')
df['tags'] = pd.DataFrame(all_notes).groupby(["title","date"])['tags'].apply(lambda x: list(np.unique(x))).reset_index(name='tags')['tags'].values
df['url'] = pd.DataFrame(all_notes).groupby(["title","date"])['url'].apply(lambda x: list(np.unique(x))).reset_index(name='url')['url'].values

# update last pull in .env file
last_pull = max(df['date'])
print(last_pull)

# bundle new notes to unique folder
base_path = os.path.join(ROOT, "out", "hypothesis", last_pull)
os.makedirs(base_path, exist_ok=True)

# create markdown files for each document with highlights and notes
for i,note_file in df.iterrows():

    title = note_file['title']
    tags = note_file['tags']
    date = note_file['date']
    uri = note_file['uri']

    with open(os.path.join(base_path, title+'.md'), 'w', encoding='utf-8') as out:
        title_line= "# "+title[11:]+"\n\n"
        tag_line = "tags: "+ " ".join([i for i in " ".join(tags).split(" ") if len(i)>1])+"\n"
        uri_line = "uri: ["+title[11:]+"]("+uri+")\n"
        date_line = "date: "+ date+"\n"

        high_line = ""
        for index,high in enumerate(note_file['highlights']):
            high_line += high +"\n"
            high_line += "[hypothesis ref]("+note_file['url'][0]+")\n\n ----\n"

        out.writelines([title_line,
                        tag_line,
                        uri_line,
                        date_line,
                        "### highlight:\n",high_line])
        
dotenv_file = find_dotenv()
set_key(dotenv_file, "hypothesis_last_pull", last_pull)


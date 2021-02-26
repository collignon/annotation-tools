import json
import string

import numpy as np
import pandas as pd


with open('annotations.json', 'r') as j:
     contents = json.loads(j.read())

all_notes =[]

# extract annotation info from each hypothesis document
for i in range(len(contents['annotations'])):

    anno = contents['annotations'][i]

    created = anno['created']
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
    n['highlights'] = "```" +highlights +"``` \n" +note 
    n['uri'] = uri
    
    all_notes.append(n)


# create dataframe and unify notes with same title / date pairs
df = pd.DataFrame(all_notes).groupby(["title","date","uri"])['highlights'].apply(list).reset_index(name='highlights')
df['tags'] = pd.DataFrame(all_notes).groupby(["title","date"])['tags'].apply(lambda x: list(np.unique(x))).reset_index(name='tags')['tags'].values
df['url'] = pd.DataFrame(all_notes).groupby(["title","date"])['url'].apply(lambda x: list(np.unique(x))).reset_index(name='url')['url'].values

# create markdown files for each document with highlights and notes
for i,note_file in df.iterrows():

    title = note_file['title']
    tags = note_file['tags']
    date = note_file['date']
    uri = note_file['uri']

    with open("out/"+title+'.md','w') as out:
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
        
        
    

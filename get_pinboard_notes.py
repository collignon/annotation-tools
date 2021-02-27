import json
import string

import pinboard

import secrets as se
 
pk = se.pinboard_key
pb = pinboard.Pinboard(pk)

out = pb.posts.all(parse_response=False)
out = json.loads(out.read().decode("utf-8"))

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
        

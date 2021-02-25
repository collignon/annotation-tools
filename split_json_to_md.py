import json
import string

with open('annotations.json', 'r') as j:
     contents = json.loads(j.read())

for i in range(len(contents['annotations'])):

    anno = contents['annotations'][i]

    created = anno['created']
    if len(anno['document'])==0:
        title = "no title"
    else:
        title = anno['document']['title'][0]
        title = title.translate(str.maketrans('', '', string.punctuation)).lower()

    context_href = anno['links']['incontext']
    tags = anno['tags']
    try:
        highlights = [i['exact'] for i in anno['target'][0]['selector'] if 'exact' in i.keys()][0]
    except:
        print(i)
        print(anno['target'])
    
    note = anno['text']

    with open("out/"+created[:10]+"-"+title.replace(" ", "-")+'.md','w') as out:
        date = 'date: '+ created[:10]+"\n"
        tags = "tags: #"+' #'.join(tags) + "hypothesis_note"+"\n"
        url = "url: [here]("+context_href+")"+"\n\n"
        title = '# '+title+"\n"

        out.writelines([date,tags,url,title,"### highlight:\n",highlights,"\n\n### note\n",note])
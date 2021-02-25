import json
import string

def increment_title(title,titles):
    i = 1
    while title in titles:
        if title+'-'+str(i) in titles:
            i+=1
        else:
            title=title+'-'+str(i)
    else:
        title=title
    return title   


with open('annotations.json', 'r') as j:
     contents = json.loads(j.read())

all_titles = []

for i in range(len(contents['annotations'])):

    anno = contents['annotations'][i]

    created = anno['created']
    if len(anno['document'])==0:
        title = created[:10]+"-"+"no-title"
    else:
        title = anno['document']['title'][0]
        title = title.translate(str.maketrans('', '', string.punctuation)).lower()
        title = (created[:10]+"-"+title).replace(" ", "-")
        
    title = increment_title(title,all_titles)
    all_titles.append(title)  
     

    context_href = anno['links']['incontext']
    tags = anno['tags']
    try:
        highlights = [i['exact'] for i in anno['target'][0]['selector'] if 'exact' in i.keys()][0]
    except:
        print(i)
        print(anno['target'])
    
    note = anno['text']

    with open("../../out/"+title+'.md','w') as out:
        date = 'date: '+ created[:10]+"\n"
        tags = "tags: #"+' #'.join(tags) + "hypothesis_note"+"\n"
        url = "url: [here]("+context_href+")"+"\n\n"
        title = '# '+title+"\n"

        out.writelines([date,tags,url,title,"### highlight:\n",highlights,"\n\n### note\n",note])
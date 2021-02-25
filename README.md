# Annotation tools

## exporting hypothesis annotations to obsidian (markdown files)

Inspired by the tutorial from [Shawn Graham](https://electricarchaeology.ca/2021/02/14/from-hypothesis-annotation-to-obsidian-note/).

First, get ‘Hypexport’ from https://github.com/karlicoss/hypexport . 

Install it with

``` pip install --user git+https://github.com/karlicoss/hypexport ```

Then, create a new text file; call it secrets.py and put into it your Hypothesis username and your developer token (which is underneath your username when you have hypothesis open) like so:

```
username = "USERNAME"
token = "TOKEN"
```

Grab all of your annotations with:

``` python -m hypexport.export --secrets secrets.py > annotations.json ```

create an out directory for the markdown notes. 

```mmkdir out```

Then run the ```split_json_to_md.py``` script.


----

## to do:

- avoid duplicates when exporting highlights
- pinboard notes to markdown
 

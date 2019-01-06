# WhatsApp-Analyzer
Analyze Chatsapp chat

The script reads an exported whatsapp chat and then extracts the data. You may need to install some packages before run it

### Preview
![](https://i.imgur.com/8kqBa4I.png)

### Requirements
- Python 2.7+ or Python 3
```python
pip install pandas emoji seaborn matplotlib numpy wordcloud 
```
### Usage
```
$ git clone https://github.com/PetengDedet/WhatsApp-Analyzer.git

$ cd WhatsApp-Analyzer
$ python python whatsapp_analyzer.py
```

### Notes
- This script use regex to extract the data
- Some date format may not supported
- Tested in python 2.7+ on MacOS
- When using virtualenv there is error backend stuff
  I don't know how to fix it yet. Help please :)
- If chat file located outside script directory, please fill it with fullpath not relativepath
- There is common words file:
  - id_cw.py for Bahasa Indonesia
  - en_cw.py for English. Thanks @Deekayen [gist](https://gist.github.com/deekayen/4148741 "gist")
  If you want to add any other language, you can make it one

### Getting chat source
#### Android:
- Open a chat/group chat
- Tap on trhee dots oh the top right
- Tap "More"
- Choose "Export chat"
- Choose "Without Media"

#### iOS
- Open a chat/group chat
- Tap on contact name/group name on the top to see the details
- Scroll down to find "Export Chat" menu
- Choose "Without Media"


## Jupyter Notebook
Description included inside
#### Visualization Preview
 - Top 20 most active member
   ![](https://i.imgur.com/dqC83Gb.png)
 - Peaktime
   ![](https://i.imgur.com/C4D2cjw.png)
 - Attachment Share
   ![](https://i.imgur.com/mEWKSRj.png)
 - Top Mentioned Website
   ![](https://i.imgur.com/9Y8hTwE.png)
 - Wordcloud
   ![](https://i.imgur.com/RaGDrEp.png)

#### Raw
   ![](https://i.imgur.com/sCIEQas.png)
  

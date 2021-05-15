# WhatsApp-Analyzer
Analyze WhatsApp chat

The script reads an exported WhatsApp chat and then extracts the data. You may need to install some packages before running it.

##### Supported Analysis
----------------------
- Chat Count
- Chat Average
- Member/Sender Rank
- Website/URL/Link Domain Rank
- Word Count and Rank
- Most Used Word by Sender
- Emoji Usage Rank
- Most Used Emoji by Sender
- Timestamp Heatmap
- Attachment Classification (In Android, there is no difference pattern for attachment. But in iOS we can actually classify between Image, Video, Audio, GIF, Sticker, Document and Contact Card)

### Preview
----------------------
- Sender Rank
![Sender rank](https://i.imgur.com/5MnQRhV.png)
- Domain rank
![Domain rank](https://i.imgur.com/jASt34p.png)
- Word Rank
![Word rank](https://i.imgur.com/NmfWGSa.png)
- Most used word by sender
![Most used word by sender](https://i.imgur.com/GdtzLFy.png)
- Emoji rank
![Emoji rank](https://i.imgur.com/PqCVcej.png)
- Most used emoji by sender
![Most used emoji by sender](https://i.imgur.com/DauFsMx.png)
- Chat activity heatmap
![Heatmap](https://i.imgur.com/6KyNJF2.png)

### Requirements
----------------------
- Python 3.6+
```python
pip install -r requirements.txt
```
### Usage
----------------------
```
$ git clone https://github.com/PetengDedet/WhatsApp-Analyzer.git

$ cd WhatsApp-Analyzer
$ python whatsapp_analyzer.py chat_example.txt --stopword indonesian 
```

```shell
usage: python whatsapp_analyzer.py FILE [-h] [-d] [-s] [-c]

Read and analyze whatsapp chat

positional arguments:
  FILE                  Chat file path

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Debug mode. Shows details for every parsed line.
  -s , --stopword       Stop Words: A stop word is a commonly used word (such
                        as 'the', 'a', 'an', 'in'). In order to get insightful
                        most common word mentioned in the chat, we need to
                        skip these type of word. The Allowed values are:
                        arabic, bulgarian, catalan, czech, danish, dutch,
                        english, finnish, french, german, hebrew, hindi,
                        hungarian, indonesian, italian, malaysian, norwegian,
                        polish, portuguese, romanian, russian, slovak,
                        spanish, swedish, turkish, ukrainian, vietnamese
  -c , --customstopword 
                        Custom Stop Words. File path to stop word. File must a
                        raw text. One word for every line
```
### Stop Words
----------------------
I've included stop words for several languages from https://github.com/Alir3z4/stop-words.
You can use your own stop word file.
Just use `-c` argument followed by filepath.
One word for each file like below
```
able
ableabout
about
above
abroad
abst
```


### Notes
----------------------
- This script uses regex to extract the data.
- Currently supports the chat pattern below:
 ```python
    "14/10/18, 11:16 - Contact Name: this is a message"
    "2/30/18, 2:07 AM - Contact Name:  Test👌"
    "[30/12/18 4.59.25 PM] Nama User: 🙏test"
    "[06/07/17 13.23.30] ‪+62 123-456-78910‬: image omitted"
  ```
- Some date formats may not be supported


## Flowchart
----------------------
Describe how the script identify and classify the chat
```
           +------------------+
      +----+    Empty line?   +----+
      |    +------------------+    |
      |                            |
      |                            |
  +---v---+                   +----v---+
  |  Yes  | +-----------------+   No   |
  +-------+ |                 +---+----+
            |                     |
  +---------+-+             +-----v-----+
  | Event Log |        +----+    Chat   +----+
  +-----------+        |    +-----------+    |
                       |                     |
                +------v-----+         +-----v------+   +--------------------+
          +-----+Regular Chat+----+    | Attachment +-->+ Clasify Attachment |
          |     +------------+    |    +------------+   +-------+------------+
          v                       v                             |
+---------+---------+   +---------+----------+                  |
|   Starting Line   |   |   Following Line   |                  |
+------+------------+   +-+------------------+                  |
       |                  |                                     |
       |                  |                                     |
       |           +------v-------+                             |
       |           | COUNTER      |                             |
       |           | 1 Chat       |                             |
       +---------->+ 2 Timestamp  +<----------------------------+
                   | 3 Sender     |
                   | 4 Domain     |
                   | 5 Words      |
                   | 6 Attachment |
                   | 7 Emoji      |
                   +-----+--------+
                         |
                         |
                         |
                         v
              +----------+----------------+
              |          Visualize        |
              +---------------------------+
```


### Getting chat source
#### Android:
- Open a chat/group chat
- Tap on three dots on the top right
- Tap "More"
- Choose "Export chat"
- Choose "Without Media"

#### iOS
- Open a chat/group chat
- Tap on contact name/group name on the top to see the details
- Scroll down to find "Export Chat" menu
- Choose "Without Media"

## Other Tech Port
----------------------
- Web: Coming soon
- Jupyter Notebook: Coming soon
- NodeJS: Coming soon

### Help Needed
----------------------
- Need contributor to rearrange directory structure to match python best practice.
- iOS exported example needed 

#### Buy me a coffee
<a href="https://www.buymeacoffee.com/PetengDedet" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/lato-orange.png" alt="Buy Me A Coffee" style="height: 22px !important;" ></a>

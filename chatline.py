# -*- coding: utf-8 -*-
import re
from dateutil import parser
import emoji

# TODO: Classify attachment Move regex pattern to separate file or variable for dynamic change

class Chatline:

    def __init__(self, line="", previous_line=None, debug=False):
        self.previous_line = previous_line
        self.line = line
        self.line_type = None # Chat/Event/Attachment
        self.timestamp = None
        self.sender = None
        self.body = ""
        self.is_startingline = False
        self.is_followingline = False
        self.is_deleted_chat = False
        self.words = []
        self.emojis = []
        self.domains = []

        self.parse_line(line)
        if debug:
            print()
            for i in self.__dict__:
                print(i, ':',  self.__dict__[i])
            print("------")

    def replace_bad_character(self, line=""):
        return line.strip().replace(u"\u202a", "").replace(u"\u200e", "").replace(u"\u202c", "").replace(u"\xa0", " ")

    def is_starting_line(self, line=""):
        """
        Starting line mean a line that started with date time.
        Because there are multiline chat. I called it following line.
        A starting line must be classified before it's data being extracted.

        The Rule is:
        <datetime><separator><contact/phone number>
        """
        pattern = r"""
            (\[?)       #Zero or one open square bracket '['
            (((\d{1,2})   #1 to 2 digit date
            (/|-)       #'/' or '-' separator
            (\d{1,2})   #1 to 2 digit month
            (/|-)       #'/' or '-' separator
            (\d{2,4}))   #2 to 4 digit of year
            (,?\s)      #Zero or one comma ',' and ingle space
            ((\d{1,2})  #1 to 2 digit of hour
            (:|\.)      #Colon ':' or dot '.' separator
            (\d{2})     #2 digit of minute
            (\.|:)?     #Zero or one of dot '.' or colon ':'
            (\d{2})?    #Zero or one of 2 digits of second
            (\s?[apAP][mM])?))  #Zero or one of ('space', 'A' or 'P', and 'M'
            (\]?\s-?\s?\s?)#Zero or one close square bracket ']', Zero or one (space and '-'), zero or one space
            (.+)        #One or more character of chat member phone number or contact name
        """
        match = re.match(re.compile(pattern, re.VERBOSE), line)
        if match:
            return match

        return None

    def is_chat(self, body=""):
        """
        "Is Chat" means the body of a line is not an event.
        May contains attachment

        The Rule is:
        <contact/phone number><separator><message body>
        """
        pattern = r"""
                ([^:]+)#Chat member
                (:)   #Colon separator
                (.+)  #One or more charachter of message content
        """
        match = re.match(re.compile(pattern, re.VERBOSE), body)
        if match:
            return match

        return None

    def is_deleted(self, body=""):
        """
        Deleted message
        """
        p = [
            r".*This message was deleted$",
            r".*Pesan ini telah dihapus$"
        ]
        
        for p in p:
            match = re.match(p, body)
            if match:
                return body
        return None

    def contains_attachment(self, body=""):
        """
        Classify attachment
        Note: in Android, there is no difference pattern wether it's an image, 
            video, audio, gif, document or sticker.
        """
        pattern_attachment = [
            r".*<Media omitted>$", #English version of android attachment
            r".*<Media tidak disertakan>$", #Indonesia version of android attachment
            r".*Archivo omitido*", #Spanish version of android attachment
            r".*Pesan tidak didukung$", #Some device not recognize sticker attachment
            r".+\.vcf \(file\sterlampir\)$", #Indonesian version of android contact card,
            r".+\.vcf \(file\sattached\)$", #Indonesian version of android contact card,
            r".*image omitted$",
            r".*video omitted$",
            r".*document omitted$",
            r".*Contact card omitted$",
            r".*audio omitted$",
            r".*GIF omitted$",
            r".*sticker omitted$",
            r".*imagen omitida*",
            r".*audio omitido*",
            r".*GIF omitido*",
            r".*sticker omitido*",
            r".*video omitido*"
        ]
        
        for p in pattern_attachment:
            if re.match(p, body):
                return body
        return None

    def extract_timestamp(self, time_string=""):
        """
        EXTRACT TIMESTAMP
        """
        timestamp = parser.parse(time_string)
        return timestamp
    
    def extract_url(self, body=""):
        """
        Check if chat contais a url
        """
        # pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
        pattern = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,6}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        
        return re.findall(pattern, body)
    
    def get_domain(self, url=""):
        domain = url[0].replace("http://", '')
        domain = domain.replace("https://", '')
        domain = domain.split("/")
        return domain[0]

    def get_words(self, string=""):
        
        #remove non alpha content
        regex = re.sub(r"[^a-z\s]+", "", string.lower())
        regex = re.sub(r'[^\x00-\x7f]',r'', regex)
        words = re.sub(r"[^\w]", " ",  string).split()
        
        return words

    def extract_emojis(self, string=""):
        emj = []
        for c in string:
            if c in emoji.UNICODE_EMOJI:
                emj.append(c)
        return emj

    def is_event(self, body=""):
        """Detect wether the body of chat is event log.
        If the body if an event, it won't be count and the body of the message will not analized

        Event log means note of event.
        Below are known event log patterns in difference language
        - Group created
        - User joining group
        - User left group
        - Adding group member
        - Removing group member
        - Security code changed
        - Phone number changed
        -

        Feel free to add similar pattern for other known pattern or language

        Keyword arguments:
        body -- body of exported chat

        The Rule is:
        Match the known event message
        """
        pattern_event = [
            # Welcoming message
            r"Messages to this group are now secured with end-to-end encryption\.$",  # EN
            # User created group
            r".+\screated this group$",  # EN
            # User left group
            r".+\sleft$",  # EN
            r".+\skeluar$",  # ID
            # User join group via inviation link
            r".+\sjoined using this group's invite link$",  # EN
            r".+\stelah bergabung menggunakan tautan undangan grup ini$",  # ID
            # Admin adds member
            r".+\sadded\s.+",  # EN
            r".+\smenambahkan\s.+",  # ID
            # Admin removes member
            r".+\sremoved\s.+",  # EN
            # Member's security code changed
            r".+'s security code changed\.$",  # EN
            # Member changes phone number
            r".*changed their phone number to a new number. Tap to message or add the new number\.$"  # EN
            r".*telah mengganti nomor teleponnya ke nomor baru. Ketuk untuk mengirim pesan atau menambahkan nomor baru\.$",  # ID
        ]

        for p in pattern_event:
            match = re.match(p, body)
            if match:
                return match
        return None

    def parse_line(self, line=""):
        line = self.replace_bad_character(line)
        # Check wether the line is starting line or following line
        starting_line = self.is_starting_line(line)

        if starting_line:
            # Set startingline
            self.is_startingline = True

            # Extract timestamp
            dt = self.extract_timestamp(starting_line.group(2).replace(".", ":"))
            # Set timestamp
            if dt:
                self.timestamp = dt

            # Body of the chat separated from timestamp
            body = starting_line.group(18)
            self.parse_body(body)

        else:
            # The line is following line
            # Set following
            self.is_followingline = True

            # Check if previous line has sender
            if self.previous_line and self.previous_line.sender:
                # Set current line sender, timestamp same to previous line
                self.sender = self.previous_line.sender
                self.timestamp = self.previous_line.timestamp
                self.line_type = "Chat"

            body = line
            self.body = line
            self.parse_body(body, following=True)

    def parse_body(self, body="", following=False):
        # Check wether the starting line is a chat or an event
        chat = self.is_chat(body)

        if chat or following:
            # Set line type, sender and body
            self.line_type = "Chat"
            message_body = body
            if not following:
                self.sender = chat.group(1)
                message_body = chat.group(3)

            self.body = message_body

            has_attachment = self.contains_attachment(message_body)
            
            if has_attachment:
                # Set chat type to attachment
                self.line_type = "Attachment"
                
            else:
                if self.is_deleted(message_body):
                    # Set deleted
                    self.is_deleted_chat = True
                else:
                    words = message_body

                    #URL & Domain
                    urls = self.extract_url(message_body)
                    if urls:
                        for i in urls:
                            # Exclude url from words
                            words = words.replace(i[0], "")

                            # Set domains
                            self.domains.append(self.get_domain(i))
                    
                    # Set Words
                    self.words = self.get_words(words)

                    #Emoji
                    emjs = self.extract_emojis(message_body)
                    if emjs:
                        self.emojis = emjs

        elif self.is_event(body):
            # Set line_type
            self.line_type = "Event"
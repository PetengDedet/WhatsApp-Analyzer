# -*- coding: utf-8 -*-
import re
from dateutil import parser
import emoji
import patterns

# TODO: Classify attachment

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
        line = line.strip()
        for x in patterns.BAD_CHARS:
            line = line.replace(x, "")

        return line

    def is_starting_line(self, line=""):
        """
        Starting line mean a line that started with date time.
        Because there are multiline chat. I called it following line.
        A starting line must be classified before it's data being extracted.

        The Rule is:
        <datetime><separator><contact/phone number>
        """
        match = re.match(re.compile(patterns.IS_STARTING_LINE, re.VERBOSE), line)
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
        match = re.match(re.compile(patterns.IS_CHAT, re.VERBOSE), body)
        if match:
            return match

        return None

    def is_deleted(self, body=""):
        """
        Deleted message
        """
        for p in patterns.IS_DELETED_CHAT:
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
        for p in patterns.IS_ATTACHMENT:
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
        return re.findall(patterns.IS_URL, body)

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
        return [c["emoji"] for c in emoji.emoji_list(string)]

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
        for p in patterns.IS_EVENT:
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
            dt = self.extract_timestamp(starting_line.group(2))
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

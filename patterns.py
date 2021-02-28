BAD_CHARS = [
    u"\u202a",
    u"\u200e",
    u"\u202c",
    u"\xa0",
]

IS_STARTING_LINE = r"""
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
    (\s?[apAP]\.?[mM]\.?)?))  #Zero or one of ('space', 'A' or 'P', and 'M'
    (\]?\s-?\s?\s?)#Zero or one close square bracket ']', Zero or one (space and '-'), zero or one space
    (.+)        #One or more character of chat member phone number or contact name
"""

IS_CHAT = r"""
    ([^:]+)#Chat member
    (:)   #Colon separator
    (.+)  #One or more charachter of message content
"""

IS_DELETED_CHAT = [
    r".*This message was deleted$",
    r".*Pesan ini telah dihapus$"
]

IS_ATTACHMENT = [
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
    r".*video omitido*",
]


IS_URL = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,6}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"

IS_EVENT = [
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



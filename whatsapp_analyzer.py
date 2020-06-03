#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import io
import sys
from collections import Counter
import emoji

# imported from current directory
from chatline import Chatline
from font_color import Color


"""
CLI Set
"""
parser = argparse.ArgumentParser(
    description='Read and analyze whatsapp chat',
    usage="python whatsapp_analyzer.py FILE [-h] [-d] [-s] [-c]"
)

stop_words_options = [ "arabic","bulgarian","catalan","czech","danish","dutch","english","finnish","french","german","hebrew","hindi","hungarian","indonesian","italian","malaysian","norwegian","polish","portuguese","romanian","russian","slovak","spanish","swedish","turkish","ukrainian","vietnamese"]

parser.add_argument('file', 
    metavar='FILE',
    help='Chat file path')

parser.add_argument(
    '-d', 
    '--debug', 
    required=False, 
    help="Debug mode. Shows details for every parsed line.", action="store_true")

parser.add_argument(
    '-s', 
    '--stopword', 
    required=False, 
    choices=stop_words_options,  
    metavar='',
    help="Stop Words: A stop word is a commonly used word (such as 'the', 'a', 'an', 'in').\
        In order to get insightful most common word mentioned in the chat, we need to skip these type of word.\
        The Allowed values are: " + ", ".join(stop_words_options))

parser.add_argument(
    '-c', 
    '--customstopword', 
    required=False, 
    metavar='',
    help="Custom Stop Words. File path to stop word. File must a raw text. One word for every line"
)

args = parser.parse_args()

"""
READ FILE
"""
try:
    with io.open(args.file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
except IOError as e:
    print("File \"" + args.file + "\" not found. Please recheck your file location")
    sys.exit()

stop_words = []
if args.stopword:
    try:
        with io.open("stop-words/" + args.stopword + ".txt", "r", encoding="utf-8") as file:
            stop_words = [x.strip() for x in file.readlines()]
    except IOError as e:
        print("Stop Words file not found in \"" + args.file + "\" not found.")
        sys.exit()


if args.customstopword:
    try:
        with io.open(args.customstopword, "r", encoding="utf-8") as file:
            stop_words = [x.strip() for x in file.readlines()]
    except IOError as e:
        print("Stop Words file not found in \"" + args.file + "\" not found.")
        sys.exit()
        
"""
PARSING AND COUNTING
"""
chat_counter = {
    'chat_count': 0,
    'deleted_chat_count': 0,
    'event_count': 0,
    'senders': [],
    'timestamps': [],
    'words': [],
    'domains': [],
    'emojis': [],
    'fav_emoji': [],
    'fav_word': []
}


previous_line = None
for line in lines:
    chatline = Chatline(line=line, previous_line=previous_line, debug=args.debug)
    previous_line = chatline

    # Counter
    if chatline.line_type == 'Chat':
        chat_counter['chat_count'] += 1

    if chatline.line_type == 'Event':
        chat_counter['event_count'] += 1

    if chatline.is_deleted_chat:
        chat_counter['deleted_chat_count'] += 1

    if chatline.sender is not None:
        chat_counter['senders'].append(chatline.sender)
        for i in chatline.emojis:
            chat_counter['fav_emoji'].append((chatline.sender, i))
        
        for i in chatline.words:
            chat_counter['fav_word'].append((chatline.sender, i))

    if chatline.timestamp:
        chat_counter['timestamps'].append(chatline.timestamp)

    if len(chatline.words) > 0:
        chat_counter['words'].extend(chatline.words)

    if len(chatline.emojis) > 0:
        chat_counter['emojis'].extend(chatline.emojis)

    if len(chatline.domains) > 0:
        chat_counter['domains'].extend(chatline.domains)


"""
REDUCE AND ORDER DATA
"""

def reduce_and_sort(data):
    return sorted(
        dict(
            zip(
                Counter(data).keys(), 
                Counter(data).values()
            )
        ).items(), 
        key=lambda x: x[1],
        reverse=True
    )

def reduce_and_filter_words(list_of_words):
    val = [w.lower() for w in list_of_words if (len(w) > 1) and (w.isalnum()) and (not w.isnumeric()) and (w.lower() not in stop_words)]
    return val

def filter_single_word(w):
    return (len(w) > 1) and (w.isalnum()) and (not w.isnumeric()) and (w.lower() not in stop_words)

def reduce_fav_item(data):
    exist = []
    arr = []
    for i in data:
        if i[1] > 0 and not i[0][0] in exist:
            exist.append(i[0][0])
            arr.append(i)
    return arr
    
chat_counter['senders'] = reduce_and_sort(chat_counter['senders'])
chat_counter['words'] = reduce_and_sort(reduce_and_filter_words(chat_counter['words']))
chat_counter['domains'] = reduce_and_sort(chat_counter['domains'])
chat_counter['emojis'] = reduce_and_sort(chat_counter['emojis'])
chat_counter['timestamps'] = reduce_and_sort([(x.strftime('%A'), x.strftime('%H')) for x in chat_counter['timestamps']])
chat_counter['fav_emoji'] = reduce_fav_item(reduce_and_sort(chat_counter['fav_emoji']))
chat_counter['fav_word'] = reduce_fav_item(reduce_and_sort([x for x in chat_counter['fav_word'] if filter_single_word(x[1])]))

"""
VISUALIZE
"""
def printBar (value, total, label = '', prefix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    filledLength = int(value / (total / length))
    bar = fill * filledLength + '' * (length - filledLength)
    print("\r{} |{} {}".format(label, bar, Color.bold(str(value))), end = printEnd)
    print()

def printBarChart(data, fill="█"):
    if len(data) <= 0:
        print("Empty data")
        return
    
    total = max([x[1] for x in data])
    max_label_length = len(sorted(data, key=lambda tup: len(tup[0]), reverse=True)[0][0])
    for i in data:
        label = i[0] + " " * (max_label_length - len(i[0]))
        printBar(i[1], total, length=50, fill=fill, label=label)

def printCalendar(data):
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = ['0' + str(x) if len(str(x)) < 2 else str(x) for x in range(24)]

    max_val = float(data[max(data, key=data.get)]) if len(data) else 0

    ticks = [
        0,
        0.25 * max_val,
        0.50 * max_val,
        0.75 * max_val,
    ]

    sys.stdout.write("     ")
    for day in days:
        sys.stdout.write('\t[' + day[:3] + "]")
        
    sys.stdout.write('\n')

    for hour in hours:
        sys.stdout.write("[" + hour + ':00]')
        
        for day in days:
            
            dict_key = (day, hour)
            
            if dict_key in data:
                # tick = str(ct[dict_key])
                
                if data[dict_key] > ticks[3]:
                    tick = Color.custom("███", bold=True, fg_red=True)
                elif data[dict_key] > ticks[2]:
                    tick = Color.custom("▓▓▓", bold=True, fg_orange=True)
                elif data[dict_key] > ticks[1]:
                    tick = Color.custom("▒▒▒", bold=True, fg_green=True)
                else:
                    tick = Color.custom("░░░", bold=True, fg_light_grey=True)
            else:
                tick = Color.custom('===', bold=False, fg_white=True)
            
            sys.stdout.write('\t ' + tick)
        sys.stdout.write('\n')


# Senders
data = chat_counter['senders']
print(Color.red("-" * 50))
print(Color.red("Chat Count by Sender"))
print(Color.red("-" * 50))
print("Active Sender\t:", Color.red("{}".format(len(data))))
print("Total Chat\t:", Color.red("{}".format(sum([x[1] for x in data]))))
print("Average \t:", Color.red("{:.1f} chat per member".format((sum([x[1] for x in data]) / len(data)) if len(data) else 0)))
print()
printBarChart(data[:20], fill=Color.red("█"))
if len(data) > 20:
    print("---")
    print("Other from {} member | {}".format(Color.red(str(len(data[20:]))), Color.red(str(sum([x[1] for x in data[20:]])))))
print()
print()

# Domains
data = chat_counter['domains']
print(Color.blue("-" * 50))
print(Color.blue("Mentioned Domain (Shared Link/URL)"))
print(Color.blue("-" * 50))
print("Domain Count\t: ", Color.blue(str(len(data))))
print("Mention Count\t: ", Color.blue(str(sum([x[1] for x in data]))))
print()
printBarChart(data[:20], fill=Color.blue("█"))
if len(data) > 20:
    print("---")
    print("Other {} domain | {}".format(Color.blue(str(len(data[20:]))), Color.blue(str(sum([x[1] for x in data[20:]])))))
print()
print()


# Emojis
data = [(x[0] + " (" + emoji.demojize(x[0]) + ") ", x[1]) for x in chat_counter['emojis']]
print(Color.orange("-" * 50))
print(Color.orange("Used Emoji"))
print(Color.orange("-" * 50))
print("Unique Emoji\t: ", Color.orange(str(len(data))))
print("Total Count\t: ", Color.orange(str(sum([x[1] for x in data]))))
print()
printBarChart(data[:20], fill=Color.orange("█"))
if len(data) > 20:
    print("---")
    print("Other {} emoji | {}".format(Color.orange(str(len(data[20:]))), Color.orange(str(sum([x[1] for x in data[20:]])))))
print()
print()

# Fav Emojis
data = [(x[0][0] + " | " + x[0][1] + " | (" + emoji.demojize(x[0][1]) + ")", x[1]) for x in chat_counter['fav_emoji']]
print(Color.orange("-" * 50))
print(Color.orange("Favorite Emoji by Member"))
print(Color.orange("-" * 50))
print()
printBarChart(data[:20], fill=Color.orange("█"))
print()
print()

# Words
data = chat_counter['words']
print(Color.green("-" * 50))
print(Color.green("Used Word"))
print(Color.green("-" * 50))
print("Unique Word\t: ", Color.green(str(len(data))))
print("Total Count\t: ", Color.green(str(sum([x[1] for x in data]))))
print()
printBarChart(data[:20], fill=Color.green("█"))
if len(data) > 20:
    print("---")
    print("Other {} word | {}".format(Color.green(str(len(data[20:]))), Color.green(str(sum([x[1] for x in data[20:]])))))
print()
print()

# Fav Word
data = [(x[0][0] + " | " + x[0][1] + " | ", x[1]) for x in chat_counter['fav_word']]
print(Color.green("-" * 50))
print(Color.green("Favorite Word by Member"))
print(Color.green("-" * 50))
print()
printBarChart(data[:20], fill=Color.green("█"))
print()
print()

# Heatmap
data = chat_counter['timestamps']
print(Color.purple("-" * 50))
print(Color.purple("Chat Activity Heatmap"))
print(Color.purple("-" * 50))
if len(data) > 0:
    print("Most Busy\t: {}, at {} ({} chat)".format(
        Color.purple(str(data[0][0][0])), 
        Color.purple(str(data[0][0][1]) + ":00"), 
        Color.purple(str(data[0][1]))))
    print("Most Silence\t: {}, at {} ({} chat)".format(
        Color.purple(str(data[-1][0][0])), 
        Color.purple(str(data[-1][0][1]) + ":00"), 
        Color.purple(str(data[-1][1]))))
print()
print('---')
print('X: Days')
print('Y: Hours')
print('---')
print('Less [{}{}{}{}{}] More'.format(
    Color.custom("===", bold=False), 
    Color.custom("░░░", bold=True, fg_light_grey=True),
    Color.custom("▒▒▒", bold=True, fg_green=True),
    Color.custom("▓▓▓", bold=True, fg_orange=True),
    Color.custom("███", bold=True, fg_red=True)
))
print()
printCalendar(dict(data))
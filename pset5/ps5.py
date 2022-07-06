# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name: Amanda Wright
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime, timezone
import pytz
import re


#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory
class NewsStory(object):
    def __init__(self, guid, title, description, link, pubdate):
        """
        Parameters
        ----------
        guid : string
            A globally unique identifier for the news story.
        title : string
            Title of the news story.
        description : string
            A summarization of the news story.
        link : string
            A link to a website with the full news story.
        pubdate : datetime
            Date the news story was published.

        Returns
        -------
        None.

        """
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubdate = pubdate
        
    def get_guid(self):
        """
        Returns: self.guid
        """
        return self.guid
    
    def get_title(self):
        """
        Returns
        -------
        self.title
        """
        return self.title
    
    def get_description(self):
        """
        Returns
        -------
        self.description
        """
        return self.description

    def get_link(self):
        """
        Returns
        -------
        self.link

        """
        return self.link
    
    def get_pubdate(self):
        """
        Returns
        -------
        self.pubdate

        """
        return self.pubdate

#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    
    def __init__(self, phrase):
        Trigger.__init__(self)
        self.phrase = phrase
    
    def is_phrase_in(self, text):
        """
        Parameters
        ----------
        text : string

        Returns
        -------
        True if phrase is in text.
        False otherwise.
        """
        punctuation = string.punctuation
        clean_text = text.lower()
        for char in text:
            if char in punctuation:
                clean_text = ' '.join(clean_text.split(char))
                    
        clean_list = []
        for word in clean_text.split(' '):
            if word != '':
                clean_list.append(word)

        if re.search("\\b" + self.phrase.lower() + "\\b", ' '.join(clean_list)):
            return True
        else:
            return False
            

# Problem 3
# TODO: TitleTrigger
class TitleTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
        
    def evaluate(self, story: NewsStory) -> bool:
        """
        Parameters
        ----------
        story : NewsStory
            DESCRIPTION.

        Returns
        -------
        bool
            DESCRIPTION.

        """
        
        if not isinstance(story, NewsStory):
            raise ValueError
        
        if self.is_phrase_in(story.get_title()) == True: ## need to use title as the input 
            return True
        else:
            return False
# Problem 4
# TODO: DescriptionTrigger
class DescriptionTrigger(PhraseTrigger):
    def __init__(self, phrase):
        PhraseTrigger.__init__(self, phrase)
    
    def evaluate(self, story):
        """
        Parameters
        ----------
        story : NewsStory

        Returns
        -------
        True if phrase in story's description.
        False otherwise.
        """
        
        if self.is_phrase_in(story.get_description()) == True:
            return True
        else:
            False
            
# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.
class TimeTrigger(Trigger):
    def __init__(self, time):
        Trigger.__init__(self)
        time = datetime.strptime(time, "%d %b %Y %H:%M:%S")
        time = time.replace(tzinfo=pytz.timezone("EST"))        
        self.time = time
        
        
# Problem 6
# TODO: BeforeTrigger and AfterTrigger
class BeforeTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)
    
    def evaluate(self, story):
        """

        Parameters
        ----------
        story : NewsStory

        Returns
        -------
        True if story was published strictly before trigger's time.

        """
        if self.time > story.get_pubdate().replace(tzinfo=pytz.timezone("EST")):
            return True
        else:
            return False

class AfterTrigger(TimeTrigger):
    def __init__(self, time):
        TimeTrigger.__init__(self, time)
    
    def evaluate(self, story):
        if self.time < story.get_pubdate().replace(tzinfo=pytz.timezone("EST")):
            return True
        else:
            return False
        
# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger
class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trigger = trigger
        Trigger.__init__(self)
    
    def evaluate(self, story):
        if not self.trigger.evaluate(story):
            return True
        else:
            return False

# Problem 8
# TODO: AndTrigger
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        Trigger.__init__(self)
    
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)
            

# Problem 9
# TODO: OrTrigger
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        Trigger.__init__(self)
        
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)
    triggered_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                triggered_stories.append(story)
    return triggered_stories



#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    print(lines) # for now, print it so you see what it contains!
    trigger_dict = {}
    for line in lines:
        
        line_split = line.split(',')

        trigger_dict[line_split[0]] = line_split[1:]
        
    print(trigger_dict)
    
    for key in trigger_dict.keys():
        # print(trigger_dict[key])
        # print("key", key)
        # print(trigger_dict[key][0])
        if trigger_dict[key][0] == 'TITLE':
            trigger_dict[key] = TitleTrigger(trigger_dict[key][1])
        elif trigger_dict[key][0] == 'DESCRIPTION':
            trigger_dict[key] = DescriptionTrigger(trigger_dict[key][1])
        elif trigger_dict[key][0] == 'BEFORE':
            trigger_dict[key] = BeforeTrigger(trigger_dict[key][1])
        elif trigger_dict[key][0] == 'AFTER':
            trigger_dict[key] = AfterTrigger(trigger_dict[key][1])
        elif trigger_dict[key][0] == 'AND':
            trigger_dict[key] = AndTrigger(trigger_dict[trigger_dict[key][1]], trigger_dict[trigger_dict[key][2]])
        elif trigger_dict[key][0] == 'NOT':
            trigger_dict[key] = NotTrigger(trigger_dict[trigger_dict[key][1]], trigger_dict[trigger_dict[key][2]])
        elif trigger_dict[key][0] == 'OR':
            trigger_dict[key] = OrTrigger(trigger_dict[trigger_dict[key][1]], trigger_dict[trigger_dict[key][2]])
            
        if key == 'ADD':
            triggerlist = []
            for value in range(len(trigger_dict['ADD'])):
                triggerlist.append(trigger_dict[trigger_dict['ADD'][value]])
            return triggerlist
            
SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("Biden")
        t2 = DescriptionTrigger("Congress")
        t3 = DescriptionTrigger("infrastructure")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            # stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    root = Tk()
    root.title("Some RSS parser")
    t = threading.Thread(target=main_thread, args=(root,))
    t.start()
    root.mainloop()


import re
import datetime

# it is OK to not pass in a name
def form_spam(name,message,date_string):

    # set False as default
    is_spam = False
    spam_reason = 'Not Spam'
    spam_notes = ''

    # the quickest way to rule out spam is the submit diff
    # spam is always too fast
    submit_diff = is_submit_diff_spam(date_string)

    if submit_diff['is_spam']:
        is_spam = True
        spam_reason = submit_diff['spam_reason']

    # if there was no submit diff spam and a name exists
    if not is_spam and name:

        name_spam = is_name_spam(name)

        if name_spam['is_spam']:
            is_spam = True
            spam_reason = name_spam['spam_reason']
            spam_notes = name_spam['spam_notes']

    # if there is still no spam, check the message

    # first, remove all of the links from the message
    message = remove_message_links(message)

    message_spam = is_message_spam(message)

    if message_spam['is_spam']:

        is_spam = True
        spam_reason = message_spam['spam_reason']
        spam_notes = message_spam['spam_notes']


    spam_obj = {
        'is_spam': is_spam,
        'spam_reason': spam_reason,
        'spam_notes': spam_notes
    }

    return spam_obj


def spam_keywords():

    # a list of keywords that are mostly spam
    words = ['profit','USD','domains','spam','euros','lottery','adsense','cialis','penis','viagra','casino','porn','pussy','anal','racist','t.cn','ascialis.com','questionnaire','resurge','prescription','medications','vaginitis','pharmacy','impotence','erectile','urinary','cholesterol','corticosteroids','testosterone','youtube.com','seo','teen','galleries','filipina','russian','hacking','ransomware','webmaster','optimizing','backlink','audit','sexuality','sexual','freepornsex','software','backlinks','profitable','unsubscribe','seo','advertise','competitors','clients ']

    return words

def is_name_spam(name):

    # start with false by default
    is_spam = False
    spam_reason = 'Not Spam'
    spam_notes = ''

    # spammers are entering their names in CamelCase
    camel_name = re.search('[A-Z][a-z]+[A-Z][a-z]+', name)

    if camel_name:
        is_spam = True
        spam_reason = 'Camel Case Name'
        spam_notes = name

    # temp solution to the Crytoesold issue
    # I need to create a better SPAM filter
    if name.startswith('Crytoesold'):
        is_spam = True
        spam_reason = 'Crytoesold'
        spam_notes = name

    spam_obj = {
        'is_spam': is_spam,
        'spam_reason': spam_reason,
        'spam_notes': spam_notes
    }

    return spam_obj

def is_submit_diff_spam(date_string):

    # create a datetime object from the posted date so we can
    # check to see how quickly the form was posted
    try:
        date_string_split = date_string.split(':')

        # piece the date back together
        date = datetime.datetime(
            int(date_string_split[0]),
            int(date_string_split[1]),
            int(date_string_split[2]),
            int(date_string_split[3]),
            int(date_string_split[4]),
            int(date_string_split[5]),
            int(date_string_split[6]),
        )

    # if the above fails, use the current date and time
    except:
        date = datetime.datetime.now()

    # create a time difference between the form time and now
    try:
        now = datetime.datetime.now()
        diff = (now-date).total_seconds()

    except:
        diff = 0

    # if a bot filled this out, it can happen quick
    # it's a short form and some people autocomplete their info
    # so it can't be too long. start here.
    if diff < 6: #6 seconds
        is_spam = True
        spam_reason = 'too fast (' + str(round(diff)) + ' secs)'

    # if the form was cached on their server for a while
    # the time difference could be a long time
    elif diff > 600: #10 minutes
        is_spam = True
        spam_reason = 'too slow (' + str(round(diff)) + ' secs)'

    else:
        is_spam = False
        spam_reason = 'not spam (' + str(round(diff)) + ' secs)'

    spam_obj = {
        'is_spam': is_spam,
        'spam_reason': spam_reason
    }

    return spam_obj

def is_message_spam(message):

    # False by default
    is_spam = False
    spam_reason = 'Not Spam'
    spam_notes = ''

    # split the message up by spaces
    message_split = message.split(' ')

    # start with a simple message length
    # most SPAM has a lot of words in it
    if len(message_split) > 100:
        is_spam = True
        spam_reason = 'Message too long (' + str(len(message_split)) + ')'

    # if it's already been determined as SPAM, there is no need to
    # loop each word looking for spam, we know it's SPAM
    if not is_spam:

        # get a list of spam words
        keyword_list = spam_keywords()

        # create a starting count and word list
        # the word list is so we can see which words triggered it
        spam_word_count = 0
        spam_word_list = []

        # loop through the spam words and see if they are in the message
        for word in message_split:

            # if the word is in the keyword_list
            if word.lower() in keyword_list:

                # increment the spam count
                spam_word_count += 1

                # increment the spam_word_list
                spam_word_list.append(word.lower())

        # adjust as needed
        if spam_word_count > 2:

            is_spam = True
            spam_reason = 'Spam Word Count (' + str(spam_word_count) + ')'
            spam_notes = spam_word_list

    spam_obj = {
        'is_spam': is_spam,
        'spam_reason': spam_reason,
        'spam_notes': spam_notes
    }

    return spam_obj

def remove_message_links(message):

    suffix_list = [
        '.com',
        '.net',
        '.org',
        '.mil',
    ]

    # replace http and https with a link tag
    # leave spaces so the spam checker can still find spam words in the url
    message = message.replace('https:',' [link] ')
    message = message.replace('http:',' [link] ')

    # replace popular suffixes
    for s in suffix_list:

        if s in message:
            # remove the dot and put and wrap the suffix
            # leave spaces for same reason as above
            message = message.replace(s,' [' + s[1:] + '] ')


    # remove these
    message = message.replace('www.','')
    message = message.replace('<a href="','')
    message = message.replace('">','')
    message = message.replace('</a>','')
    message = message.replace('//','')

    # we also need to remove commas and periods so words are judged on their own
    message = message.replace(',',' ')
    message = message.replace('.',' ')

    return message

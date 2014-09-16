import re
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def craft_message(username, feed, entry):
    # Might wanna get into timezones later:
    #pd = entry.published_parsed
    #parsed_date = datetime.datetime(year=pd.tm_year, month=pd.tm_mon, 
    #                                day=pd.tm_mday, hour=pd.tm_hour, 
    #                                minute=pd.tm_min, second=pd.tm_sec)
    parsed_date = time.mktime(entry.published_parsed)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = entry.title
    msg['From'] = 'shalala@example.com'
    msg['To'] = username
    msg['Date'] = entry.published
    hheader = '<table border="1" width="100%" cellpadding="0" ' + \
            'cellspacing="0" borderspacing="0"><tr><td>' + \
            '<table width="100%" bgcolor="#EDEDED" cellpadding="4" ' + \
            'cellspacing="2"><tr><td align="right"><b>Feed:</b></td> ' + \
            '<td width="100%"><a href="' + feed.link + '">' + \
            '<b>' + feed.title + '</b></a></td></tr><tr>' + \
            '<td align="right"><b>Item:</b></td><td width="100%">' + \
            '<a href="' + entry.link + '"><b>' + entry.title + '</b>' + \
            '</a></td></tr></table></td></tr></table><br/>'
    hfooter = '<hr width="100%"/><table width="100%" cellpadding="0" ' + \
        'cellspacing="0"><tr><td align="right"><font color="#ababab">' + \
        'Date:</font>&nbsp</td><td><font color="#ababab">' + \
        entry.published + '</font></td></tr></table>'
    html = hheader + entry.summary + hfooter
    theader = '<' + entry.link + '><br/><br/>'
    tfooter = '[A]<br/><br/>[A] ' + entry.link + '<br/>--<br/>Feed: ' + feed.title + \
            '<' + feed.link + '><br/>Item: ' + entry.title + '<br/><' + \
            entry.link + '><br/>Date: ' + entry.published
    text = theader + striphtml(html) + tfooter
    
    #Don't specify the charset until we know what we're doing
    #part1 = MIMEText(text, 'plain', _charset='utf-8')
    #part2 = MIMEText(html, 'html', _charset='utf-8')
    
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')
    msg.attach(part1)
    msg.attach(part2)
    
    return msg
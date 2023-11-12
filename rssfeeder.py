# Generate an RSS feed from a list of files

import os, toml, time
from ftplib import FTP

# read config
config = toml.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.toml'))
server = config['server']
username = config['username']
password = config['password']
directory = config['directory']
source = config['source']

# prepare xml parts
def xmlparser(title, link, description):
    start = f'''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd"  xmlns:content="http://purl.org/rss/1.0/modules/content/">
<channel>
    <title>{title}</title>
    <link>{link}</link>
    <description>{description}</description>
    <language>"en-us"</language>
    <image>
	    <url>https://rss.guillermohidalgogadea.com/logo.png</url>
	    <title>Logo</title>
	    <link>https://GuillermoHidalgoGadea.com</link>
    </image>'''
    end = '''
</channel>
</rss>
    '''
    return start, end

def xmlitem(title, link, description, size, date):
    item = f'''
    <item>
        <title>{title}</title>
        <enclosure url = "{link}" length="{size}" type="video/mpeg" />
        <link>{link}</link>
        <pubDate>{date} GMT</pubDate>
        <description>{description}</description>
    </item>'''
    return item

def getinfo(item):
    title = (' ').join(os.path.basename(item).split('.')[0].split('_'))
    link = 'https://'+item
    # TODO get more description from file
    description = f'This is a cool audiobook titled: {title}, enjoy!' 
    size = ftp.size(item)
    return title, link, description, size

# start server connection
ftp = FTP(server)
print(ftp.getwelcome())
loginRepsonse = ftp.login(username, password)
print(loginRepsonse)

# import new audiobooks from source
uploadcue = [os.path.join(source, file) for file in os.listdir(source) if 'mp3' in file]

for file in uploadcue:
    print(f'Uploading file "{os.path.basename(("_").join(file.split()))}" to ftp://{directory} ...')
    with open(file,'rb') as book:
        ftp.storbinary(f'STOR {os.path.join(directory, os.path.basename(("_").join(file.split())))}', book)

# list files on server
print("reading server content...")
audiobooks = [file for file in ftp.nlst(directory) if 'mp3' in file]
print(f"Found {len(audiobooks)} audiobooks!")
ftp.sendcmd("TYPE i")

# prepare xml
title = 'My Audiobooks'
link = 'https://GuillermoHidalgoGadea.com'
description = 'RSS feed to my self-hosted Audiobooks'
# TODO get creation date instead
date = time.strftime("%a, %d %b %Y %I:%M:%S", time.gmtime())
start, end = xmlparser(title, link, description)

# write rss feed as xml
print("writing xml feed...")
rss_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'RSS.xml')
with open(rss_file, 'w') as f:
    f.write(start)

    for item in audiobooks:
        title, link, description, size = getinfo(item)
        f.write(xmlitem(title, link, description, size, date))
    
    f.write(end)

htmlfeed = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'index.html')
with open(htmlfeed, 'w') as f:
    f.write(start)

    for item in audiobooks:
        title, link, description, size = getinfo(item)
        f.write(xmlitem(title, link, description, size, date))
    
    f.write(end)

# upload feed and quit connection
ftp.sendcmd("TYPE a")
with open(htmlfeed,'rb') as feed:
    ftp.storbinary(f'STOR {directory}/index.html', feed)

ftp.quit()
print("RSS feed updated!")

f = open(htmlfeed, 'r')
print(f.read())
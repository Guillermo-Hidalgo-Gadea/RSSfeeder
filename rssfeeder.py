# Generate an RSS feed from a list of files

import os, toml
from ftplib import FTP

# read config
config = toml.load('config.toml')
server = config['server']
username = config['username']
password = config['password']
directory = config['directory']
source = config['source']

# prepare xml parts
def xmlparser(title, link, description):
    start = f'''
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>{title}</title>
  <link>{link}</link>
  <description>{description}</description>
'''
    end = '''
</channel>
</rss>
    '''
    return start, end

def xmlitem(title, link, description):
    item = f'''
    <item>
        <title>{title}</title>
        <link>{link}</link>
        <description>{description}</description>
    </item>'''
    return item

def getinfo(item):
    title = (' ').join(os.path.basename(item).split('.')[0].split('_'))
    link = 'https://'+item
    # TODO get more description from file
    description = f'This is a cool audiobook titled: {title}, enjoy!' 
    return title, link, description

# start server connection
ftp = FTP(server)
ftp.login(username, password)

# import new audiobooks from source
uploadcue = [os.path.join(source, file) for file in os.listdir(source) if 'mp3' in file]

for file in uploadcue:
    print(f'Uploading file "{os.path.basename(("_").join(file.split()))}" to ftp://{directory} ...')
    with open(file,'rb') as book:
        ftp.storbinary(f'STOR {os.path.join(directory, os.path.basename(("_").join(file.split())))}', book)

# list files on server
audiobooks = [file for file in ftp.nlst(directory) if 'mp3' in file]

# prepare xml
title = 'My self-hosted Audiobooks'
link = 'https://GuillermoHidalgoGadea.com'
description = 'RSS feed to my self-hosted Audiobooks'

start, end = xmlparser(title, link, description)

# write rss feed as xml
with open('RSS.xml', 'w') as f:
    f.write(start)

    for item in audiobooks:
        title, link, description = getinfo(item)
        f.write(xmlitem(title, link, description))
    
    f.write(end)

# upload feed and quit connection
with open('RSS.xml','rb') as feed:
    ftp.storbinary(f'STOR {directory}/index.html', feed)

ftp.quit()

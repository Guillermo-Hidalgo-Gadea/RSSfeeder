# Generate an RSS feed from a list of files

import os, toml
from ftplib import FTP

# read config
config = toml.load('config.toml')
server = config['server']
username = config['username']
password = config['password']
directory = config['directory']

# start server connection
ftp = FTP(server)
ftp.login(username, password)

# list files on server
files = ftp.nlst(directory)
audiobooks = [file for file in files if 'mp3' in file]


# write xml on server
with open('RSS.xml', 'w') as f:
    f.write('''<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>My self-hosted Audiobooks</title>
  <link>https://GuillermoHidalgoGadea.com</link>
  <description>RSS feed to my self-hosted Audiobooks</description>
''')

    for item in audiobooks:
        title = os.path.basename(item)
        link = 'https://'+item
        description = 'This is a cool audiobook'

        f.write(f'''<item>
    <title>{title}</title>
    <link>{link}</link>
    <description>{description}</description>
    </item>
    ''')
    f.write('''</channel>
</rss>
    ''')

# upload feed and quit connection
with open('RSS.xml','rb') as feed:
    ftp.storbinary(f'STOR {directory}/RSS.xml', feed)

ftp.quit()
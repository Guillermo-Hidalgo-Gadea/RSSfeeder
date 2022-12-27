# RSSfeeder

Generate RSS feeds from a list of files in python.

I want to host all of my Audiobooks, maybe even some music on a server, but sharing these files via platform specific shared links is not particularly elegant, especially if accessing from mobile.

Instead, I generate an `RSS.xml` feed with the file links to listen to them from my podcast app:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">

<channel>
  <title>My Audiobooks</title>
  <link>https://rss.GuillermoHidalgoGadea.com</link>
  <description>RSS feed to all my Audiobooks</description>
  <item>
    <title>Fooled by Randomness</title>
    <link>https://testguillermo.com/audiobooks/Fooled%20by%20Randomness.mp3</link>
    <description>This is a cool audiobook</description>
  </item>
</channel>

</rss>
```
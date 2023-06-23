# Youtube channel/playlist to an audio podcast RSS feed
A rudimentary python script to generate an audio podcast feed from a Youtube channel leveraging yt-dlp.

Dumps the output into the specified directories set in `options.json`:

	{
		"BASEPATH": "/var/www/html/name_feed",
		"PUBLICURL": "https://web.site/name_feed/",
		"REMOVE_WORDS": ["common words in the titles to remove", "totally optional"],
		"CHANNELID": "channel ID/playlist ID/anything yt-dlp recognizes as a list of videos",
		"matchtitle": "(optionalregextomatchtitles|egPodcast)",
		"download_archive": "downloaded.txt",
		"format": "bestaudio/best",
		"postprocessors": [{
			"key": "FFmpegExtractAudio",
			"preferredcodec": "mp3",
			"preferredquality": "256"
		}],
		"playlistend": 10,
		"outtmpl": "%(upload_date>[%Y%m%d])s %(title)s.%(ext)s"
	}

Modify the contents of `podcasttemplate.rss` to match your target output:

	<rss version="2.0">
	    <channel>
	        <title>Podcast Name (RSS)</title>
	        <description>Podcast description</description>
	        <image>
	            <link>https://web.site/podcastname/</link>
	            <title>Podcast Name (RSS)</title>
	            <url>https://web.site/podcastname/icon.jpg</url>
	        </image>
	        <link>https://web.site/podcastname/</link>
	    </channel>
	</rss>

The `<image>` URL should point to an icon image, as that is what most podcast readers will display.

## Example

`podcasttemplate.rss`

	<rss version="2.0">
	    <channel>
	        <title>Level1 News (RSS)</title>
	        <description>Level1 News - ripped from youtube.</description>
	        <image>
	            <link>https://web.site/level1/</link>
	            <title>Level1 News (RSS)</title>
	            <url>https://web.site/level1/icon.jpg</url>
	        </image>
	        <link>https://web.site/level1/</link>
	    </channel>
	</rss>

`options.json`

	{
		"BASEPATH": "/var/www/html/level1",
		"PUBLICURL": "https://web.site/level1/",
		"REMOVE_WORDS": ["The Level1 Show", "Level1"],
		"CHANNELID": "UU4w1YQAJMWOz4qtxinq55LQ",
		"matchtitle": "(Level1 Show|202)",
		"download_archive": "downloaded.txt",
		"format": "bestaudio/best",
		"postprocessors": [{
			"key": "FFmpegExtractAudio",
			"preferredcodec": "mp3",
			"preferredquality": "256"
		}],
		"playlistend": 10,
		"outtmpl": "%(upload_date>[%Y%m%d])s %(title)s.%(ext)s"
	}

Result as displayed in my podcast app of choice:

![example](example.png)

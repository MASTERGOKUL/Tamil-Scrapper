# Tamil Scraper
### A Web Scraping  tool for Tamil

This tool can be helpful to scrap the content on the websites easily, 
in which the data can be used for dataset creation or some NLP tasks

### Installing 
Required 🐍 Python version >= 3.8

```
pip install tamilscraper
```

### How to use it ?:
#### creating object
```commandline
from tamilscraper import TamilScraper
scraped_content = TamilScraper('https://www.projectmadurai.org/pm_etexts/utf8/pmuni0001.html')
```

This tool can give the data in 4 ways
1. Tamil text which present inside a tag(may contain Non-Tamil character)
2. Only Tamil text in the full webpage
3. Only Non-Tamil text or characters on the webpage
4. Tables on the website which got any Tamil characters(may contain non-tamil character)

### 1. Tamil text which present inside a tag

The below function gives the Tamil text in any of the HTML tags on the page.
```commandline
tamil_text = scraped_content.get_text()
```
Sample Output:
```commandline
['\nதிருவள்ளுவர் அருளிய திருக்குறள்   ', 'திருக்குறள்', '\n1.  அறத்துப்பால்', '\n1.1  கடவுள் வாழ்த்து ', '\n1.1.1   கடவுள் வாழ்த்து ', '\nஅகர முதல' ...]
```
The below function gives the Tamil text in a **particular**  HTML tags on the page.
```commandline
tamil_text = scraped_content.get_by_tag('h3')
```
Sample Output:
```commandline
['1.  அறத்துப்பால்1.1  கடவுள் வாழ்த்து', '1.1.2   வான்சிறப்பு', '1.1.3.  நீத்தார் பெருமை',...]
```

### 2. Only Tamil text in the webpage
By making the parameter **only_tamil=True**, you can get only tamil text(words) in a line(tag), as a list of lines
```commandline
tamil_text = scraped_content.get_text(only_tamil=True)
tamil_text = scraped_content.get_by_tag('h1',only_tamil=True)
```
Sample Output:
```commandline
[['திருவள்ளுவர்', 'அருளிய', 'திருக்குறள்'], ['திருக்குறள்'], ['அறத்துப்பால்'], ['கடவுள்', 'வாழ்த்து'], ['கடவுள்', 'வாழ்த்து']...]
```

### 3. Only Non-Tamil characters in the webpage
By making the parameter **only_other=True**, you can get only tamil text(words) in a line(tag), as a list of lines
```commandline
tamil_text = scraped_content.get_text(only_other=True)
tamil_text = scraped_content.get_by_tag('h1',only_other=True)
```
Sample Output:
```commandline
[[' Project Madurai '], ['\n'], [' Copyright (c) 2000 All Rights Reserved '],...]
```

**NOTE** : You can't able to do 2 and 3 same time.<br>
Example:
```commandline
scraped_content.get_text(only_other=True,only_tamil=True) # not allowed ❌
```
### 4. Tables in the website which got any tamil characters
The below function gives you the list of tables in pandas.DataFrame structure that got tamil characters.
If a table got only one tamil character it will also include.
```commandline
tamil_text = scraped_content.get_table()
```
Sample Output:
```commandline
[                                                   0   1
0     அகர முதல எழுத்தெல்லாம் ஆதி பகவன் முதற்றே உலகு.   1
1  கற்றதனால் ஆய பயனென்கொல் வாலறிவன் நற்றாள் தொழாஅ...   2
2  மலர்மிசை ஏகினான் மாணடி சேர்ந்தார் நிலமிசை நீடு...   3
3  வேண்டுதல் வேண்டாமை இலானடி சேர்ந்தார்க்கு யாண்ட...   4
4  இருள்சேர் இருவினையும் சேரா இறைவன் பொருள்சேர் ப...   5
5  பொறிவாயில் ஐந்தவித்தான் பொய்தீர் ஒழுக்க நெறிநி...   6
6  தனக்குவமை இல்லாதான் தாள்சேர்ந்தார்க் கல்லால் ம...   7
7  அறவாழி அந்தணன் தாள்சேர்ந்தார்க் கல்லால் பிறவாழ...   8
8  கோளில் பொறியின் குணமிலவே எண்குணத்தான் தாளை வணங...   9
9  பிறவிப் பெருங்கடல் நீந்துவர் நீந்தார் இறைவன் அ...  10,
...]
```
### NOTE:
If the webpage is not allowed for webscraping, this tool cant able to get the data, so make sure the content to open to 
use

## 😊 Pull Requests are welcome...




# Tamil Scraper
### A Web Scraping tool for tamil

This tool can be helpful to scrap tamil the content in the websites easily, 
in which the data can be used for dataset creation or some NLP tasks

### Installing 
Required Python version >= 3.8

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
1. Tamil text which present inside a tag(may contain non-tamil character)
2. Only Tamil text in the full webpage
3. Only Non-Tamil text or characters in the webpage
4. Tables in the website which got any tamil characters(may contain non-tamil character)

### 1. Tamil text which present inside a tag

The below function gives the Tamil text in any of the HTML tags on the page.
```commandline
tamil_text = scraped_content.get_text()
```
Sample Output:
```commandline
['\ntamil_sentance', 'tamil_sentance', '\n1. tamil_sentance',... ]
```
The below function gives the Tamil text in a **particular**  HTML tags on the page.
```commandline
tamil_text = scraped_content.get_by_tag('h3')
```
Sample Output:
```commandline
['1.tamil_heading1.1 tamil_heading', '1.1.2 tamil_heading', '1.1.3.tamil_heading',...]
```

### 2. Only Tamil text in the webpage
By making the parameter **only_tamil=True**, you can get only tamil text(words) in a line(tag), as a list of lines
```commandline
tamil_text = scraped_content.get_text(only_tamil=True)
tamil_text = scraped_content.get_by_tag('h1',only_tamil=True)
```
Sample Output:
```commandline
[['tamil-word', 'tamil-word', 'tamil-word'], ['tamil-word'], ['tamil-word'],...]
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
scraped_content.get_text(only_other=True,only_tamil=True) # not allowed
```
### 4. Tables in the website which got any tamil characters
The below function gives you the list of tables in pandas.DataFrame structure that got tamil characters.
If a table got only one tamil character it will also include.
```commandline
tamil_text = scraped_content.get_table()
```
Sample Output:
```commandline
[ Df_table 1, Df_table 2 ]
```
### NOTE:
If the webpage is not allowed for webscraping, this tool cant able to get the data, so make sure the content to open to 
use

Github Repository Link : https://github.com/MASTERGOKUL/Tamil-Scrapper




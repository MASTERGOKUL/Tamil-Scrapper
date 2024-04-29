import re
from urllib.error import HTTPError
import pandas
import requests
from bs4 import BeautifulSoup


def filter_non_tamil_text(texts: list) -> list[list]:
    """
    To get only the text which is not in tamil characters.
    which may useful for process the data later.

    Ex: [['non_tamil_word1'],
    ['non_tamil_word1', 'non_tamil_word2', 'non_tamil_word3']]


    it may include other language texts , symbols and delimiters like !@#$%^&*()_+{}[]:;"',./?\
    :param texts: extracted web content with other language texts (input may contain tamil text).
    :return: 2D array : which contains only non-tamil characters, each row contains text separated by words.
    """
    non_tamil_text = []
    for single_tag_text in texts:
        non_tamil_text_only = re.findall('[^ஂ-௺]+',
                                         single_tag_text)  # to find the text which contains non-tamil words
        non_tamil_text.append(non_tamil_text_only)
    return non_tamil_text


def filter_tamil_text(texts: list) -> list[list]:
    """
    To get the pure tamil text, that does not contain any other ascii characters

    Ex: [['tamil_word1'],
    ['tamil_word1', 'tamil_word2', 'tamil_word3']]

    :param texts: extracted web content with tamil language texts(input may contain other characters).
    :return: 2D array : which includes only tamil characters, each row contains text separated by words.
    """
    tamil_text = []
    for single_tag_text in texts:
        tamil_only_text = re.findall('[ஂ-௺]+', single_tag_text)  # to find tamil text in each line
        tamil_text.append(tamil_only_text)
    return tamil_text


def get_web_content(link: str) -> BeautifulSoup:
    """
    To get the bs4 version of the html page.

    :param link: URL for the website that need to be scrapped
    :return: BeautifulSoup: the content of the website in the bs4 format
    """
    response = requests.get(link)
    web_content = BeautifulSoup(response.content, 'lxml')
    return web_content


class TamilScraper:
    def __init__(self, link: str):
        """
        Tamil Scraper is designed to extract Tamil text from online sources.

        It utilizes web scraping techniques to retrieve Tamil content from the specified URL.

        Example:

        >>> import TamilScraper
        >>> tamil_scrap = TamilScraper('https://www.projectmadurai.org/pm_etexts/utf8/pmuni0002.html')
        >>> tamil_scrap.get_text() # gives the text of tamil characters inside any tag (may contain non-tamil characters).
        >>> tamil_scrap.get_by_tag('h1') # gives the text of tamil characters inside h1 tag (may contain non-tamil characters).
        >>> tamil_scrap.get_table() # gives the tables that contains any tamil character.

        :param link: URL of the website to be scrapped
        """
        self.link = link
        self.web_content = get_web_content(link)

    def get_text(self, only_other: bool = False, only_tamil: bool = False) -> list[str] | list[list]:
        """
        Gives the tamil text(may contain non-tamil characters) (or) only tamil text (or) only non-tamil text, based on the
        parameters in the hierarchical order of the webpage.

        ---
        NOTE
        ---

        if this function returns empty array it means there is no content available

        (or)

        The Website you are looking is NOT ALLOWING content to be scraped


        :param only_other: True, if only non-tamil characters needed
        :param only_tamil: True, if only tamil characters needed
        :return: list[str]: if the function is called normally; list[list]: only_tamil (or) only_other is True.
        :raise ValueError: If both only_other and only_tamil are True, for one function call one type of output
        """

        if only_tamil and only_other:
            raise ValueError("Both the 'only_other' and 'only_tamil' arguments can't be true")

        # To get text except Tamil characters
        if only_other:
            non_tamil_text = self.web_content.find_all(string=re.compile('[^ஂ-௺]+'))
            return filter_non_tamil_text(non_tamil_text)
        else:
            # To get Tamil text
            tamil_text = self.web_content.find_all(string=re.compile('[ஂ-௺]+'))

            # To get only Tamil text
            if only_tamil:
                return filter_tamil_text(tamil_text)

            # returns tamil text , it may contain non-tamil characters
            return tamil_text

    def get_by_tag(self, tag: str, only_other: bool = False, only_tamil: bool = False) -> list[list] | list[str]:
        """
        Gives the tamil text(may contain non-tamil characters) (or) only tamil text (or) only non-tamil text,
        of the tag name mentioned.

        ---
        NOTE
        ---

        if this function returns empty array it means there is no content available

        (or)

        The Website you are looking is NOT ALLOWING content to be scraped

        :param tag: The HTML tag name that is needed to get the text.
        :param only_other: True, if only non-tamil characters needed.
        :param only_tamil: True, if only tamil characters needed.
        :return: list[str]: if the function is called normally; list[list]: only_tamil (or) only_other is True.
        :raise ValueError: If both only_other and only_tamil are True, for one function call one type of output
        """

        if only_tamil and only_other:
            raise ValueError("Both the 'only_other' and 'only_tamil' arguments can't be true")
        tag_elements = self.web_content.find_all(tag)
        # Extract text content from each element and store in a list
        tag_texts = [element.get_text(strip=True) for element in tag_elements]
        if only_tamil:
            return filter_tamil_text(tag_texts)

        if only_other:
            return filter_non_tamil_text(tag_texts)
        return tag_texts

    def get_table(self) -> list[pandas.DataFrame] | list:
        """
        Gives the table that contains any tamil characters.
        It will get the table even any of the columns have a single tamil character.

        :return: list: List of pandas DataFrames, containing tables with Tamil text.
        """
        # Read HTML tables from the specified URL
        try:
            df_list = pandas.read_html(self.link)
        except HTTPError as e:
            print('The Website You are trying to scrap is not allowing to get the content, better try another site\n',
                  e)
            return []
        # Initialize a list to store DataFrames with Tamil text
        df_tamil_list = []

        # Iterate to all the tables scraped from the website
        for df in df_list:
            tamil_text_found = False

            # Iterate over each column in the DataFrame
            for column in df.columns:
                # Check if any cell in the column contains Tamil characters using regex
                if df[column].apply(lambda x: bool(re.search('[ஂ-௺]+', str(x)))).any():
                    tamil_text_found = True
                    break  # Stop checking further columns if Tamil text is found

            # If Tamil text is found in any column, append the DataFrame to the list
            if tamil_text_found:
                df_tamil_list.append(df)

        return df_tamil_list

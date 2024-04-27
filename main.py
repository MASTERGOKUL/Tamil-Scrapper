import re
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


def get_web_content(link) -> BeautifulSoup:
    """
    To get the bs4 version of the html page.

    :param link: URL for the website that need to be scrapped
    :return: BeautifulSoup: the content of the website in the bs4 format
    """
    response = requests.get(link)
    web_content = BeautifulSoup(response.content, 'lxml')
    return web_content


class TamilScarper:
    def __init__(self, link: str):
        """
        Tamil Scraper is a tool to scarp tamil contents from online.
        :param link: URL of the website to be scrapped
        """
        self.link = link
        self.web_content = get_web_content(link)

    def get_text(self, only_other: bool = False, only_tamil: bool = False) -> list | list[list]:
        """
        Gives the tamil text(may contain non-tamil characters) (or) only tamil text (or) only non-tamil text, based on the
        parameters in the hierarchical order of the webpage.

        :param only_other: True, if only non-tamil characters needed
        :param only_tamil: True, if only tamil characters needed
        :return:
        """

        # to get text except tamil characters
        if only_other:
            non_tamil_text = self.web_content.find_all(string=re.compile('[^ஂ-௺]+'))
            return filter_non_tamil_text(non_tamil_text)
        else:
            # to get tamil text
            tamil_text = self.web_content.find_all(string=re.compile('[ஂ-௺]+'))

            # to get only tamil text
            if only_tamil:
                return filter_tamil_text(tamil_text)

            # returns tamil text , it may contain non-tamil characters
            return tamil_text

    def get_by_tag(self, tag: str, only_other: bool = False, only_tamil: bool = False) -> list[list] | list[str]:
        """
        Gives the tamil text(may contain non-tamil characters) (or) only tamil text (or) only non-tamil text,
        of the tag name mentioned
        :param tag : The HTML tag name that need to get.
        :param only_other: True, if only non-tamil characters needed.
        :param only_tamil: True, if only tamil characters needed.
        :return:
        """

        tag_elements = self.web_content.find_all(tag)
        # Extract text content from each element and store in a list
        tag_texts = [element.get_text(strip=True) for element in tag_elements]
        if only_tamil:
            return filter_tamil_text(tag_texts)

        if only_other:
            return filter_non_tamil_text(tag_texts)
        return tag_texts

    def get_table(self) -> list[pandas.DataFrame]:
        """
        Extracts HTML tables containing Tamil text from a given URL.

        :return: list: List of pandas DataFrames containing tables with Tamil text.
        """
        # Read HTML tables from the specified URL
        df_list = pandas.read_html(self.link)

        # Initialize a list to store DataFrames with Tamil text
        df_tamil_list = []

        # Check each DataFrame for columns containing Tamil text
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


if __name__ == '__main__':
    extracted_tamil_text = TamilScarper('https://ta.wikipedia.org/wiki/%E0%AE%95%E0%AF%8B%E0%AE%AF%E0%AE%BF%E0%AE%B2%E0%AF%8D_%E0%AE%AE%E0%AE%A3%E0%AE%BF%E0%AE%AF%E0%AF%8B%E0%AE%9A%E0%AF%88')
    print(extracted_tamil_text.get_table())

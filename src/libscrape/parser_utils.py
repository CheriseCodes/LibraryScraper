"""
Library containing utility functions for logging data from web scraping activities to
aid in debugging and testing.
"""

from datetime import date
import os

curr_path = os.path.dirname(__file__)


def save_output_as_html(contents, title):
    """
    Saves the contents to a html file with the given title. The current date will be appended to the title in the
    format Month-Day-Year.

    Parameters
    ----------
    contents: a string representing the text that should be written to the html file
    title: the title of the html file
    """
    html_title = title + date.today().strftime("-%b-%d-%Y") + '.html'
    full_path = curr_path + '/../libscrape/sample_pages/' + html_title
    f = open(full_path, 'w', encoding='utf-8')
    f.write(contents)
    f.close()


def save_output_as_txt(contents, title):
    """
    Saves the contents to a plain text file (*.txt) with the given title. The current date will be appended to the
    title in the format Month-Day-Year.

    Parameters
    ----------
    contents: a string representing the text that should be written to the plain text file
    title: the title of the plain text file
    """
    txt_title = title + date.today().strftime("-%b-%d-%Y") + '.txt'
    full_path = curr_path + '/../libscrape/txt_logs/' + txt_title
    f = open(full_path, 'w', encoding='utf-8')
    f.write(contents)
    f.close()

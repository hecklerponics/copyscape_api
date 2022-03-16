import requests as r
import xml.etree.ElementTree as ET
import pandas as pd


class CopyScapeReport:

    def __init__(self):
        self.end_point = "https://www.copyscape.com/api/"

        try:
            self.get_api_info()

        except FileNotFoundError as not_found:
            print("Missing API Auth File: "
                  + str(not_found.filename))
            print("-" * 10)
            print("""Create a .txt file named 'copyscape_api_key' and 
                  include a dictionary with the values api_key, and username.""")

            return

        self.parameters = {'u': self.user_name,
                           'k': self.api_key}

        return

    def get_api_info(self):

        """
        Reads a text file that contains a dict w/ the copyscape API
        username and key.
        """

        import ast

        with open('copyscape_api_key.txt') as f:
            data = ast.literal_eval(f.read())

        self.api_key = data['api_key']
        self.user_name = data['username']

        return self

    def check_url_for_copies(self, url):

        """
        Takes a URL and looks for duplicated content
        based on the provided URL; return a response object
        and the URL used for the query
        """

        self.parameters['o'] = 'csearch'
        self.parameters['q'] = url
        print(self.parameters)

        return r.get(self.end_point, params=self.parameters), url


def output_formatted_xml(resp):

    """
    Simple function to print out a xml response
    """

    root = ET.fromstring(resp.text)
    print(ET.tostring(root, encoding='utf8').decode('utf8'))
    return


def parse_xml_report_response(resp):

    """
    Parses the copyscape xml for URL results; returns the
    - URL, TITLE, Miniumum Matches Words, VIEWURL (copyscape URi), TEXT SNIPPET
    """

    xml_tree = ET.fromstring(resp.text)
    output_dict = {}

    for element in xml_tree.iter('result'):

        for item in element.iter('result'):
            try:
                output_dict[item.find('index').text] = {'url': item.find('url').text,
                                                    'title': item.find('title').text,
                                                    'min_matched_words': item.find('minwordsmatched').text,
                                                    'viewurl': item.find('viewurl').text,
                                                    'textsnippet': item.find('textsnippet').text}
            except AttributeError:
                pass

    return output_dict


def process_list_of_urls(url_list):

    """
    Simple batch job for taking a list of URL and running them through
    the job of checking them for duplicates via the copyscape API.
    """

    output_df = pd.DataFrame()

    for url in url_list:
        response, url = CopyScapeReport().check_url_for_copies(url)
        output_df = create_df_from_results_dict(response, url).append(output_df)

    return output_df


def create_df_from_results_dict(response, query_url):

    """
    Takes results response and the query URL and returns a DF.
    """
    try:
        result = parse_xml_report_response(response)
        df = pd.DataFrame(result.values(),
                          index=result.keys())

        df['query_url'] = query_url

    except AttributeError:
        pass

    return df

import requests as r
import urllib
import xml.etree.ElementTree as ET


def output_formatted_xml(resp):
    root = ET.fromstring(resp.text)
    print(ET.tostring(root, encoding='utf8').decode('utf8'))
    return


def parse_xml_report_response(resp):
    xml_tree = ET.fromstring(resp.text)

    output_dict = {}
    print("Set empty dict.")

    for element in xml_tree.findall('response').iter():
        print("checking an item")
        print(xml_tree.find('query').text)

        for item in element.iter():
            output_dict[xml_tree.find('query').text] = {'url': item.find('url').text,
                                                    'title': item.find('title').text,
                                                    'min_matched_words': item.find('minwordsmatched').text}

        print(output_dict)
        print(element)

    print("done looping")

    return output_dict


class CopyScape_report():

    def __init__(self):
        self.end_point = "https://www.copyscape.com/api/"
        self.user_name = "localseoguide"
        self.api_key = "masalnl2v8d1elcr"

        self.parameters = {'u': self.user_name,
                           'k': self.api_key}

        return

    def check_url_for_copies(self, url):
        self.parameters['o'] = 'csearch'
        self.parameters['q'] = url
        print(self.parameters)

        response = r.get(self.end_point,
                         params=self.parameters)

        return response

# CopyScape API Connector

A simple connector for checking URLs against [CopyScape's](http://www.copyscape.com/) 
API for duplication of the content. This script will work on Python 3.5+ and returns data in the form of a 
`pd.DataFrame()`:
```
columns =  ['url',  # Matched URL
            'title',  # Title of the matched URL
            'min_match_words'  # Minimum number of matched words, 
            'viewurl',  # CopyScape URL to view comparison
            'textsnippet'  # Text from positive match
            'query_url'  # The URL queried for the result
```


## Setting It Up
The script requires API information to be included in a file named `copyscape_api_key.txt` which contains a
dictionary with the keys `api_key` and `username`.  To check if your setup is correct use the following to 
ensure the api creds are being read correctly: 

```python
import copyscape_connector as cc

report_obj = cc.CopyScapeReport()
print(report_obj.user_name, report_obj.api_key)
```

To pull records based on a single URL:
```python
url = 'https://www.localseoguide.com'

cc.CopyScapeReport().check_url_for_copies(url)
```

To pull records for a list of URLs: 
```python
url_list = ['https://www.localseoguide.com'
            'https://www.localu.com/',
            'https://blumenthals.com/blog/'] 

cc.process_list_of_urls(url_list)
```

### Current Functionality: 
- Pull URLs that have been flagged as having duplicated content by providing a list of URLs.
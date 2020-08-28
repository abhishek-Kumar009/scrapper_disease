import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Put the url here
url = "https://icdlist.com/icd-10/index/intraoperative-and-postprocedural-complications-of-skin-and-subcutaneous-tissue-l76"
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
codes = soup.find_all('li')
hrefs = []
category = []
condition = []
# Find the hrefs in the given page
for li in codes:
    if li.span:
        if li.span.text == "BILLABLE CODE":
            s = li.text.replace(li.a.text, '').replace("BILLABLE CODE", '').replace('-', '').strip()
            hrefs.append("https://icdlist.com/" + li.a['href'][6:])
            category.append(li.a.text)
            condition.append(s)
# print(category)
# print(condition)

catData = []
count = 1
len_data = len(hrefs)
for href in hrefs:
    data = []
    html = urlopen(href)
    soup = BeautifulSoup(html, 'html.parser')
    synonyms = soup.find('ul', style="columns: 2;")
    print('Progress %', count/len_data*100)
    # Find the Synonyms
    if synonyms:
        for li in synonyms:
            data.append(li.text)
        catData.append(data)
        count = count + 1        
    else:
        catData.append(data)
        count = count + 1

# print(catData)

dataframeSyn = pd.DataFrame({
     'Synonyms': catData
});

#Save the csv file
dataframeSyn.to_csv('/home/abhishek/Desktop/scrapper/L76Syn.csv')
'''
Most of the code is specific to the website, and hence for scraping any website, we need to check it's terms and conditon(/robots.txt) and then the data from the website[Ctrl+Shift+I(inspect), Ctrl+U(source code)]
'''

import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.titlelink')
subtext = soup.select('.subtext')
links2 = soup2.select('.titlelink')
subtext2 = soup2.select('.subtext')
# we are taking .subtext instead of .score because there is a chance of getting 0 points/votes in some news links which will lead to an error.

mega_links = links + links2
mega_subtext = subtext + subtext2

def sort_stories_by_votes(hnlist):
  return sorted(hnlist, key= lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
  hn = []
  for idx, item in enumerate(links):
    title = item.getText()
    href = item.get('href', None)
    vote = subtext[idx].select('.score') # inside subtext we are selecting score
    if len(vote):
      points = int(vote[0].getText().replace(' points', ''))
      if points > 99:
        hn.append({'title': title, 'link': href, 'votes': points})
  return sort_stories_by_votes(hn)
 
pprint.pprint(create_custom_hn(mega_links, mega_subtext))
# pprint make the output neater
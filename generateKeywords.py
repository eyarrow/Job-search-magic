import requests
from bs4 import BeautifulSoup
import yake

# Scrape html content from the provided web page
def getWebpage(url: str) -> str:
  page = requests.get(url)
  return page.text

# parse HTML and remove tags that occurs within the given CSS class
def parseHTML(contentToParse: str, classToUse: str) -> str:
  soup = BeautifulSoup(contentToParse, 'html.parser')
  # classSearch = "_class" + "=" + classToUse
  # print(f"Class search is {classSearch}.")
  data_str = ""
  for item in soup.find_all(class_=classToUse):
    data_str = data_str + item.get_text() + " "
  return data_str

post = 'section'
urlToUse = 'https://www.amazon.jobs/en/jobs/2350484/software-development-engineer-ii'
rawPage = getWebpage(urlToUse)
parsedPage = parseHTML(rawPage, post)
print(parsedPage)
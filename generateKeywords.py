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

# Generate a list of keywords based on the parsed text
def generateKeywords(parsedPage: str) -> str:
  kwExtractor = yake.KeywordExtractor()
  keywords = kwExtractor.extract_keywords(parsedPage)
  for word in keywords:
    print(word)

# Saves a 'preetified' version of the whole job description
def generateJobDescription(contentToParse: str) -> str:
  

post = 'description'
urlToUse = 'https://careers.azenta.com/job/1417/us_payroll_manager'
rawPage = getWebpage(urlToUse)
parsedPage = parseHTML(rawPage, post)
generateKeywords(parsedPage)
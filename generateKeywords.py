import requests
from bs4 import BeautifulSoup
import yake

def getWebpage(url: str) -> str:
  page = requests.get(url)
  return page.text


post = 'job-detail'
urlToUse = 'https://www.amazon.jobs/en/jobs/2350484/software-development-engineer-ii'
rawPage = getWebpage(urlToUse)
print(rawPage)
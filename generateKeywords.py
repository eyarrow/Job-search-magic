import os
import requests
from bs4 import BeautifulSoup
import yake

# Todo: Change all variable to snake case

# Scrape html content from the provided web page
def getWebpage(url: str) -> str:
  page = requests.get(url)
  return page.text

# parse HTML and remove tags that occurs within the given CSS class
def parseHTML(contentToParse: str, classToUse: str) -> str:
  soup = BeautifulSoup(contentToParse, 'html.parser')
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

# Saves a 'preetified' version of the whole job description, which only pulls from content
# in paragraph tags and headers
def generateJobDescription(contentToParse: str) -> str:
  soup = BeautifulSoup(contentToParse, 'html.parser')
  data_str = ""
  for item in soup.find_all(['p', 'h1', 'h2']):
    data_str = data_str + item.get_text(separator='\n')
  return data_str

# Set the file settings for saving the final file
def setFileConfig(save_path: str, file_name: str) -> str:
  return os.path.join(save_path, file_name)

# Set the location to save the file here
save_path = '/home/elizabeth/jobs'
file_name = "test5.txt"

complete_name = setFileConfig(save_path, file_name)
post = 'description'
urlToUse = 'https://careers.azenta.com/job/1417/us_payroll_manager'
employer = 'Azenta'
rawPage = getWebpage(urlToUse)
parsedPage = parseHTML(rawPage, post)
jobDescription = generateJobDescription(rawPage)
generateKeywords(parsedPage)

file_to_write = "Employer:  " + employer + '\n' + '\n' + "URL: " + urlToUse + '\n' + '\n' + "Job Description: " + jobDescription +  '\n' +'\n' 

file1 = open(complete_name, "w")
file1.write(file_to_write)
file1.close
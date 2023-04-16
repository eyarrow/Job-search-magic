import os
import requests
from bs4 import BeautifulSoup
import yake

post = 'description'
url_to_use = 'https://careers.azenta.com/job/1417/us_payroll_manager'
employer = 'Chucky Cheese'
directory = employer
save_path = '/home/elizabeth/jobs'
file_name = f"job-description-{employer}.txt"

# Scrape html content from the provided web page
def get_webpage(url: str) -> str:
  page = requests.get(url)
  return page.text

# parse HTML and remove tags that occurs within the given CSS class
def parse_html(content_to_parse: str, class_to_use: str) -> str:
  soup = BeautifulSoup(content_to_parse, 'html.parser')
  data_str = ""
  for item in soup.find_all(class_=class_to_use):
    data_str = data_str + item.get_text() + " "
  return data_str

# Generate a list of keywords based on the parsed text
def generate_keywords(parsed_page: str) -> str:
  kwExtractor = yake.KeywordExtractor()
  keywords = kwExtractor.extract_keywords(parsed_page)
  for word in keywords:
    print(word)
  return keywords

# Saves a 'preetified' version of the whole job description, which only pulls from content
# in paragraph tags and headers
def generate_job_description(content_to_parse: str) -> str:
  soup = BeautifulSoup(content_to_parse, 'html.parser')
  data_str = ""
  for item in soup.find_all(['p', 'h1', 'h2']):
    data_str = data_str + item.get_text(separator='\n')
  return data_str

# Set the file settings for saving the final file
def set_file_config(save_path: str, file_name: str) -> str:
  # dynamically set file name here
  # check to make sure the file name does not already exist
  # if it does increment it
  return os.path.join(save_path, file_name)

# Set the location to save the file here
path = os.path.join(save_path, directory)
try:
  os.mkdir(path)
except:
  pass




complete_name = set_file_config(save_path, file_name)

raw_page = get_webpage(url_to_use)
parsed_page = parse_html(raw_page, post)
job_description = generate_job_description(raw_page)
keyword = generate_keywords(parsed_page)

file_to_write = "Employer:  " + employer + '\n' + '\n' + "URL: " + url_to_use + '\n' + '\n' + "Job Description: " + job_description +  '\n' +'\n' + "Keywords: " 

# file1 = open(complete_name, "w")
# file1.write(file_to_write)
# file1.close
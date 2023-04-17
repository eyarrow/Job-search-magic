import os
import requests
from bs4 import BeautifulSoup
import yake
import tkinter as tk

fields = ('Employer Name', 'Job Listing URL', 'File Path to Save to', 'CSS tag for requirements (Optional)', 'Skills Section Text (Optional)' )
keywords = ""

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
  kw = ""
  kwExtractor = yake.KeywordExtractor()
  keywords = kwExtractor.extract_keywords(parsed_page)
  for word in keywords:
    kw = kw + '\n' + word[0]
  return kw

# Saves a 'prettified' version of the whole job description, which only pulls from content
# in paragraph tags
def generate_job_description(content_to_parse: str) -> str:
  soup = BeautifulSoup(content_to_parse, 'html.parser')
  data_str = ""
  for item in soup.find_all(['p', 'ul', 'h1', 'h2', 'h3']):
    # can I pull out links
    data_str = data_str + item.get_text(separator='\n')
  return data_str

# Adds a directory set by default to the employer's name.
# If it already exists it will add files to the existing directory. 
def generate_directory(save_path: str, directory: str) -> str:
  path = os.path.join(save_path, directory)
  try:
    os.mkdir(path)
  except:
    pass
  return path

# Set the file settings for saving the final file
def set_file_config(save_path: str, file_name: str) -> str:
  # dynamically set file name here
  # check to make sure the file name does not already exist
  # if it does increment it
  file_name = f"job-description-{file_name}.txt"
  return os.path.join(save_path, file_name)

# Utilizes input from the user to run the script
def generate_file_usr_input(input: dict) -> dict:
  employer = input['Employer Name'].get()
  directory = employer
  class_to_use = input['CSS tag for requirements (Optional)'].get()
  url_to_use = input['Job Listing URL'].get()
  skills_section = input['Skills Section Text (Optional)'].get()
  # save_path = input['File Path to Save to'].get() 
  save_path = '/home/elizabeth/jobs'
  path = generate_directory(save_path, directory)
  path_to_write = set_file_config(path, employer)
  raw_page = get_webpage(url_to_use)
  if class_to_use:
    parsed_keywords = parse_html(raw_page, class_to_use)
    keywords = generate_keywords(parsed_keywords)
  elif skills_section:
    keywords = generate_keywords(skills_section)
  else:
    keywords = ""
  
  job_description = generate_job_description(raw_page)
  file_to_write = "Employer:  " + employer + '\n' + '\n' + "URL: " + url_to_use + '\n' + '\n' + "Job Description: " + job_description +  '\n' +'\n' + "Keywords: " + keywords
  
  if os.path.isfile(path_to_write):
    print("File is already in use. Please rename the existing file and try again.")
  else:
    file1 = open(path_to_write, "w")
    file1.write(file_to_write)
    file1.close
  
# Generate UI fields  
def makeform(root, fields):
    entries = {}
    for field in fields:
        print(field)
        row = tk.Frame(root)
        lab = tk.Label(row, width=30, text=field+": ", anchor='w')
        ent = tk.Entry(row)
        ent.insert(0, "")
        row.pack(side=tk.TOP, 
                 fill=tk.X, 
                 padx=5, 
                 pady=5)
        lab.pack(side=tk.LEFT, fill=tk.X)
        ent.pack(side=tk.RIGHT, 
                 expand=tk.NO, 
                 fill=tk.X)
        entries[field] = ent
    return entries


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("450x250")
    ents = makeform(root, fields)
    b1 = tk.Button(root, text='Generate Job File',
           command=(lambda e=ents: generate_file_usr_input(e)))
    b1.pack(side=tk.RIGHT, padx=5, pady=5)
    b3 = tk.Button(root, text='Quit', command=root.quit)
    b3.pack(side=tk.LEFT, padx=5, pady=5)
    root.mainloop()
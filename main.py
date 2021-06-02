from bs4 import BeautifulSoup
import requests
import pandas as pd

def extract_page(page):
    """Creates get request for Indeed website"""

    URL = f"https://uk.indeed.com/jobs?q=Software+Developer&l=London+W13&radius=15&start={page}"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup

def job_info(soup):
    """Iterates through relevant areas of job search and appends each job to a list"""

    divs = soup.find_all("div", class_ = "jobsearch-SerpJobCard")
    for item in divs:
        job_title = item.find("a", class_ = "jobtitle turnstileLink").text.strip()
        company = item.find("span", class_ = "company").text.strip()
        try:
            location = item.find("span", class_ = "location accessible-contrast-color-location").text.strip()
        except:
            location = "N/A"   
        try:
            salary = item.find("span", class_ = "salaryText").text.strip()
        except: 
            salary = "N/A"
        summary = item.find("div", {"class": "summary"}).text.strip().replace("\n", "")
        posted = item.find("span", class_ = "date date-a11y").text.strip()
        
        
        jobs = {
            "Title": job_title,
            "Company Name": company,
            "Location": location,
            "Salary": salary,
            "Summary": summary,
            "Posted": posted}

        available_jobs.append(jobs)
    return

available_jobs = [] # List of dictionaries for each job    

# Iterates over each page on indeed to return as many jobs as required
for i in range(0, 30, 10):
    print(f"Getting Page: {i}")
    c = extract_page(i)
    job_info(c)

# Transforms list into dataframe for readability purposes
df = pd.DataFrame(available_jobs)
print(df)
# df.to_csv("dev_job_search.csv")
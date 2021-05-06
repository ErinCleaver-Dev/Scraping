import requests
from bs4 import BeautifulSoup
import time

URL = "https://www.indeed.com/jobs?q=javascript&l="

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

# gets the number of jobs and printers out the value - Erin Cleaver
def get_number_of_jobs():
    count_pages_list = soup.find(id="searchCountPages").text.strip().split()
    number_of_jobs = int(count_pages_list[3].replace(',', ""))
    print(f"Number of jobs {number_of_jobs}")

# gets the next page in the application.
def get_next_page(soup):
    pagination = soup.find("ul", class_="pagination-list")
    pages = pagination.find_all("li")
    last_page = pages[-1].find("a")['href']
    next_page = f"https://www.indeed.com/{last_page}"
    return next_page

def get_jobs(soup):
    job_list = soup.find_all("div", class_="jobsearch-SerpJobCard")
    jobs = []
    for job in job_list:
        title = job.find("a", class_="jobtitle").text.strip()
        url = job.find("a", href=True)
        url = "https://www.indeed.com" + url['href']
        company = job.find("span", class_="company").text.strip()
        try:
            location = job.find("span", class_="location").text.strip()
        except (TypeError, AttributeError):
            location = ""
        summary = job.find("div", class_="summary").text.strip()
        date = job.find("span", class_="date").text.strip()
        if (location == "Remote"):
            jobs.append((title, url, company, location, summary, date))
        
    return jobs

        


get_number_of_jobs()
print("")

get_next_page(soup)
job_list = [];

def generate_jobs_array(job_list, soup):
    try:
        job_list.append(get_jobs(soup))
        URL = get_next_page(soup)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        return generate_jobs_array(job_list, soup)
    except (TypeError, AttributeError):
        return job_list


count = 0;
job_list = generate_jobs_array(job_list, soup)
for job_info in job_list:
    for gathered_job in gathered_jobs:
        for job in gathered_job:
            count+=1;
            print(job)
        print("")

print(count)
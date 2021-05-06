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
        print(title)
        url = job.find("a", href=True)
        url = "https://www.indeed.com" + url['href']
        print(url)
        company = job.find("span", class_="company").text.strip()
        print(company)
        try:
            location = job.find("span", class_="location").text.strip()
            print(location)
        except (TypeError, AttributeError):
            print("no location found")
            location = ""
        summary = job.find("div", class_="summary").text.strip()
        print(summary)
        date = job.find("span", class_="date").text.strip()
        print (date)
        print("")
        jobs.append((title, url, company, location, summary, date))
    return jobs

        


get_number_of_jobs()
get_next_page(soup)
get_jobs(soup)

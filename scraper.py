import requests
from bs4 import BeautifulSoup
import time


def get_soup (url):
    URL = url
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


# gets the number of jobs and printers out the value - Erin Cleaver
def get_number_of_jobs(soup):
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

#gets the information for each jobs on the page
def get_jobs(soup, type):
    job_list = soup.find_all("div", class_="jobsearch-SerpJobCard")
    jobs = []

    job_list_dict = {}
    for job in job_list:
        title = job.find("a", class_="jobtitle").text.strip()
        url = job.find("a", href=True)
        url = "https://www.indeed.com" + url['href']
        company = job.find("span", class_="company").text.strip()
        try:
            location = job.find("span", class_="location").text.strip()
        except (TypeError, AttributeError):
            location = ""
        rating = job.find("span", class_="rating")
        if rating: 
            rating.text.strip()
        else: 
            ""
        summary = job.find("div", class_="summary").text.strip()
        date = job.find("span", class_="date").text.strip().split(" ")
        date = date[0];
        day = 8;
        
        if(date.isnumeric()): 
           day = int(date)
        if (location == "Remote" and (day < 2 or date == "Today")):
            job_list_dict = {
                "title": title if title else None,
                "url": url if url else None,
                "company": company if company else None,
                "rating": rating if rating else None,
                "location": location if location else None,
                "summary": summary if summary else None,
                "date": date if date else None,   
                "type": type if type else None
               }

        if(job_list_dict):
            jobs.append(job_list_dict)
        
    
    print("\n\n")
    return jobs

        

job_list = [];

# gathers a list of jobs.  
def generate_jobs_array(job_list, soup, type):
    for i in range(100):
        try:
            job_list+=get_jobs(soup, type)
            url = get_next_page(soup)
            print(url);
            soup = get_soup(url)
        except (TypeError, AttributeError):
            break

    return job_list



soup = get_soup("https://www.indeed.com/jobs?q=javascript&l=")
get_number_of_jobs(soup)

job_list += generate_jobs_array(job_list, soup, "javascript")

soup = get_soup("https://www.indeed.com/jobs?q=react&l")
get_number_of_jobs(soup)

job_list += generate_jobs_array(job_list, soup, "react")

soup = get_soup("https://www.indeed.com/jobs?q=python&l=")
get_number_of_jobs(soup)

job_list += generate_jobs_array(job_list, soup, "python")


for job_info in job_list:
    for gathered_job in job_info:
        print("Title: ", job_info["title"] )
        print("Url: ", job_info["url"])
        print("Company: ", job_info["company"])
        print ("Rating: ",job_info["rating"])
        print ("Localtion: ",job_info["location"])
        print ("Summary: ", job_info["summary"])
        print ("Date: ", job_info["date"])
        print ("Date: ", job_info["type"])
        print("")        

print(len(job_list))

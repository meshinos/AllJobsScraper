from bs4 import BeautifulSoup
import requests
from deep_translator import GoogleTranslator
import pandas as pd

"""
scrapes the AllJobs website for available programming positions and saves them in an XLSX file.
"""

job_titles = []
companies = []
job_descriptions = []
for i in range(1,9):
    URL = f"https://www.alljobs.co.il/SearchResultsGuest.aspx?page={i}&position=&type=&freetxt=python%20developer&city=&region="
    page = requests.get(URL)  # fetches the static site content,You now have access to the site’s HTML from within your Python script.
    soup = BeautifulSoup(page.text, "html.parser")

    job_cards = soup.find_all(name="div", class_="job-content-top")
    for card in job_cards:
        job_title = card.find("h3").string
        job_title = GoogleTranslator(source='auto', target='en').translate(job_title)
        job_titles.append(job_title)
        company = str(card.select_one("div.T14 a"))[str(card.select_one("div.T14 a")).find(">"):str(card.select_one("div.T14 a")).find("<", 1)]
        company = company.replace("<", "")
        company = company.replace(">", "")
        company = GoogleTranslator(source='auto', target='en').translate(company)
        companies.append(company)
        job_description = str(card.select_one("div.PT15 ").text)
        job_description = GoogleTranslator(source='auto', target='en').translate(job_description)
        job_descriptions.append(job_description)

df = pd.DataFrame(
    {
        "Job Title": job_titles,
        "Company": companies,
        "Job Description": job_descriptions
    }
)

writer = pd.ExcelWriter("converted_to_excel.xlsx")
df.to_excel(writer)
writer.save()
print("DataFrame is exported successfully to 'converted-to-excel.xlsx' Excel File.")





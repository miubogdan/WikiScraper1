import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_company_links(ftse_url):
    response = requests.get(ftse_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    constituents_table = soup.find('table', id='constituents')
    company_links = {}
    if constituents_table:
        for row in constituents_table.find_all('tr')[1:]:  # Skip header
            cells = row.find_all('td')
            if cells and cells[0].find('a'):  # Anchor/Hyperlink
                company_name = cells[0].text.strip()
                company_link = 'https://en.wikipedia.org' + cells[0].find('a')['href']
                company_links[company_name] = company_link
    return company_links


def extract_company_info(company_name, company_url):
    response = requests.get(company_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    info_box = soup.find('table', class_='infobox vcard')
    company_info = {'Company Name': company_name}
    if info_box:
        for row in info_box.find_all('tr'):
            if row.find('th') and row.find('td'):
                key = row.find('th').text.strip()
                value = row.find('td').text.strip().replace('\xa0', ' ')
                company_info[key] = value
    return company_info

def dataframe(company_data):
    df = pd.DataFrame(company_data)
    return df

ftse_url = 'https://en.wikipedia.org/wiki/FTSE_100_Index'
company_links = get_company_links(ftse_url)
company_data = [extract_company_info(name, url) for name, url in company_links.items()]
df = dataframe(company_data)

df.to_csv('ftse_100_company_info.csv')
print(df.head())
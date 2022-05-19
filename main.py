import csv
import requests
import bs4
from bs4 import BeautifulSoup
from alive_progress import alive_bar


def is_sfra(site_dom: bs4.BeautifulSoup):
    div_element = site_dom.find_all('div', class_='page', attrs={'data-action': True}, limit=1)  # Stricter check
    # div_element = site_dom.find_all('div', attrs={'data-action': True}, limit=1)  # Not recommended check
    if div_element:
        return True
    return False


def is_site_genesis(site_dom: bs4.BeautifulSoup):
    div_element = site_dom.find_all('div', class_='pt_storefront', attrs={'id': 'wrapper'}, limit=1)
    if div_element:
        return True
    return False


def read_urls_from_csv(route: str):
    file = open(route)
    reader = csv.reader(file)
    next(reader)  # Skip headers
    rows = []
    for row in reader:
        rows.append(row)
    file.close()
    return rows


def scan_site(url: str):
    try:
        html_text = requests.get(url,
                                 headers={
                                     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                                                   'KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
                                 },
                                 timeout=10).text
        site_dom = BeautifulSoup(html_text, 'html.parser')
        if is_sfra(site_dom):
            return 'SFRA'
        if is_site_genesis(site_dom):
            return 'Site Genesis'
        return 'Could not determine'
    except:
        return 'Could not analyze'


def write_csv(results: list):
    file = open('output.csv', 'w')
    writer = csv.writer(file)
    for row in results:
        writer.writerow(row)
    file.close()


def process_sites(sites: list):
    results = [{'Site', 'Result'}]
    print(f"Total sites to be processed: {len(sites)}")
    with alive_bar(len(sites)) as bar:
        for site in sites:
            if site[0][0: 7] != 'https://':
                site[0] = 'https://' + site[0]
            result = scan_site(site[0])
            results.append({result, site[0]})
            print(f"Processed {site[0]} - {result}")
            bar()
    return results


if __name__ == '__main__':
    write_csv(process_sites(read_urls_from_csv('./SFCC_Websites.csv')))  # Be sure to set the proper route to your csv

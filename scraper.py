from selenium import webdriver
from bs4 import BeautifulSoup
import time 
import csv
planet_data = []
start_url = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("C:\Users\Aadhi\Downloads\Win_1000278_chrome-win32-syms")
headers = ["name","light_year_from_earth","planet_mass","STELLAR_MAGNITUDE","discovery_date","hyper_link","planet_type","planet_radius","orbital_radius","orbital_period","eccentricity"]
def scrape():
    for i in range(0,428):
        soup = BeautifulSoup(browser.page_source,"html.parser")
        for ul_tag in soup.find_all("ul",attrs = {"class","exoplanet"}):
            li_tag = ul_tag.find_all("li")
            temp_list = []
            for index_li_tag in enumerate(li_tag):
                if index == 0 :
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else :
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
                        planet_data.append(temp_list)
                        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
                    
scrape() 
new_planets_data = []
def scrape_more_data(hyper_link):
    try:
        page = requests.get(hyper_link)
        soup = BeautifulSoup(page.content,'html.parser')
        temp_list = []
        for tr_tag in soup.find_all("tr",attrs = {"class":"fact_row"}):
            td_tags = tr_tags.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs = {"class":"value"})[0].contents[0]) 
                except:
                    temp_list.append("")
        new_planets_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyper_link)
#calling the method
for index,data in enumerate(planet_data):
    scrape_more_data(data[5])
    print("scaping is completed")
print(new_planets_data[0:10])
final_planet_data = []
for index,data in enumerate(planet_data):
    new_planets_data_element = new_planets_data[index]
    new_planets_data_element = [elem.replace("\n", "") for elem in new_planets_data_element]
    new_planets_data_element = new_planets_data_element[:7]
    final_planet_data.append(data+new_planets_data_element)
with open("scrapper_2.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_planet_data)

    


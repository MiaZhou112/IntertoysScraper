import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
import time
import os
from PIL import Image

links = []
names = []
prices = []
descriptions = []

class Intertoyss(webdriver.Chrome):
    def __init__(self, driver_path=r"/Users/yuezhou/PycharmProjects/chromedriver_mac64/chrome"):
        # can instantiate an instance of class intertoyss ; default attribute driver_path
        self.driver_path = driver_path
        os.environ['PATH'] += self.driver_path
        # web driver path
        super(Intertoyss, self).__init__()
        #  can instantiate an instance of class webdriver.Chrome
        self.implicitly_wait(5)
        # wait 10s until an element is ready
        self.maximize_window()
        # maximize browser window


    def land_first_page(self):
        self.get("https://www.intertoys.nl")


    def remove_popup(self):
        accept_button = self.find_element(By.XPATH,
                          "//a[@class= 'button_primary tlignore PrivacyAcceptBtn']")
        accept_button.click()

    def search(self,text ='game'):
        search_box = self.find_element(By.XPATH,
                                       "//input[@class='searchBar']")
        search_box.send_keys(f'{text}')

        search_button = self.find_element(By.XPATH,
                                          "//div[@class='searchButtonText']")
        search_button.click()

        self.page_url = self.current_url

    def get_links_of_all_games(self):

        links_page1 = self.find_elements(By.XPATH,
                                     "//div[@class='product_name']/a")
        for link in links_page1:
            links.append(link.get_attribute('href'))

        page = 'Exist'
        while page:
            try:
                page = self.find_element(By.XPATH,
                                    "//a[@id = 'WC_SearchBasedNavigationResults_pagination_link_right_categoryResults']")
                page.click()
                links_pages = self.find_elements(By.XPATH,
                                     "//div[@class='product_name']/a")
                for link in links_pages:
                    links.append(link.get_attribute('href'))
            except ElementNotInteractableException:
                page = None

        print(links)

    def get_game_name_price_description(self):
        self.get(self.page_url)

        for link in links:
            self.get(link)
            name = self.find_element(By.XPATH,
                                      "//h1[@class='main_header']")
            names.append(name.text)
            price = self.find_element(By.XPATH,
                                       "//span[@class= 'price']")
            prices.append(price.text)
            description = self.find_element(By.XPATH,
                                     "//div[@class='product_text']")
            descriptions.append(description.text)

            mypath = '/Users/yuezhou/PycharmProjects/pythonProject/screenshots/intertoys'
            if not os.path.isdir(mypath):
                os.makedirs(mypath)
            self.save_screenshot(f"{mypath}/{name.text}.png")

        print(names)
        print(prices)
        print(descriptions)

    def create_dateframe(self):
        dic = {'name':names,'price':prices,'description':descriptions}
        df = pd.DataFrame(dic,columns=['name','price','description'])
        df.to_excel(r"IntertoyScaper/Intertoys_MarioGame_WebScrapping.xlsx",index=False)












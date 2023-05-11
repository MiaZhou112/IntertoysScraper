from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from PIL import Image
import pandas as pd


class IntertoysScraper(webdriver.Chrome):
    def __init__(self, screenshots_path, driver_path):
        """Initialization function     self/bot = IntertoysScraper(screenshots_path, driver_path)
        Args:
            default attribute "driver_path": Path to chromedriver.
            default attribute "screenshots_path": Path to screenshots folder.
        """
        self.screenshots_path = screenshots_path
        self.driver_path = driver_path

        # Inheritance from class webdriver.Chrome      self/bot = webdriver.Chrome()
        super(IntertoysScraper, self).__init__(executable_path=self.driver_path)

        # wait 10s until an element is ready
        self.implicitly_wait(10)
        # maximize browser window
        self.maximize_window()

    def land_first_page(self):
        self.get("https://www.intertoys.nl")

    def remove_popup(self):
        accept_button = self.find_element(
            By.XPATH, "//a[@class= 'button_primary tlignore PrivacyAcceptBtn']"
        )
        accept_button.click()

    def search(self, text="game"):
        """Method to search in for query on Intertoys website
        Args:
            text: The query string. Defaults to "game".
        """
        self.text = text
        search_box = self.find_element(By.XPATH, "//input[@class='searchBar']")
        search_box.send_keys(f"{text}")

        search_button = self.find_element(By.XPATH, "//div[@class='searchButtonText']")
        search_button.click()

        self.page_url = self.current_url

    def get_links_of_all_games(self, links=[]):
        """This function gets the url link of each game.
        Args:
            links: Defaults to [].
        """        
        self.links = links
        links_page1 = self.find_elements(By.XPATH, "//div[@class='product_name']/a")
        for link in links_page1:
            self.links.append(link.get_attribute("href"))

        page = "Exist"
        while page:
            try:
                page = WebDriverWait(self, 10).until(
                    EC.visibility_of_element_located(
                        (
                            By.XPATH,
                            "//a[@id = 'WC_SearchBasedNavigationResults_pagination_link_right_categoryResults']",
                        )
                    )
                )
                page.click()
                links_pages = self.find_elements(
                    By.XPATH, "//div[@class='product_name']/a"
                )
                for link in links_pages:
                    self.links.append(link.get_attribute("href"))
            except:
                page = None

    def get_name_price_description_screenshots(self, names=[], prices=[], descriptions=[]):
        self.names = names
        self.prices = prices
        self.descrptions = descriptions

        self.get(self.page_url)

        for link in self.links:
            self.get(link)
            name = self.find_element(By.XPATH, "//h1[@class='main_header']")
            self.names.append(name.text)
            price = self.find_element(By.XPATH, "//span[@class= 'price']")
            self.prices.append(price.text)
            description = self.find_element(By.XPATH, "//div[@class='product_text']")
            self.descrptions.append(description.text)
            self.save_screenshot(f"{self.screenshots_path}/{name.text}.png")

        print(self.names)
        print(self.prices)
        print(self.descrptions)

    def create_dataframe(self):
        dic = {
            "name": self.names,
            "price": self.prices,
            "description": self.descrptions,
            "query": self.text,
        }
        self.dataframe = pd.DataFrame(dic, columns=["name", "price", "description","query"])

    def write_to_excel(self, output_filename):
        self.dataframe.to_excel(output_filename, index=False)

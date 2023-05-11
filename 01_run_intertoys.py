from IntertoysScraper.Intertoys import IntertoysScraper  # import class
import time
from IntertoysScraper.db import add_file_in_DB    # import function 
import yaml
from IntertoysScraper.utils import read_config    # import function

cfg = read_config('config.yaml')

with IntertoysScraper(
    screenshots_path=cfg["SCREENSHOTS_PATH"], driver_path=cfg["DRIVER_PATH"]
) as bot:  # bot = IntertoysScraper()
    bot.land_first_page()
    bot.remove_popup()
    bot.search(text=cfg["QUERY"])
    bot.get_links_of_all_games()
    bot.get_name_price_description_screenshots()
    bot.create_dataframe()
    bot.write_to_excel(cfg["EXCEL_FILENAME"])
    time.sleep(10)

add_file_in_DB(cfg["DATABASE_URI"], cfg["DATABASE_TABLE"], cfg["EXCEL_FILENAME"])

from IntertoyScaper.Intertoys import Intertoyss
import time

with Intertoyss() as bot:
    bot.land_first_page()
    bot.remove_popup()
    bot.search(text= 'Mario Game')
    bot.get_links_of_all_games()
    bot.get_game_name_price_description()
    bot.create_dateframe()
    time.sleep(10)

print('hello')
print("i hate it")



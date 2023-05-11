import psycopg2
import pandas as pd
import spacy
import matplotlib.pyplot as plt
import seaborn as sns
import yaml
from IntertoysScraper.utils import read_config

def tokenize(x):
    doc = nlp(x)
    tokens = [token.text for token in doc]  # list comprehension
    return tokens

cfg = read_config('config.yaml')

# import file from database
db_connection = psycopg2.connect(
    host = cfg['HOST'],
    database = cfg['DATABASE'],
    user = cfg['USER'],
    password = cfg['PASSWORD'],
    port = cfg['PORT']
)
print('Successfully connected to database!')

c = db_connection.cursor()
query = 'SELECT * FROM "IntertoysTable_Marvel" UNION ALL SELECT * FROM "IntertoysTable_Lego" UNION ALL SELECT * FROM "IntertoysTable_HarryPotter" UNION ALL SELECT * FROM "IntertoysTable_Mario" UNION ALL SELECT * FROM "IntertoysTable_Pokémon" UNION ALL SELECT * FROM "IntertoysTable_Sonic"'
c.execute(query)

df = pd.read_sql_query(query,db_connection,index_col=None)
print(df)

# data transformation: add new columns 'words', 'word_count'
nlp = spacy.load("nl_core_news_sm")
df['word'] = df['description'].apply(lambda x: tokenize(x))
df['word_count'] = df['word'].apply(lambda x:len(x))
print(df)

# Analysis and Visualization 
#1: which game is most expensive? which game is cheapest?    
max_price = df['price'].max()
max_name = df.loc[df['price'] == max_price, 'name'].iloc[0]
min_price = df['price'].min()
min_name = df.loc[df['price'] == min_price, 'name'].iloc[0]
print(f"The most expensive game is {max_name}, the price is {max_price}.")
print(f"The cheapest game is {min_name}, the price is {min_price}.")

# Visualization 1
price_groups = df['price'].groupby(df['query']).agg(['min','max','mean']).round(2)
fig1 = price_groups.plot(kind='bar')
fig1 = fig1.get_figure()
fig1.set_size_inches(7, 6)
plt.ylabel("Average Price")
plt.title("Average Price Per Query related to Games")
fig1.savefig("graph1_average price.png")
plt.clf()

#3: Visualization 2
word_count_groups= df['word_count'].groupby([df['query']]).mean().round(0)
print(word_count_groups)
fig2 = word_count_groups.plot(kind='bar')
fig2 = fig2.get_figure()
fig2.set_size_inches(7, 6)
plt.ylabel("Average Word Count")
plt.title("Average Word Count Per Query related to Games")
fig2.savefig("graph2_average word count.png")
plt.clf()

#4: Visualization 3
fig3 = sns.scatterplot(x="word_count", y="price", data=df, hue="query")
fig3 = fig3.get_figure()
fig3.savefig('graph3_the relationship between price and word count.png')





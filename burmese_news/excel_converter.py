import pandas as pd
df = pd.read_csv('data.csv')
df.to_excel('burmese_news.xlsx', index=False)

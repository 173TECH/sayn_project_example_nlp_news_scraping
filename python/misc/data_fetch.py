import feedparser as f
import pandas as pd

def fetch_data(link):
    raw_data = f.parse(link)
    data = pd.DataFrame(raw_data.entries)
    data.drop(data.columns[[1, 3, 4, 9]], axis=1, inplace=True)
    data["source"] = link[29:-8].replace("/","_") # automatic source labelling
    return data

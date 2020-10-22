import feedparser as f
import pandas as pd

# Get RSS data and return it in a pandas DataFrame
def fetch_data(link):
    raw_data = f.parse(link)
    data = pd.DataFrame(raw_data.entries)
    data.drop(["title_detail", "summary_detail", "links", "published_parsed"], axis=1, inplace=True) # remove incompatible columns
    data["source"] = link[29:-8].replace("/","_") # automatic source labelling
    return data

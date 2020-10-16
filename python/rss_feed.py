import feedparser as f
import pandas as pd
data = f.parse("http://feeds.bbci.co.uk/news/england/rss.xml")
print(f"Number of posts: {len(data.entries)}\n")
print(list((data.entries[1]).keys()))
datap = pd.DataFrame(data.entries)
datap.drop(datap.columns[[1, 3, 4]], axis=1, inplace=True)
print(datap)
print(datap.columns)

# for key in data.entries[1].keys():
#     print(key)

# for entry in data.entries:
#     print("-"*100)
#     for sub in entry:
#         print(f"{sub}: {entry[sub]}\n")
#     print("*** End of Article ***")

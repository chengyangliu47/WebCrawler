import pymongo
from wordcloud import WordCloud
import matplotlib.pyplot as plt

mongo_url = "127.0.0.1:27017"
client = pymongo.MongoClient(mongo_url)
DATABASE = "IndeedData"
db = client[DATABASE]
COLLECTION = "indeed"
db_coll = db[COLLECTION]

words = []
for x in db_coll.find({}, {"_id": 1, "url": 0}):
    words.append(x['jobTitle'])
    print(x['jobTitle'])

word = []
for x in words:
    word += x.split()

# convert list to string and generate
unique_string = " ".join(word)
wordcloud = WordCloud(width=1000, height=500).generate(unique_string)
plt.figure(figsize=(15, 8))
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig("your_file_name" + ".png", bbox_inches='tight')
plt.show()
plt.close()

import pymongo
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# mongodb服务的地址和端口号
mongo_url = "127.0.0.1:27017"

# 连接到mongodb，如果参数不填，默认为“localhost:27017”
client = pymongo.MongoClient(mongo_url)
#连接到数据库myDatabase
DATABASE = "IndeedData"
db = client[DATABASE]

#连接到集合(表):myDatabase.myCollection
COLLECTION = "makingStudentInformationClone"
db_coll = db[COLLECTION]

words = []
for x in db_coll.find({},{ "_id":1, "url": 0 }):
  words.append(x['jobTitle'])
  print(x['jobTitle'])

word = []
for x in words:
    word += x.split()

#convert list to string and generate
unique_string=(" ").join(word)
wordcloud = WordCloud(width = 1000, height = 500).generate(unique_string)
plt.figure(figsize=(15,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.savefig("your_file_name"+".png", bbox_inches='tight')
plt.show()
plt.close()
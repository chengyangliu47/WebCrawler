import pymongo
from pymongo import MongoClient
import datetime


MONGO_DB_URI = 'mongodb://localhost:27017'
MONGO_DB_NAME = 'test'

maxSevSelDelay = 1000  # Assume 1ms maximum server selection delay


def delete_single_database_repeat_data():
    client = MongoClient(MONGO_DB_URI)
    db = client.MONGO_DB_NAME
    maxSevSelDelay = 1000  # Assume 1ms maximum server selection delay
    client = pymongo.MongoClient("someInvalidURIOrNonExistantHost",
                                 serverSelectionTimeoutMS=maxSevSelDelay)
    client.server_info()
    client.close()
    collection = db.indeed
    posts = collection.posts
    print(posts.count_documents({}))
    for table in db.list_collection_names():
        print('table name is ', table)
        collection = db[table]
        for url in collection.distinct('gif_url'):  # 使用distinct方法，获取每一个独特的元素列表
            num = collection.count({"gif_url": url})  # 统计每一个元素的数量
            print(num)
            for i in range(1, num):  # 根据每一个元素的数量进行删除操作，当前元素只有一个就不再删除
                print('delete %s %d times ' % (url, i))
                # 注意后面的参数， 很奇怪，在mongo命令行下，它为1时，是删除一个元素，这里却是为0时删除一个
                collection.remove({"gif_url": url}, 0)
            for i in collection.find({"gif_url": url}):  # 打印当前所有元素
                print(i)


if __name__ == "__main__":
    print('start')
    client = MongoClient('localhost', 27017)
    db = client.MONGO_DB_NAME
    collection = db.test_collection
    post = {"author": "Mike",
            "text": "My first blog post!",
            "tags": ["mongodb", "python", "pymongo"],
            "date": datetime.datetime.utcnow()}
    posts = db.posts
    post_id = posts.insert_one(post).inserted_id
    print('finished')

## 1. pip install -r requirements.txt
## 2. cd yelp
## 3. scrapy crawl yielp_link_spider -a link=<YOUR_LINK> -o <FILE_NAME>.json

#### I didnt use proxy. But if it weren't for a test assignment I would have to use. (robot.txt does not give access - the site does not want me to parse it)
#### I did not do automatic saving to json because this is a test task, and as far as I understand not the best format for storing large amounts of data(SQL, NoSQL)
#
##### I saved some fields in the form in which I think it would be best
##### in some cases I just deleted extra data (realizing that there is no extra data)

##### It can be some problems to use python 3.8+ with Twisted, so use python 3.7
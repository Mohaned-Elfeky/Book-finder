from django.db import models

# Create your models here.
class Book:
    def __init__(self, title,author,thumbnail,publish_date,prev_link,read):
        self.title = title
        self.author = author
        self.thumbnail=thumbnail
        self.publish_date=publish_date
        self.prev_link=prev_link
        self.read=read
        
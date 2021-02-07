from django.shortcuts import render
import requests
from .models import Book
import os

# Create your views here.
def index(request):
    error=""
    books=[]
    api_key=os.environ['google_api_key']
    
    if 'submit' in request.GET:   # request from form
        title=request.GET["title"]
        if request.GET["author"] == "" :
          url="https://www.googleapis.com/books/v1/volumes?q="+title+"&key="+api_key
        else:
            author=request.GET["author"]
            url="https://www.googleapis.com/books/v1/volumes?q="+title+"+inauthor:"+author+"&key="+api_key
        
        
        response=requests.get(url)
        data=response.json()
        
        
        if('error' in data):  #api responded with error
            
            print("error")
            
        else:  #api provided data
            items=data["items"]
            
            for i in range(len(items)):
                curr=items[i]
                book=Book()
                book.title=curr["volumeInfo"]["title"]
                
                if "imageLinks" in curr["volumeInfo"]:
                    book.thumbnail=curr["volumeInfo"]["imageLinks"]["thumbnail"]
                else:
                    # book=Book(curr["volumeInfo"]["title"],curr["volumeInfo"]["authors"][0],
                    # "none",curr["volumeInfo"]["publishedDate"],curr["volumeInfo"]["previewLink"],curr["accessInfo"]["webReaderLink"])
                    book.thumbnail=""
                
                if "authors" in curr["volumeInfo"]:
                    book.author=curr["volumeInfo"]["authors"][0]
                else:
                    book.author="not available"
                    
                if "publishedDate" in curr["volumeInfo"]:
                    book.publish_date=curr["volumeInfo"]["publishedDate"]
                else:
                    book.publish_date="not available"
                
                book.prev_link= curr["volumeInfo"]["previewLink"]
                book.read=curr["accessInfo"]["webReaderLink"]
                      
                books.append(book)
                
            return render(request,"index.html",{"books":books})  
            
        
        return render(request,"index.html")   
        
        
    else:  #request without form
        return render(request,"index.html",{"books":books}) 
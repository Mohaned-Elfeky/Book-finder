from django.shortcuts import render
import requests
from .models import Book

# Create your views here.
def index(request):
    error=""
    books=[]
        
    if 'submit' in request.GET:   # request from form
        title=request.GET["title"]
        if request.GET["author"] == "" :
          url="https://www.googleapis.com/books/v1/volumes?q="+title+"&key=AIzaSyBhBb7Y2OWtKmzf-qSfQZX9cFV3yDg1mr0"
        else:
            author=request.GET["author"]
            url="https://www.googleapis.com/books/v1/volumes?q="+title+"+inauthor:"+author+"&key=AIzaSyBhBb7Y2OWtKmzf-qSfQZX9cFV3yDg1mr0"
        
        
        response=requests.get(url)
        data=response.json()
       
        
        if('error' in data):  #api responded with error
            
            print("error")
            
        else:  #api provided data
            items=data["items"]
            
            for i in range(len(items)):
                curr=items[i]
                if "imageLinks" in curr["volumeInfo"]:
                    book=Book(curr["volumeInfo"]["title"],curr["volumeInfo"]["authors"][0],
                    curr["volumeInfo"]["imageLinks"]["thumbnail"],curr["volumeInfo"]["publishedDate"],
                    curr["volumeInfo"]["previewLink"],curr["accessInfo"]["webReaderLink"])
                else:
                    book=Book(curr["volumeInfo"]["title"],curr["volumeInfo"]["authors"][0],
                    "none",curr["volumeInfo"]["publishedDate"],curr["volumeInfo"]["previewLink"],curr["accessInfo"]["webReaderLink"])
                books.append(book)
            return render(request,"index.html",{"books":books})  
            
        
        return render(request,"index.html")   
        
        
    else:  #request without form
        return render(request,"index.html",{"books":books}) 
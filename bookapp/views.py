from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import render,redirect
from .forms import BookForm,AuthorForm
# Create your views here.
from .models import Book, Author


# def createBook(request):
#     books = Book.objects.all()
#
#     if request.method=='POST':
#         title=request.POST.get('title')
#         price=request.POST.get('price')
#
#         book=Book(title=title,price=price)
#         book.save()
#
#     return render(request,'book.html',{'books':books})


def listBook(request):
    books=Book.objects.all().order_by('title')
    paginator= Paginator(books,4)
    page_number=request.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.page(page_number.num_pages)

    return render(request,'owner/listbook.html',{'books':books,'page':page})

def detailsView(request,book_id):
    book=Book.objects.get(id=book_id)
    return render(request,'owner/detailsview.html',{'book':book})

# def updateBook(request,book_id):
#     book=Book.objects.get(id=book_id)
#
#     if request.method=="POST":
#
#         title = request.POST.get('title')
#         price = request.POST.get('price')
#
#         book.title=title
#         book.price=price
#
#         book.save()
#
#         return redirect('/')
#     return render(request,'updateview.html',{'book':book})

def deleteView(request,book_id):
    book=Book.objects.get(id=book_id)

    if request.method=="POST":
        book.delete()

        return redirect('booklist')
    return render(request,'owner/deleteview.html',{'book':book})

def createBook(request):
    books=Book.objects.all()

    if request.method=='POST':
        form=BookForm(request.POST,files=request.FILES)

        if form.is_valid():
            form.save()
            return redirect('booklist')
    else:
        form = BookForm()
    return render(request,'owner/book.html',{'form':form,'books':books})

def Create_Author(request):
    authors=Author.objects.all()

    if request.method=='POST':
        form=AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('author')
    else:
        form=AuthorForm()
    return render(request,'owner/author.html',{'form':form,'authors':authors})

def updateBook(request,book_id):
    book=Book.objects.get(id=book_id)
    if request.method=='POST':
        form=BookForm(request.POST,files=request.FILES,instance=book)
        if form.is_valid():
            form.save()

            return redirect('booklist')
    else:
        form=BookForm(instance=book)
    return render(request,'owner/updateview.html',{'form':form})

def index(request):
    return render(request,'base.html')

def Search_Book(request):

    query=None
    books=None

    if 'q' in request.GET:

        query=request.GET.get('q')
        books=Book.objects.filter(Q(title__icontains=query))

    else:
        books=[]

    context={'books':books,'query':query}
    return render(request,'owner/search.html',context)

def deleteAuthor(request,author_id):
    author=Author.objects.get(id=author_id)

    if request.method=="POST":
        author.delete()

        return redirect('author')
    return render(request,'owner/deleteauthor.html',{'author':author})

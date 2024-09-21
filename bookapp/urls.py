from django.urls import path
from .import views


urlpatterns = [
    path("create-book",views.createBook,name='createbook'),
    path('author/',views.Create_Author,name='author'),
    path('ownerbook/',views.listBook,name='booklist'),
    path('detailsview/<int:book_id>/',views.detailsView,name='details'),
    path('updateview/<int:book_id>/',views.updateBook,name='update'),
    path('deleteview/<int:book_id>/',views.deleteView,name='delete'),
    path('deleteauthor/<int:author_id>/',views.deleteAuthor,name='deleteauthor'),
    path('index/',views.index),
    path('search/',views.Search_Book,name='search')
]


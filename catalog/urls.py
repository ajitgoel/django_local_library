from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	#path() function defines a pattern to match against the URL ('books/'), 
	# a view function that will be called if the URL matches (views.BookListView.as_view()), 
	#and a name for this particular mapping.
	#The generic view will query the database to get all records for the specified model (Book) 
	# then render a template located at /locallibrary/catalog/templates/catalog/book_list.html 
	#Within the template you can access the list of books with the template variable named object_list OR 
	# book_list (i.e. generically "the_model_name_list").
    path('books/', views.BookListView.as_view(), name='books'),
	#we use '<int:pk>' to capture the book id and pass it to the view as a parameter named pk. 
	#This is the id that is being used to store the book uniquely in the database, as defined in the Book Model.
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),

	path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [   
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]
urlpatterns += [   
    path('allborrowed/', views.LoanedBooksListView.as_view(), name='all-borrowed'),
]
urlpatterns += [   
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
    path('singlestripecharge/', views.SingleStripeChargeView, name='singlestripecharge'),
    path('singlestripepayment/', views.SingleStripePaymentView.as_view(), name='singlestripepayment'),
]
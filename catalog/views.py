from django.shortcuts import render
from catalog.models import Book, Author, BookInstance, Genre
from django.views.generic.base import TemplateView
from django.conf import settings
import stripe
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count() 
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    num_genres=Genre.objects.count()
    num_of_books_that_contain_book_word=Book.objects.filter(title__icontains='book').count()
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
		'num_genres':num_genres,
		'num_of_books_that_contain_book_word': num_of_books_that_contain_book_word,
        'num_visits': num_visits,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic
class BookListView(generic.ListView):
    model = Book
    paginate_by = 2

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 2

class AuthorDetailView(generic.DetailView):
    model = Author

# import and derive from LoginRequiredMixin, so that only a logged in user can call this view. 
from django.contrib.auth.mixins import LoginRequiredMixin
#Generic class-based view listing books on loan to current user
class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    # show "on loan" items for a user, oldest items displayed first.
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

from django.contrib.auth.mixins import PermissionRequiredMixin
#Generic class-based view listing books on loan
class LoanedBooksListView(PermissionRequiredMixin,generic.ListView):
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed.html'
    paginate_by = 10
    # show "on loan" items for all users, oldest items displayed first.
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

import datetime
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import RenewBookForm

#View function for renewing a specific BookInstance by librarian
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):    
    #get_object_or_404(): Returns a specified object from a model based on its primary key value, 
    # and raises an Http404 exception (not found) if the record does not exist. 
    book_instance = get_object_or_404(BookInstance, pk=pk)
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            #reverse() generates a URL from a URL configuration name and a set of arguments. 
            # It is the Python equivalent of the url tag that we've been using in our templates.
            return HttpResponseRedirect(reverse('all-borrowed') )
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
    context = {
        'form': form,
        'book_instance': book_instance,
    }
    return render(request, 'catalog/book_renew_librarian.html', context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author
class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}
class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

class SingleStripePaymentView(TemplateView):
    template_name = 'catalog/SingleStripePayment.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

def SingleStripeChargeView(request):
    if request.method == 'POST':
        charge = stripe.Charge.create(amount=500, currency='usd', 
        description='A Django charge', source=request.POST['stripeToken'])
    return render(request, 'catalog/SingleStripeCharge.html')

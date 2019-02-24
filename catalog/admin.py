from django.contrib import admin
from catalog.models import Author, Genre, Book, BookInstance, Language

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra=0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

class BooksInline(admin.TabularInline):
    model = Book
    extra=0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    inlines = [BooksInline]
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

admin.site.register(Genre)

#Adding borrower field to list_display and fieldsets=>Availability, will make the field visible 
# in the Admin section, allowing us to assign a User to a BookInstance when needed.
@admin.register(BookInstance) 
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )
admin.site.register(Language)
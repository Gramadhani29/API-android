import graphene
from graphene import ObjectType, String, Int, Boolean, Field, List
from models import Book as BookModel, Borrowing as BorrowingModel
from data import books, borrowings, get_next_book_id, get_next_borrowing_id
from datetime import datetime, timedelta

# GraphQL Types
class BookType(ObjectType):
    id = Int()
    title = String()
    author = String()
    isbn = String()
    category = String()
    available = Boolean()

class BorrowingType(ObjectType):
    id = Int()
    book_id = Int()
    borrower_name = String()
    borrow_date = String()
    due_date = String()
    return_date = String()
    status = String()
    book = Field(lambda: BookType)

    def resolve_book(self, info):
        return next((book for book in books if book.id == self.book_id), None)

# Queries
class Query(ObjectType):
    # Book queries
    books = List(BookType, available=Boolean())
    book = Field(BookType, id=Int(required=True))
    
    # Borrowing queries
    borrowings = List(BorrowingType, status=String())
    borrowing = Field(BorrowingType, id=Int(required=True))
    
    def resolve_books(self, info, available=None):
        if available is not None:
            return [book for book in books if book.available == available]
        return books
    
    def resolve_book(self, info, id):
        return next((book for book in books if book.id == id), None)
    
    def resolve_borrowings(self, info, status=None):
        if status:
            return [b for b in borrowings if b.status == status]
        return borrowings
    
    def resolve_borrowing(self, info, id):
        return next((b for b in borrowings if b.id == id), None)

# Mutations
class AddBook(graphene.Mutation):
    class Arguments:
        title = String(required=True)
        author = String(required=True)
        isbn = String(required=True)
        category = String(required=True)
    
    book = Field(lambda: BookType)
    
    def mutate(self, info, title, author, isbn, category):
        new_book = BookModel(
            id=get_next_book_id(),
            title=title,
            author=author,
            isbn=isbn,
            category=category,
            available=True
        )
        books.append(new_book)
        return AddBook(book=new_book)

class UpdateBook(graphene.Mutation):
    class Arguments:
        id = Int(required=True)
        title = String()
        author = String()
        isbn = String()
        category = String()
        available = Boolean()
    
    book = Field(lambda: BookType)
    
    def mutate(self, info, id, title=None, author=None, isbn=None, category=None, available=None):
        book = next((book for book in books if book.id == id), None)
        if not book:
            raise Exception("Book not found")
        
        if title is not None:
            book.title = title
        if author is not None:
            book.author = author
        if isbn is not None:
            book.isbn = isbn
        if category is not None:
            book.category = category
        if available is not None:
            book.available = available
        
        return UpdateBook(book=book)

class DeleteBook(graphene.Mutation):
    class Arguments:
        id = Int(required=True)
    
    success = Boolean()
    message = String()
    
    def mutate(self, info, id):
        book = next((book for book in books if book.id == id), None)
        if not book:
            return DeleteBook(success=False, message="Book not found")
        
        # Check if book is currently borrowed
        active_borrowing = next((b for b in borrowings if b.book_id == id and b.status == "borrowed"), None)
        if active_borrowing:
            return DeleteBook(success=False, message="Cannot delete book that is currently borrowed")
        
        books.remove(book)
        return DeleteBook(success=True, message="Book deleted successfully")

class BorrowBook(graphene.Mutation):
    class Arguments:
        book_id = Int(required=True)
        borrower_name = String(required=True)
        days = Int(default_value=14)
    
    borrowing = Field(lambda: BorrowingType)
    
    def mutate(self, info, book_id, borrower_name, days=14):
        # Check if book exists
        book = next((book for book in books if book.id == book_id), None)
        if not book:
            raise Exception("Book not found")
        
        # Check if book is available
        if not book.available:
            raise Exception("Book is not available")
        
        # Create borrowing record
        new_borrowing = BorrowingModel(
            id=get_next_borrowing_id(),
            book_id=book_id,
            borrower_name=borrower_name,
            borrow_date=datetime.now().isoformat(),
            due_date=(datetime.now() + timedelta(days=days)).isoformat(),
            status="borrowed"
        )
        
        # Update book availability
        book.available = False
        
        borrowings.append(new_borrowing)
        return BorrowBook(borrowing=new_borrowing)

class ReturnBook(graphene.Mutation):
    class Arguments:
        borrowing_id = Int(required=True)
    
    borrowing = Field(lambda: BorrowingType)
    
    def mutate(self, info, borrowing_id):
        # Find borrowing record
        borrowing = next((b for b in borrowings if b.id == borrowing_id), None)
        if not borrowing:
            raise Exception("Borrowing record not found")
        
        if borrowing.status != "borrowed":
            raise Exception("Book has already been returned")
        
        # Update borrowing record
        borrowing.return_date = datetime.now().isoformat()
        borrowing.status = "returned"
        
        # Update book availability
        book = next((book for book in books if book.id == borrowing.book_id), None)
        if book:
            book.available = True
        
        return ReturnBook(borrowing=borrowing)

class Mutation(ObjectType):
    # Book mutations
    add_book = AddBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()
    
    # Borrowing mutations
    borrow_book = BorrowBook.Field()
    return_book = ReturnBook.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

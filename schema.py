from ariadne import QueryType, MutationType, ObjectType, make_executable_schema
from data import books, borrowings, get_next_book_id, get_next_borrowing_id
from models import Book as BookModel, Borrowing as BorrowingModel
from datetime import datetime, timedelta

# Define GraphQL Schema
type_defs = """
    type Query {
        books(available: Boolean): [Book!]!
        book(id: Int!): Book
        borrowings(status: String): [Borrowing!]!
        borrowing(id: Int!): Borrowing
    }
    
    type Book {
        id: Int!
        title: String!
        author: String!
        isbn: String!
        category: String!
        available: Boolean!
    }
    
    type Borrowing {
        id: Int!
        bookId: Int!
        borrowerName: String!
        borrowDate: String!
        dueDate: String!
        returnDate: String
        status: String!
        book: Book
    }
    
    type Mutation {
        addBook(title: String!, author: String!, isbn: String!, category: String!): BookResponse!
        updateBook(id: Int!, title: String, author: String, isbn: String, category: String, available: Boolean): BookResponse!
        deleteBook(id: Int!): DeleteResponse!
        borrowBook(bookId: Int!, borrowerName: String!, days: Int): BorrowingResponse!
        returnBook(borrowingId: Int!): BorrowingResponse!
    }
    
    type BookResponse {
        book: Book
    }
    
    type BorrowingResponse {
        borrowing: Borrowing
    }
    
    type DeleteResponse {
        success: Boolean!
        message: String!
    }
"""

# Initialize type objects
query = QueryType()
mutation = MutationType()
borrowing_type = ObjectType("Borrowing")

# Query Resolvers
@query.field("books")
def resolve_books(_, info, available=None):
    if available is not None:
        return [book for book in books if book.available == available]
    return books

@query.field("book")
def resolve_book(_, info, id):
    return next((book for book in books if book.id == id), None)

@query.field("borrowings")
def resolve_borrowings(_, info, status=None):
    if status:
        return [b for b in borrowings if b.status == status]
    return borrowings

@query.field("borrowing")
def resolve_borrowing(_, info, id):
    return next((b for b in borrowings if b.id == id), None)

# Borrowing field resolvers
@borrowing_type.field("book")
def resolve_borrowing_book(borrowing, info):
    return next((book for book in books if book.id == borrowing.book_id), None)

# Mutation Resolvers
@mutation.field("addBook")
def resolve_add_book(_, info, title, author, isbn, category):
    new_book = BookModel(
        id=get_next_book_id(),
        title=title,
        author=author,
        isbn=isbn,
        category=category,
        available=True
    )
    books.append(new_book)
    return {"book": new_book}

@mutation.field("updateBook")
def resolve_update_book(_, info, id, title=None, author=None, isbn=None, category=None, available=None):
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
    
    return {"book": book}

@mutation.field("deleteBook")
def resolve_delete_book(_, info, id):
    book = next((book for book in books if book.id == id), None)
    if not book:
        return {"success": False, "message": "Book not found"}
    
    # Check if book is currently borrowed
    active_borrowing = next((b for b in borrowings if b.book_id == id and b.status == "borrowed"), None)
    if active_borrowing:
        return {"success": False, "message": "Cannot delete book that is currently borrowed"}
    
    books.remove(book)
    return {"success": True, "message": "Book deleted successfully"}

@mutation.field("borrowBook")
def resolve_borrow_book(_, info, bookId, borrowerName, days=14):
    # Check if book exists
    book = next((book for book in books if book.id == bookId), None)
    if not book:
        raise Exception("Book not found")
    
    # Check if book is available
    if not book.available:
        raise Exception("Book is not available")
    
    # Create borrowing record
    new_borrowing = BorrowingModel(
        id=get_next_borrowing_id(),
        book_id=bookId,
        borrower_name=borrowerName,
        borrow_date=datetime.now().isoformat(),
        due_date=(datetime.now() + timedelta(days=days)).isoformat(),
        status="borrowed"
    )
    
    # Update book availability
    book.available = False
    
    borrowings.append(new_borrowing)
    return {"borrowing": new_borrowing}

@mutation.field("returnBook")
def resolve_return_book(_, info, borrowingId):
    # Find borrowing record
    borrowing = next((b for b in borrowings if b.id == borrowingId), None)
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
    
    return {"borrowing": borrowing}

# Create executable schema
schema = make_executable_schema(type_defs, query, mutation, borrowing_type)

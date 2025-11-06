from datetime import datetime, timedelta

class Book:
    def __init__(self, id, title, author, isbn, category, available=True):
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.category = category
        self.available = available

class Borrowing:
    def __init__(self, id, book_id, borrower_name, borrow_date=None, due_date=None, return_date=None, status="borrowed"):
        self.id = id
        self.book_id = book_id
        self.borrower_name = borrower_name
        self.borrow_date = borrow_date or datetime.now().isoformat()
        self.due_date = due_date or (datetime.now() + timedelta(days=14)).isoformat()
        self.return_date = return_date
        self.status = status  # borrowed, returned, overdue

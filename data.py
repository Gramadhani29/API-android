from models import Book, Borrowing
from datetime import datetime, timedelta

# Data dummy untuk testing
books = [
    Book(1, "Laskar Pelangi", "Andrea Hirata", "978-979-22-2941-4", "Novel"),
    Book(2, "Bumi Manusia", "Pramoedya Ananta Toer", "978-979-22-3813-3", "Novel"),
    Book(3, "Python Programming", "John Smith", "978-1-59327-928-8", "Technology"),
    Book(4, "Clean Code", "Robert C. Martin", "978-0-13-235088-4", "Technology"),
    Book(5, "Design Patterns", "Gang of Four", "978-0-20163-361-0", "Technology"),
]

borrowings = [
    Borrowing(
        1, 
        book_id=1, 
        borrower_name="Ahmad Rizki",
        borrow_date=(datetime.now() - timedelta(days=5)).isoformat(),
        due_date=(datetime.now() + timedelta(days=9)).isoformat(),
        status="borrowed"
    ),
    Borrowing(
        2,
        book_id=3,
        borrower_name="Siti Nurhaliza",
        borrow_date=(datetime.now() - timedelta(days=20)).isoformat(),
        due_date=(datetime.now() - timedelta(days=6)).isoformat(),
        return_date=(datetime.now() - timedelta(days=3)).isoformat(),
        status="returned"
    ),
]

# Counter untuk ID auto-increment
book_counter = len(books) + 1
borrowing_counter = len(borrowings) + 1

def get_next_book_id():
    global book_counter
    book_counter += 1
    return book_counter - 1

def get_next_borrowing_id():
    global borrowing_counter
    borrowing_counter += 1
    return borrowing_counter - 1

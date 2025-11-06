# API GraphQL Manajemen Pinjam Buku

API GraphQL untuk sistem manajemen peminjaman buku perpustakaan yang dibangun dengan Python, Flask, dan Graphene.

## Fitur

- ✅ CRUD Buku (Create, Read, Update, Delete)
- ✅ Peminjaman Buku (dengan nama peminjam)
- ✅ Pengembalian Buku
- ✅ Tracking Status Peminjaman
- ✅ GraphiQL Interface untuk testing

## Teknologi

- Python 3.x
- Flask
- Graphene (GraphQL untuk Python)
- Flask-CORS
- Flask-GraphQL

## Instalasi

### Cara 1: Menggunakan Python Langsung

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Jalankan server:
```bash
python app.py
```

3. Akses GraphiQL interface di: http://localhost:5000/graphql

### Cara 2: Menggunakan Docker

1. Build dan jalankan dengan Docker Compose:
```bash
docker-compose up -d
```

2. Akses GraphiQL interface di: http://localhost:5000/graphql

3. Lihat logs:
```bash
docker-compose logs -f
```

4. Stop container:
```bash
docker-compose down
```

### Cara 3: Menggunakan Docker Manual

1. Build image:
```bash
docker build -t buku-graphql-api .
```

2. Jalankan container:
```bash
docker run -d -p 5000:5000 --name buku-api buku-graphql-api
```

3. Stop container:
```bash
docker stop buku-api
docker rm buku-api
```

## Contoh Query

### Query Semua Buku
```graphql
query {
  books {
    id
    title
    author
    isbn
    category
    available
  }
}
```

### Query Buku yang Tersedia
```graphql
query {
  books(available: true) {
    id
    title
    author
    available
  }
}
```

### Query Semua Peminjaman
```graphql
query {
  borrowings {
    id
    borrowerName
    borrowDate
    dueDate
    returnDate
    status
    book {
      title
      author
    }
  }
}
```

## Contoh Mutation

### Tambah Buku Baru
```graphql
mutation {
  addBook(
    title: "The Pragmatic Programmer"
    author: "Andrew Hunt"
    isbn: "978-0-13-595705-9"
    category: "Technology"
  ) {
    book {
      id
      title
      author
      available
    }
  }
}
```

### Update Buku
```graphql
mutation {
  updateBook(
    id: 1
    title: "Laskar Pelangi - Edisi Revisi"
    available: true
  ) {
    book {
      id
      title
      available
    }
  }
}
```

### Hapus Buku
```graphql
mutation {
  deleteBook(id: 5) {
    success
    message
  }
}
```

### Pinjam Buku
```graphql
mutation {
  borrowBook(
    bookId: 2
    borrowerName: "Ahmad Rizki"
    days: 14
  ) {
    borrowing {
      id
      borrowerName
      borrowDate
      dueDate
      status
      book {
        title
        available
      }
    }
  }
}
```

### Kembalikan Buku
```graphql
mutation {
  returnBook(borrowingId: 1) {
    borrowing {
      id
      returnDate
      status
      book {
        title
        available
      }
    }
  }
}
```

## Status Peminjaman

- `borrowed` - Buku sedang dipinjam
- `returned` - Buku sudah dikembalikan
- `overdue` - Buku terlambat dikembalikan (dapat diimplementasikan)

## Struktur Data

### Book (Buku)
- id: Int
- title: String
- author: String
- isbn: String
- category: String
- available: Boolean

### Borrowing (Peminjaman)
- id: Int
- bookId: Int
- borrowerName: String
- borrowDate: String
- dueDate: String
- returnDate: String (nullable)
- status: String

## Port

Default: http://localhost:5000

## License

MIT

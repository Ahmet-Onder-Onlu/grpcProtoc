# grpcurl Test Dokümantasyonu

Bu dokümanda tüm gRPC servislerinin `grpcurl` aracı ile test edilmesi için gerekli komutlar ve beklenen çıktılar yer almaktadır.

## Gereksinimler

- `grpcurl` aracı kurulu olmalıdır
- gRPC sunucu `localhost:50051` adresinde çalışıyor olmalıdır
- Reflection özelliği aktif olmalıdır (sunucuda etkinleştirin)

## BookService Testleri

### 1. Servisleri Listeleme
```bash
grpcurl -plaintext localhost:50051 list
```

**Beklenen Çıktı:**
```
university.BookService
university.StudentService  
university.LoanService
```

### 2. BookService Metotlarını Listeleme
```bash
grpcurl -plaintext localhost:50051 list university.BookService
```

**Beklenen Çıktı:**
```
university.BookService.CreateBook
university.BookService.DeleteBook
university.BookService.GetBook
university.BookService.ListBooks
university.BookService.UpdateBook
```

### 3. Kitapları Listeleme
```bash
grpcurl -plaintext -d '{"page_size": 10, "page_number": 1}' localhost:50051 university.BookService/ListBooks
```

**Beklenen Çıktı:**
```json
{
  "books": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Python Programming",
      "author": "John Doe",
      "isbn": "978-0134444321",
      "publisher": "Tech Books",
      "pageCount": 450,
      "stock": 5
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "title": "Data Structures",
      "author": "Jane Smith",
      "isbn": "978-0321573513",
      "publisher": "Academic Press",
      "pageCount": 600,
      "stock": 3
    }
  ],
  "totalCount": 2
}
```

### 4. Belirli Bir Kitabı Getirme
```bash
grpcurl -plaintext -d '{"id": "550e8400-e29b-41d4-a716-446655440000"}' localhost:50051 university.BookService/GetBook
```

### 5. Yeni Kitap Ekleme
```bash
grpcurl -plaintext -d '{
  "book": {
    "title": "Advanced gRPC",
    "author": "Tech Writer",
    "isbn": "978-1234567890",
    "publisher": "Tech Publications",
    "page_count": 400,
    "stock": 3
  }
}' localhost:50051 university.BookService/CreateBook
```

### 6. Kitap Güncelleme
```bash
grpcurl -plaintext -d '{
  "book": {
    "id": "BOOK_ID_HERE",
    "title": "Updated Book Title",
    "author": "Updated Author",
    "isbn": "978-1234567890",
    "publisher": "Updated Publisher",
    "page_count": 500,
    "stock": 5
  }
}' localhost:50051 university.BookService/UpdateBook
```

### 7. Kitap Silme
```bash
grpcurl -plaintext -d '{"id": "BOOK_ID_HERE"}' localhost:50051 university.BookService/DeleteBook
```

## StudentService Testleri

### 1. Öğrencileri Listeleme
```bash
grpcurl -plaintext -d '{"page_size": 10, "page_number": 1}' localhost:50051 university.StudentService/ListStudents
```

**Beklenen Çıktı:**
```json
{
  "students": [
    {
      "id": "student-uuid-1",
      "name": "Ali Veli",
      "studentNumber": "2021001",
      "email": "ali.veli@university.edu",
      "isActive": true
    },
    {
      "id": "student-uuid-2", 
      "name": "Ayşe Yılmaz",
      "studentNumber": "2021002",
      "email": "ayse.yilmaz@university.edu",
      "isActive": true
    }
  ],
  "totalCount": 2
}
```

### 2. Belirli Bir Öğrenciyi Getirme
```bash
grpcurl -plaintext -d '{"id": "STUDENT_ID_HERE"}' localhost:50051 university.StudentService/GetStudent
```

### 3. Yeni Öğrenci Ekleme
```bash
grpcurl -plaintext -d '{
  "student": {
    "name": "Fatma Demir",
    "student_number": "2024003",
    "email": "fatma.demir@university.edu",
    "is_active": true
  }
}' localhost:50051 university.StudentService/CreateStudent
```

### 4. Öğrenci Güncelleme
```bash
grpcurl -plaintext -d '{
  "student": {
    "id": "STUDENT_ID_HERE",
    "name": "Updated Name",
    "student_number": "2024999",
    "email": "updated@university.edu",
    "is_active": false
  }
}' localhost:50051 university.StudentService/UpdateStudent
```

### 5. Öğrenci Silme
```bash
grpcurl -plaintext -d '{"id": "STUDENT_ID_HERE"}' localhost:50051 university.StudentService/DeleteStudent
```

## LoanService Testleri

### 1. Ödünç Kayıtlarını Listeleme
```bash
grpcurl -plaintext -d '{"page_size": 10, "page_number": 1}' localhost:50051 university.LoanService/ListLoans
```

### 2. Belirli Bir Ödünç Kaydını Getirme
```bash
grpcurl -plaintext -d '{"id": "LOAN_ID_HERE"}' localhost:50051 university.LoanService/GetLoan
```

### 3. Yeni Ödünç Oluşturma
```bash
grpcurl -plaintext -d '{
  "student_id": "STUDENT_ID_HERE",
  "book_id": "BOOK_ID_HERE"
}' localhost:50051 university.LoanService/CreateLoan
```

**Beklenen Çıktı:**
```json
{
  "loan": {
    "id": "loan-uuid",
    "studentId": "student-uuid",
    "bookId": "book-uuid", 
    "loanDate": "2024-01-15",
    "returnDate": "",
    "status": "ONGOING"
  }
}
```

### 4. Kitap İade Etme
```bash
grpcurl -plaintext -d '{"loan_id": "LOAN_ID_HERE"}' localhost:50051 university.LoanService/ReturnBook
```

**Beklenen Çıktı:**
```json
{
  "loan": {
    "id": "loan-uuid",
    "studentId": "student-uuid",
    "bookId": "book-uuid",
    "loanDate": "2024-01-15", 
    "returnDate": "2024-01-20",
    "status": "RETURNED"
  }
}
```

## Hata Senaryoları

### 1. Olmayan Kitap Getirme (404)
```bash
grpcurl -plaintext -d '{"id": "non-existent-id"}' localhost:50051 university.BookService/GetBook
```

**Beklenen Hata:**
```
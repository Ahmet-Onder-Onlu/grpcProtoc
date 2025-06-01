import grpc
from concurrent import futures
import uuid
from datetime import datetime, date, timedelta
import university_pb2
import university_pb2_grpc

# Mock data storage
books_db = {}
students_db = {}
loans_db = {}

# Initialize with some sample data
def initialize_data():
    # Sample books
    book1 = university_pb2.Book(
        id=str(uuid.uuid4()),
        title="Python Programming",
        author="John Doe",
        isbn="978-0134444321",
        publisher="Tech Books",
        page_count=450,
        stock=5
    )
    book2 = university_pb2.Book(
        id=str(uuid.uuid4()),
        title="Data Structures",
        author="Jane Smith",
        isbn="978-0321573513",
        publisher="Academic Press",
        page_count=600,
        stock=3
    )
    books_db[book1.id] = book1
    books_db[book2.id] = book2
    
    # Sample students
    student1 = university_pb2.Student(
        id=str(uuid.uuid4()),
        name="Ali Veli",
        student_number="2021001",
        email="ali.veli@university.edu",
        is_active=True
    )
    student2 = university_pb2.Student(
        id=str(uuid.uuid4()),
        name="Ayşe Yılmaz",
        student_number="2021002",
        email="ayse.yilmaz@university.edu",
        is_active=True
    )
    students_db[student1.id] = student1
    students_db[student2.id] = student2

class BookServiceServicer(university_pb2_grpc.BookServiceServicer):
    def GetBook(self, request, context):
        book = books_db.get(request.id)
        if book:
            return university_pb2.GetBookResponse(book=book)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Book not found')
            return university_pb2.GetBookResponse()
    
    def ListBooks(self, request, context):
        all_books = list(books_db.values())
        page_size = request.page_size or 10
        page_number = request.page_number or 1
        
        start_idx = (page_number - 1) * page_size
        end_idx = start_idx + page_size
        
        books_page = all_books[start_idx:end_idx]
        
        return university_pb2.ListBooksResponse(
            books=books_page,
            total_count=len(all_books)
        )
    
    def CreateBook(self, request, context):
        book = request.book
        if not book.id:
            book.id = str(uuid.uuid4())
        
        books_db[book.id] = book
        return university_pb2.CreateBookResponse(book=book)
    
    def UpdateBook(self, request, context):
        book = request.book
        if book.id in books_db:
            books_db[book.id] = book
            return university_pb2.UpdateBookResponse(book=book)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Book not found')
            return university_pb2.UpdateBookResponse()
    
    def DeleteBook(self, request, context):
        if request.id in books_db:
            del books_db[request.id]
            return university_pb2.DeleteBookResponse(success=True, message="Book deleted successfully")
        else:
            return university_pb2.DeleteBookResponse(success=False, message="Book not found")

class StudentServiceServicer(university_pb2_grpc.StudentServiceServicer):
    def GetStudent(self, request, context):
        student = students_db.get(request.id)
        if student:
            return university_pb2.GetStudentResponse(student=student)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Student not found')
            return university_pb2.GetStudentResponse()
    
    def ListStudents(self, request, context):
        all_students = list(students_db.values())
        page_size = request.page_size or 10
        page_number = request.page_number or 1
        
        start_idx = (page_number - 1) * page_size
        end_idx = start_idx + page_size
        
        students_page = all_students[start_idx:end_idx]
        
        return university_pb2.ListStudentsResponse(
            students=students_page,
            total_count=len(all_students)
        )
    
    def CreateStudent(self, request, context):
        student = request.student
        if not student.id:
            student.id = str(uuid.uuid4())
        
        students_db[student.id] = student
        return university_pb2.CreateStudentResponse(student=student)
    
    def UpdateStudent(self, request, context):
        student = request.student
        if student.id in students_db:
            students_db[student.id] = student
            return university_pb2.UpdateStudentResponse(student=student)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Student not found')
            return university_pb2.UpdateStudentResponse()
    
    def DeleteStudent(self, request, context):
        if request.id in students_db:
            del students_db[request.id]
            return university_pb2.DeleteStudentResponse(success=True, message="Student deleted successfully")
        else:
            return university_pb2.DeleteStudentResponse(success=False, message="Student not found")

class LoanServiceServicer(university_pb2_grpc.LoanServiceServicer):
    def GetLoan(self, request, context):
        loan = loans_db.get(request.id)
        if loan:
            return university_pb2.GetLoanResponse(loan=loan)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Loan not found')
            return university_pb2.GetLoanResponse()
    
    def ListLoans(self, request, context):
        all_loans = list(loans_db.values())
        page_size = request.page_size or 10
        page_number = request.page_number or 1
        
        start_idx = (page_number - 1) * page_size
        end_idx = start_idx + page_size
        
        loans_page = all_loans[start_idx:end_idx]
        
        return university_pb2.ListLoansResponse(
            loans=loans_page,
            total_count=len(all_loans)
        )
    
    def CreateLoan(self, request, context):
        # Check if student exists
        if request.student_id not in students_db:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Student not found')
            return university_pb2.CreateLoanResponse()
        
        # Check if book exists and has stock
        book = books_db.get(request.book_id)
        if not book:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Book not found')
            return university_pb2.CreateLoanResponse()
        
        if book.stock <= 0:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details('Book out of stock')
            return university_pb2.CreateLoanResponse()
        
        # Create loan
        loan = university_pb2.Loan(
            id=str(uuid.uuid4()),
            student_id=request.student_id,
            book_id=request.book_id,
            loan_date=date.today().isoformat(),
            return_date="",
            status=university_pb2.ONGOING
        )
        
        # Update book stock
        book.stock -= 1
        books_db[book.id] = book
        
        loans_db[loan.id] = loan
        return university_pb2.CreateLoanResponse(loan=loan)
    
    def ReturnBook(self, request, context):
        loan = loans_db.get(request.loan_id)
        if not loan:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Loan not found')
            return university_pb2.ReturnBookResponse()
        
        if loan.status != university_pb2.ONGOING:
            context.set_code(grpc.StatusCode.FAILED_PRECONDITION)
            context.set_details('Loan is not ongoing')
            return university_pb2.ReturnBookResponse()
        
        # Update loan
        loan.return_date = date.today().isoformat()
        loan.status = university_pb2.RETURNED
        
        # Update book stock
        book = books_db.get(loan.book_id)
        if book:
            book.stock += 1
            books_db[book.id] = book
        
        loans_db[loan.id] = loan
        return university_pb2.ReturnBookResponse(loan=loan)

def serve():
    initialize_data()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    university_pb2_grpc.add_BookServiceServicer_to_server(BookServiceServicer(), server)
    university_pb2_grpc.add_StudentServiceServicer_to_server(StudentServiceServicer(), server)
    university_pb2_grpc.add_LoanServiceServicer_to_server(LoanServiceServicer(), server)
    
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    
    print(f"Starting gRPC server on {listen_addr}")
    server.start()
    
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop(0)

if __name__ == '__main__':
    serve()
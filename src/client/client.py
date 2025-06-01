import grpc
import university_pb2
import university_pb2_grpc
import uuid

def run_client():
    # Create a channel to the server
    with grpc.insecure_channel('localhost:50051') as channel:
        # Create stubs for each service
        book_stub = university_pb2_grpc.BookServiceStub(channel)
        student_stub = university_pb2_grpc.StudentServiceStub(channel)
        loan_stub = university_pb2_grpc.LoanServiceStub(channel)
        
        print("=" * 50)
        print("gRPC Client Testing")
        print("=" * 50)
        
        # Test Book Service
        print("\n1. Testing Book Service")
        print("-" * 30)
        
        # List books
        print("Listing books...")
        list_books_response = book_stub.ListBooks(university_pb2.ListBooksRequest(page_size=10, page_number=1))
        print(f"Found {list_books_response.total_count} books:")
        book_ids = []
        for book in list_books_response.books:
            print(f"  - {book.title} by {book.author} (ID: {book.id[:8]}...)")
            book_ids.append(book.id)
        
        # Get a specific book
        if book_ids:
            print(f"\nGetting book details for ID: {book_ids[0][:8]}...")
            get_book_response = book_stub.GetBook(university_pb2.GetBookRequest(id=book_ids[0]))
            book = get_book_response.book
            print(f"Book: {book.title}")
            print(f"Author: {book.author}")
            print(f"ISBN: {book.isbn}")
            print(f"Stock: {book.stock}")
        
        # Create a new book
        print("\nCreating a new book...")
        new_book = university_pb2.Book(
            title="gRPC in Action",
            author="Tech Author",
            isbn="978-1234567890",
            publisher="Tech Publisher",
            page_count=300,
            stock=2
        )
        create_book_response = book_stub.CreateBook(university_pb2.CreateBookRequest(book=new_book))
        created_book = create_book_response.book
        print(f"Created book: {created_book.title} (ID: {created_book.id[:8]}...)")
        
        # Test Student Service
        print("\n2. Testing Student Service")
        print("-" * 30)
        
        # List students
        print("Listing students...")
        list_students_response = student_stub.ListStudents(university_pb2.ListStudentsRequest(page_size=10, page_number=1))
        print(f"Found {list_students_response.total_count} students:")
        student_ids = []
        for student in list_students_response.students:
            print(f"  - {student.name} ({student.student_number}) - ID: {student.id[:8]}...")
            student_ids.append(student.id)
        
        # Get a specific student
        if student_ids:
            print(f"\nGetting student details for ID: {student_ids[0][:8]}...")
            get_student_response = student_stub.GetStudent(university_pb2.GetStudentRequest(id=student_ids[0]))
            student = get_student_response.student
            print(f"Student: {student.name}")
            print(f"Number: {student.student_number}")
            print(f"Email: {student.email}")
            print(f"Active: {student.is_active}")
        
        # Create a new student
        print("\nCreating a new student...")
        new_student = university_pb2.Student(
            name="Mehmet Özkan",
            student_number="2024001",
            email="mehmet.ozkan@university.edu",
            is_active=True
        )
        create_student_response = student_stub.CreateStudent(university_pb2.CreateStudentRequest(student=new_student))
        created_student = create_student_response.student
        print(f"Created student: {created_student.name} (ID: {created_student.id[:8]}...)")
        
        # Test Loan Service
        print("\n3. Testing Loan Service")
        print("-" * 30)
        
        # Create a loan
        if student_ids and book_ids:
            print("Creating a new loan...")
            create_loan_response = loan_stub.CreateLoan(
                university_pb2.CreateLoanRequest(
                    student_id=student_ids[0],
                    book_id=book_ids[0]
                )
            )
            created_loan = create_loan_response.loan
            print(f"Created loan: ID {created_loan.id[:8]}...")
            print(f"Student ID: {created_loan.student_id[:8]}...")
            print(f"Book ID: {created_loan.book_id[:8]}...")
            print(f"Loan Date: {created_loan.loan_date}")
            print(f"Status: {university_pb2.LoanStatus.Name(created_loan.status)}")
            
            # List loans
            print("\nListing loans...")
            list_loans_response = loan_stub.ListLoans(university_pb2.ListLoansRequest(page_size=10, page_number=1))
            print(f"Found {list_loans_response.total_count} loans:")
            for loan in list_loans_response.loans:
                status_name = university_pb2.LoanStatus.Name(loan.status)
                print(f"  - Loan ID: {loan.id[:8]}... - Status: {status_name}")
            
            # Return the book
            print(f"\nReturning book for loan ID: {created_loan.id[:8]}...")
            return_book_response = loan_stub.ReturnBook(
                university_pb2.ReturnBookRequest(loan_id=created_loan.id)
            )
            returned_loan = return_book_response.loan
            print(f"Book returned successfully!")
            print(f"Return Date: {returned_loan.return_date}")
            print(f"Status: {university_pb2.LoanStatus.Name(returned_loan.status)}")
        
        print("\n" + "=" * 50)
        print("Client testing completed successfully!")
        print("=" * 50)

if __name__ == '__main__':
    try:
        run_client()
    except grpc.RpcError as e:
        print(f"gRPC error: {e.code()} - {e.details()}")
    except Exception as e:
        print(f"Error: {e}")
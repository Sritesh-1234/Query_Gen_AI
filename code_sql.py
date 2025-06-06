import psycopg2
from psycopg2 import sql

# Define the connection parameters
connection_params = {
    'dbname': 'student_db_kbfo',
    'user': 'root',
    'password': 'Cp9iJlKiYux6RD5aI4Vp0K7s80mHbAXI',
    'host': 'dpg-cr1c0ijqf0us73fleeag-a.oregon-postgres.render.com',
    'port': '5432'
}

# Establish a connection to the PostgreSQL database
try:
    conn = psycopg2.connect(**connection_params)
    conn.autocommit = True  # Enable autocommit so that each command is executed immediately
    cur = conn.cursor()

    # SQL queries to create tables and insert data
    sql_queries = [
        """
        CREATE TABLE Students (
            student_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            date_of_birth DATE,
            gender VARCHAR(10) CHECK (gender IN ('Male', 'Female')),
            email VARCHAR(100)
        );
        """,
        """
        CREATE TABLE Courses (
            course_id SERIAL PRIMARY KEY,
            course_name VARCHAR(100),
            course_description TEXT,
            credits INT
        );
        """,
        """
        CREATE TABLE Enrollments (
            enrollment_id SERIAL PRIMARY KEY,
            student_id INT,
            course_id INT,
            enrollment_date DATE,
            FOREIGN KEY (student_id) REFERENCES Students(student_id),
            FOREIGN KEY (course_id) REFERENCES Courses(course_id)
        );
        """,
        """
        INSERT INTO Students (first_name, last_name, date_of_birth, gender, email) VALUES
        ('John', 'Doe', '2000-01-15', 'Male', 'john.doe@example.com'),
        ('Jane', 'Smith', '2001-02-20', 'Female', 'jane.smith@example.com'),
        ('Alice', 'Johnson', '1999-03-25', 'Female', 'alice.johnson@example.com'),
        ('Bob', 'Brown', '2002-04-30', 'Male', 'bob.brown@example.com');
        """,
        """
        INSERT INTO Courses (course_name, course_description, credits) VALUES
        ('Mathematics', 'An introduction to mathematical concepts and principles.', 3),
        ('Physics', 'Basic principles of physics and their applications.', 4),
        ('Chemistry', 'Fundamentals of chemistry and laboratory techniques.', 3),
        ('Computer Science', 'Introduction to programming and computer science.', 4);
        """,
        """
        INSERT INTO Enrollments (student_id, course_id, enrollment_date) VALUES
        (1, 1, '2023-08-01'),
        (1, 2, '2023-08-01'),
        (2, 3, '2023-08-01'),
        (3, 4, '2023-08-01'),
        (4, 1, '2023-08-01'),
        (4, 4, '2023-08-01');
        """,
        """
        SELECT * FROM Courses;
        """,
        """
        SELECT * FROM Enrollments;
        """,
        """
        SELECT * FROM Students;
        """
    ]

    # Execute each query
    for query in sql_queries:
        cur.execute(query)
        if query.strip().lower().startswith('select'):
            rows = cur.fetchall()
            for row in rows:
                print(row)

    cur.close()
    conn.close()

except psycopg2.Error as e:
    print(f"Error: {e}")
finally:
    if conn:
        conn.close()

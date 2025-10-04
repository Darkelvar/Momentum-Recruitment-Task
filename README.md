I implemented automatic migration for database in the docker-compose file, so only "docker-compose up" is required to start the app.

Address to the docs playground in browser: http://localhost:8000/docs#/

Available endpoints:
- [POST] /api/v1/books - used to create a book. serial_number, title and author are required. books are created with the status of borrowing automatically set to available (is_borrowed = false)
- [GET] /api/v1/books - used to get the list of all books
- [GET] /api/v1/books/{serial_number} – used to get the data of a single book
- [PUT] /api/v1/books/{serial_number} - used to change the  availability status of a book. is_borrowed is a required field, borrowed_at and borrowed_by are required if is_borrowed is being set to true. in case of setting is_borrowed to false, borrowed_at and by will automatically be nullified
- [DELETE] /api/v1/books/{serial_number} - used to delete a book

What I thought about implementing, but the task description didn't specify so I opted not to:
- setting the status of a book while creating it
- ability to edit a book's title and author
- filtering, pagination and limits for getting the book list
- tests.


# library_management
Simplistic borrower and member framework

1. Create a virtualenv using virtualenvwrapper: `mkvirtualenv lib_management`
2. Install requirements: `pip install -r requirements.txt`
3. Create database: `python db_create.py`
4. Create Migration: `python db_migrate.py`
5. `python run.py`

# Routes Expossed: </br>
## Members:</br>
`GET` /members/ - Returns all members </br>
`GET` /members/:id - Return member with given ID </br> 
`POST` /members/ - Creates member </br>
`{
	"username":"test",
	"email": "test7@gmail.com"
}`
</br>
`PUT` /members/:id - Updates member details 
<br>
`{
	"email": "test8@gmail.com"
}`
</br>
`DELETE` /members/:id - Deletes member</br>

## Books:</br>
`GET` /books/ - Returns all books </br>
`GET` /books/:id - Return book with given ID </br> 
`POST` /books/ - Add book </br>
`{
	"sku":"ita1",
	"title": "Introduction to algorithms",
	"count": 10
}`
</br>
`PUT` /books/:id - Updates book details 
<br>
`{
	"count": 20
}`
</br>
`DELETE` /books/:id - Deletes book</br>

## Borrow Book:</br>
`POST` /books/borrow/ - Borrow book </br>
`{
	"book_id":1,
	"member_id": 1
}`

## Return Book:</br>
`POST` /books/return/ - Return book </br>
`{
	"rented_id":1
}`

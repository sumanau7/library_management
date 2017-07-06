from app import app
from app import views

def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])


register_api(views.MembersAPI, 'members_api', '/members/', pk='member_id')
register_api(views.BooksAPI, 'books_api', '/books/', pk='book_id')
register_api(views.BorrowAPI, 'borrow_api', '/books/borrow/')
register_api(views.BookReturnAPI, 'return_api', '/books/return/', pk='rented_id')

if __name__ == '__main__':
    app.run(debug=True)
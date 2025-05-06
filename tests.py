from main import BooksCollector
import pytest

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test
class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()

    def test_initial_state(self, collector):
        assert collector.get_books_genre() == {}
        assert collector.get_list_of_favorites_books() == []

    def test_add_new_book_correct_add_book_successful_add(self, collector):
        collector.add_new_book('Азбука')
        assert collector.get_book_genre('Азбука') == ''
        assert len(collector.get_books_genre()) == 1
    
    def test_add_new_book_incorrect_add_book_unsuccessful_add(self, collector):
        collector.add_new_book('Азбука')
        assert len(collector.get_books_genre()) == 1
        collector.add_new_book('Азбука')
        assert len(collector.get_books_genre()) == 1
        collector.add_new_book('Азбука' * 10)
        assert len(collector.get_books_genre()) == 1

    def test_set_book_genre_correct_genre_success(self, collector):
        collector.add_new_book('Азбука')
        collector.set_book_genre('Азбука', 'Ужасы')
        assert collector.books_genre['Азбука'] == 'Ужасы'

    def test_set_book_genre_incorrect_genre_unsuccess(self, collector):
        collector.set_book_genre('Азбука', 'Ужасы')
        assert len(collector.books_genre) == 0
        collector.add_new_book('Азбука')
        collector.set_book_genre('Азбука', 'FFFFFF')
        assert collector.books_genre['Азбука'] == ''

    def test_get_book_genre(self, collector):
        collector.add_new_book('Азбука')
        collector.set_book_genre('Азбука', 'Ужасы')
        assert collector.get_book_genre('Азбука') == 'Ужасы'

    def test_get_books_with_specific_genre(self, collector):
        books = ['Азбука', 'Алгебра', 'Маленький принц']
        for book in books:
            collector.add_new_book(book)
            collector.set_book_genre(book, 'Ужасы')
        
        collector.add_new_book('Ну погоди')
        collector.set_book_genre('Ну погоди', 'Мультфильмы')

        assert len(collector.get_books_with_specific_genre('Ужасы')) == 3
        assert len(collector.get_books_with_specific_genre('Мультфильмы')) == 1

    def test_get_books_genre(self, collector):
        collector.add_new_book('Азбука')
        assert collector.get_books_genre() == {'Азбука': ''}

    def test_get_books_for_children(self, collector):
        books = ['детская1', 'детская2', 'детская3', 'взрослая1', 'взрослая2']
        genres = ['Фантастика', 'Мультфильмы', 'Комедии', 'Ужасы', 'Детективы']

        for i in range(len(books)):
            collector.add_new_book(books[i])
            collector.set_book_genre(books[i], genres[i])

        children_books = collector.get_books_for_children()
        assert len(children_books) == 3
        assert 'детская1' in children_books
        assert 'детская2' in children_books
        assert 'детская3' in children_books
        assert 'взрослая1' not in children_books
        assert 'взрослая2' not in children_books

    def test_add_book_in_favorites(self, collector):
        collector.add_book_in_favorites('Азбука')
        assert len(collector.get_books_genre()) == 0
        collector.add_new_book('Азбука')
        collector.add_book_in_favorites('Азбука')
        assert len(collector.get_books_genre()) == 1
        assert len(collector.favorites) == 1
        assert 'Азбука' in collector.favorites
        collector.add_book_in_favorites('Азбука')
        assert len(collector.favorites) == 1

    def test_delete_book_from_favorites(self, collector):
        collector.add_new_book('Азбука')
        collector.add_book_in_favorites('Азбука')
        collector.delete_book_from_favorites('Алгебра')
        assert len(collector.favorites) == 1
        assert 'Азбука' in collector.favorites
        collector.delete_book_from_favorites('Азбука')
        assert len(collector.favorites) == 0
        assert 'Азбука' not in collector.favorites

    def get_list_of_favorites_books(self, collector):
        collector.add_new_book('Азбука')
        collector.add_book_in_favorites('Азбука')
        collector.add_new_book('Алгебра')
        collector.add_book_in_favorites('Алгебра')
        assert len(collector.get_list_of_favorites_books()) == 2
        assert 'Азбука' in collector.get_list_of_favorites_books()
        assert 'Алгебра' in collector.get_list_of_favorites_books()
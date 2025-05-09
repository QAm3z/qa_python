import pytest

from main import BooksCollector


@pytest.fixture()
def collector():
    return BooksCollector()

class TestBooksCollector:

    def test_add_new_book_add_two_books(self, collector):
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        assert 'Книга 1' in collector.get_books_genre() and 'Книга 2' in collector.get_books_genre()

    @pytest.mark.parametrize(
        'name, genre',
        [
            ('Книга 1', 'Фантастика'),
            ('Книга 2', 'Мультфильмы'),
            ('Книга 3', 'Комедии'),
        ]
    )
    def test_set_book_genre_sets_correct_genre(self, collector, name, genre):
        collector.add_new_book(name)
        collector.set_book_genre(name, genre)
        assert collector.get_book_genre(name) == genre

    def test_get_book_genre_returns_empty_string_if_not_set(self, collector):
        collector.add_new_book('Книга 1')
        assert collector.get_book_genre('Книга 1') == ''

    def test_get_books_with_specific_genre_returns_correct_books(self, collector):
        collector.add_new_book('Книга 1')
        collector.set_book_genre('Книга 1', 'Комедии')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 2', 'Фантастика')
        assert collector.get_books_with_specific_genre('Комедии') == ['Книга 1']

    def test_get_books_genre_returns_correct_dict(self, collector):
        collector.add_new_book('Книга 1')
        collector.set_book_genre('Книга 1', 'Фантастика')
        assert collector.get_books_genre() == {'Книга 1': 'Фантастика'}

    def test_get_books_for_children_excludes_books_with_age_rating(self, collector):
        collector.add_new_book('Книга 1')
        collector.set_book_genre('Книга 1', 'Ужасы')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 2', 'Мультфильмы')
        assert collector.get_books_for_children() == ['Книга 2']

    def test_add_book_in_favorites_adds_only_once(self, collector):
        collector.add_new_book('Книга 1')
        collector.add_book_in_favorites('Книга 1')
        collector.add_book_in_favorites('Книга 1')
        assert collector.get_list_of_favorites_books() == ['Книга 1']

    def test_delete_book_from_favorites_removes_book(self, collector):
        collector.add_new_book('Книга 1')
        collector.add_book_in_favorites('Книга 1')
        collector.delete_book_from_favorites('Книга 1')
        assert collector.get_list_of_favorites_books() == []

    @pytest.mark.parametrize(
        'book_names',
        [
            (['Книга 1', 'Книга 2']),
            (['Книга 3', 'Книга 4']),
        ]
    )
    def test_get_list_of_favorites_books_returns_all_favorites(self, collector, book_names):
        for name in book_names:
            collector.add_new_book(name)
            collector.add_book_in_favorites(name)
        assert collector.get_list_of_favorites_books() == book_names

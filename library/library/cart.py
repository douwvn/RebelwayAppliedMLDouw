import json
from dataclasses import dataclass, field
from library.book import Book
from library.random_number_utils import RandomUtils
from library.file_io import Fstream

@dataclass
class Cart:
    database_path: str
    isEmpty: bool = True
    isActive: bool = False
    id: str = field(init=False, default_factory=RandomUtils.generate_random_id)

    def get_all_books(self, verbose=0)->dict:
        """
        Reads and returns a has map with all the available books

        Args:
            if verbose is set to 1, it will print all the books.

        Returns:
            dict: a hash map with all the books in the database.
        """
        data_file = Fstream.load_json_files(self.database_path)

        if len(data_file.items()) > 0:
            self.isEmpty = False
            self.isActive = True

        try:
            if verbose == 1:
                Fstream.print_json_structure(data_file)
                return data_file
            else:
                return data_file

        except:
            raise ValueError("The value for the verbose as to be 0 or 1")



    def search_books(self, query: str)->list[Book]:
        """
        """
        data = Fstream.load_json_files(self.database_path)
        matching_books = []
        for book_id, book_data in data["Books"].items():
            book = Book(title=book_data["title"], author=book_data["author"], category=book_data["category"], subcategory=book_data["subcategory"], id=book_id)
            if query.lower() in book.search_string.lower():
                matching_books.append(book)

        if len(matching_books) == 0:
            print("Not books found")

        else:
            for book in matching_books:
                print(f"Found: {book.title} {book.author} {book.category} {book.subcategory}")

        return matching_books

    def get_total_book_count(self)->int:
        """
        Returns the total number of Books in the cart.

        Returns:
            int: The total number of books in the cart.
        """
        data = self.get_all_books()
        return len(data["Books"].items())

    def add_book_to_cart(self, book: Book):
        """
        Adds a book to the cart and updates the database.json file.

        Args:
            book (Book): The book to add to the cart.
        """
        data = self.get_all_books()

        new_book = {
            "title": book.title,
            "author": book.author,
            "category": book.category,
            "subcategory": book.subcategory,
        }

        data["Books"][book.id] = new_book

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        self.isEmpty = False
        self.isActive = True

        print(f"Added {book.title} to the cart.")

    def remove_books_from_cart_by_query(self, query: str):
        """
        Removes all the instances of a book from the cart based on a query.

        Args:
            query (str): The search query to find the book to remove.
        """
        data = self.get_all_books()
        books_to_remove = []

        for book_id, book_data in data["Books"].items():
            if query.lower() in book_data["title"].lower() or query.lower() in book_data["author"].lower() or query.lower() in book_data["category"].lower()  or query.lower() in book_data["subcategory"].lower() :
                books_to_remove.append(book_id)

        if not books_to_remove:
            print(f"No books found matching '{query}'")
            return

        for book_id in books_to_remove:
            book_name = data["Books"][book_id]["title"]
            del data["Books"][book_id]
            print(f"Removed {book_name} from the cart.")

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        if not data["Books"]:
            self.isEmpty = True
            self.isActive = False

    def remove_books_from_cart_by_selection(self):
        """
        Removes the selected book by index.
        """

        data = self.get_all_books()
        books = []
        i = 1
        for book_id, book_data in data["Books"].items():
            books.append(book_id)
            print(f"{i}: {book_data}")
            i += 1
        try:
            usr_choice = int(input("Select the book to delete by number, example: 0: ")) - 1
        except:
            raise ValueError("You must select a valid number!")

        if usr_choice > len(books):
            print("Book not found!")
            return

        book_to_delete = books[usr_choice]
        book_name = data["Books"][book_to_delete]["title"]
        del data["Books"][book_to_delete]
        print(f"Removed {book_name} from the cart.")

        with open(self.database_path, 'w') as file:
            json.dump(data, file, indent=4)

        if not data["Books"]:
            self.isEmpty = True
            self.isActive = False


    def empty_cart(self):
        """
        Clear all the books in the cart.
        """
        data = self.get_all_items()
        if len(data["Books"].items()) > 0:
            data = {"Books":{}}

            with open(self.database_path, 'w') as file:
                json.dump(data, file, indent=4)

            if not data["Books"]:
                self.isEmpty = True
                self.isActive = False
            print("The cart is empty")
        else:
            print("The cart is already empty")


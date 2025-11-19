from library.book import Book
from library.cart import Cart

if __name__ == "__main__":

    #the main database for the cart to pass to the class
    database = "./database.json"
    my_cart = Cart(database)

    #search for an item
    print("Searching books...")
    results = my_cart.search_books("The Color of Magic")
    print("------------------------")




    #get the total amount of books in the cart
    print("Total books in the current cart:")
    total_item_count = my_cart.get_total_book_count()
    print(f"Total items count: {total_item_count}")

    print("------------------------")



    #Create a Book object so it can be added to the cart
    print("Adding books to the cart:...")
    print("------------------------")
    The_Da_Vinci_Code =     Book("The Da Vinci Code", "Dan Brown", "Fiction", "Thriller")
    my_cart.add_book_to_cart(The_Da_Vinci_Code)





    #get all the books in the cart
    print("------------------------")
    print("Getting all the items in the cart:")
    print("------------------------")
    my_cart.get_all_books(verbose=1)

    print("------------------------")


    

    #remove all books by title or category
    print("Removing all instances of a book:")
    print("------------------------")
    my_cart.remove_books_from_cart_by_query("Science")
    print("------------------------")
    print("\n")

  
    #removes a selected book
    print("Removing a specific book by selection:")
    print("------------------------")
    my_cart.remove_books_from_cart_by_selection()
    print("------------------------")




    print("All the current book in the cart:")
    my_cart.get_all_books(verbose=1)
    print("------------------------")



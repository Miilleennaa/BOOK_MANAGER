class Book:
    def __init__(self, id, author, title, publisher, year, copies, price):
        self.id = id
        self.author = author
        self.title = title
        self.publisher = publisher
        self.year = year
        self.copies = int(copies)
        self.price = float(price)

class BookShop:
    def __init__(self):
        self.books = []
        
    def load_from_file(self, filename):
        self.books = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(';')
                    if len(parts) == 6:
                        self.books.append(Book(
                            len(self.books) + 1,
                            parts[0].strip(),
                            parts[1].strip(),
                            parts[2].strip(),
                            parts[3].strip(),
                            parts[4].strip(),
                            parts[5].strip()
                        ))
                            
    def sort_by_copies(self, reverse=False):
        self.books.sort(key=lambda book: book.copies, reverse=reverse)
        
    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            for book in self.books:
                file.write(f"{book.author};{book.title};{book.publisher};"
                          f"{book.year};{book.copies};{book.price}\n")
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidgetItem, 
                             QPushButton, QMessageBox, QTableWidget, QInputDialog) 
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from book_classes import Book, BookShop

class BookManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            ui_path = os.path.join(os.path.dirname(__file__), "book_manager.ui")
            loadUi(ui_path, self)
        except FileNotFoundError:
            QMessageBox.critical(self, "Ошибка", 
                               f"Файл интерфейса 'book_manager.ui' не найден по пути: {ui_path}!")
            sys.exit(1)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки UI: {str(e)}")
            sys.exit(1) 
        self.book_shop = BookShop()
        self.filename = "book.txt"
        self.edit_mode = False
        self.setup_buttons()
        self.setup_table()
        
    def setup_buttons(self):
        """Проверяем наличие кнопок и подключаем сигналы"""
        self.pushButton_load.clicked.connect(self.load_and_display_data)
        self.Redact_Button.clicked.connect(self.toggle_edit_mode)
        self.pushButton_save.clicked.connect(self.save_to_file)
        self.pushButton_sort.clicked.connect(self.sort_by_copies)
        self.pushButton_add.clicked.connect(self.add_new_book)
        self.pushButton_delete.clicked.connect(self.delete_selected_book)
        self.pushButton_filter.clicked.connect(self.filter_data)
        self.pushButton_clear_filter.clicked.connect(self.clear_filter)
        
    def setup_table(self):
        """Настройка таблицы"""
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels([
            "ID", "Автор", "Название", "Издательство", "Год", "Экземпляры", "Цена"
        ])
        self.tableWidget.setRowCount(0)
        self.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.tableWidget.setSelectionMode(QTableWidget.SingleSelection)
        
    def toggle_edit_mode(self):
        """Переключение режима редактирования"""
        self.edit_mode = not self.edit_mode
        self.tableWidget.setEditTriggers(
            QTableWidget.AllEditTriggers if self.edit_mode 
            else QTableWidget.NoEditTriggers
        )
        self.Redact_Button.setText("Завершить" if self.edit_mode else "Редактировать")
        if not self.edit_mode:
            self.save_changes()
            QMessageBox.information(self, "Сохранено", "Изменения сохранены в памяти!")
            
    def load_and_display_data(self):
        """Загрузка и отображение данных"""
        try:
            if not os.path.exists(self.filename):
                QMessageBox.warning(self, "Предупреждение", f"Файл {self.filename} не найден!")
                return  
            self.book_shop.load_from_file(self.filename)
            self.display_books()
            QMessageBox.information(self, "Успех", "Данные успешно загружены!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при загрузке данных: {str(e)}")
            
    def display_books(self):
        """Отображение книг в таблице"""
        self.tableWidget.setRowCount(len(self.book_shop.books))
        for row, book in enumerate(self.book_shop.books):
            item = QTableWidgetItem(str(book.id))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.tableWidget.setItem(row, 0, item)
            
            self.tableWidget.setItem(row, 1, QTableWidgetItem(book.author))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(book.title))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(book.publisher))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(book.year))
            
            item = QTableWidgetItem(str(book.copies))
            item.setData(Qt.EditRole, book.copies)
            self.tableWidget.setItem(row, 5, item)
            
            item = QTableWidgetItem(f"{book.price:.2f}")
            item.setData(Qt.EditRole, book.price)
            self.tableWidget.setItem(row, 6, item)
        self.tableWidget.resizeColumnsToContents()
        
    def save_changes(self):
        """Сохранение изменений из таблицы в модель"""
        try:
            for row in range(self.tableWidget.rowCount()):
                book_id = int(self.tableWidget.item(row, 0).text())
                for book in self.book_shop.books:
                    if book.id == book_id:
                        book.author = self.tableWidget.item(row, 1).text()
                        book.title = self.tableWidget.item(row, 2).text()
                        book.publisher = self.tableWidget.item(row, 3).text()
                        book.year = self.tableWidget.item(row, 4).text()
                        book.copies = int(self.tableWidget.item(row, 5).text())
                        book.price = float(self.tableWidget.item(row, 6).text())
                        break
            return True
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении: {str(e)}")
            return False
            
    def save_to_file(self):
        """Сохранение данных в файл"""
        if not self.save_changes():
            return  
        try:
            self.book_shop.save_to_file(self.filename)
            QMessageBox.information(self, "Успех", "Данные успешно сохранены в файл!")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при сохранении в файл: {str(e)}")
            
    def sort_by_copies(self):
        """Сортировка по количеству экземпляров"""
        if not self.book_shop.books:
            QMessageBox.warning(self, "Предупреждение", "Нет данных для сортировки!")
            return   
        self.book_shop.sort_by_copies(reverse=True)
        self.display_books()
        QMessageBox.information(self, "Успех", "Данные отсортированы!")
        
    def add_new_book(self):
        """Добавление новой книги через диалоговые окна"""
        try:
            author, ok = QInputDialog.getText(self, 'Добавить книгу', 'Автор:')
            if not ok or not author:
                return           
            title, ok = QInputDialog.getText(self, 'Добавить книгу', 'Название:')
            if not ok or not title:
                return         
            publisher, ok = QInputDialog.getText(self, 'Добавить книгу', 'Издательство:')
            if not ok or not publisher:
                return        
            year, ok = QInputDialog.getText(self, 'Добавить книгу', 'Год издания:')
            if not ok or not year:
                return        
            copies, ok = QInputDialog.getInt(self, 'Добавить книгу', 'Количество экземпляров:', 1, 1, 10000)
            if not ok:
                return        
            price, ok = QInputDialog.getDouble(self, 'Добавить книгу', 'Цена:', 0, 0, 100000, 2)
            if not ok:
                return     
            new_id = max([book.id for book in self.book_shop.books], default=0) + 1
            new_book = Book(
                id=new_id,
                author=author,
                title=title,
                publisher=publisher,
                year=year,
                copies=copies,
                price=price
            )
            self.book_shop.books.append(new_book)  
            self.display_books()   
            QMessageBox.information(self, "Успех", "Книга успешно добавлена!")   
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при добавлении книги: {str(e)}")
            
    def delete_selected_book(self):
        """Удаление выбранной книги"""
        selected_rows = self.tableWidget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Предупреждение", "Пожалуйста, выберите книгу для удаления!")
            return
            
        row = selected_rows[0].row()
        book_id = int(self.tableWidget.item(row, 0).text())
        
        reply = QMessageBox.question(
            self, 'Подтверждение', 
            'Вы уверены, что хотите удалить эту книгу?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.book_shop.books = [book for book in self.book_shop.books if book.id != book_id]
            self.display_books()
            QMessageBox.information(self, "Успех", "Книга успешно удалена!")
            
    def filter_data(self):
        """Фильтрация данных по тексту"""
        filter_text, ok = QInputDialog.getText(self, "Фильтрация", "Введите текст для поиска:")
        if not ok or not filter_text:
            return
        
        for row in range(self.tableWidget.rowCount()):
            match = False
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item and filter_text.lower() in item.text().lower():
                    match = True
                    break
            
            self.tableWidget.setRowHidden(row, not match)
            
    def clear_filter(self):
        """Очистка фильтра и отображение всех книг"""
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHidden(row, False)
        QMessageBox.information(self, "Фильтр", "Фильтр сброшен, отображаются все книги.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookManagerApp()
    window.show()
    sys.exit(app.exec_())
import unittest
from laba6_web import app
from logic import items, add_item, next_id
import unittest

class FlaskAppTests(unittest.TestCase):

   def setUp(self):
      # Тестовий клієнт Flask
      self.client = app.test_client()

      # Очистка даних перед кожним тестом
      items.clear()
      global next_id
      next_id = 1

      # Початкові тестові дані
      add_item("Телефон", "Іван", 5000)
      add_item("Ноутбук", "Оксана", 12000)

   # ---------- Домашня сторінка ----------
   def test_home_page(self):
      response = self.client.get("/")
      self.assertEqual(response.status_code, 200)
      self.assertIn("Моя колекція речей", response.data)
      self.assertIn("Телефон", response.data)

   # ---------- Додавання ----------
   def test_add_item_route(self):
      response = self.client.post("/add", data={
            "name": "Книга",
            "owner": "Андрій",
            "value": "300"
      }, follow_redirects=True)

      self.assertEqual(response.status_code, 200)
      self.assertIn("Книга", response.data)
      self.assertEqual(len(items), 3)

   # ---------- Видалення ----------
   def test_delete_item(self):
      # ID першої речі = 1
      response = self.client.get("/delete/1", follow_redirects=True)

      self.assertEqual(response.status_code, 200)
      self.assertNotIn("Телефон", response.data)
      self.assertEqual(len(items), 1)

   def test_delete_not_found(self):
      response = self.client.get("/delete/999", follow_redirects=True)
      self.assertEqual(response.status_code, 200)
      # Просто перевірка, що сторінка відкрилась
      self.assertIn("Моя колекція речей", response.data)

   # ---------- Пошук ----------
   def test_search_found(self):
      response = self.client.get("/search?keyword=Тел")
      self.assertEqual(response.status_code, 200)
      self.assertIn("Телефон", response.data)
      self.assertIn("Результати пошуку", response.data)

   def test_search_by_id(self):
      response = self.client.get("/search?keyword=2")
      self.assertEqual(response.status_code, 200)
      self.assertIn("Ноутбук", response.data)

   def test_search_not_found(self):
      response = self.client.get("/search?keyword=qqq")
      self.assertEqual(response.status_code, 200)
      self.assertIn("не знайдена", response.data)


if __name__ == "__main__":
   unittest.main()
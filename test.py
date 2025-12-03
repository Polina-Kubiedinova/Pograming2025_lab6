import unittest
from laba6_web import app
from logic import items, add_item, next_id

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
      html = response.data.decode("utf-8")  # декодуємо bytes -> str
      self.assertIn("Моя колекція речей", html)
      self.assertIn("Телефон", html)

   # ---------- Додавання ----------
   def test_add_item_route(self):
      response = self.client.post("/add", data={
         "name": "Книга",
         "owner": "Андрій",
         "value": "300"
      }, follow_redirects=True)
      self.assertEqual(response.status_code, 200)
      html = response.data.decode("utf-8")
      self.assertIn("Книга", html)
      self.assertEqual(len(items), 3)

   # ---------- Видалення ----------
   def test_delete_item(self):
      response = self.client.get("/delete/1", follow_redirects=True)
      self.assertEqual(response.status_code, 200)
      html = response.data.decode("utf-8")
      self.assertNotIn("Телефон", html)
      self.assertEqual(len(items), 1)

   def test_delete_not_found(self):
      response = self.client.get("/delete/999", follow_redirects=True)
      self.assertEqual(response.status_code, 200)
      html = response.data.decode("utf-8")
      self.assertIn("Моя колекція речей", html)

   # ---------- Пошук ----------
   def test_search_found(self):
      response = self.client.get("/search?keyword=Тел")
      self.assertEqual(response.status_code, 200)
      html = response.data.decode("utf-8")
      self.assertIn("Телефон", html)
      self.assertIn("Результати пошуку", html)

   def test_search_by_id(self):
      response = self.client.get("/search?keyword=2")
      self.assertEqual(response.status_code, 200)
      html = response.data.decode("utf-8")
      self.assertIn("Ноутбук", html)

   def test_search_not_found(self):
      response = self.client.get("/search?keyword=qqq")
      self.assertEqual(response.status_code, 200)
      html = response.data.decode("utf-8")
      self.assertIn("не знайдена", html)

if __name__ == "main":
   unittest.main()
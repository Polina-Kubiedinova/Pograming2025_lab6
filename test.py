import unittest
from laba6_web import app
import logic


class TestLogic(unittest.TestCase):

   def setUp(self):
      """Очищуємо items перед кожним тестом"""
      logic.items.clear()
      logic.next_id = 1

   def test_add_item(self):
      result = logic.add_item("Телефон", "Іван", 5000)
      self.assertEqual(len(logic.items), 1)
      self.assertEqual(logic.items[0]["name"], "Телефон")
      self.assertIn("Додано", result)

   def test_add_duplicate_item(self):
      logic.add_item("Телефон", "Іван", 5000)
      result = logic.add_item("Телефон", "Іван", 5000)
      self.assertEqual(result.strip(), "Така річ вже існує")
      self.assertEqual(len(logic.items), 1)

   def test_remove_item_by_id(self):
      logic.add_item("Телефон", "Іван", 5000)
      result = logic.remove_item_by_id(1)
      self.assertEqual(len(logic.items), 0)
      self.assertIn("Видалено", result)

   def test_remove_item_not_found(self):
      result = logic.remove_item_by_id(123)
      self.assertIn("не знайдена", result)

   def test_total_value(self):
      logic.add_item("Телефон", "Іван", 5000)
      logic.add_item("Ноутбук", "Оксана", 10000)
      result = logic.total_value()
      self.assertIn("15000 грн", result)

   def test_search_item_by_name(self):
      logic.add_item("Телефон", "Іван", 5000)
      html = logic.search_item("тел")
      self.assertIn("Телефон", html)
      self.assertIn("5000", html)

   def test_search_item_by_id(self):
      logic.add_item("Ноутбук", "Оксана", 12000)
      html = logic.search_item("1")
      self.assertIn("Ноутбук", html)
      self.assertIn("12000", html)


if __name__ == "__main__":
   unittest.main()
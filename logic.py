items = []
next_id = 1


# ------------------- ФУНКЦІЇ -------------------
def add_item(name, owner, value):
   global next_id
   for item in items:
      if item["name"] == name and item["owner"] == owner and item["value"] == value:
            return " Така річ вже існує"
   item = {"id": next_id, "name": name, "owner": owner, "value": value}
   items.append(item)
   next_id += 1
   return f" Додано: {item}"


def remove_item_by_id(item_id):
   for item in items:
      if item["id"] == item_id:
            items.remove(item)
            return f" Видалено: {item}"
   return f" Річ з ID {item_id} не знайдена"


def show_items():
   if not items:
      return "<p>Список речей порожній</p>"
   html = "<table border='1' cellpadding='6' style='border-collapse:collapse; background:white;'>"
   html += "<tr><th>ID</th><th>Назва</th><th>Власник</th><th>Вартість</th><th>Дії</th></tr>"
   for item in items:
      html += f"<tr><td>{item['id']}</td><td>{item['name']}</td><td>{item['owner']}</td><td>{item['value']} грн</td>"
      html += f"<td><a href='/delete/{item['id']}'>Видалити</a></td></tr>"
   html += "</table>"
   return html


def search_item(keyword):
   results = [item for item in items
   if keyword.lower() in item["name"].lower() or str(item["id"]) == str(keyword)]
   if results:
      html = f"<h3> Результати пошуку за '{keyword}':</h3><ul>"
      for item in results:
            html += f"<li>ID: {item['id']}, {item['name']} — {item['value']} грн</li>"
      html += "</ul>"
   else:
      html = f"<p> Річ з ключовим словом '{keyword}' не знайдена.</p>"
   html += "<p><a href='/'>⬅ Повернутись</a></p>"
   return html


def total_value():
   if not items:
      return "Список порожній, загальна вартість = 0 грн"
   total = sum(item["value"] for item in items)
   return f" Загальна оціночна вартість: {total} грн"

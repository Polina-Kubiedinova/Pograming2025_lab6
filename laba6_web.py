from flask import Flask, request, redirect
from logic import add_item, remove_item_by_id, search_item, show_items, total_value, items, next_id
app = Flask(__name__)



# ------------------- ВЕБ-СТОРІНКИ -------------------
@app.route("/")
def home():
   html = """
   <html>
   <head>
      <title>Моя колекція речей</title>
      <style>
            body { font-family: Arial; margin: 40px; background-color: #f9f9f9; }
            h1 { color: #333; }
            form { background: white; padding: 15px; margin-top: 20px; border-radius: 10px; width: fit-content; }
            input, button { margin: 5px; padding: 8px; }
      </style>
   </head>
   <body>
      <h1> Моя колекція речей</h1>
   """
   html += show_items()
   html += f"<p><b>{total_value()}</b></p>"

   html += """
      <h3> Додати річ</h3>
      <form action="/add" method="post">
            Назва: <input name="name" required>
            Власник: <input name="owner" required>
            Вартість: <input name="value" type="number" required>
            <button type="submit">Додати</button>
      </form>

      <h3> Пошук</h3>
      <form action="/search" method="get">
            Ключове слово або ID: <input name="keyword" required>
            <button type="submit">Шукати</button>
      </form>
   </body></html>
   """
   return html


@app.route("/add", methods=["POST"])
def add():
   name = request.form["name"]
   owner = request.form["owner"]
   value = int(request.form["value"])
   add_item(name, owner, value)
   return redirect("/")


@app.route("/delete/<int:item_id>")
def delete(item_id):
   remove_item_by_id(item_id)
   return redirect("/")


@app.route("/search")
def search():
   keyword = request.args.get("keyword", "")
   return search_item(keyword)


# ------------------- ЗАПУСК -------------------
if __name__ == "__main__":
   # Початкові дані (як у консолі)
   add_item("Телефон", "Іван", 5000)
   add_item("Ноутбук", "Оксана", 12000)
   add_item("Телефон", "Петро", 7000)

   app.run(host="0.0.0.0", port=5000)
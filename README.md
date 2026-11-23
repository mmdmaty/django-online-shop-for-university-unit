<div align="center">

# 🛒 Django Online Store

A Django-based e-commerce website with **semantic product search** powered by embeddings and a vector database.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)
![Vector DB](https://img.shields.io/badge/Vector%20DB-...-orange)

</div>

---

## ✨ Features

- Product catalog with categories, product pages and shopping cart
- User authentication and order management
- **Semantic search**: finds relevant products by meaning, not just exact keywords
- Admin panel for managing products and orders

## 🔍 How the Search Works

1. When a product is added, its name is converted to a vector using an embedding model and stored in the vector database.
2. When a user searches, the query is converted to a vector with the same model.
3. The vector database returns the products closest to the query vector, ranked by similarity.

This means a search like "laptop bag" can also match products named "notebook backpack".

```
Product name ──► Embedding model ──► Vector DB
                                         ▲
User query ───► Embedding model ─────────┘  (similarity search)
```

## 🧰 Tech Stack

| Layer      | Technology        |
| ---------- | ----------------- |
| Backend    | Django            |
| Database   | ...               |
| Search     | Embedding model + ... (Vector DB) |
| Frontend   | HTML, CSS, JS     |

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/<username>/<repo>.git
cd <repo>

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env

# 5. Run migrations and start the server
python manage.py migrate
python manage.py runserver
```

To index existing products into the vector database:

```bash
python manage.py <your_index_command>
```


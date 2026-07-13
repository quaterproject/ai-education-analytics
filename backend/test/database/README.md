sql = postgress-sql
no-sql = mongo-db
vector db = qdrant

sqlalchemy psycopg[binary]

uvicorn app:app --reload

cmd = curl -X GET ^
"http://127.0.0.1:8000/" ^
-H "accept: application/json"

DATABASE_URI="postgresql://postgres:YOUR_PASSWORD_HERE@localhost:5432/YOUR_DB_NAME"
uv add "fastapi[standard]" psycopg[binary] sqlalchemy python-dotenv

```
add this in url = """+psycopg:"""
postgresql+psycopg://
```

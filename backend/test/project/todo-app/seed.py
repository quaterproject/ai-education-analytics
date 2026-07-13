from database import Base, SessionLocal, engine
from models import Todo

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)


def seed_database():
    db = SessionLocal()

    try:
        # Don't seed again if data already exists
        if db.query(Todo).first():
            print("Database already contains data. Skipping seed.")
            return

        todos = [
            Todo(title="Learn FastAPI", completed=False),
            Todo(title="Learn SQLAlchemy", completed=True),
            Todo(title="Build REST API", completed=False),
            Todo(title="Connect PostgreSQL", completed=True),
            Todo(title="Write Unit Tests", completed=False),
        ]

        db.add_all(todos)
        db.commit()

        print(f"Inserted {len(todos)} todos successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
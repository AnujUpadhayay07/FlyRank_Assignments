from app.db.database import SessionLocal
from app.models.submission import Sale


db = SessionLocal()

sales = [
    Sale(customer_name="Rahul", product="Laptop", amount=50000, status="completed"),
    Sale(customer_name="Ankit", product="Mouse", amount=1500, status="completed"),
    Sale(customer_name="Priya", product="Laptop", amount=55000, status="pending"),
    Sale(customer_name="Neha", product="Keyboard", amount=2500, status="completed"),
    Sale(customer_name="Ravi", product="Monitor", amount=15000, status="completed"),
    Sale(customer_name="Pooja", product="Mouse", amount=1800, status="pending"),
    Sale(customer_name="Aman", product="Laptop", amount=60000, status="completed"),
]


db.add_all(sales)
db.commit()

print("Sample data inserted successfully!")

db.close()
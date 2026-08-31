from sqlalchemy import func
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.db.database import SessionLocal
from app.models.submission import Sale


def get_report_data():
    db = SessionLocal()

    total_sales = db.query(func.count(Sale.id)).scalar()

    total_revenue = db.query(func.sum(Sale.amount)).scalar()

    completed_sales = (
        db.query(func.count(Sale.id))
        .filter(Sale.status == "completed")
        .scalar()
    )

    pending_sales = (
        db.query(func.count(Sale.id))
        .filter(Sale.status == "pending")
        .scalar()
    )

    product_summary = (
        db.query(
            Sale.product,
            func.count(Sale.id).label("sales_count"),
            func.sum(Sale.amount).label("revenue")
        )
        .group_by(Sale.product)
        .all()
    )

    product_summary = [
        {
            "product": row.product,
            "sales_count": row.sales_count,
            "revenue": row.revenue
        }
        for row in product_summary
    ]

    db.close()

    return {
        "total_sales": total_sales,
        "total_revenue": total_revenue or 0,
        "completed_sales": completed_sales,
        "pending_sales": pending_sales,
        "product_summary": product_summary
    }


def generate_pdf_report(file_path):
    data = get_report_data()

    pdf = canvas.Canvas(file_path, pagesize=A4)

    width, height = A4

    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(50, height - 50, "Sales Report")

    pdf.setFont("Helvetica", 12)

    y = height - 100

    pdf.drawString(50, y, f"Total Sales: {data['total_sales']}")
    y -= 25

    pdf.drawString(50, y, f"Total Revenue: Rs. {data['total_revenue']}")
    y -= 25

    pdf.drawString(50, y, f"Completed Sales: {data['completed_sales']}")
    y -= 25

    pdf.drawString(50, y, f"Pending Sales: {data['pending_sales']}")
    y -= 50

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Product Summary")

    y -= 30

    pdf.setFont("Helvetica-Bold", 11)

    pdf.drawString(50, y, "Product")
    pdf.drawString(200, y, "Sales")
    pdf.drawString(300, y, "Revenue")

    y -= 20

    pdf.setFont("Helvetica", 11)

    for product in data["product_summary"]:
        pdf.drawString(50, y, product["product"])
        pdf.drawString(200, y, str(product["sales_count"]))
        pdf.drawString(300, y, f"Rs. {product['revenue']}")

        y -= 20

    pdf.save()

    return file_path
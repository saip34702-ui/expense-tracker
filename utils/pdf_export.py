from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.flowables import PageBreak
from database import db


def export_pdf(user_id):

    data = db.get_expenses(user_id)

    pdf = SimpleDocTemplate("expense_report.pdf")

    elements = []

    styles = getSampleStyleSheet()

    title = Paragraph("Expense Report", styles['Title'])

    elements.append(title)
    elements.append(Spacer(1, 20))

    table_data = [["Date", "Category", "Amount"]]

    total = 0

    for row in data:

        table_data.append([
            row[2],
            row[3],
            f"₹ {row[4]}"
        ])

        total += float(row[4])

    table_data.append([
        "",
        "TOTAL",
        f"₹ {int(total)}"
    ])

    table = Table(table_data, colWidths=[150, 150, 150])

    style = TableStyle([

        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

        ('GRID', (0, 0), (-1, -1), 1, colors.black),

        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),

    ])

    table.setStyle(style)

    elements.append(table)

    pdf.build(elements)

    print("PDF Exported!")
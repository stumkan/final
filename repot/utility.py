# views.py

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import green, gray


def header_footer(canvas, doc):
    canvas.saveState()
    # Footer
    canvas.setFont("Helvetica", 10)
    canvas.setFillColor(gray)
    footer_text = "This is a confidential report created by 10db Studios. All rights reserved."
    canvas.drawString(30, 20, footer_text)
    canvas.restoreState()


def generate_fault_report(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="fault_report.pdf"'

    # Set up the document
    doc = BaseDocTemplate(
        response,
        pagesize=letter,
        rightMargin=30,
        leftMargin=30,
        topMargin=70,
        bottomMargin=40
    )

    # Create a frame (content area) excluding header/footer
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height - 50,  # Leave space for footer
        id='normal'
    )

    # Define a page template with the frame and header/footer function
    template = PageTemplate(id='report_template', frames=frame, onPage=header_footer)
    doc.addPageTemplates([template])

    # Create the content
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='GreenTitle', fontSize=24, textColor=green, spaceAfter=20, alignment=1))  # Center alignment
    styles.add(ParagraphStyle(name='Body', fontSize=12, spaceAfter=12))

    elements = []

    # Add the title
    title = Paragraph("Fault Report", styles['GreenTitle'])
    elements.append(title)

    # Add the first div content
    div1 = Paragraph("The report contents will come here.", styles['Body'])
    elements.append(div1)
    elements.append(Spacer(1, 20))

    # Add the second div content
    div2 = Paragraph("The conclusions will come here.", styles['Body'])
    elements.append(div2)

    # Build the document
    doc.build(elements)

    return response

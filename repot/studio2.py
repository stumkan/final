from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.colors import Color, gray

def header_footer(canvas, doc):
    """
    Function to create a consistent header and footer.
    """
    canvas.saveState()
    
    # Footer
    footer_text = "This is a confidential report created by 10db Studios. All rights reserved."
    canvas.setFont("Helvetica", 10)
    canvas.setFillColor(gray)
    canvas.drawString(30, 20, footer_text)  # Positioned at 20 units from the bottom
    
    canvas.restoreState()

def set_background(canvas, doc):
    """
    Function to set the background color of the page.
    """
    background_color = Color(221/255, 210/255, 195/255)  # Create a Color object for the background
    canvas.setFillColor(background_color)
    canvas.rect(0, 0, *letter, stroke=0, fill=1)  # Fill the entire page

def generate_fault_report(file_path, fault_ref, fault_start, fault_end, fault_duration, events, conclusion):
    """
    Function to generate a fault report PDF with a consistent header, footer, background color, and a logo.
    """
    # Create a document template
    doc = BaseDocTemplate(file_path, pagesize=letter)
    
    # Define the frame for the content
    frame = Frame(
        30,  # Left margin
        50,  # Bottom margin
        letter[0] - 60,  # Width
        letter[1] - 100,  # Height (leave space for header and footer)
        id='normal'
    )
    
    # Add a page template with the background, header, and footer
    doc.addPageTemplates([
        PageTemplate(id='content', frames=[frame], onPage=set_background, onPageEnd=header_footer)
    ])
    
    # Get styles
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    title_style = styles['Title']
    heading3_style = styles['Heading3']
    
    # Increase font sizes
    title_style.fontSize = 20
    title_style.textColor = Color(18/255, 96/255, 8/255)  # Heading color
    
    heading3_style.fontSize = 16
    heading3_style.textColor = Color(18/255, 96/255, 8/255)  # Heading color
    
    normal_style.fontSize = 14  # Increase normal text size
    
    # Build the report content
    content = []
    content.append(Paragraph("10dB Studios Fault Report", title_style))
    content.append(Spacer(1, 0.5 * inch))
    
    # Add the logo
    logo_path = "logo.png"  # Ensure this path points to your logo file
    logo = Image(logo_path)
    logo.drawHeight = 1.0 * inch  # Set logo height
    logo.drawWidth = 1.0 * inch  # Set logo width
    content.append(logo)
    content.append(Spacer(1, 0.5 * inch))
    
    # Fault stats
    content.append(Paragraph(f"<b>Fault Ref:</b> {fault_ref}", normal_style))
    content.append(Paragraph(f"<b>Fault Start:</b> {fault_start}", normal_style))
    content.append(Paragraph(f"<b>Fault End:</b> {fault_end}", normal_style))
    content.append(Paragraph(f"<b>Fault Duration:</b> {fault_duration}", normal_style))
    content.append(Spacer(1, 0.25 * inch))
    
    # Events
    content.append(Paragraph("Fault Events", heading3_style))
    content.append(Paragraph(events, normal_style))
    content.append(Spacer(1, 0.5 * inch))
    
    # Conclusion
    content.append(Paragraph("Fault Conclusion", heading3_style))
    content.append(Paragraph(conclusion, normal_style))
    
    # Build the document
    doc.build(content)

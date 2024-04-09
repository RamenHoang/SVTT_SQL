from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
import os

def add_text_to_pdf(input_pdf_path: str, output_pdf_path: str, data: dict, username: str):
    # Đọc file PDF đầu vào
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Lấy số lượng trang của PDF
    num_pages = len(reader.pages)

    # Tải font Times New Roman hỗ trợ tiếng Việt
    pdfmetrics.registerFont(TTFont('Times_New_Roman', 'times.ttf'))

    # Tạo một trang mới với reportlab
    c = canvas.Canvas("temp.pdf")
    c.setFont("Times_New_Roman", 12)
    c.drawString(150, 721, data['student_fullname'])
    c.drawString(75, 700, data['student_class'])
    c.drawString(125, 680, "Trung tâm CNTT - VNPT Vĩnh Long")
    c.drawString(183, 659, data['mentor_fullname'])
    c.drawString(256, 622, data['r1_text'])
    c.drawString(195, 591, data['r2_text'])
    c.drawString(151, 563, data['r3_text'])
    c.drawString(170, 535, data['r4_text'])
    c.drawString(232, 507, data['r5_text'])
    c.drawString(225, 480, data['r6_text'])
    c.drawString(99, 433, data['r7_text'])
    c.drawString(73, 345, data['r1_number'])
    c.drawString(133, 345, data['r2_number'])
    c.drawString(193, 345, data['r3_number'])
    c.drawString(253, 345, data['r4_number'])
    c.drawString(315, 345, data['r5_number'])
    c.drawString(375, 345, data['r6_number'])
    c.drawString(435, 345, data['r7_number'])
    c.drawString(500, 345, data['r8_number'])
    c.drawString(75, 170, data['mentor_fullname'])
    c.save()

    # Đọc trang mới được tạo
    new_page = PdfReader("temp.pdf").pages[0]

    # Duyệt qua từng trang và thêm văn bản
    for page in reader.pages:
        page.merge_page(new_page)
        writer.add_page(page)

    output_path = os.path.join('DOCX', username)
    os.makedirs(output_path, exist_ok=True)

    # Ghi tệp PDF đầu ra
    with open(os.path.join(output_path, output_pdf_path), 'wb') as output_pdf:
        writer.write(output_pdf)

    return os.path.join(output_path, output_pdf_path)

# if __name__=="__main__":
#     data: dict = {
#         "student_fullname": "Phan Thanh Giảng",
#         "student_class": "DI16Z6A2",
#         "mentor_fullname": "Phan Thanh Giảng",
#         "r1_text": "Tốt",
#         "r2_text": "Tốt",
#         "r3_text": "Tốt",
#         "r4_text": "Tốt",
#         "r5_text": "Tốt",
#         "r6_text": "Tốt",
#         "r7_text": "Tốt",
#         "r1_number": "100",
#         "r2_number": "100",
#         "r3_number": "100",
#         "r4_number": "100",
#         "r5_number": "100",
#         "r6_number": "100",
#         "r7_number": "100",
#         "r8_number": "100"
#     }
#     # Đường dẫn tới file PDF đầu vào và file PDF đầu ra
#     input_pdf_path = 'phieudanhgia_vlute.pdf'
#     output_pdf_path = 'output.pdf'
#     # Thêm văn bản vào PDF
#     add_text_to_pdf(input_pdf_path, output_pdf_path, data)

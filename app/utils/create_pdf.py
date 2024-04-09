from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from io import BytesIO
import os

def vlute_xuat_danh_gia(input_pdf_path: str, output_pdf_path: str, data: dict, username: str):
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
    c.drawString(150, 701, data['student_fullname'])
    c.drawString(75, 685, data['student_class'])
    c.drawString(125, 670, "Trung tâm CNTT - VNPT Vĩnh Long")
    c.drawString(183, 654, data['mentor_fullname'])
    c.drawString(256, 614, data['r1_text'])
    c.drawString(195, 588, data['r2_text'])
    c.drawString(151, 560, data['r3_text'])
    c.drawString(170, 532, data['r4_text'])
    c.drawString(232, 505, data['r5_text'])
    c.drawString(225, 477, data['r6_text'])
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

def ctu_xuat_phieu_tiep_nhan(input_pdf_path: str, output_pdf_path: str, data: dict, username: str):
    # Đọc file PDF đầu vào
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Lấy số lượng trang của PDF
    num_pages = len(reader.pages)

    # Tải font Times New Roman hỗ trợ tiếng Việt
    pdfmetrics.registerFont(TTFont('Times_New_Roman', 'times.ttf'))

    # Tạo một trang mới với reportlab
    c = canvas.Canvas("temp.pdf")
    c.setFont("Times_New_Roman", 15)
    c.setFillColor(colors.black)
    c.drawString(300, 759, data['ngaybatdau'])
    c.drawString(405, 759, data['ngayketthuc'])
    c.setFont("Times_New_Roman", 13)
    c.drawString(205, 665, data['nhd_hoten'])
    c.drawString(450, 665, data['nhd_sdt'])
    c.drawString(205, 647, data['nhd_email'])
    c.drawString(100, 574, data['sv_hoten'])
    c.drawString(440, 574, data['sv_mssv'])
    c.drawString(105, 556, data['sv_malop'])
    c.drawString(215, 556, data['sv_nganh'])
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
#         "ngaybatdau": "13/05/2024",
#         "ngayketthuc": "05/07/2024",
#         "nhd_hoten": "Phan Thanh Giảng",
#         "nhd_sdt": "0914747190",
#         "nhd_email": "giangpt.vlg@vnpt.vn",
#         "sv_hoten": "Phan Thanh Giảng",
#         "sv_mssv": "B1609816",
#         "sv_malop": "DI16Z6A2",
#         "sv_nganh": "Khoa học Máy tính"
#     }
#     # Đường dẫn tới file PDF đầu vào và file PDF đầu ra
#     input_pdf_path = 'pdf/phieutiepnhan_ctu.pdf'
#     output_pdf_path = 'output.pdf'
#     # Thêm văn bản vào PDF
#     ctu_xuat_phieu_tiep_nhan(input_pdf_path, output_pdf_path, data, "giangpt")

from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.lib import colors

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


def ctu_xuat_phieu_giao_viec(input_pdf_path: str, output_pdf_path: str, data: dict, username: str):
    # Đọc file PDF đầu vào
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Lấy số lượng trang của PDF
    num_pages = len(reader.pages)

    # Tải font Times New Roman hỗ trợ tiếng Việt
    pdfmetrics.registerFont(TTFont('Times_New_Roman', 'times.ttf'))

    # Tạo một trang mới với reportlab
    c = canvas.Canvas("temp.pdf")
    c.setFont("Times_New_Roman", 13)
    c.setFillColor(colors.black)
    c.drawString(170, 759, data['sv_hoten'])
    c.drawString(430, 759, data['sv_mssv'])
    c.drawString(250, 713, data['ngaybatdau'])
    c.drawString(365, 713, data['ngayketthuc'])
    c.drawString(220, 729, data['nhd_hoten'])
    c.setFont("Times_New_Roman", 11)
    c.drawString(85, 627, data['tuan1_batdau'])
    c.drawString(85, 604, data['tuan1_ketthuc'])
    c.drawString(150, 650, data['tuan1_congviec'])
    c.drawString(85, 565, data['tuan2_batdau'])
    c.drawString(85, 541, data['tuan2_ketthuc'])
    c.drawString(150, 587, data['tuan2_congviec'])
    c.drawString(85, 500, data['tuan3_batdau'])
    c.drawString(85, 476, data['tuan3_ketthuc'])
    c.drawString(150, 525, data['tuan3_congviec'])
    c.drawString(85, 435, data['tuan4_batdau'])
    c.drawString(85, 411, data['tuan4_ketthuc'])
    c.drawString(150, 460, data['tuan4_congviec'])
    c.drawString(85, 371, data['tuan5_batdau'])
    c.drawString(85, 347, data['tuan5_ketthuc'])
    c.drawString(150, 395, data['tuan5_congviec'])
    c.drawString(85, 307, data['tuan6_batdau'])
    c.drawString(85, 283, data['tuan6_ketthuc'])
    c.drawString(150, 330, data['tuan6_congviec'])
    c.drawString(85, 245, data['tuan7_batdau'])
    c.drawString(85, 221, data['tuan7_ketthuc'])
    c.drawString(150, 265, data['tuan7_congviec'])
    c.drawString(85, 180, data['tuan8_batdau'])
    c.drawString(85, 157, data['tuan8_ketthuc'])
    c.drawString(150, 205, data['tuan8_congviec'])
    c.drawString(245, 43, data['sv_hoten'])
    c.drawString(425, 43, data['nhd_hoten'])
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


def ctu_xuat_phieu_danh_gia(input_pdf_path: str, output_pdf_path: str, data: dict, username: str):
    # Đọc file PDF đầu vào
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Lấy số lượng trang của PDF
    num_pages = len(reader.pages)

    # Tải font Times New Roman hỗ trợ tiếng Việt
    pdfmetrics.registerFont(TTFont('Times_New_Roman', 'times.ttf'))

    # Tạo một trang mới với reportlab
    c = canvas.Canvas("temp.pdf")
    c.setFont("Times_New_Roman", 13)
    c.drawString(255, 725, data['nhd_hoten'])
    c.drawString(125, 707, data['nhd_sdt'])
    c.drawString(385, 707, data['nhd_email'])
    c.drawString(210, 671, data['sv_hoten'])
    c.drawString(398, 671, data['sv_mssv'])
    c.drawString(250, 653, data['ngaybatdau'])
    c.drawString(405, 653, data['ngayketthuc'])
    c.drawString(480, 590, str(data['thuchiennoiquy']))
    c.drawString(480, 568, str(data['chaphanhgiogiac']))
    c.drawString(480, 540, str(data['thaidogiaotiep']))
    c.drawString(480, 515, str(data['thaidolamviec']))
    c.drawString(480, 470, str(data['dapungyeucau']))
    c.drawString(480, 450, str(data['tinhthanhochoi']))
    c.drawString(480, 427, str(data['sangkien']))
    c.drawString(480, 385, str(data['baocaotiendo']))
    c.drawString(480, 365, str(data['hoanthanhcongviec']))
    c.drawString(480, 342, str(data['ketquadonggop']))
    c.drawString(480, 320, str(data['tong']))
    c.drawString(235, 290, data['nhanxetkhac'])
    c.drawString(58, 230, 'x' if data['phuhopthucte'] else '')
    c.drawString(203, 230, 'x' if data['khongphuhopthucte'] else '')
    c.drawString(382, 230, 'x' if data['tangcuongkynangmem'] else '')
    c.drawString(58, 215, 'x' if data['tangcuongngoaingu'] else '')
    c.drawString(203, 215, 'x' if data['tangcuongkynangnhom'] else '')
    c.drawString(265, 200, data['dexuat'])
    c.drawString(380, 20, data['nhd_hoten'])
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
#         "nhd_hoten": "Phan Thanh Giảng",
#         "nhd_sdt": "0914747190",
#         "nhd_email": "giangpt.vlg@vnpt.vn",
#         "sv_hoten": "Phan Thanh Giảng",
#         "sv_mssv": "B1609816",
#         "ngaybatdau": "13/05/2024",
#         "ngayketthuc": "05/07/2024",
#         "thuchiennoiquy": 100,
#         "chaphanhgiogiac": 99,
#         "thaidogiaotiep": 98,
#         "thaidolamviec": 97,
#         "dapungyeucau": 96,
#         "tinhthanhochoi": 95,
#         "sangkien": 94,
#         "baocaotiendo": 93,
#         "hoanthanhcongviec": 92,
#         "ketquadonggop": 91,
#         "tong": 100,
#         "nhanxetkhac": "Hoàn thành tốt kì thực tập",
#         "phuhopthucte": True,
#         "khongphuhopthucte": True,
#         "tangcuongkynangmem": True,
#         "tangcuongngoaingu": True,
#         "tangcuongkynangnhom": True,
#         "dexuat": "Không có đề xuất gì thêm"
#     }
#     # Đường dẫn tới file PDF đầu vào và file PDF đầu ra
#     input_pdf_path = 'pdf/phieudanhgia_ctu.pdf'
#     output_pdf_path = 'output.pdf'
#     # Thêm văn bản vào PDF
#     ctu_xuat_phieu_danh_gia(input_pdf_path, output_pdf_path, data, "giangpt")

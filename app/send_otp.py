from config import create_connection
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyotp
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

host = os.getenv('EMAIL_HOST')
port = os.getenv('EMAIL_PORT')
username = os.getenv('EMAIL_USERNAME')
password = os.getenv('EMAIL_PASSWORD')

conn = create_connection()
cursor = conn.cursor()

# Hàm để gửi email với mã OTP và lưu thông tin vào cơ sở dữ liệu
def send_otp_email(email):
    # Tạo một đối tượng TOTP với một secret key mới
    totp = pyotp.TOTP(pyotp.random_base32())

    # Tạo mã OTP hiện tại
    otp = totp.now()

    # Lưu thông tin vào cơ sở dữ liệu
    save_otp_to_database(email, otp)

    # Nội dung email
    body = f"""
    <html>
    <body>
        <p>Xin chào,</p>
        <p>Bạn đã đăng ký thực tập tại Trung tâm Công nghệ Thông tin - VNPT Vĩnh Long thành công. Vui lòng xác thực thông tin bằng cách nhập mã OTP.</p>
        <p>Dưới đây là mã OTP của bạn: <strong>{otp}</strong></p>
        <p>Đây là một email được tạo tự động. Vui lòng không trả lời.</p>
    </body>
    </html>
    """

    # Tạo đối tượng MIMEMultipart để xây dựng email
    message = MIMEMultipart()
    message["From"] = username
    message["To"] = email
    message["Subject"] = "Xác thực OTP"

    # Gắn nội dung email
    message.attach(MIMEText(body, "plain"))

    # Kết nối đến máy chủ email (ở đây sử dụng Gmail)
    with smtplib.SMTP(host, port) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(username, email, message.as_string())

    return True

# Hàm để lưu thông tin mã OTP vào cơ sở dữ liệu
def save_otp_to_database(email, otp):
    try:
        # Kiểm tra xem email đã tồn tại trong bảng chưa
        cursor.execute("SELECT COUNT(*) FROM OtpTable WHERE Email = ?", email)
        email_count = cursor.fetchone()[0]

        if email_count > 0:
            # Nếu tồn tại, cập nhật mã OTP mới
            cursor.execute("UPDATE OtpTable SET OtpCode = ?, ExpiryTime = ? WHERE Email = ?", otp, datetime.now() + timedelta(minutes=5), email)
        else:
            # Nếu chưa tồn tại, thêm mới
            cursor.execute("INSERT INTO OtpTable (Email, OtpCode, ExpiryTime) VALUES (?, ?, ?)", email, otp, datetime.now() + timedelta(minutes=5))

        conn.commit()

    except Exception as e:
        print("Error:", e)

    finally:
        if conn:
            conn.close()

# Hàm để kiểm tra xem mã OTP có còn hạn không
def is_otp_valid(email, entered_otp):    
    try:
        # Lấy thông tin về thời gian hết hạn của mã OTP
        cursor.execute("SELECT ExpiryTime FROM OtpTable WHERE Email = ? AND OtpCode = ?", email, entered_otp)
        expiry_time = cursor.fetchone()

        if expiry_time:
            expiry_time = expiry_time[0]
            # Kiểm tra xem thời gian hiện tại có nhỏ hơn thời gian hết hạn hay không
            return datetime.now() < expiry_time
        else:
            return False

    except Exception as e:
        print("Error:", e)
        return False

    finally:
        if conn:
            conn.close()


# Nhập email từ người dùng
user_email = input("Nhập địa chỉ email của bạn: ")

# Gửi email chứa mã OTP và lưu thông tin vào cơ sở dữ liệu
send_otp_email(user_email)

# Nhập mã OTP từ người dùng
entered_otp = input("Nhập mã OTP từ email: ")

# Kiểm tra mã OTP có còn hạn không
if is_otp_valid(user_email, entered_otp):
    print("Mã OTP hợp lệ.")
else:
    print("Mã OTP không hợp lệ hoặc đã hết hạn.")


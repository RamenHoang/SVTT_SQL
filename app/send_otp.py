from .config import create_connection, email_host, email_port, email_username, email_password, email_name
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pyotp
from datetime import datetime, timedelta

conn = create_connection()
cursor = conn.cursor()

# Hàm để gửi email với mã OTP và lưu thông tin vào cơ sở dữ liệu


def send_otp_email(email: str, hoten: str):
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
        <p>Xin chào {hoten},</p>
        <p>Dưới đây là mã OTP của bạn: <strong>{otp}</strong></p>
        <p>Đây là một email được tạo tự động. Vui lòng không trả lời.</p>
        <br/>
        <p>---------------</p>
        <b>Trung tâm CNTT - VNPT Vĩnh Long</b>
        <p>Số 3, Trưng Nữ Vương, Phường 1, Tp. Vĩnh Long, Vĩnh Long</p>
    </body>
    </html>
    """

    # Tạo đối tượng MIMEMultipart để xây dựng email
    message = MIMEMultipart()
    message["From"] = email_name
    message["To"] = email
    message["Subject"] = "Xác thực OTP"

    # Gắn nội dung email dưới dạng HTML
    message.attach(MIMEText(body, "html"))

    # Kết nối đến máy chủ email (ở đây sử dụng Gmail)
    with smtplib.SMTP(email_host, email_port) as server:
        server.starttls()
        server.login(email_username, email_password)
        server.sendmail(email_username, email, message.as_string())

    return True

# Hàm để lưu thông tin mã OTP vào cơ sở dữ liệu


def save_otp_to_database(email, otp):
    try:
        # Kiểm tra xem email đã tồn tại trong bảng chưa
        cursor.execute("SELECT COUNT(*) FROM Temp_OTP WHERE Email = ?", email)
        email_count = cursor.fetchone()[0]

        if email_count > 0:
            # Nếu tồn tại, cập nhật mã OTP mới
            cursor.execute("UPDATE Temp_OTP SET OtpCode = ?, ExpiryTime = ?, IsVerified = ? WHERE Email = ?",
                           otp, datetime.now() + timedelta(minutes=5), 0, email)
        else:
            # Nếu chưa tồn tại, thêm mới
            cursor.execute("INSERT INTO Temp_OTP (Email, OtpCode, ExpiryTime, IsVerified) VALUES (?, ?, ?, ?)",
                           email, otp, datetime.now() + timedelta(minutes=5), 0)

        conn.commit()

    except Exception as e:
        print("Error:", e)


# Hàm để kiểm tra xem mã OTP có còn hạn không
def is_otp_valid(email, entered_otp):
    try:
        # Lấy thông tin về thời gian hết hạn của mã OTP
        cursor.execute(
            "SELECT ExpiryTime, IsVerified FROM Temp_OTP WHERE Email = ? AND OtpCode = ?", email, entered_otp)
        result = cursor.fetchone()
        expiry_time = result[0]
        isVerified = result[1]
        if expiry_time:
            if int(isVerified) == 0:
                # expiry_time[1] = 0 là chưa xác thực thì xác thực rồi cập nhật lại = 1
                cursor.execute("EXEC UpdateVerifiedOTP ?, ?",
                               email, entered_otp)
                cursor.commit()
                # Kiểm tra xem thời gian hiện tại có nhỏ hơn thời gian hết hạn hay không
                return datetime.now() < expiry_time
            else:
                return False
        else:
            return False

    except Exception as e:
        return False


# # Nhập email từ người dùng
# user_email = input("Nhập địa chỉ email của bạn: ")
# hoten = input(" Họ tên: ")

# # Gửi email chứa mã OTP và lưu thông tin vào cơ sở dữ liệu
# send_otp_email(user_email, hoten)

# # Nhập mã OTP từ người dùng
# entered_otp = input("Nhập mã OTP từ email: ")

# # Kiểm tra mã OTP có còn hạn không
# if is_otp_valid(user_email, entered_otp):
#     print("Mã OTP hợp lệ.")
# else:
#     print("Mã OTP không hợp lệ hoặc đã hết hạn.")

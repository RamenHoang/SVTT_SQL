import pandas as pd
import pyodbc

server = '10.91.13.128'
database = 'QL_SinhVien'
username = 'sa'
password = 'Vnpt@123'

conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password};CHARSET=UTF8')

# Đối với pyodbc
cursor = conn.cursor()
df = pd.DataFrame(pd.read_excel('NguoiHuongDan.xlsx'))

for i in df.itertuples(index=False):
    insert = cursor.execute("INSERT INTO NGUOIHUONGDAN(HoTen, Email, ChucDanh, Phong, Username, Password, Facebook, Github, Avatar) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (i[0], i[2], i[3], i[4], i[5], i[6], i[7], i[9], i[10]))
    # cursor.execute("INSERT INTO TRUONG(Ten, KyHieu) VALUES(?, ?)", (i[1], i[2]))
    cursor.commit()
    print(f'Inserted {i[0]}')

# Đóng kết nối sau khi hoàn thành
conn.close()

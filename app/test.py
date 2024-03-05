from config import create_connection

conn = create_connection()
cursor = conn.cursor()

for sv in cursor.execute("SELECT ID FROM SINHVIEN").fetchall():
    cursor.execute("INSERT INTO TAIKHOAN_SINHVIEN(ID_SinhVien, Password, isVerified) VALUES(?, ?, ?)", sv[0], '8556e3c09bfa488eede8f3a6593f967fe057a18634ce006f93d6be99b4d93a2e', 1)
    cursor.commit()
    print(f'inserted {sv[0]}')
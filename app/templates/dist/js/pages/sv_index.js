var Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
});

$(document).ready(function() {
    let cookie = document.cookie;
    let email = cookie.split('username=')[1].replaceAll('"', '');
    let bangthongtin = $('#bang_thongtinsinhvien tbody');
    $.ajax({
        type: 'GET',
        url: '/xem_thong_tin_sv?email='+email,
        success: function(res){
            html = `
                <tr>
                    <td>MSSV:</td>
                    <td>${res.mssv}</td>
                </tr>
                <tr>
                    <td>Họ tên:</td>
                    <td>${res.hoten}</td>
                </tr>
                <tr>
                    <td>Giói tính:</td>
                    <td>${res.gioitinh == 1 ? 'Nam' : 'Nữ'}</td>
                </tr>
                <tr>
                    <td>Số điện thoại:</td>
                    <td>${res.sdt}</td>
                </tr>
                <tr>
                    <td>Email:</td>
                    <td>${res.email}</td>
                </tr>
                <tr>
                    <td>Địa chỉ:</td>
                    <td>${res.diachi}</td>
                </tr>
                <tr>
                    <td>Mã lớp:</td>
                    <td>${res.malop}</td>
                </tr>
                <tr>
                    <td>Ngành:</td>
                    <td>${res.nganh}</td>
                </tr>
                <tr>
                    <td>Trường:</td>
                    <td>${res.truong}</td>
                </tr>
                <tr>
                    <td>Nhóm:</td>
                    <td>${res.nhomhuongdan===null ? '' : res.nhomhuongdan}</td>
                </tr>
            `;

            bangthongtin.append(html);
        }
    });
});
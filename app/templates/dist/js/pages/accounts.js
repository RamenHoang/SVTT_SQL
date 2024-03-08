var Toast = Swal.mixin({
  toast: true,
  position: "top-end",
  showConfirmButton: false,
  timer: 3000,
});

let bangdstaikhoan = $("#bangdstaikhoan").DataTable({
  paging: true,
  lengthChange: false,
  searching: true,
  ordering: true,
  info: true,
  autoWidth: false,
  responsive: true,
  ajax: {
    type: "GET",
    url: "get_ds_tai_khoan",
    dataSrc: "",
  },
  columns: [
    {
      data: "id",
      render: function (data, type, row) {
        return "<center>" + data + "</center>";
      },
    },
    { data: "hoten" },
    { data: "username" },
    { data: "email" },
    {
      data: "role",
      render: function (data, type, row) {
        if (data == 0) {
          return '<center><span class="badge badge-primary"><i class="fa-solid fa-user"></i> Người hướng dẫn</span></center>';
        } else if(data==1) {
          return '<center><span class="badge badge-success"><i class="fa-solid fa-user-tie"></i> Quản trị</span></center>';
        }
      },
    },
    {
      data: "trangthai",
      render: function (data, type, row) {
        if (data == 0) {
          return '<center><span class="badge badge-danger"><i class="fa-solid fa-x"></i> Ngưng hoạt động</span></center>';
        } else {
          return '<center><span class="badge badge-success"><i class="fa-solid fa-check"></i> Đang hoạt động</span></center>';
        }
      },
    },
    {
      data: "id",
      render: function (data, type, row) {
        return (
          `<center>
            <a class="btn btn-info btn-sm" id="editBtn" data-id="${data}" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Sửa thông tin">
              <i class="fa-solid fa-pencil-alt"></i>
            </a>
            <a class="btn btn-primary btn-sm" id="roleBtn" data-id="${data}" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Phân quyền">
              <i class="fa-solid fa-pen-ruler"></i>
            </a>
            <a class="btn btn-warning btn-sm" id="banBtn" data-id="${data}" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Ngưng sử dụng">
              <i class="fa-solid fa-user-slash"></i>
            </a>
            <a class="btn btn-danger btn-sm" id="deleteBtn" data-id="${data}" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Xoá người dùng">
              <i class="fa-solid fa-trash"></i>
            </a>
          </center>`
        );
      },
    },
  ],
});

// Clear modal
function clear_modal() {
  $("#modal_title").empty();
  $("#modal_body").empty();
  $("#modal_footer").empty();
}

// Xoá người dùng
$("#bangdstaikhoan").on("click", "#deleteBtn", function() {
  let id = $(this).data("id");

  Swal.fire({
    title: `Xác nhận xoá người dùng`,
    showDenyButton: false,
    showCancelButton: true,
    confirmButtonText: "Xoá",
    cancelButtonText: "Huỷ",
  }).then((result)=>{
    if (result.isConfirmed){
      $.ajax({
        type: `POST`,
        url: `update_xoa_nguoi_huong_dan_by_id?id=${id}`,
        success: function(res) {
          if(res.status=='OK'){
            Toast.fire({
              icon: "success",
              title: `Xoá người dùng thành công.`
            });
            bangdstaikhoan.ajax.reload();
          }else if(res.status=='EXISTS'){
            Toast.fire({
              icon: "warning",
              title: "Người dùng đang hướng dẫn nhóm. Vui lòng chọn Ngừng sử dụng."
            });
          }
        },
        error: function() {
          Toast.fire({
            icon: "error",
            title: `Xoá người dùng thất bại.`
          });
        }
      })
    }
  });
});

// Ban người dùng
$("#bangdstaikhoan").on("click", "#banBtn", function() {
  let id = $(this).data("id");

  Swal.fire({
    title: `Xác nhận ngưng sử dụng người dùng`,
    showDenyButton: false,
    showCancelButton: true,
    confirmButtonText: "Ngưng",
    cancelButtonText: "Huỷ",
  }).then((result)=>{
    if (result.isConfirmed){
      $.ajax({
        type: `POST`,
        url: `update_ban_nguoi_huong_dan_by_id?id=${id}`,
        success: function(res) {
          if(res.status=='OK'){
            Toast.fire({
              icon: "success",
              title: `Đã ngưng người dùng`
            });
            bangdstaikhoan.ajax.reload();
          }else if(res.status=='IS_ADMIN'){
            Toast.fire({
              icon: "warning",
              title: "Người dùng đang là Quản trị viên."
            });
          }
        },
        error: function() {
          Toast.fire({
            icon: "error",
            title: `Đã xảy ra lỗi. Vui lòng thử lại sau.`
          });
        }
      })
    }
  });
});
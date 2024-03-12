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
      data: null,
      render: function (data, type, row, meta) {
        // Use meta.row to get the current row index, and add 1 to start from 1
        return "<center>" + (meta.row + 1) + "</center>";
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
        if(row.trangthai==1){
          return (
            `<center>
              <a class="btn btn-secondary btn-sm" id="resetBtn" data-id="${data}" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Reset mật khẩu">
                <i class="fa-solid fa-key"></i>
              </a>
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
        }else{
          return (`
            <center>
              <a class="btn btn-success btn-sm" id="activeBtn" data-id="${data}" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Ngưng sử dụng">
                <i class="fa-solid fa-user-check"></i>
              </a>
              <a class="btn btn-danger btn-sm" id="deleteBtn" data-id="${data}" data-bs-toggle="tooltip" data-bs-placement="top" data-bs-title="Xoá người dùng">
                <i class="fa-solid fa-trash"></i>
              </a>
            </center>
          `);
        }
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

// Active người dùng
$("#bangdstaikhoan").on("click", "#activeBtn", function() {
  let id = $(this).data("id");

  Swal.fire({
    title: `Xác nhận kích hoạt người dùng`,
    showDenyButton: false,
    showCancelButton: true,
    confirmButtonText: "Kích hoạt",
    cancelButtonText: "Huỷ",
  }).then((result)=>{
    if (result.isConfirmed){
      $.ajax({
        type: `POST`,
        url: `update_active_nguoi_huong_dan_by_id?id=${id}`,
        success: function(res) {
          if(res.status=='OK'){
            Toast.fire({
              icon: "success",
              title: `Đã kích hoạt người dùng.`
            });
            bangdstaikhoan.ajax.reload();
          }else if(res.status=='NOT_BANNED'){
            Toast.fire({
              icon: "warning",
              title: "Người dùng đang hoạt động."
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

// Reset mật khẩu người dùng
$("#bangdstaikhoan").on("click", "#resetBtn", function() {
  let id = $(this).data("id");

  Swal.fire({
    title: `Xác nhận reset mật khẩu người dùng`,
    showDenyButton: false,
    showCancelButton: true,
    confirmButtonText: "Reset",
    cancelButtonText: "Huỷ",
  }).then((result)=>{
    if (result.isConfirmed){
      $.ajax({
        type: `POST`,
        url: `reset_password?id=${id}`,
        success: function(res) {
          if(res.status=='OK'){
            Toast.fire({
              icon: "success",
              title: `Đã reset mật khẩu người dùng.`
            });
            bangdstaikhoan.ajax.reload();
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


// Cập nhật quyền người dùng
$("#bangdstaikhoan").on("click", "#roleBtn", function() {
  let id = $(this).data("id");

  clear_modal();

  $("#modal_title").text(`Phân quyền người dùng`);
  $("#modal_body").html(`
    <div class="form-group">
      <label for="modal_role_select">Phân quyền</label>
      <select id="modal_role_select" class="form-control">
        <option value="1">Quản trị viên</option>
        <option value="0">Người hướng dẫn</option>
      </select>
    </div>
  `);
  $("#modal_footer").append(
    `<button type="button" class="btn btn-primary" data-id="${id}" id="modal_submit_btn">
      <i class="fa-solid fa-floppy-disk"></i> 
      Lưu thay đổi
    </button>`
  );

  $("#modal_id").modal("show");

  $("#modal_submit_btn").on('click', function(){
    $.ajax({
      type: `POST`,
      url: `update_phan_quyen_nguoi_huong_dan_by_id?id=${id}&role=${$("#modal_role_select").val()}`,
      success: function(res) {
        if(res.status=='OK'){
          Toast.fire({
            icon: "success",
            title: `Đã phân quyền người dùng.`
          });
          $("#modal_id").modal("hide");
          bangdstaikhoan.ajax.reload();
        }
      },
      error: function() {
        Toast.fire({
          icon: "error",
          title: `Đã xảy ra lỗi. Vui lòng thử lại sau.`
        });
      }
    });
  });
});


// Cập nhật thông tin người dùng
$("#bangdstaikhoan").on("click", "#editBtn", function() {
  let id = $(this).data("id");

  clear_modal();

  $("#modal_title").text(`Chỉnh sửa thông tin người dùng`);
  $("#modal_body").html(`
    <div class="form-group">
      <label for="modal_hoten_input">Họ tên</label>
      <input type="text" class="form-control" id="modal_hoten_input" required />
    </div>
    <div class="form-group">
      <label for="modal_email_input">Email</label>
      <input type="email" class="form-control" id="modal_email_input" required />
    </div>
    <div class="form-group">
      <label for="modal_sdt_input">Số điện thoại</label>
      <input type="number" class="form-control" id="modal_sdt_input" required />
    </div>
    <div class="form-group">
      <label for="modal_chucdanh_select">Chức danh</label>
      <select id="modal_chucdanh_select" class="form-control">
        <option value="Nhân viên">Nhân viên</option>
        <option value="Phó phòng">Phó phòng</option>
        <option value="Trưởng phòng">Trưởng phòng</option>
      </select>
    </div>
    <div class="form-group">
      <label for="modal_phong_select">Phòng</label>
      <select id="modal_phong_select" class="form-control">
        <option value="Phòng GP CNTT 1">Phòng GP CNTT 1</option>
        <option value="Phòng GP CNTT 2">Phòng GP CNTT 2</option>
        <option value="Phòng KD">Phòng KD</option>
      </select>
    </div>
    <div class="form-group">
      <label for="modal_zalo_input">Zalo</label>
      <input type="text" class="form-control" id="modal_zalo_input" />
    </div>
    <div class="form-group">
      <label for="modal_facebook_input">Facebook</label>
      <input type="text" class="form-control" id="modal_facebook_input" />
    </div>
    <div class="form-group">
      <label for="modal_github_input">Github</label>
      <input type="text" class="form-control" id="modal_github_input" />
    </div>
    <div class="form-group">
      <label for="modal_avatar_input">Avatar</label>
      <input type="text" class="form-control" id="modal_avatar_input" />
    </div>
  `);
  $("#modal_footer").append(
    `<button type="button" class="btn btn-primary" data-id="${id}" id="modal_submit_btn">
      <i class="fa-solid fa-floppy-disk"></i> 
      Lưu thay đổi
    </button>`
  );

  $("#modal_id").modal("show");

  let hoten = $("#modal_hoten_input");
  let email = $("#modal_email_input");
  let sdt = $("#modal_sdt_input");
  let chucdanh = $("#modal_chucdanh_select");
  let phong = $("#modal_phong_select");
  let zalo = $("#modal_zalo_input");
  let facebook = $("#modal_facebook_input");
  let github = $("#modal_github_input");
  let avatar = $("#modal_avatar_input");

  // Load chi tiết
  $.ajax({
    type: `GET`,
    url: `get_thong_tin_nguoi_huong_dan_by_id?id=${id}`,
    success: function(res) {
      hoten.val(res.hoten);
      email.val(res.email);
      sdt.val(res.sdt);
      chucdanh.val(res.chucdanh);
      phong.val(res.phong);
      zalo.val(res.zalo);
      facebook.val(res.facebook);
      github.val(res.github);
      avatar.val(res.avatar);
    }
  });


  $("#modal_submit_btn").on('click', function(){
    $.ajax({
      type: `POST`,
      url: `update_chi_tiet_tai_khoan_by_id?id=${id}&hoten=${hoten.val()}&email=${email.val()}&sdt=${sdt.val()}&chucdanh=${chucdanh.val()}&phong=${phong.val()}&zalo=${zalo.val()}&facebook=${facebook.val()}&github=${github.val()}&avatar=${avatar.val()}`,
      success: function(res) {
        if(res.status=='OK'){
          Toast.fire({
            icon: "success",
            title: `Đã cập nhật thông tin.`
          });
          $("#modal_id").modal("hide");
          bangdstaikhoan.ajax.reload();
        }
      },
      error: function() {
        Toast.fire({
          icon: "error",
          title: `Đã xảy ra lỗi. Vui lòng thử lại sau.`
        });
      }
    });
  });
});

// Tạo thông tin người dùng
$("#taoTaiKhoanBtn").on("click", function() {
  clear_modal();

  $("#modal_title").text(`Tạo người dùng`);
  $("#modal_body").html(`
    <div class="form-group">
      <label for="modal_hoten_input">Họ tên</label>
      <input type="text" class="form-control" id="modal_hoten_input" required />
    </div>
    <div class="form-group">
      <label for="modal_username_input">Username</label>
      <input type="text" class="form-control" id="modal_username_input" required />
    </div>
    <div class="form-group">
      <label for="modal_email_input">Email</label>
      <input type="email" class="form-control" id="modal_email_input" required />
    </div>
    <div class="form-group">
      <label for="modal_sdt_input">Số điện thoại</label>
      <input type="number" class="form-control" id="modal_sdt_input" required />
    </div>
    <div class="form-group">
      <label for="modal_chucdanh_select">Chức danh</label>
      <select id="modal_chucdanh_select" class="form-control">
        <option value="Nhân viên">Nhân viên</option>
        <option value="Phó phòng">Phó phòng</option>
        <option value="Trưởng phòng">Trưởng phòng</option>
      </select>
    </div>
    <div class="form-group">
      <label for="modal_phong_select">Phòng</label>
      <select id="modal_phong_select" class="form-control">
        <option value="Phòng GP CNTT 1">Phòng GP CNTT 1</option>
        <option value="Phòng GP CNTT 2">Phòng GP CNTT 2</option>
        <option value="Phòng KD">Phòng KD</option>
      </select>
    </div>
    <div class="form-group">
      <label for="modal_zalo_input">Zalo</label>
      <input type="text" class="form-control" id="modal_zalo_input" />
    </div>
    <div class="form-group">
      <label for="modal_facebook_input">Facebook</label>
      <input type="text" class="form-control" id="modal_facebook_input" />
    </div>
    <div class="form-group">
      <label for="modal_github_input">Github</label>
      <input type="text" class="form-control" id="modal_github_input" />
    </div>
    <div class="form-group">
      <label for="modal_avatar_input">Avatar</label>
      <input type="text" class="form-control" id="modal_avatar_input" />
    </div>
  `);
  $("#modal_footer").append(
    `<button type="button" class="btn btn-primary" id="modal_submit_btn">
      <i class="fa-solid fa-floppy-disk"></i> 
      Thêm
    </button>`
  );

  $("#modal_id").modal("show");

  let hoten = $("#modal_hoten_input");
  let username = $("#modal_username_input");
  let email = $("#modal_email_input");
  let sdt = $("#modal_sdt_input");
  let chucdanh = $("#modal_chucdanh_select");
  let phong = $("#modal_phong_select");
  let zalo = $("#modal_zalo_input");
  let facebook = $("#modal_facebook_input");
  let github = $("#modal_github_input");
  let avatar = $("#modal_avatar_input");

  $("#modal_submit_btn").on('click', function(){
    $.ajax({
      type: `POST`,
      url: `them_nguoi_huong_dan?hoten=${hoten.val()}&email=${email.val()}&sdt=${sdt.val()}&chucdanh=${chucdanh.val()}&phong=${phong.val()}&username=${username.val()}&zalo=${zalo.val()}&facebook=${facebook.val()}&github=${github.val()}&avatar=${avatar.val()}`,
      success: function(res) {
        if(res.status=='OK'){
          Toast.fire({
            icon: "success",
            title: `Đã thêm người hướng dẫn.`
          });
          $("#modal_id").modal("hide");
          bangdstaikhoan.ajax.reload();
        }else{
          Toast.fire({
            icon: "error",
            title: `Username đã tồn tại, vui lòng chọn username khác.`
          });
        }
      },
      error: function() {
        Toast.fire({
          icon: "error",
          title: `Đã xảy ra lỗi. Vui lòng thử lại sau.`
        });
      }
    });
  });
});
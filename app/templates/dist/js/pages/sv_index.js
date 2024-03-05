var Toast = Swal.mixin({
  toast: true,
  position: "top-end",
  showConfirmButton: false,
  timer: 3000,
});

$(document).ready(function () {
  let cookie = document.cookie.split(";");
  let bangthongtin = $("#bang_thongtinsinhvien tbody");
  cookie.forEach(function (val) {
    if (val.includes("username=")) {
      let email = val.split("username=")[1].replaceAll('"', "");

      $.ajax({
        type: "GET",
        url: `/xem_thong_tin_sv?username=${email}`,
        success: function (res) {
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
                            <td>${res.gioitinh == 1 ? "Nam" : "Nữ"}</td>
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
                            <td>${
                              res.nhomhuongdan === null ? "" : res.nhomhuongdan
                            }</td>
                        </tr>
                    `;

          bangthongtin.append(html);
        },
      });
    }
  });

  // Chọn nhóm
  $.ajax({
    type: "GET",
    url: "get_ds_nhom_thuc_tap_con_han",
    success: function (res) {
      html = "";
      if (res.length > 0) {
        $.each(res, function (idx, val) {
          html +=
            '<option value="' +
            val.id +
            '">[' +
            val.id +
            "]\t" +
            val.tendetai +
            "</option>";
        });
      } else {
        html +=
          '<option value="" selected>Hiện tại chưa có nhóm hoặc hết hạn chọn nhóm</option>';
      }

      $("#danhsachnhom").append(html);
    },
  });

  $("#danhsachnhom").on("change", function () {
    let nhom = $("#danhsachnhom").val();
    if (nhom != "") {
      $.ajax({
        type: "GET",
        url: "get_chi_tiet_nhom_thuc_tap_by_id?id=" + nhom,
        success: function (res) {
          let soluongdangky =
            String(res.nhomthuctap_dadangky) +
            "/" +
            String(res.nhomthuctap_soluong);
          $("#nguoihuongdan").val(res.nguoihuongdan_hoten);
          $("#mota").val(res.detai_mota.replace(/<br>/g, "\r\n"));
          $("#soluongsv").val(soluongdangky);
        },
      });
    } else {
      $("#nguoihuongdan").val("");
      $("#mota").val("");
      $("#soluongsv").val("");
    }
  });

  if (document.cookie.indexOf("groupid") !== -1) {
    $("#submitBtn").prop("disabled", true);
  } else {
    $("#submitBtn").on("click", function () {
      let id_nhom = $("#danhsachnhom").val();
      cookie.forEach(function (val) {
        if (val.includes("username=")) {
          let email = val.split("username=")[1].replaceAll('"', "");
          $.ajax({
            type: "POST",
            url: `/them_nhom_thuc_tap_sv?username=${email}&idnhom=${id_nhom}`,
            success: function (res) {
              if (res.status == "OK") {
                Toast.fire({
                  icon: "success",
                  title: "Đã đăng ký",
                });
                $("#submitBtn").prop("disabled", true);
              } else {
                Toast.fire({
                  icon: "error",
                  title: "Nhóm đã đủ số lượng",
                });
              }
            },
            error: function () {
              Toast.fire({
                icon: "error",
                title:
                  "Nhóm đã đủ số lượng.<br/>Vui lòng liên hệ người hướng dẫn.",
              });
            },
          });
        }
      });
    });
  }

  // Gửi đánh giá
  function submitDanhGia(email, nhomhuongdan_id) {
    let cau_1 = $("input[name='q1']:checked").val();
    let cau_2 = $("input[name='q2']:checked").val();
    let cau_3 = $("input[name='q3']:checked").val();
    let cau_4 = $("input[name='q4']:checked").val();
    let gopy = $("#gopy")
      .val()
      .replace(/[\r\n]+/g, "<br/>");

    if (
      cau_1 == undefined ||
      cau_2 == undefined ||
      cau_3 == undefined ||
      cau_4 == undefined
    ) {
      Toast.fire({
        icon: "error",
        title: "Vui lòng chọn đủ 4 đáp án",
      });
    } else {
      $.ajax({
        type: "POST",
        url: `/danh_gia_thuc_tap?username=${email}&id_nhd=${nhomhuongdan_id}&dapan_1=${cau_1}&dapan_2=${cau_2}&dapan_3=${cau_3}&dapan_4=${cau_4}&gopy=${gopy}`,
        success: function () {
          Toast.fire({
            icon: "success",
            title: "Đã gửi đánh giá",
          });
          $("#submitDanhGiaBtn").prop("disabled", true);
          $("<center><p>Bạn đã gửi đánh giá</p></center>").replaceAll(
            $("#review_form")
          );
        },
        error: function () {
          Toast.fire({
            icon: "error",
            title: "Gửi đánh giá không thành công hoặc bạn đã đánh giá rồi!",
          });
        },
      });
    }
  }

  // Bắt sự kiện submit
  $("#submitDanhGiaBtn").on("click", function () {
    let email = "";
    let groupid = -1;
    cookie.forEach(function (val) {
      if (val.includes("username=")) {
        email = val.split("username=")[1].replaceAll('"', "");
      }

      if (val.includes("groupid=")) {
        groupid = val.split("groupid=")[1];
      }
    });

    if (email != "" && groupid != -1) {
      submitDanhGia(email, groupid);
    }
  });
});

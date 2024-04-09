let currentDate = new Date();
currentDate.setDate(currentDate.getDate() + 3);
let currentTimestamp = parseInt(currentDate.getTime() / 1000);

var Toast = Swal.mixin({
  toast: true,
  position: "top-end",
  showConfirmButton: false,
  timer: 3000,
});

function empty_modal() {
  $("#modal_title").empty();
  $("#modal_body").empty();
  $("#modal_footer").empty();
}

// load filter
function loadFilter() {
  // load kỳ thực tập
  $.ajax({
    type: "GET",
    url: "/get_ky_thuc_tap_by_username",
    success: function (data) {
      let filter_kythuctap = $("#filter_kythuctap");
      data.forEach((element) => {
        filter_kythuctap.append(
          `<option value="${element.id}">${element.ngaybatdau} - ${element.ngayketthuc}</option>`
        );
      });
    },
  });
}

$("#bangdssv").on("click", "#downloadBtn", function () {
  let id = $(this).data("id");
  Toast.fire({
    icon: "info",
    title: "Đang tạo file đánh giá",
  });
  window.open("/xuat_danh_gia?id=" + id, '_blank', 'noopener', 'noreferrer');
});

$("#bangdssv").on("click", "#xuatPhieuTiepNhanBtn", function () {
  let id = $(this).data("id");
  Toast.fire({
    icon: "info",
    title: "Đang xuất phiếu tiếp nhận",
  });
  window.open(`ctu_xuat_phieu_tiep_nhan?id=${id}`, '_blank', 'noopener', 'noreferrer');
});

$("#uploadBtn").click(function () {
  $("#fileInput").click();
});

$("#fileInput").change(function () {
  var fileName = $(this).val();
  if (fileName) {
    var form = new FormData();
    form.append("file", fileInput.files[0], fileName);

    var settings = {
      url: "import_danh_gia_sv",
      method: "POST",
      timeout: 0,
      processData: false,
      mimeType: "multipart/form-data",
      contentType: false,
      data: form,
    };

    $.ajax(settings).done(function (response) {
      if (response) {
        Toast.fire({
          icon: "success",
          title: "Import thành công",
        });
        bangdssv.ajax.reload();
      } else {
        Toast.fire({
          icon: "error",
          title: "Import thất bại",
        });
      }
    });
  }
});

$("#downloadBtn").on("click", function () {
  empty_modal();

  $.ajax({
    type: "GET",
    url: "get_ky_thuc_tap_by_username",
    success: function (res) {
      $("#modal_title").text("Download đánh giá theo kỳ thực tập");
      html =
        '<div class="form-group"><label for="modal_kythuctap_select">Kỳ thực tập</label><select id="modal_kythuctap_select" class="form-control"></select></div>';
      $("#modal_body").append(html);

      $.each(res, function (idx, val) {
        $("#modal_kythuctap_select").append(
          `<option value="${val.id}">${val.ngaybatdau} - ${val.ngayketthuc}</option>`
        );
      });

      $("#modal_footer").append(
        '<button type="button" class="btn btn-primary" id="modal_submit_btn"><i class="fa-solid fa-floppy-disk"></i> Download</button>'
      );
      $("#modal_id").modal("show");

      $("#modal_submit_btn").click(function () {
        let url =
          "xuat_ds_sinh_vien_da_danh_gia?kythuctap=" +
          $("#modal_kythuctap_select").val();

        $.ajax({
          type: "GET",
          url: url,
          success: function (res) {
            Toast.fire({
              icon: "success",
              title: "Vui lòng chờ trong giây lát",
            });
            window.location.href = url;
          },
          error: function (xhr, status, error) {
            Toast.fire({
              icon: "error",
              title: "Chưa có đánh giá cho sinh viên trong kỳ thực tập này",
            });
          },
        });
      });
    },
  });
});

$(document).ready(function () {
  $(".select2").select2({
    theme: "bootstrap",
  });
  empty_modal();
  loadFilter();
  create_table("-1", "-1");
  $("#filter_kythuctap").on("change", function () {
    let id = $("#filter_kythuctap").val();
    let filter_nhomthuctap = $("#filter_nhomthuctap");
    create_table(id, "-1");

    $.ajax({
      type: `GET`,
      url: `get_danh_sach_nhom_theo_ky_id?id=${id}`,
      success: function (res) {
        // empty first
        filter_nhomthuctap.empty();

        $.each(res, function (idx, val) {
          filter_nhomthuctap.append(`
            <option value="${val.id}">${val.tennhom}</option>
          `);
        });
      },
    });

    filter_nhomthuctap.on(`change`, function () {
      create_table(id, filter_nhomthuctap.val());
    });
  });
});

function create_table(kythuctap, nhomthuctap) {
  var bangdssv = $("#bangdssv").DataTable({
    paging: true,
    lengthChange: false,
    searching: true,
    ordering: true,
    info: true,
    destroy: true,
    autoWidth: false,
    responsive: true,
    ajax: {
      type: "GET",
      url: `get_ds_sinh_vien_by_username?kythuctap=${kythuctap}&nhomthuctap=${nhomthuctap}`,
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
      { data: "mssv" },
      { data: "hoten" },
      {
        data: "gioitinh",
        render: function (data, type, row) {
          return "<center>" + data + "</center>";
        },
      },
      { data: "nganh" },
      { data: "detai" },
      { data: "tennhom" },
      {
        data: "trangthai",
        render: function (data, type, row) {
          if (data == 1) {
            return '<center><span class="badge badge-warning"><i class="fa-solid fa-circle-exclamation"></i> Chưa đánh giá</span></center>';
          } else {
            return '<center><span class="badge badge-success"><i class="fa-solid fa-check"></i> Đã đánh giá</span></center>';
          }
        },
      },
      {
        data: "id",
        render: function (data, type, row, meta) {
          if (row.handanhgia >= currentTimestamp) {
            return (
              `<center>
                <a class="btn btn-info btn-sm" id="editBtn" data-id="${data}">
                  <i class="fas fa-pencil-alt"></i>
                </a>
                ${row.kyhieu_truong == "CTU" ? `<a class="btn btn-primary btn-sm" id="xuatPhieuTiepNhanBtn" data-id="${data}"><i class="fa-solid fa-file-export"></i></a>` : ""}
                <a class="btn btn-success btn-sm" id="downloadBtn" data-id="${data}">
                  <i class="fa-solid fa-print"></i>
                </a>
              </center>`
            );
          } else {
            return (
              `<center>
                <a class="btn btn-info btn-sm" id="editBtn" data-id="${data}" data-edit="false">
                  <i class="fa-solid fa-eye"></i>
                </a>
                <a class="btn btn-success btn-sm" id="downloadBtn" data-id="${data}">
                  <i class="fa-solid fa-print"></i>
                </a>
              </center>`);
          }
        },
      },
    ],
    columnDefs: [
      { "orderable": false, "targets": 0 } // Tắt tính năng sắp xếp cho cột 0
    ]
  });

  $("#bangdssv").on("click", "#editBtn", function () {
    let id = $(this).data("id");

    empty_modal();
    $.ajax({
      url: "get_chi_tiet_danh_gia_sv_by_id?id=" + id,
      type: "GET",
      success: function (res) {
        $(".modal-dialog").addClass("modal-lg");
        $("#modal_title").text("Đánh giá sinh viên");
        let html = `
          <form id="editForm">
            <div class="form-group row"> 
              <div class="col-sm-10"> 
                <label for="ythuckyluat" class="col-form-label">Ý thức kỷ luật, tuân thủ nội quy</label> 
              </div> 
              <div class="col-sm-2"> 
                <input type="number" class="form-control" id="ythuckyluat_number" name="ythuckyluat_number" min="0" max="100" value="0"> 
              </div> 
              <div class="col-sm mt-4"> 
                <textarea id="ythuckyluat_text" class="form-control" rows="3"></textarea> 
              </div> 
            </div> 
            <div class="form-group row mt-4"> 
              <div class="col-sm-10"> 
                <label for="tuanthuthoigian" class="col-form-label">Tuân thủ thời gian</label> 
              </div> 
              <div class="col-sm-2"> 
                <input type="number" class="form-control" id="tuanthuthoigian_number" name="tuanthuthoigian_number" min="0" max="100" value="0"> 
              </div> 
              <div class="col-sm mt-4"> 
                <textarea id="tuanthuthoigian_text" class="form-control" rows="3"></textarea> 
              </div> 
            </div> 
            <div class="form-group row mt-4"> 
              <div class="col-sm-10"> 
                <label for="kienthuc" class="col-form-label">Kiến thức</label> 
              </div> 
            <div class="col-sm-2"> 
              <input type="number" class="form-control" id="kienthuc_number" name="kienthuc_number" min="0" max="100" value="0"> 
            </div> 
            <div class="col-sm mt-4"> 
              <textarea id="kienthuc_text" class="form-control" rows="3"></textarea> 
            </div>
          </div> 
          <div class="form-group row mt-4"> 
            <div class="col-sm-10"> 
              <label for="kynangnghe" class="col-form-label">Kỹ năng nghề</label> 
            </div> 
            <div class="col-sm-2"> 
              <input type="number" class="form-control" id="kynangnghe_number" name="kynangnghe_number" min="0" max="100" value="0"> 
            </div> 
            <div class="col-sm mt-4"> 
              <textarea id="kynangnghe_text" class="form-control" rows="3"></textarea> 
            </div> 
          </div> 
          <div class="form-group row mt-4"> 
            <div class="col-sm-10"> 
              <label for="khanangdoclap" class="col-form-label">Khả năng làm việc độc lập</label> 
            </div> 
            <div class="col-sm-2"> 
              <input type="number" class="form-control" id="khanangdoclap_number" name="khanangdoclap_number" min="0" max="100" value="0"> 
            </div> 
            <div class="col-sm mt-4"> 
              <textarea id="khanangdoclap_text" class="form-control" rows="3"></textarea> 
            </div> 
          </div> 
          <div class="form-group row mt-4"> 
            <div class="col-sm-10"> 
              <label for="khanangnhom" class="col-form-label">Khả năng làm việc nhóm</label> 
            </div> 
            <div class="col-sm-2"> 
              <input type="number" class="form-control" id="khanangnhom_number" name="khanangnhom_number" min="0" max="100" value="0"> 
            </div> 
            <div class="col-sm mt-4"> 
              <textarea id="khanangnhom_text" class="form-control" rows="3"></textarea> 
            </div> 
          </div> 
          <div class="form-group row mt-4"> 
            <div class="col-sm-10"> 
              <label for="khananggiaiquyetcongviec" class="col-form-label">Khả năng giải quyết công việc</label> 
            </div> 
            <div class="col-sm-2"> 
              <input type="number" class="form-control" id="khananggiaiquyetcongviec_number" name="khananggiaiquyetcongviec_number" min="0" max="100" value="0">
            </div> 
            <div class="col-sm mt-4"> 
              <textarea id="khananggiaiquyetcongviec_text" class="form-control" rows="3"></textarea> 
            </div> 
          </div> 
          <div class="form-group row mt-4"> 
            <div class="col-sm-10"> 
              <label for="danhgiachung" class="col-form-label">Đánh giá chung</label> 
            </div> 
            <div class="col-sm-2"> 
              <input type="number" class="form-control" id="danhgiachung_number" name="danhgiachung_number" min="0" max="100" value="0"> 
            </div> 
          </div> 
        </form>`;
        $("#modal_body").empty();
        $("#modal_body").append(html);

        $("input, textarea").val("");
        let ythuckyluat_number = $("#ythuckyluat_number");
        let ythuckyluat_text = $("#ythuckyluat_text");
        let tuanthuthoigian_number = $("#tuanthuthoigian_number");
        let tuanthuthoigian_text = $("#tuanthuthoigian_text");
        let kienthuc_number = $("#kienthuc_number");
        let kienthuc_text = $("#kienthuc_text");
        let kynangnghe_number = $("#kynangnghe_number");
        let kynangnghe_text = $("#kynangnghe_text");
        let khanangdoclap_number = $("#khanangdoclap_number");
        let khanangdoclap_text = $("#khanangdoclap_text");
        let khanangnhom_number = $("#khanangnhom_number");
        let khanangnhom_text = $("#khanangnhom_text");
        let khananggiaiquyetcongviec_number = $(
          "#khananggiaiquyetcongviec_number"
        );
        let khananggiaiquyetcongviec_text = $("#khananggiaiquyetcongviec_text");
        let danhgiachung_number = $("#danhgiachung_number");

        if (Object.keys(res).length > 0) {
          ythuckyluat_number.val(res.ythuckyluat_number);
          ythuckyluat_text.val(res.ythuckyluat_text);
          tuanthuthoigian_number.val(res.tuanthuthoigian_number);
          tuanthuthoigian_text.val(res.tuanthuthoigian_text);
          kienthuc_number.val(res.kienthuc_number);
          kienthuc_text.val(res.kienthuc_text);
          kynangnghe_number.val(res.kynangnghe_number);
          kynangnghe_text.val(res.kynangnghe_text);
          khanangdoclap_number.val(res.khanangdoclap_number);
          khanangdoclap_text.val(res.khanangdoclap_text);
          khanangnhom_number.val(res.khanangnhom_number);
          khanangnhom_text.val(res.khanangnhom_text);
          khananggiaiquyetcongviec_number.val(
            res.khananggiaiquyetcongviec_number
          );
          khananggiaiquyetcongviec_text.val(res.khananggiaiquyetcongviec_text);
          danhgiachung_number.val(res.danhgiachung_number);
        }

        $("#modal_footer").empty();
        if (res.handanhgia <= currentTimestamp) {
          $("input, textarea").prop("disabled", true);
          $("#modal_footer").html(``);
        } else {
          $("#modal_footer").append(
            `<button type="button" class="btn btn-primary" data-id="${id}" id="modal_submit_btn"><i class="fa-solid fa-floppy-disk"></i> Lưu thay đổi</button>`
          );
        }
        $("#modal_id").modal("show");

        // Tính năng lưu thay đổi
        $("#modal_submit_btn").click(function () {
          // Get ID Nhom
          $.ajax({
            type: "GET",
            url: "get_id_nhom_by_sv_id?id=" + id,
            success: function (res) {
              let data_update =
                "?sinhvienid=" +
                String(id) +
                "&nhomid=" +
                parseInt(res.id) +
                "&ythuckyluat_number=" +
                parseFloat(ythuckyluat_number.val()) +
                "&ythuckyluat_text=" +
                ythuckyluat_text.val() +
                "&tuanthuthoigian_number=" +
                parseFloat(tuanthuthoigian_number.val()) +
                "&tuanthuthoigian_text=" +
                tuanthuthoigian_text.val() +
                "&kienthuc_number=" +
                parseFloat(kienthuc_number.val()) +
                "&kienthuc_text=" +
                kienthuc_text.val() +
                "&kynangnghe_number=" +
                parseFloat(kynangnghe_number.val()) +
                "&kynangnghe_text=" +
                kynangnghe_text.val() +
                "&khanangdoclap_number=" +
                parseFloat(khanangdoclap_number.val()) +
                "&khanangdoclap_text=" +
                khanangdoclap_text.val() +
                "&khanangnhom_number=" +
                parseFloat(khanangnhom_number.val()) +
                "&khanangnhom_text=" +
                khanangnhom_text.val() +
                "&khananggiaiquyetcongviec_number=" +
                parseFloat(khananggiaiquyetcongviec_number.val()) +
                "&khananggiaiquyetcongviec_text=" +
                khananggiaiquyetcongviec_text.val() +
                "&danhgiachung_number=" +
                parseFloat(danhgiachung_number.val());

              $.ajax({
                type: "POST",
                url: "update_danh_gia_sv_by_id" + data_update,
                data: data_update,
                headers: {
                  "Content-Type": "application/json",
                },
                success: function (data) {
                  if (data.status == "OK") {
                    $("#modal_id").modal("hide");
                    bangdssv.ajax.reload();
                    Toast.fire({
                      icon: "success",
                      title: "Cập nhật thành công",
                    });
                  } else {
                    Toast.fire({
                      icon: "error",
                      title: "Đã quá hạn đánh giá",
                    });
                  }
                },
                error: function (xhr, status, error) {
                  Toast.fire({
                    icon: "error",
                    title: "Đã xãy ra lỗi",
                  });
                },
              });
            },
          });
        });
      },
    });
  });

  // Handle "Check All" checkbox click event
  $('#checkAll').on('click', function () {
    var rows = bangdssv.rows({ 'search': 'applied' }).nodes();
    $('input[type="checkbox"]', rows).prop('checked', this.checked);
  });

  // Handle individual checkbox click event
  $('#bangdssv tbody').on('change', 'input[type="checkbox"]', function () {
    if (!this.checked) {
      var el = $('#checkAll').get(0);
      if (el && el.checked && ('indeterminate' in el)) {
        el.indeterminate = true;
      }
    }
  });

  // Bắt sự kiến nút đánh giá nhiều
  $("#reviewBtn").on("click", function () {
    // Kiem tra neu chua co check box thi bao loi
    let dsSinhVien = [];
    $("#bangdssv tr").each(function (idx) {
      // Kiểm tra checkbox trong mỗi hàng
      let checkbox = $(this).find("input[type='checkbox']:first");

      if (checkbox.prop("checked")) {
        let id = checkbox.data("id");
        if (id !== undefined) {
          dsSinhVien.push(id);
        }
      }
    });

    if (dsSinhVien.length == 0) {
      Toast.fire({
        icon: "warning",
        title: "Vui lòng chọn sinh viên cần đánh giá",
      });
    } else {
      $(".modal-dialog").addClass("modal-lg");
      $("#modal_title").text(`Đánh giá ${dsSinhVien.length} sinh viên đã chọn`);
      let html = `
          <form id="editForm">
            <div class="form-group row"> 
              <div class="col-sm-10"> 
                <label for="ythuckyluat" class="col-form-label">Ý thức kỷ luật, tuân thủ nội quy</label> 
              </div> 
              <div class="col-sm-2"> 
                <input type="number" class="form-control" id="ythuckyluat_number" name="ythuckyluat_number" min="0" max="100" value="0"> 
              </div> 
              <div class="col-sm mt-4"> 
                <textarea id="ythuckyluat_text" class="form-control" rows="3"></textarea> 
              </div> 
            </div> 
            <div class="form-group row mt-4"> 
              <div class="col-sm-10"> 
                <label for="tuanthuthoigian" class="col-form-label">Tuân thủ thời gian</label> 
              </div> 
              <div class="col-sm-2"> 
                <input type="number" class="form-control" id="tuanthuthoigian_number" name="tuanthuthoigian_number" min="0" max="100" value="0"> 
              </div> 
              <div class="col-sm mt-4"> 
                <textarea id="tuanthuthoigian_text" class="form-control" rows="3"></textarea> 
              </div> 
            </div> 
            <div class="form-group row mt-4"> 
              <div class="col-sm-10"> 
                <label for="kienthuc" class="col-form-label">Kiến thức</label> 
              </div> 
            <div class="col-sm-2"> 
              <input type="number" class="form-control" id="kienthuc_number" name="kienthuc_number" min="0" max="100" value="0"> 
            </div> 
            <div class="col-sm mt-4"> 
              <textarea id="kienthuc_text" class="form-control" rows="3"></textarea> 
            </div>
          </div> 
          <div class="form-group row mt-4"> 
            <div class="col-sm-10"> 
              <label for="kynangnghe" class="col-form-label">Kỹ năng nghề</label> 
            </div> 
            <div class="col-sm-2"> 
              <input type="number" class="form-control" id="kynangnghe_number" name="kynangnghe_number" min="0" max="100" value="0"> 
            </div> 
            <div class="col-sm mt-4"> 
              <textarea id="kynangnghe_text" class="form-control" rows="3"></textarea> 
            </div> 
          </div> 
          <div class="form-group row mt-4"> 
            <div class="col-sm-10"> 
              <label for="khanangdoclap" class="col-form-label">Khả năng làm việc độc lập</label> 
            </div> 
            <div class="col-sm-2"> 
              <input type="number" class="form-control" id="khanangdoclap_number" name="khanangdoclap_number" min="0" max="100" value="0"> 
            </div> 
            <div class="col-sm mt-4"> 
              <textarea id="khanangdoclap_text" class="form-control" rows="3"></textarea> 
            </div> 
          </div> 
          <div class="form-group row mt-4"> 
            <div class="col-sm-10"> 
              <label for="khanangnhom" class="col-form-label">Khả năng làm việc nhóm</label> 
            </div> 
            <div class="col-sm-2"> 
              <input type="number" class="form-control" id="khanangnhom_number" name="khanangnhom_number" min="0" max="100" value="0"> 
            </div> 
            <div class="col-sm mt-4"> 
              <textarea id="khanangnhom_text" class="form-control" rows="3"></textarea> 
            </div> 
          </div> 
          <div class="form-group row mt-4"> 
            <div class="col-sm-10"> 
              <label for="khananggiaiquyetcongviec" class="col-form-label">Khả năng giải quyết công việc</label> 
            </div> 
            <div class="col-sm-2"> 
              <input type="number" class="form-control" id="khananggiaiquyetcongviec_number" name="khananggiaiquyetcongviec_number" min="0" max="100" value="0">
            </div> 
            <div class="col-sm mt-4"> 
              <textarea id="khananggiaiquyetcongviec_text" class="form-control" rows="3"></textarea> 
            </div> 
          </div> 
          <div class="form-group row mt-4"> 
            <div class="col-sm-10"> 
              <label for="danhgiachung" class="col-form-label">Đánh giá chung</label> 
            </div> 
            <div class="col-sm-2"> 
              <input type="number" class="form-control" id="danhgiachung_number" name="danhgiachung_number" min="0" max="100" value="0"> 
            </div> 
          </div> 
        </form>`;
      $("#modal_body").empty();
      $("#modal_body").append(html);

      $("#modal_footer").empty();
      $("#modal_footer").append(
        `<button type="button" class="btn btn-primary" id="modal_submit_btn"><i class="fa-solid fa-floppy-disk"></i> Lưu thay đổi</button>`
      );
      $("#modal_id").modal("show");

      // Submit form đánh giá
      $("#modal_submit_btn").on("click", function () {
        let ythuckyluat_number = parseFloat($("#ythuckyluat_number").val());
        let ythuckyluat_text = $("#ythuckyluat_text").val();
        let tuanthuthoigian_number = parseFloat(
          $("#tuanthuthoigian_number").val()
        );
        let tuanthuthoigian_text = $("#tuanthuthoigian_text").val();
        let kienthuc_number = parseFloat($("#kienthuc_number").val());
        let kienthuc_text = $("#kienthuc_text").val();
        let kynangnghe_number = parseFloat($("#kynangnghe_number").val());
        let kynangnghe_text = $("#kynangnghe_text").val();
        let khanangdoclap_number = parseFloat($("#khanangdoclap_number").val());
        let khanangdoclap_text = $("#khanangdoclap_text").val();
        let khanangnhom_number = parseFloat($("#khanangnhom_number").val());
        let khanangnhom_text = $("#khanangnhom_text").val();
        let khananggiaiquyetcongviec_number = parseFloat(
          $("#khananggiaiquyetcongviec_number").val()
        );
        let khananggiaiquyetcongviec_text = $(
          "#khananggiaiquyetcongviec_text"
        ).val();
        let danhgiachung_number = parseFloat($("#danhgiachung_number").val());

        $.ajax({
          type: `POST`,
          url: `danh_gia_nhieu_sv?dssv=${dsSinhVien}&ythuckyluat_number=${ythuckyluat_number}&ythuckyluat_text=${ythuckyluat_text}&tuanthuthoigian_number=${tuanthuthoigian_number}&tuanthuthoigian_text=${tuanthuthoigian_text}&kienthuc_number=${kienthuc_number}&kienthuc_text=${kienthuc_text}&kynangnghe_number=${kynangnghe_number}&kynangnghe_text=${kynangnghe_text}&khanangdoclap_number=${khanangdoclap_number}&khanangdoclap_text=${khanangdoclap_text}&khanangnhom_number=${khanangnhom_number}&khanangnhom_text=${khanangnhom_text}&khananggiaiquyetcongviec_number=${khananggiaiquyetcongviec_number}&khananggiaiquyetcongviec_text=${khananggiaiquyetcongviec_text}&danhgiachung_number=${danhgiachung_number}`,
          success: function () {
            Toast.fire({
              icon: "success",
              title: "Đã lưu đánh giá",
            });
            $("#modal_id").modal("hide");
            bangdssv.ajax.reload();
          },
          error: function () {
            Toast.fire({
              icon: "error",
              title: "Lưu đánh giá thất bại",
            });
          },
        });
      });
    }
  });

}

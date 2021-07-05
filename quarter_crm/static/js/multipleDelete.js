$(".nav-link").click(function () {
  $("[type=checkbox]").prop("checked", false);
  $(".serviceMultiDeleteBtn").addClass("d-none");
  $(".quarterMultiDeleteBtn").addClass("d-none");
});

// MULTIPLE DELETE REPAIR/INSTALL REQUEST
$(".req_checkbox ").click(function () {
  if ($(".req_checkbox ").is(":checked")) {
    $(".serviceMultiDeleteBtn").removeClass("d-none");
  } else {
    $(".serviceMultiDeleteBtn").addClass("d-none");
  }
});

$(".serviceMultiDeleteBtn").click(function () {
  let ids_list = [];
  $(".req_checkbox:checked").each(function (i) {
    ids_list.push($(this).val());
  });
  // TO REMOVE DUPLICATES FROM ids_list ARRAY
  ids = Array.from(new Set(ids_list));
  //
  console.log(ids);
  $.ajax({
    type: "POST",
    url: "/service_multiple_delete",
    data: {
      ids,
    },
    success: function (response) {
      location.reload(true);
      $(".alert").removeClass("d-none");
      $(".alert").text("تم الحذف");
    },
  });
});

// MULTIPLE DELETE QUARTER REQUESTS
$(".qua_checkbox ").click(function () {
  if ($(".qua_checkbox ").is(":checked")) {
    $(".quarterMultiDeleteBtn").removeClass("d-none");
  } else {
    $(".quarterMultiDeleteBtn").addClass("d-none");
  }
});

$(".quarterMultiDeleteBtn").click(function () {
  let ids_list = [];
  $(".qua_checkbox:checked").each(function (i) {
    ids_list.push($(this).val());
  });
  // Remove Duplicates
  ids = Array.from(new Set(ids_list));
  $.ajax({
    type: "POST",
    url: "/quarter/quarter_multi_delete",
    data: {
      ids,
    },
    success: function (response) {
      location.reload(true);
      $(".alert").removeClass("d-none");
      $(".alert").text("تم الحذف");
    },
  });
});

$(".nav-link").click(function () {
  $("[type=checkbox]").prop("checked", false);
  $(".quarterMultiDeleteBtn").addClass("d-none");
});

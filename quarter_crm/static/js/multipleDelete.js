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
  let ids = [];
  $(".req_checkbox:checked").each(function (i) {
    ids.push($(this).val());
  });
  $.ajax({
    type: "POST",
    // url: "{% url 'service_multiple_delete' %}",
    url: "/service_multiple_delete",
    data: {
      ids,
    },
    success: function (response) {
      location.reload(true);
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
  let ids = [];
  $(".qua_checkbox:checked").each(function (i) {
    ids.push($(this).val());
  });
  $.ajax({
    type: "POST",
    // url: "{% url 'service_multiple_delete' %}",
    url: "/quarter/quarter_multi_delete",
    data: {
      ids,
    },
    success: function (response) {
      location.reload(true);
    },
  });
});

$(".nav-link").click(function () {
  $("[type=checkbox]").prop("checked", false);
  $(".quarterMultiDeleteBtn").addClass("d-none");
});

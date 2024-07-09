$(document).ready(function () {
  $(".increment-btn").click(function (e) {
    e.preventDefault();

    var inc_value = $(this).closest(".menuCard").find(".qty-input").val();
    var value = parseInt(inc_value, 10);
    value = isNaN(value) ? 0 : value;
    if (value < 10) {
      value++;
      $(this).closest(".menuCard").find(".qty-input").val(value);
    }
  });

  $(".decrement-btn").click(function (e) {
    e.preventDefault();

    var inc_value = $(this).closest(".menuCard").find(".qty-input").val();
    var value = parseInt(inc_value, 10);
    value = isNaN(value) ? 0 : value;
    if (value > 1) {
      value--;
      $(this).closest(".menuCard").find(".qty-input").val(value);
    }
  });

  $(".addtoCart").click(function (e) {
    e.preventDefault();

    var menuId = $(this).closest(".menuCard").find(".menuId").val();
    var menuQty = $(this).closest(".menuCard").find(".qty-input").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      type: "post",
      url: "/add-to-cart/",
      data: {
        menuId: menuId,
        menuQty: menuQty,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        console.log(response);
        location.reload();
      },
      error: function (response) {
        console.log("Error: ", response);
      },
    });
  });

  $(".changeQty").click(function (e) {
    e.preventDefault();

    var menuId = $(this).closest(".menuCard").find(".menuId").val();
    var menuQty = $(this).closest(".menuCard").find(".qty-input").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      type: "post",
      url: "/update-cart/",
      data: {
        menuId: menuId,
        menuQty: menuQty,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        $(".total-cost").text(response.total_cost);
        console.log(response);
      },
      error: function (response) {
        console.log("Error: ", response);
      },
    });
  });

  $(".remBtn").click(function (e) {
    e.preventDefault();

    var menuId = $(this).closest(".menuCard").find(".menuId").val();
    var token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
      type: "POST",
      url: "/remove-item/",
      data: {
        menuId: menuId,
        csrfmiddlewaretoken: token,
      },
      success: function (response) {
        $(".total-cost").text(response.total_cost);
        console.log(response);
        location.reload();
      },
    });
  });
});

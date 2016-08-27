var modal = document.getElementById('modal-popup');
window.onclick = function(event) {
    if (event.target == modal) {
        // clear
        $('#modal-info-header').text("");
        $('#modal-info-footer').text("");
        $("#modal-date-created").text("");
        $("#modal-error").html("");
        $(".modal-body").html("");
        $("#ad").hide();
        $('#h-roomid').text("");
        $('#modal-place-button-add').hide("");
        $('#tx-ad').css({"background-color": "white"});
        $("#change-ad").hide();

        modal.style.display = "none";
    }
};

$('.popup-link').click(function () {
    modal.style.display = "block";
});

$(".close").click(function () {
    // clear
    $('#modal-info-header').text("");
    $('#modal-info-footer').text("");
    $("#modal-date-created").text("");
    $("#modal-error").html("");
    $(".modal-body").html("");
    $("#ad").hide();
    $('#h-roomid').text("");
    $('#modal-place-button-add').hide("");
    $('#tx-ad').css({"background-color": "white"});
    $("#change-ad").hide();

    $('#modal-popup').hide();
});

function renderInfo(roomId, roomName, roomPrivacy) {
        $('#modal-info-header').text(roomName);
        $('#modal-info-footer').text(roomPrivacy);
        $('#h-roomid').text(roomId);
        $('#loader-place').html("<div class='loader'></div>");
        $.ajax({
            type: "post",
            url: "/get_details",
            cache: false,
            data: {
                room_id: roomId
            },
            success: function (data) {
                if (data == "403" || data == "401") {
                    $("#ad").hide();
                    $("#modal-error").html("Permission denied =(");
                }
                else if(data == "404") {
                    $("#ad").hide();
                    $(".modal-body").html("");
                    $("#modal-date-created").text("");
                    $("#modal-error").html("Here is empty...");
                    $("#modal-place-button-add").fadeIn(500);
                }
                else {
                    $("#ad").fadeIn();
                    var datails = JSON.parse(data);
                    $("#modal-error").html("");
                    $("#tb-rooms").html("<table>");
                    $(".modal-body").html("<p>" + datails["name"] + "</p>");
                    $("#modal-date-created").text(datails["created"]);
                }
                $(".loader").remove();
            }
        });
    }

     $("#ad").mouseenter(function(){
         $("#change-ad").fadeIn();
     });

    $("#ad").mouseleave(function(){
         $("#change-ad").hide();
    });

    function changeGlance() {
        if ($('#tx-ad').val() != "") {
            $('#loader-place').html("<div class='loader'></div>");
            var roomId = $("#h-roomid").text();
            $.ajax({
                type: "post",
                url: "/change_glance",
                cache: false,
                data: {
                    room_id: roomId,
                    title: $('#tx-ad').val()
                },
                success: function (data) {
                    renderInfo(roomId,
                            $('#modal-info-header').text(),
                            $("#modal-info-footer").text()
                    );
                    $('#tx-ad').val("");
                }
            });
        }
        else {
            $('#tx-ad').css({"background-color": "lightcoral"});
        }
    }

    $("#tx-ad").click(function () {
       $("#tx-ad").css({"background-color": "white"});
    });

    function deleteGlance() {
        $('#loader-place').html("<div class='loader'></div>");
        var roomId = $("#h-roomid").text();
        $.ajax({
            type: "post",
            url: "/delete_glance",
            cache: false,
            data: {
                room_id: roomId
            },
            success: function (data) {
                 renderInfo(roomId,
                            $('#modal-info-header').text(),
                            $("#modal-info-footer").text()
                 );
                $('#tx-ad').val("");
                $('#tx-ad').css({"background-color": "white"});
            }
        });
    }

    function createGlance() {
        $("#modal-place-button-add").hide(300);
        $('#loader-place').html("<div class='loader'></div>");
        var roomId = $("#h-roomid").text();
        $.ajax({
            type: "post",
            url: "/create_glance",
            cache: false,
            data: {
                room_id: roomId
            },
            success: function (data) {
                 renderInfo(roomId,
                            $('#modal-info-header').text(),
                            $("#modal-info-footer").text()
                 );
                $("#change-ad").fadeIn();
            }
        });
    }

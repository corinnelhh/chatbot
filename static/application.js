$(document).ready(function(){

    $(".slidingDiv").hide();
    $(".show_hide").show();

    $('.show_hide').click(function(){
    $(".slidingDiv").slideToggle();
    });

    $( "#output_filter" ).change(function() {
    if ($("#output_filter").val() == "No Filter Selected") {
        $("#output_filter2").hide();
        $("#out_descrip_1").hide();
    }
    else {
        $("#output_filter2").show();
        var name = $("#output_filter").val()
        var description = $("#output_filter").find(":selected").attr("data-description");
        $("#out_descrip_1").text(name + ": " + description);
        $("#out_descrip_1").show();
    }
    });

    $( "#output_filter2" ).change(function() {
    if ($("#output_filter2").val() == "No Filter Selected") {
        $("#output_filter3").hide();
        $("#out_descrip_2").hide();
    }
    else {
        $("#output_filter3").show();
        var name = $("#output_filter2").val()
        var description = $("#output_filter2").find(":selected").attr("data-description");
        $("#out_descrip_2").text(name + ": " + description);
        $("#out_descrip_2").show();
    }
    });

    $( "#output_filter3" ).change(function() {
    if ($("#output_filter2").val() == "No Filter Selected") {
        $("#out_descrip_2").hide();
    }
    else {
        $("#output_filter3").show();
        var name = $("#output_filter3").val()
        var description = $("#output_filter3").find(":selected").attr("data-description");
        $("#out_descrip_3").text(name + ": " + description);
        $("#out_descrip_3").show();
    }
    });

    $( "#input_filter" ).change(function() {
    if ($("#input_filter").val() == "No Filter Selected") {
        $("#input_filter").hide();
    }
    else {
        var name = $("#input_filter").val()
        var description = $("#input_filter").find(":selected").attr("data-description");
        $("#input_filter").text(name + ": " + description);
        $("#input_filter").show();
    }
    });

});

// Inspired by http://papermashup.com/simple-jquery-showhide-div/
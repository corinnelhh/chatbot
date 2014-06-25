$(document).ready(function(){

        $(".slidingDiv").hide();
        $(".show_hide").show();

    $('.show_hide').click(function(){
    $(".slidingDiv").slideToggle();
    });
    $( "#output_filter" ).change(function() {
    if ($("#output_filter").val() == "default") {
        $("#output_filter2").hide();
    }
    else {
        $("#output_filter2").show();
    }
    });
});

// Inspired by http://papermashup.com/simple-jquery-showhide-div/
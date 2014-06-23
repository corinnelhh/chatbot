$(document).ready(function(){

        $(".slidingDiv").hide();
        $(".show_hide").show();

    $('.show_hide').click(function(){
    $(".slidingDiv").slideToggle();
    });

});

// Inspired by http://papermashup.com/simple-jquery-showhide-div/
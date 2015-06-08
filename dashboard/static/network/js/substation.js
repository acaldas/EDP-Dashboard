/**
 * Created by Afonso on 07/06/2015.
 */
$(document).ready(function() {

    $('#substation-assets tr').click(function() {
        var href = $(this).find("a").attr("href");
        if(href) {
            window.location = href;
        }
    });

});
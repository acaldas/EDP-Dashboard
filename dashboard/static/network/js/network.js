/**
 * Created by Afonso on 12/06/2015.
 */

$.fn.networkautocomplete = function(form) {
    var _form = $(form);
    var urlSrc = _form.attr("data-src") + "?q=";
    var urlDest = _form.attr("data-dest");
    var list = $("<ul class=\"autocomplete-list list-group\"></ul>");
    list.hide();
    _form.append(list);
    var button = $(".btn-autocomplete", _form);
    var input = $("> input", _form);
    input.on("input",function(){
        searchAutocomplete();
    });

    input.focusin(function(){
        searchAutocomplete();
    });

    button.click(function(){
        searchAutocomplete();
    });

    var searchAutocomplete = function(){
        var text = input.val();
        if(text.length == 0) { list.empty(); return; }
        var valUrl = urlSrc + encodeURIComponent(text);
        $.get(valUrl, function(data){
            list.empty();
            var results = data.results;
            if(results.length == 0) { return; }
            results.forEach(function(result){
                var resultUrl = urlDest + result.id;
                var link = jQuery("<a class=\"list-group-item autocomplete-link\" href=\"" + resultUrl + "\">" + result.text + "</a>");
                list.append(link);
            });
            list.show();
        });
    };
};

var autocompleteForm = $(".autocomplete-form");
autocompleteForm.each(function(index, form){
    $.fn.networkautocomplete(form);
});
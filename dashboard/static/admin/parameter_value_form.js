(function($) {
            $(document).ready(function() {
                var update_options = function(parameter){
                    var possible_values = parameter_values[$(parameter).find(':selected').text()];
                    if(possible_values) {
                        var possible_ids = possible_values.map(function (v) {
                            return v.id
                        });
                        var value = $('#' + parameter.id.substring(0, parameter.id.length - 9) + 'value_interval');
                        var selected_option = $(value).find('option:selected')[0];
                        var selected_value = $(selected_option).attr('value');

                        $(value).empty();
                        $(value).append('<option value="">---------</option>');
                        possible_values.forEach(function (option) {
                            var optxt = '<option ';
                            if (option.id == selected_value)
                                optxt +='selected="selected" '
                            optxt +='value="' + option.id + '">'+option.value+'</option>';
                            $(value).append(optxt)
                        });
                    }
                }
                var watch_parameter = function(parameter){
                    $(parameter).on('change', function(){
                        update_options(parameter);
                    })
                };

                var parameters = $('.parameter select').toArray();
                parameters.forEach(function(parameter){
                    update_options(parameter);
                    watch_parameter(parameter);
                })
            });
})(grp.jQuery);
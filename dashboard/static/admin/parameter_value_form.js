(function($) {
            $(document).ready(function() {

                var clean_options = function(value){
                    $(value).empty();
                    $(value).append('<option value="">---------</option>');
                };
                var update_options = function(parameter) {
                    var current_parameter = parameter_values[$(parameter).find(':selected').attr('value')]

                    var value = $('#' + parameter.id.substring(0, parameter.id.length - 9) + 'value_interval');
                    if (!current_parameter) {
                         clean_options(value);
                    } else if(current_parameter){


                        var possible_values = current_parameter.values;
                        if (possible_values) {
                            var possible_ids = possible_values.map(function (v) {
                                return v.id
                            });
                            var selected_option = $(value).find('option:selected')[0];
                            var selected_value = $(selected_option).attr('value');

                            clean_options(value);
                            possible_values.forEach(function (option) {
                                var optxt = '<option ';
                                if (option.id == selected_value)
                                    optxt += 'selected="selected" '
                                optxt += 'value="' + option.id + '">' + option.value + '</option>';
                                $(value).append(optxt)
                            });
                        }

                        if(current_parameter.function){
                            $(value).css('border-color','rgb(204, 204, 204)');
                            $('#' + parameter.id.substring(0, parameter.id.length - 9) + 'value').css('border-color','green');
                        } else {
                            $(value).css('border-color','green');
                            $('#' + parameter.id.substring(0, parameter.id.length - 9) + 'value').css('border-color','rgb(204, 204, 204)');
                        }
                    }
                }
                var watch_parameter = function(parameter){
                    $(parameter).off('change').on('change', function(){
                        update_options(parameter);
                    })
                };

                var parameters = $('.parameter select').toArray();
                parameters.forEach(function(parameter){
                    update_options(parameter);
                    watch_parameter(parameter);
                });

                $('a.parametervalue_set-group.grp-add-handler').toArray().forEach(function(addButton){
                    $(addButton).mouseup(function(){

                        setTimeout(function(){
                            var parameters = $('.parameter select').toArray();
                            var newparameter = parameters[parameters.length-2];
                            update_options(newparameter);
                            watch_parameter(newparameter);
                        }, 50);
                    });
                });
            });
})(grp.jQuery);
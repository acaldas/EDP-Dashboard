$(function() {

    var draw_chart = function(value) {
        value = value || "geral";
        if(value == "geral") {
            var data = asset_historic;
            var ykeys = ['health_index', 'reliability', 'failure_probability', 'remaining_lifetime'];
            var labels = ['Índice de Saúde', 'Confiança', 'Probabilidade de Falha', 'Vida Restante'];
        } else {
           var parameter = all_parameters.filter(function(p){return p.id == value});
           if(parameter.length) {
               parameter = parameter[0];
               var data = parameter.values
               var ykeys = ['hi'];
               var labels = ['Índice de Saúde'];
           }
        }
        $('#morris-historic-chart').empty();
        Morris.Line({
            element: 'morris-historic-chart',
            data: data,
            xkey: 'date',
            ykeys: ykeys,
            labels: labels,
            lineColors: ['#5CB85C', '#92C74B', 'rgb(217, 83, 79)', '#0b62a4'],
            smooth: false,
            pointSize: 5,
            hideHover: 'auto',
            resize: true
        });
    };
    $('.chart_parameter_select label').toArray().forEach(function(label){
        $(label).click(function(){
            var checkbox = $($(label).prev()[0]);
            checkbox.click();
        });

    });
    $('input[name="graph_parameter"]').toArray().forEach(function(checkbox){
        if($(checkbox).attr('checked'))
            draw_chart($(checkbox).attr('value'));
        $(checkbox).change(function(){
            var value = $(checkbox).attr('value');
            draw_chart(value)
        });
    });



    Morris.Donut({
        element: 'morris-donut-chart',
        data: [{
            label: "Download Sales",
            value: 12
        }, {
            label: "In-Store Sales",
            value: 30
        }, {
            label: "Mail-Order Sales",
            value: 20
        }],
        resize: true
    });

    Morris.Bar({
        element: 'morris-bar-chart',
        data: [{
            y: '2006',
            a: 100,
            b: 90
        }, {
            y: '2007',
            a: 75,
            b: 65
        }, {
            y: '2008',
            a: 50,
            b: 40
        }, {
            y: '2009',
            a: 75,
            b: 65
        }, {
            y: '2010',
            a: 50,
            b: 40
        }, {
            y: '2011',
            a: 75,
            b: 65
        }, {
            y: '2012',
            a: 100,
            b: 90
        }],
        xkey: 'y',
        ykeys: ['a', 'b'],
        labels: ['Series A', 'Series B'],
        hideHover: 'auto',
        resize: true
    });

});

$(function() {
    console.log('hello');
    console.log(asset_historic);
    Morris.Line({
        element: 'morris-historic-chart',
        data: asset_historic,
        xkey: 'date',
        ykeys: ['health_index', 'reliability', 'failure_probability', 'remaining_lifetime'],
        labels: ['Índice de Saúde', 'Confiança', 'Probabilidade de Falha', 'Vida Restante'],
        lineColors: ['#5CB85C', '#92C74B', 'rgb(217, 83, 79)', '#0b62a4'],
        pointSize: 5,
        hideHover: 'auto',
        resize: true
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

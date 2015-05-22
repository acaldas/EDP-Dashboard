/**
 * Created by Afonso on 22/05/2015.
 */

$(document).ready(function() {

    var g = new JustGage({
        id: "gauge",
        value: 0,
        min: 0,
        max: 100,
        showMinMax: true,
        title: "Índice de Saúde",
        levelColorsGradient: true,
        levelColors: [ '#d9534f', '#FEE62A', '#5cb85c'],
        refreshAnimationTime: 2000,
        refreshAnimationType:"linear",
        gaugeWidthScale: 1.2
        //http://justgage.com/
    });

    setTimeout(function () {
        g.refresh(90);
    }, 1000);

    function barWobble(element, height, speed) {
        //If user clicks/adjusts too fast, stop previous animation, and start new one.
        //$(element).stop().animate({height: height + "%"}, speed, 'easeOutElastic');
    }

    function updateBar(bar_elem) {
        var colors = ['#5CB85C', '#6EBD56', '#80C250', '#92C74B', '#A4CC45', '#B6D140', '#C8D63A', '#DADB35', '#ECE02F',
            '#FEE62A', '#F9D52E', '#F5C532', '#F1B536', '#EDA43A', '#E9943E', '#E58442', '#E17346', '#DD634A', '#D9534F'];

        var bar = $(bar_elem);
        var value = bar.data('value') || 0; //If parseInt returns NaN, use 0
        var max = bar.data('max') || 100; //If parseInt returns NaN, use 0
        var levels = bar.find('li');
        //Make sure value is within our boundaries (if <0, set to 0, if >max, set to max)
        value = value < 0 ? 0 : value > max ? max : value;
        value /= max / 100; //Normalize the height to percentage (same as value/max * 100)

        var setLevelsColor = function(levels, i) {
            if((levels.length-i)*100/levels.length<= value)
                $(levels.toArray()[i]).css('background-color', colors[i]);
            if(i>0)
                setTimeout(function(){setLevelsColor(levels, i-1)}, 150);

        };

        setLevelsColor(levels, levels.length);



        //barWobble(level, value, 700); //Do the wobble
    }

    $(document).ready(function () {
        $('ul.asset-progress-bar').toArray().forEach(updateBar);
    });
})

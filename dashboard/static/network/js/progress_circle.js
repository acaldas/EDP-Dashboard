/**
 * Created by Afonso on 26/05/2015.
 */

function drawProgress(percent){
	$('div.prog').html('<div class="percent"></div><div id="slice"'+(percent > 50?' class="gt50"':'')+'><div class="pie"></div>'+(percent > 50?'<div class="pie fill"></div>':'')+'</div>');
	var deg = 360/100*percent;
	$('#slice .pie').css({
		'-moz-transform':'rotate('+deg+'deg)',
		'-webkit-transform':'rotate('+deg+'deg)',
		'-o-transform':'rotate('+deg+'deg)',
		'transform':'rotate('+deg+'deg)'
	});
	$('.percent').html('<p>' + Math.round(percent)+'%</p>');
}
function animateDraw(percent, currentPercent) {
    var current = currentPercent | 0;
    var next = current+1;
    if(current <= percent) {
        drawProgress(current);
        setTimeout(function(){animateDraw(percent, next)}, 20)
    }
}

$(document).ready(function(){
    var value = $('#prog-contain').data('value');
    if(value <= 100 && value >= 0)
	    animateDraw(value, 0);
});
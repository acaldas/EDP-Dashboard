/**
 * Created by Afonso on 12/06/2015.
 */
$('#substationAutocomplete').yourlabsAutocomplete({
    url: 'autocomplete/SubstationAutocomplete/',
    placeholder: 'Procurar Subestação',
    choiceSelector: '[data-value]'
})

$('#substationAutocomplete').bind('selectChoice', function(e, choice, autocomplete) {
    window.location.href += 'substation/' + $(choice[0]).data('value');
});
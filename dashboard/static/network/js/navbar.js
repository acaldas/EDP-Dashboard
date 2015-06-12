/**
 * Created by Afonso on 12/06/2015.
 */

$('#assetAutocomplete').yourlabsAutocomplete({
    url: 'http://localhost:8000/autocomplete/AssetAutocomplete',
    placeholder: 'Procurar Ativo',
    choiceSelector: '[data-value]'
})

$('#assetAutocomplete').bind('selectChoice', function(e, choice, autocomplete) {
    window.location.href = 'http://localhost:8000/asset/' + $(choice[0]).data('value');
});
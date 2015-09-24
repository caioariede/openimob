function get_cookie_value($el) {
    return $el.garlic('getStorage').get($el.garlic('getPath'));
}

function handle_update_price_options() {
    function update_price_options() {
        $('[name=min_price], [name=max_price]').attr('disabled', null);

        var listing_type = $('[name=listing_type]').val();

        var min_price = $('[name=min_price]'),
            max_price = $('[name=max_price]');

        var min_price_cookie_value = get_cookie_value(min_price),
            max_price_cookie_value = get_cookie_value(max_price);

        min_price.find('option').remove();
        max_price.find('option').remove();

        var choices = min_max_prices_json[listing_type];

        for (var i = 0; i < choices.length; ++i) {
            var choice = choices[i],
                option = $('<option/>').val(choice[0]).html(choice[1]);

            min_price.append(option.clone());
            max_price.append(option.clone());
        }

        max_price.find('option:last').attr('selected', true);

        if (min_price.find('option').filter(function(){ return this.value == min_price_cookie_value; }).length)
            min_price.val(min_price_cookie_value);

        if (max_price.find('option').filter(function(){ return this.value == max_price_cookie_value; }).length)
            max_price.val(max_price_cookie_value);

        min_price.trigger('change');
        max_price.trigger('change');
    }

    $('[name=listing_type]').change(update_price_options);
    $('[name=min_price], [name=max_price]').attr('disabled', true);

    setTimeout(function(){
        update_price_options();
    }, 500);
}

function handle_neighbourhood_options() {
    function update_neighbourhood_options() {
        var neighbourhood_field = $('[name=neighbourhood]');
        
        var city_field = $('[name=city]'), city = city_field.val(),
            neighbourhood_options_url = city_field.data('neighbourhood-options-url');

        var neighbourhood_optgroup = $('#neighbourhood-neighbourhood'),
            condominium_optgroup = $('#neighbourhood-condominium');

        neighbourhood_field.attr('disabled', true);

        $.ajax({
            url: neighbourhood_options_url,
            data: {'city': city},
            dataType: 'json',
            success: function(result){
                var cookie_value = get_cookie_value(neighbourhood_field);

                neighbourhood_field.attr('disabled', null);

                // neighbourhood
                neighbourhood_optgroup.find('option').remove();

                for (var i = 0; i < result.neighbourhoods.length; ++i) {
                    var r = result.neighbourhoods[i],
                        value = 'neighbourhood-' + r[0], html = r[1];

                    neighbourhood_optgroup.append(
                        $('<option/>').val(value).html(html));
                }

                // condominium
                condominium_optgroup.find('option').remove();

                for (var i = 0; i < result.condominiums.length; ++i) {
                    var r = result.condominiums[i],
                        value = 'condominium-' + r[0], html = r[1];

                    condominium_optgroup.append(
                        $('<option/>').val(value).html(html));
                }

                if (cookie_value)
                    neighbourhood_field.val(cookie_value);

                neighbourhood_field.trigger('change');
            }
        });
    }

    $('[name=city]').change(update_neighbourhood_options);
    $('[name=neighbourhood]').attr('disabled', true);

    setTimeout(function(){
        update_neighbourhood_options();
    }, 500);
}

function handle_search_sidebar() {
    $('[data-update-neighbourhood]').click(function(){
        $('[name=neighbourhood]').val($(this).data('update-neighbourhood')).trigger('change');
    });
}

$(function(){
    handle_update_price_options();
    handle_neighbourhood_options();
    handle_search_sidebar();

    $('.listing-same-height').equalHeights();
    $('.small-listing-same-height').equalHeights();
});

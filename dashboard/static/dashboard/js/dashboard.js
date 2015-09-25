$(function(){
    
    // prepopulate listing slug
    !function(){
        if ( ! /pages\/[^\/]+\/listing\/listingpage/.test(window.location.href))
            return;

        var uniqid = Math.random().toString(36).substr(2, 5);

        var watch_fields = '[name=city],[name=neighbourhood],[name=condominium],[name=listing_type]';

        var _populate = function() {
            var city = $('#id_city :checked').html(),
                neighbourhood = $('[name=neighbourhood] [value!=]:selected').html(),
                condominium = $('[name=condominium] [value!=]:selected').html(),
                listing_type = $.map($('[name=listing_type]:checked'), function(e){
                    return $(e).parent().text();
                }).join(' ');

            var slug = [
                    city, (condominium || neighbourhood), listing_type, uniqid
                ].join(' ').replace(/-/g, '').replace(/^\s+|\s+$/g, '');

            $('#id_slug').val(URLify(slug));
        };

        var populate = function() {
            setTimeout(_populate, 100);
        }

        if (typeof original_page_slug == 'undefined') {
            $(watch_fields).click(populate).keyup(populate).change(populate).focus(populate);
        }

        if ($('#id_reference').val() == '') {
            $('#id_reference').val(uniqid.toUpperCase());
        }
    }();

    // prepopulate listing title
    !function(){
        if ( ! /pages\/[^\/]+\/listing\/listingpage/.test(window.location.href))
            return;

        var watch_fields = '[name=neighbourhood],[name=condominium]';

        var _populate = function() {
            var category = parent_page.title,
                neighbourhood = $('[name=neighbourhood] [value!=]:selected').html(),
                condominium = $('[name=condominium] [value!=]:selected').html();

            var title = [
                    category, (condominium || neighbourhood),
                ].join(' ').replace(/-/g, '').replace(/^\s+|\s+$/g, '');

            $('#id_seo_title').val(title);
        }

        var populate = function() {
            setTimeout(_populate, 100);
        }

        $(watch_fields).click(populate).keyup(populate).change(populate).focus(populate);
    }();

    // prepopulate city slugs
    !function(){
        if ( ! /snippets\/listing\/city/.test(window.location.href))
            return;

        function prepopulate_formsets() {
            $('[name$=slug]').each(function(){
                var slug_field = $(this);

                if (slug_field.is('.prepopulate'))
                    return;

                slug_field.addClass('prepopulate');
                
                var row = slug_field.closest('.field-row'), name_field;

                if (row.length == 0) {
                    row = slug_field.closest('.object').prev();
                }
                
                name_field = row.find('[name$=name]');

                var _populate = function() {
                    slug_field.val(URLify(name_field.val()));
                };

                var populate = function() { setTimeout(_populate, 10); }

                name_field.click(populate)
                          .keyup(populate)
                          .change(populate)
                          .focus(populate);
            });
        }

        $('[id$=-ADD]').click(function(){
            setTimeout(prepopulate_formsets, 100);
        });

        prepopulate_formsets();
    }();


    $('[data-filter-by]').each(function(){
        var self = $(this), select2 = self.select2(),
            original_value = self.val(),
            filter_by = self.data('filter-by'),
            filter_url = self.data('filter-url');

        var populate = function() {
            var data = {};

            $(filter_by).each(function(){
                data[$(this).attr('name')] = $(this).val();
            });

            $.ajax({
                url: filter_url,
                dataType: 'json',
                data: data,
                success: function(results) {
                    self.find('option:gt(0)').remove();

                    for (var i = 0, option; i < results.length; ++i) {
                        option = results[i];

                        self.append(new Option(option.text, option.id, true, original_value == option.id));
                    }

                    self.trigger('change');
                }
            });
        }

        $(filter_by).change(populate);
    });
});

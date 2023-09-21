odoo.define('assafa.request_price_popup', function (require) {
    "use strict";

    var publicWidget = require('web.public.widget');

    publicWidget.registry.ProductPriceRequest = publicWidget.Widget.extend({
        selector: '.js_request_price',
        events: {
            'click': '_onRequestPriceClick',
        },
        _onRequestPriceClick: function (ev) {
            ev.preventDefault();
            var $modal = $('#productPriceRequestModal');
            $modal.modal('show');
        },
    });

    return {
        ProductPriceRequest: publicWidget.registry.ProductPriceRequest,
    };
});
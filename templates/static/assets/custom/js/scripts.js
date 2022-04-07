(function () {
    select_variation = document.getElementById('select-variations');
    variation_price = document.getElementById('variation-price');
    variation_promotional_price = document.getElementById('variation-promotional-price');

    if (!select_variation) {
        return;
    }

    if (!variation_price) {
        return;
    }

    select_variation.addEventListener('change', function () {
        price = this.options[this.selectedIndex].getAttribute('price-data');
        promotional_price = this.options[this.selectedIndex].getAttribute('promotional-price-data');

        variation_price.innerHTML = price;

        if (variation_promotional_price) {
            variation_promotional_price.innerHTML = promotional_price;
        }
    })
})();


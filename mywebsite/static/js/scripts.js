document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.product-item button');

    buttons.forEach(button => {
        button.addEventListener('click', function() {
            alert('Added to cart');
            // Here, you can add functionality to add the item to a cart.
        });
    });
});

document.querySelectorAll('.add-to-cart-btn').forEach(button => {
    button.addEventListener('click', function() {
        const productElement = this.closest('.product');
        const product = {
            name: productElement.getAttribute('data-name'),
            price: `$${productElement.getAttribute('data-price')}`,
            image: productElement.getAttribute('data-image'),
            quantity: 1  
        };
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        const existingProductIndex = cart.findIndex(item => item.name === product.name);
        if (existingProductIndex > -1) {
            cart[existingProductIndex].quantity += 1;
        } else {
            cart.push(product);
        }
        localStorage.setItem('cart', JSON.stringify(cart));
        alert(`${product.name} has been added to your cart.`);
    });
});

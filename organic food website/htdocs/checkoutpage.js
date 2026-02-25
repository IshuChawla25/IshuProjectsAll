document.addEventListener('DOMContentLoaded', () => {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartItemsContainer = document.getElementById('cart-items');
    const totalPriceElement = document.getElementById('total-price');
    const totalQuantityElement = document.getElementById('total-quantity'); 
  
    let totalPrice = 0;
    let totalQuantity = 0; 
    let items = []; 
  
    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p>Your cart is empty.</p>';
        totalPriceElement.textContent = '$0.00';
        totalQuantityElement.textContent = '0'; 
        return;
    }
  
    
    cart.forEach((item, index) => {
        const itemDiv = document.createElement('div');
        itemDiv.classList.add('cart-item');
        itemDiv.innerHTML = `
            <img src="${item.image}" alt="${item.name}" width="100" height="100">
            <div>
                <p>${item.name}</p>
                <p>Quantity: ${item.quantity}</p>
                <p>Price: ${item.price}</p>
                <p>Total: $${(parseFloat(item.price.replace('$', '')) * item.quantity).toFixed(2)}</p>
                <button class="remove-item" data-index="${index}">Remove Item</button>
            </div>
        `;
        cartItemsContainer.appendChild(itemDiv);
  
        
        totalPrice += parseFloat(item.price.replace('$', '')) * item.quantity;
        totalQuantity += item.quantity; 
  
        
        items.push(item.name);
    });
  
    totalPriceElement.textContent = `$${totalPrice.toFixed(2)}`;
    totalQuantityElement.textContent = totalQuantity; 
  
    
    document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', (event) => {
            const index = event.target.getAttribute('data-index');
            removeItem(index);
        });
    });
  
 
    document.getElementById('checkout-btn').addEventListener('click', function() {
        const selectedPayment = document.querySelector('input[name="payment"]:checked');
        const addressInputs = document.querySelectorAll('#address-form input');
  
        
        if (!selectedPayment) {
            alert('Please select a payment method!');
            return; 
        }
  
       
        for (let input of addressInputs) {
            if (!input.value.trim() && input.hasAttribute('required')) {
                alert('Please fill all required address fields!');
                return; 
            }
        }
  
        
        document.getElementById('payment-input').value = selectedPayment.value;
  
        
        document.getElementById('total-price-input').value = totalPrice.toFixed(2);
        document.getElementById('total-quantity-input').value = totalQuantity;

        
        document.getElementById('items-input').value = items.join(',');

        
        document.getElementById('address-form').submit();
    });
});


function removeItem(index) {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    cart.splice(index, 1); 
    localStorage.setItem('cart', JSON.stringify(cart));
    location.reload(); 
}

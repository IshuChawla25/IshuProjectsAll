function loadCart() {
  const cart = JSON.parse(localStorage.getItem('cart')) || [];
  const cartItems = document.getElementById('cart-items');
  const totalQuantityElement = document.getElementById('total-quantity'); 
  cartItems.innerHTML = '';

  let totalQuantity = 0; 

  if (cart.length === 0) {
      cartItems.innerHTML = '<tr><td colspan="5">Your cart is empty.</td></tr>';
      updateCartSummary();
      totalQuantityElement.textContent = '0'; 
      return;
  }

  cart.forEach((item, index) => {
      const row = document.createElement('tr');

      
      const productCell = document.createElement('td');
      productCell.innerHTML = `
          <img src="${item.image}" alt="${item.name}" width="100" height="100">
          <span class="product-name">${item.name}</span>
      `;
      row.appendChild(productCell);

     
      const priceCell = document.createElement('td');
      priceCell.className = 'product-price';
      priceCell.textContent = item.price;
      row.appendChild(priceCell);


      const quantityCell = document.createElement('td');
      quantityCell.className = 'product-quantity';
      quantityCell.innerHTML = `
          <button class="quantity-btn" onclick="updateQuantity(${index}, -1)">-</button>
          <span class="quantity">${item.quantity}</span>
          <button class="quantity-btn" onclick="updateQuantity(${index}, 1)">+</button>
          <button class="remove-item" onclick="removeItem(${index})">Remove</button>
      `;
      row.appendChild(quantityCell);

      
      const totalCell = document.createElement('td');
      totalCell.className = 'product-total';
      totalCell.textContent = `$${(item.quantity * parseFloat(item.price.replace('$', ''))).toFixed(2)}`;
      row.appendChild(totalCell);

      cartItems.appendChild(row);
      totalQuantity += item.quantity; 
  });

  totalQuantityElement.textContent = totalQuantity; 
  updateCartSummary();
}


function updateQuantity(index, change) {
  const cart = JSON.parse(localStorage.getItem('cart')) || [];
  const item = cart[index];
  const newQuantity = item.quantity + change;

  if (newQuantity < 1) return; 

  item.quantity = newQuantity;
  localStorage.setItem('cart', JSON.stringify(cart));

  
  const quantitySpan = document.querySelectorAll('.product-quantity')[index].querySelector('.quantity');
  quantitySpan.textContent = item.quantity;

  
  const price = parseFloat(item.price.replace('$', ''));
  const totalCell = document.querySelectorAll('.product-total')[index];
  totalCell.textContent = `$${(item.quantity * price).toFixed(2)}`;

  loadCart(); 
}


function removeItem(index) {
  const cart = JSON.parse(localStorage.getItem('cart')) || [];
  cart.splice(index, 1); 
  localStorage.setItem('cart', JSON.stringify(cart));

  
  loadCart();
}


function updateCartSummary() {
  const totalCells = document.querySelectorAll('.product-total');
  let total = 0;
  totalCells.forEach(cell => {
      total += parseFloat(cell.textContent.replace('$', ''));
  });
  document.querySelector('.total-price').textContent = `Total: $${total.toFixed(2)}`;
}


function resetCart() {
  
  localStorage.removeItem('cart');
  
  
  loadCart();
  
  
  alert('Your cart has been reset.');
}


window.onload = loadCart;

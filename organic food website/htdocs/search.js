const organicFoodData = [
  { name: 'Apples', price: '$3.99', image: 'images/fresh-organic-apple.jpg' },
  { name: 'Bananas', price: '$1.29', image: 'images/banana.jpg' },
  { name: 'Carrots', price: '$2.49', image: 'images/carrot.jpg' },
  { name: 'Broccoli', price: '$2.99', image: 'images/Broccoli.webp' },
  { name: 'Strawberries', price: '$4.99', image: 'images/strawberry.jpg' },
  { name: 'Spinach', price: '$3.49', image: 'images/spinach.jpg' },
  { name: 'Tomato', price: '$2.99', image: 'images/tomato.jpg' },
  { name: 'Cucumber', price: '$1.99', image: 'images/Cucumber.webp' },
  { name: 'Bell Pepper', price: '$3.49', image: 'images/pepper.jpg' },
  { name: 'Potatoes', price: '$1.79', image: 'images/potato.png' },
  { name: 'Onions', price: '$0.99', image: 'images/onion.webp' },
  { name: 'Garlic', price: '$3.99', image: 'imagesa/garlic.webp' },
  { name: 'Kiwis', price: '$4.49', image: 'images/kiwi.webp' },
  { name: 'Blueberries', price: '$2.99', image: 'images/blueberries.webp' },
  { name: 'Peaches', price: '$3.99', image: 'images/peaches.webp' },
  { name: 'Lemons', price: '$2.49', image: 'images/lemons.webp' },
  { name: 'Grapes', price: '$4.99', image: 'images/graphes.webp' },

  
];

let cart = JSON.parse(localStorage.getItem('cart')) || [];
const style = document.createElement('style');
style.textContent = `
    /* Style for Add to Cart button */
    .result-item button {
        background-color: #4CAF50; /* Green background */
        color: white; /* White text */
        border: none; /* Remove border */
        padding: 10px 20px; /* Padding for button */
        font-size: 16px; /* Font size */
        border-radius: 5px; /* Rounded corners */
        cursor: pointer; /* Pointer cursor on hover */
        transition: background-color 0.3s ease; /* Smooth background color change */
    }

    .result-item button:hover {
        background-color: #45a049; /* Darker green on hover */
    }

    .result-item button:active {
        background-color: #3e8e41; /* Even darker green when clicked */
        transform: scale(0.98); /* Slightly shrink when clicked */
    }

    /* Space around the button */
    .result-item {
        margin-bottom: 20px;
    }

    .result-item img {
        margin-bottom: 10px; /* Add space between image and other content */
    }
`;

document.head.appendChild(style);

const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const resultsList = document.getElementById('results-list');

function displayResults(data) {
  resultsList.innerHTML = '';

  if (data.length > 0) {
    data.forEach((item) => {
      const listItem = document.createElement('li');
      listItem.className = 'result-item';

      const image = document.createElement('img');
      image.src = item.image;
      image.alt = item.name;
      image.width = 100;
      image.height = 100;

      const nameAndPrice = document.createElement('p');
      nameAndPrice.textContent = `${item.name} - ${item.price}`;

      const addToCartButton = document.createElement('button');
      addToCartButton.textContent = 'Add to Cart';
      addToCartButton.addEventListener('click', () => addToCart(item));

      listItem.appendChild(image);
      listItem.appendChild(nameAndPrice);
      listItem.appendChild(addToCartButton);
      resultsList.appendChild(listItem);
    });
  } else {
    resultsList.innerHTML = '<li>No results found</li>';
  }
}

function addToCart(item) {
  const existingItem = cart.find(cartItem => cartItem.name === item.name);

  if (existingItem) {
    existingItem.quantity += 1;
  } else {
    cart.push({ ...item, quantity: 1 });
  }

  localStorage.setItem('cart', JSON.stringify(cart)); 
  alert(`${item.name} has been added to your cart.`);
}
searchButton.addEventListener('click', () => {
  const searchTerm = searchInput.value.trim().toLowerCase();
  if (searchTerm === '') {
    resultsList.innerHTML = '<li>Please enter a search term.</li>';
  } else {
    const filteredData = organicFoodData.filter(
      (item) =>
        item.name.toLowerCase().includes(searchTerm)
    );
    displayResults(filteredData);
  }
});

searchInput.addEventListener('input', () => {
  const searchTerm = searchInput.value.trim().toLowerCase();

  if (searchTerm === '') {
    resultsList.innerHTML = ''; 
  } else {
    const filteredData = organicFoodData.filter(
      (item) =>
        item.name.toLowerCase().includes(searchTerm)
    );
    displayResults(filteredData);
  }
});


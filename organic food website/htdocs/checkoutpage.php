<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "organic_food";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $full_name = $_POST['full_name'];
    $address_line1 = $_POST['address_line1'];
    $address_line2 = $_POST['address_line2'];
    $city = $_POST['city'];
    $postal_code = $_POST['postal_code'];
    $country = $_POST['country'];
    $items = $_POST['items']; 
    $total_price = $_POST['total_price'];
    $total_quantity = $_POST['total_quantity'];
    $payment_method = $_POST['payment']; 
    

    if (empty($payment_method)) {
        echo "Payment method is required.";
        exit; 
    }

    
    $sql = "INSERT INTO orders (full_name, address_line1, address_line2, city, postal_code, country, items, total_price, total_quantity, payment_method) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

    
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ssssssssss", $full_name, $address_line1, $address_line2, $city, $postal_code, $country, $items, $total_price, $total_quantity, $payment_method);

    
    if ($stmt->execute()) {
        echo "<script>
            alert('Order placed successfully!');
            window.location.href = 'index.html'; // Redirect to index.html
          </script>";
    } else {
        echo "Error: " . $stmt->error;
    }

    
    $stmt->close();
    $conn->close();
}




?>

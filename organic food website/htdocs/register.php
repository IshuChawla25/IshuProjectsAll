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
    $user_username = $_POST['username'];
    $user_email = $_POST['email'];
    $user_password = $_POST['password'];
    $confirm_password = $_POST['confirm-password'];
    $address = $_POST['address'];
    $phone = $_POST['phone'];

    if ($user_password !== $confirm_password) {
        echo "Passwords do not match!";
        exit();
    }

    $sql = "INSERT INTO users (username, email, password, address, phone) VALUES (?, ?, ?, ?, ?)";

    $stmt = $conn->prepare($sql);

    if ($stmt === false) {
        die('MySQL prepare error: ' . $conn->error);
    }
    $stmt->bind_param("sssss", $user_username, $user_email, $user_password, $address, $phone);
    if ($stmt->execute()) {
        echo "<script>
                alert('Registered successfully!');
                window.location.href = 'login.html'; // Redirect to login page
              </script>";
    } else {
        echo "Error: " . $stmt->error;
    }
    $stmt->close();
    $conn->close();
}

/*
    CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
*/
?>

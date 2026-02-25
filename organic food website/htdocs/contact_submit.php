<?php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
   
    $name = htmlspecialchars(trim($_POST['name']));
    $email = htmlspecialchars(trim($_POST['email']));
    $message = htmlspecialchars(trim($_POST['message']));

    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        die("Invalid email format. Please enter a valid email.");
    }

    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "organic_food";

    $conn = new mysqli($servername, $username, $password, $dbname);

    if ($conn->connect_error) {
        error_log("Connection Error: " . $conn->connect_error, 0);
        die("Could not connect to the database. Please try again later.");
    }

    $stmt = $conn->prepare("INSERT INTO contactform (name, email, message) VALUES (?, ?, ?)");
    if ($stmt === false) {
        error_log("SQL Prepare Error: " . $conn->error, 0);
        die("An error occurred while preparing the query. Please try again later.");
    }

    
    $stmt->bind_param("sss", $name, $email, $message);
    if ($stmt->execute()) {
        echo "<script type='text/javascript'>alert('Your message has been sent successfully!');
                window.location.href = 'contact.html';
        </script>";
    } else {
        error_log("Execute Error: " . $stmt->error, 0);
        die("An error occurred while submitting your message. Please try again later.");
    }

    $stmt->close();
    $conn->close();
} else {
    die("Invalid request method.");
}
?>

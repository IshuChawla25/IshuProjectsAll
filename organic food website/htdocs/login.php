<?php
session_start();
$servername = "localhost";
$username = "root"; // Your database username
$password = ""; // Your database password
$dbname = "organic_food"; // Your database name

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];
    $username = $conn->real_escape_string($username);
    $password = $conn->real_escape_string($password);

    $sql = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $_SESSION['username'] = $username;
        echo "<script>
                alert('Login successful!');
                window.location.href = 'index.html';
              </script>";
        exit();
    } else {
        echo "<script>
                alert('invalid username and password!');
                window.location.href = 'login.html';
              </script>";
    }
}
$conn->close();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Page</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</head>
<body>
    <header>
        <!-- Navigation Code (No Changes Here) -->
    </header>

    <div class="body">
        <main>
            <div class="search-bar">
                <form method="GET" action="search.php">
                    <input 
                        type="text" 
                        id="search-input" 
                        name="query" 
                        placeholder="Search For Products..">
                    <br><br>
                    <button id="search-button" type="submit">Search</button>
                </form>
            </div>

            <div class="search-results">
                <h2>Search Results:</h2>
                <ul id="results-list">
                    <?php
                    if (isset($_GET['query']) && !empty($_GET['query'])) {
                        $query = htmlspecialchars($_GET['query']);

                        // Connect to the database
                        $conn = new mysqli("localhost", "username", "password", "database");

                        // Check for connection error
                        if ($conn->connect_error) {
                            die("Connection failed: " . $conn->connect_error);
                        }

                        // Prepare SQL query with LIKE for search functionality
                        $stmt = $conn->prepare("SELECT name, price, image FROM products WHERE name LIKE ?");
                        $searchTerm = "%" . $query . "%";
                        $stmt->bind_param("s", $searchTerm);
                        $stmt->execute();

                        // Fetch results
                        $result = $stmt->get_result();

                        if ($result->num_rows > 0) {
                            // Output each result as a list item
                            while ($row = $result->fetch_assoc()) {
                                echo '<li class="result-item">';
                                echo '<img src="' . htmlspecialchars($row['image']) . '" alt="' . htmlspecialchars($row['name']) . '" width="100" height="100">';
                                echo '<p><strong>' . htmlspecialchars($row['name']) . '</strong> - $' . htmlspecialchars($row['price']) . '</p>';
                                echo '</li>';
                            }
                        } else {
                            // No results found
                            echo '<li>No results found for "' . htmlspecialchars($query) . '"</li>';
                        }

                        // Close statement and connection
                        $stmt->close();
                        $conn->close();
                    } else {
                        echo '<li>Please enter a search term to see results.</li>';
                    }
                    ?>
                </ul>
            </div>
        </main>
    </div>

    <footer>
        <!-- Footer Code (No Changes Here) -->
    </footer>
</body>
</html>

<?php
require_once "config.php";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Retrieve the CUNY ID from the login form
    $cunyEMPLD = $_POST["cunyEMPLD"];
    

    // Check if the CUNY ID exists in the database
    $sql = "SELECT * FROM stuUsers WHERE cunyEMPLD = '$cunyEMPLD'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        // CUNY ID found, redirect to display.php
        header("Location: display.php?cunyEMPLD=$cunyEMPLD");
        exit();
    } else {
        // CUNY ID not found, redirect to myAccount.html
        header("Location: myAccount3.html?cunyEMPLD=$cunyEMPLD");
        exit();
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <meta name ="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home Page</title>
    <link rel="stylesheet" href="style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com"> 
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;600;700&display=swap" rel="stylesheet">
<link rel ="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
<section class="sub-header">
        <nav>
            <a href="index.html"><img src="images/internshipPhoto8.png"></a>
            <div class="nav-links" id="navLinks">
                <i class="fa fa-times" onclick="hideMenu()"></i>
                <ul>
                    <li><a href="index.html">Home</a></li>
                    <li><a href="about.html">About</a></li>
                    <li><a href="jobBoard.html">Job Board</a></li>
                    <li><a href="events.html">Events</a></li>
                    <li><a href="careerInfo.html">Career Info</a></li>
                    <li><a href="login.html">Login</a></li>
                </ul>
            </div>
            <i class="fa fa-bars" onclick="showMenu()"></i>
        </nav>
    
    <h1>DELETE ACCOUNT</h1>
</section>

<?php
// Establish a connection to your MySQL database
require_once "config.php";

// Process form data when the form is submitted
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    // Retrieve the cunyEMPLD from the form
    $cunyEMPLD = $conn->real_escape_string($_POST["cunyEMPLD"]);

    // Delete the account from the database
    $sql = "DELETE FROM stuUsers WHERE cunyEMPLD = '$cunyEMPLD'";

    if ($conn->query($sql) === TRUE) {
        echo "Account deleted successfully.";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }

    // Close the database connection
    $conn->close();
}
?>

    <!------Footer--------------->

    <section class="footer">
        <h4>About Us</h4>
        <p>Our project was brought to life by the collaborative efforts of Gagne Cire Niang, Hannah George, and Mukhlisa Nematova.
            Together, we are dedicated to guiding students towards their goals by providing a platform to discover 
            relevant courses, workshops, and resources that will facilitate their career path. We believe in empowering
            students to make informed decisions and embark on a successful educational journey.</p>
        <div class="icons">
            <i class="fa fa-facebook"></i>
            <i class="fa fa-twitter"></i>
            <i class="fa fa-instagram"></i>
            <i class="fa fa-linkedin"></i>       
        </div>

</section>


</body>
</html>

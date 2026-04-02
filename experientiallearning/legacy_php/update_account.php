<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Update Account</title>
    <link rel="stylesheet" href="style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com"> 
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
</head>
<body>
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

        
        <h1>UPDATE ACCOUNT</h1>
    </section>


<?php
// Establish a connection to your MySQL database
require_once "config.php";

// Define variables and set to empty values
$errors = [];
$sName = $sEmail = $sTelephone = $cunyEMPLD = $sYear = $sMajor = $sGPA = $sGradDate = $sExplore = $sComments = "";
$sInterests = $sSkills = $sCerts = $certExp = $skillLevel = [];
$successMessage = "";

// Process form data when the form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Validate sName
    $sName = validateInput($_POST['sName'], "Name is required");

    // Validate sEmail
    $sEmail = validateInput($_POST['sEmail'], "Email is required");
    if (!filter_var($sEmail, FILTER_VALIDATE_EMAIL)) {
        $errors[] = "Invalid email format";
    }

    // Validate sTelephone
    $sTelephone = validateInput($_POST['sTelephone'], "Telephone is required");

    // Validate cunyEMPLD
    $cunyEMPLD = validateInput($_POST['cunyEMPLD'], "CUNY EMPL ID is required");

    // Validate academicYear
    $sYear = validateInput($_POST['sYear'], "Academic year is required");

    // Validate major
    $sMajor = validateInput($_POST['sMajor'], "Major is required");

    // Validate gpa
    $sGPA = validateInput($_POST['sGPA'], "GPA is required");

    // Validate gradDate
    $sGradDate = validateInput($_POST['sGradDate'], "Graduation date is required");

    // Validate sExplore
    $sExplore = isset($_POST['sExplore']) ? "Yes" : "No";

    // Set optional fields
    $sComments = isset($_POST['sComments']) ? $_POST['sComments'] : "";

    // Check if any interests are selected
    if (!empty($_POST['sInterests']) && is_array($_POST['sInterests'])) {
        $sInterests = $_POST['sInterests'];
    }

    // Check if any skills are selected
    if (!empty($_POST['sSkills']) && is_array($_POST['sSkills'])) {
        $sSkills = $_POST['sSkills'];
    }
    $skillLevel = $_POST['skillLevel'];

    // Check if any certifications are selected
    if (!empty($_POST['sCert']) && is_array($_POST['sCert'])) {
        $sCerts = $_POST['sCert'];
        $certExp = $_POST['certExp'];
    }

    // If there are no errors, update the data in the SQL tables
    if (empty($errors)) {
        // Update data in stuUsers table
        $stmt_users = $conn->prepare("UPDATE stuUsers SET sName = ?, sEmail = ?, sTelephone = ?, sYear = ?, sMajor = ?, sGPA = ?, sGradDate = ?, sExplore = ?, sComments = ? WHERE cunyEMPLD = ?");
        $stmt_users->bind_param("ssssssdsss", $sName, $sEmail, $sTelephone, $sYear, $sMajor, $sGPA, $sGradDate, $sExplore, $sComments, $cunyEMPLD);

        if ($stmt_users->execute()) {
            $successMessage = "Your information has been updated.";

            // Delete existing data in stuInterest table for the student
            $stmt_delete_interests = $conn->prepare("DELETE FROM stuInterest WHERE cunyEMPLD = ?");
            $stmt_delete_interests->bind_param("s", $cunyEMPLD);
            $stmt_delete_interests->execute();

            // Insert updated data into stuInterest table
            foreach ($sInterests as $interest) {
                $stmt_interests = $conn->prepare("INSERT INTO stuInterest (cunyEMPLD, sInterests) VALUES (?, ?)");
                $stmt_interests->bind_param("ss", $cunyEMPLD, $interest);
                $stmt_interests->execute();
            }

            // Delete existing data in stuSkills table for the student
            $stmt_delete_skills = $conn->prepare("DELETE FROM stuSkills WHERE cunyEMPLD = ?");
            $stmt_delete_skills->bind_param("s", $cunyEMPLD);
            $stmt_delete_skills->execute();

            // Insert updated data into stuSkills table
            foreach ($sSkills as $i => $skill) {
                $stmt_skills = $conn->prepare("INSERT INTO stuSkills (cunyEMPLD, sSkills, skillLevel) VALUES (?, ?, ?)");
                $stmt_skills->bind_param("sss", $cunyEMPLD, $skill, $skillLevel[$i]);
                $stmt_skills->execute();
            }

            // Delete existing data in stuCerts table for the student
            $stmt_delete_certs = $conn->prepare("DELETE FROM stuCerts WHERE cunyEMPLD = ?");
            $stmt_delete_certs->bind_param("s", $cunyEMPLD);
            $stmt_delete_certs->execute();

            // Insert updated data into stuCerts table
            foreach ($sCerts as $i => $cert) {
                $stmt_certs = $conn->prepare("INSERT INTO stuCerts (cunyEMPLD, sCerts, certExp) VALUES (?, ?, ?)");
                $stmt_certs->bind_param("sss", $cunyEMPLD, $cert, $certExp[$i]); // Retrieve certExp based on index $i
                $stmt_certs->execute();
            }
        } else {
            $errors[] = "Error: " . $stmt_users->error;
        }

        $stmt_users->close();
        $stmt_delete_interests->close();
        $stmt_delete_skills->close();
        $stmt_delete_certs->close();
    }
}

// Helper function to validate form input
function validateInput($input, $errorMessage) {
    $input = trim($input);
    if (empty($input)) {
        $GLOBALS['errors'][] = $errorMessage;
    }
    return $input;
}
?>
    <!-- Display error messages -->
    <?php if (!empty($errors)): ?>
        <ul class="errors">
            <?php foreach ($errors as $error): ?>
                <li><?php echo $error; ?></li>
            <?php endforeach; ?>
        </ul>
    <?php endif; ?>

    <!-- Display success message -->
    <?php if (!empty($successMessage)): ?>
        <h2><?php echo $successMessage; ?></h2>
    <?php endif; ?>

    <!------Footer--------------->

    <section class="footer">
        <h4>About Us</h4>
        <p>
            Our project was brought to life by the collaborative efforts of Gagne Cire Niang, Hannah George, and Mukhlisa Nematova.
            Together, we are dedicated to guiding students towards their goals by providing a platform to discover
            relevant courses, workshops, and resources that will facilitate their career path. We believe in empowering
            students to make informed decisions and embark on a successful educational journey.
        </p>
        <div class="icons">
            <i class="fa fa-facebook"></i>
            <i class="fa fa-twitter"></i>
            <i class="fa fa-instagram"></i>
            <i class="fa fa-linkedin"></i>
        </div>
    </section>
</body>
</html>



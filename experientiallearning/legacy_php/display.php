<head>
<style>


.student-info {
  background-color: #fff3f3;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin:auto;
  width: 700px;
}

.student-info h2 {
  color: #333;
  font-size: 20px;
 --margin:auto;
  text-align: center;
}

.student-info ul {
  list-style: none;
  padding: 0;
  width: 700px;
  text-align: center;
}

.student-info li {
    margin:auto;
}

.student-info li strong {
  font-weight: bold;
  margin:auto;
}

.event-calendar h2 {
  color: #000
  font-size: 20px;
  margin:auto;
  text-align: center;
}

.event {
  background-color: #fff3f3;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 5px;
  margin:auto;
  width: 700px; 
}

.event h3 {
  color: #000000
  font-size: 20px;
  margin:auto;
  text-align: center;
}

.event p {
    color: #000000
    margin-bottom: 10px;
    text-align: center;
    font-size: 15px;

}

.event p strong {

  font-weight: bold;
  margin:auto;
}

</style>
</head>
<body>
<!DOCTYPE html>
<html>
<head>
    <meta name ="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home Page</title>
    <link rel="stylesheet" href="style.css">
    <link rel="preconnect" href="https://fonts.googleapis.com"> 
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;600;700&display=swap" rel="stylesheet">
<link rel ="stylesheet" href="https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css">
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
            <h1>MY ACCOUNT</h1>
    </section>
    <nav>
        <div class="nav-links" id="navLinks">
                    <i class="fa fa-times" onclick="hideMenu()"></i>
                    <ul>
                        <a href="update.html">Update Account</a>&emsp; 
                        <a href="delete.html">Delete Account</a> <br><br>
                        </ul>
            
                <i class="fa fa-bars" onclick="showMenu()"></i>
        </div>
    </nav>
</head>

<!-----------PHP SECTION----------------->  
<?php
require_once "config.php";

// Get the CUNY EMPLID of the logged-in student
$cunyEMPLD = $_GET['cunyEMPLD']; // Replace 'cunyEMPLD' with the actual variable storing the CUNY EMPLID
//$cunyEMPLD = 12345678;
// Rest of the code to display student information


$sql = "SELECT * FROM stuUsers WHERE cunyEMPLD = '$cunyEMPLD'";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();


    echo '<div class="student-info">';
    echo '<h2>Student Information</h2>';
    echo '<ul>';
    echo "<li><strong>Name:</strong> {$row['sName']}</li>";
    echo "<li><strong>Email:</strong> {$row['sEmail']}</li>";
    echo "<li><strong>Telephone:</strong> {$row['sTelephone']}</li>";
    echo "<li><strong>CUNY EMPLID:</strong> {$row['cunyEMPLD']}</li>";
    echo "<li><strong>Year:</strong> {$row['sYear']}</li>";
    echo "<li><strong>Major:</strong> {$row['sMajor']}</li>";
    echo "<li><strong>GPA:</strong> {$row['sGPA']}</li>";
    echo "<li><strong>Graduation Date:</strong> {$row['sGradDate']}</li>";
    echo "<li><strong>Interests:</strong> ";

    $interestsSql = "SELECT sInterests FROM stuInterest WHERE cunyEMPLD = '$cunyEMPLD'";
    $interestsResult = $conn->query($interestsSql);

    if ($interestsResult->num_rows > 0) {
        echo '<ul>';
        while ($interestRow = $interestsResult->fetch_assoc()) {
            echo "<li>{$interestRow['sInterests']}</li>";
        }
        echo '</ul>';
    }

    echo '</li>';

    echo "<li><strong>Skills:</strong> ";

    $skillsSql = "SELECT sSkills, skillLevel FROM stuSkills WHERE cunyEMPLD = '$cunyEMPLD'";
    $skillsResult = $conn->query($skillsSql);

    if ($skillsResult->num_rows > 0) {
        echo '<ul>';
        while ($skillsRow = $skillsResult->fetch_assoc()) {
            echo "<li>{$skillsRow['sSkills']} ({$skillsRow['skillLevel']})</li>";
        }
        echo '</ul>';
    }

    echo '</li>';

    echo "<li><strong>Certifications:</strong> ";

    $certsSql = "SELECT sCerts, certExp FROM stuCerts WHERE cunyEMPLD = '$cunyEMPLD'";
    $certsResult = $conn->query($certsSql);

    if ($certsResult->num_rows > 0) {
        echo '<ul>';
        while ($certRow = $certsResult->fetch_assoc()) {
            echo "<li>{$certRow['sCerts']} ({$certRow['certExp']})</li>";
        }
        echo '</ul>';
    }

    echo "<li><strong>Explore:</strong> {$row['sExplore']}</li>";
    echo "<li><strong>Comments:</strong> {$row['sComments']}</li>";
    echo '</ul>';
    echo '</div><br><hr>';

    // Retrieve events registered by the student
    $eventsSql = "SELECT * FROM eventsAttendance WHERE cunyEMPLD = '$cunyEMPLD'";
    $eventsResult = $conn->query($eventsSql);

    if ($eventsResult->num_rows > 0) {
        echo '<div class="event-calendar">';
        echo '<br><br><h2>Calander Events</h2>';

        while ($eventRow = $eventsResult->fetch_assoc()) {
            echo '<div class="event">';
            echo "<h3>{$eventRow['eventName']}</h3>";
            echo "<p><strong>Date:</strong> {$eventRow['eventDate']}</p>";
            echo "<p><strong>Time:</strong>  {$eventRow['eventTime']}</p>";
            echo "<p><strong>Location:</strong>  {$eventRow['eventLocation']}</p>";
            echo '</div><br>';
        }

        echo '</div>';
    } else {
        echo '<p>No calander events found.</p>';
    }

} else {
    echo "No student found with the provided CUNY EMPLID.";
}

$conn->close();
?>

<br><br>

 <!------Footer--------------->

 <section class="footer">
            <h4>About Us</h4>
            
       
            <p>Our project was brought to life by the collaborative efforts of Gagne Cire Niang, Hannah George, and Mukhlisa Nematova.
                Together, we are dedicated to guiding students towards their goals by providing a platform to discover 
                relevant courses, workshops, and resources that will facilitate their career path. We believe in empowering
                students to make informed decisions and embark on a successful educational journey. <br>
                 <a target="_blank" href="https://sites.google.com/view/bmcctechinterns" style="color:red;">Copyright &copy 2023 - <script type="text/javascript">document.write(new Date().getFullYear());</script> BMCC Technology Learning Community Internship</a></p>
            <div class="icons">
                <i class="fa fa-facebook"></i>
                <i class="fa fa-twitter"></i>
                <i class="fa fa-instagram"></i>
                <i class="fa fa-linkedin"></i>       
            </div>
    
    </section>

</body>
</html>

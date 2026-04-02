<!DOCTYPE html>
<html>
<head>
    <meta name ="viewport" content="width=device-width, initial-scale=1.0">
    <title>Career Info</title>
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

    
    <h1>Technology Career Statistics </h1>
</section><br><br>

<!------PHP Section!----->

<?php
// Establish a connection to your MySQL database
require_once "config.php";

 //Chart1 - Job Openings in NYC
$openingsData = array(
	array("label"=> "Computer and Information Managers", "y"=> 6683),
	array("label"=> "Computer Programmers", "y"=> 1867),
	array("label"=> "Software Developers", "y"=> 17595),
	array("label"=> "Web Developer", "y"=> 1565),
	array("label"=> "Database Adminstrators", "y"=> 940),
	array("label"=> "Information Technology Project Managers", "y"=> 3150),
	array("label"=> "Business Intelligence Analysts", "y"=> 1803)
);

  //Chart2- Median Salary across different Careers 
$salaryData = array( 
	array("y" => 87,"label" => "Computer and Information Managers" ),
	array("y" => 45,"label" => "Computer Programmers" ),
	array("y" => 61,"label" => "Software Developers" ),
	array("y" => 35,"label" => "Web Developers" ),
	array("y" => 53,"label" => "Database Adminstrators"),
    array("y" => 43,"label" => "Information Technology Project Managers" ),
	array("y" => 59,"label" => "Business Intelligence Analysts")
);

// Chart3 - popular programming languages by developers!
$plData = array( 
	array("y" => 65.36, "label" => "JavaScript"),
	array("y" => 55.08, "label" => "HTML/CSS"),
	array("y" => 49.43, "label" => "SQL"),
	array("y" => 48.07, "label" => "Python"),
	array("y" => 33.27, "label" => "Java"),
	array("y" => 27.98, "label" => "C#"),
    array("y" => 22.55, "label" => "C++"),
	array("y" => 20.87, "label" => "PHP"),
	array("y" => 19.24, "label" => "C"),
	array("y" => 11.15, "label" => "Go"),
	array("y" => 6.05, "label" => "Ruby"),
	array("y" => 4.91, "label" => "Swift"),
    array("y" => 4.66, "label" => "R" ),
	array("y" => 4.10, "label" => "Matlab")
);
	
?>


    <script>
    window.onload = function () {
        //Chart 1 - current Job Openings
        var chart1 = new CanvasJS.Chart("chartContainer1", {
            animationEnabled: true,
            exportEnabled: true,
            title:{
                text: "Current Job Openings in New York",
                fontFamily:"Geneva",
                fontWeight:"bold"
            },
            subtitles: [{
                text: "This chart shows the current job openings in NYC with the leading tech jobs (Source: BMCC Career Coach)",
                fontFamily:"Geneva"
            }],
            data: [{
                type: "pie",
                showInLegend: "true",
                legendText: "{label}",
                indexLabelFontSize: 16,
                indexLabel: "{label} - #percent%",
                yValueFormatString: "##0",
                dataPoints: <?php echo json_encode($openingsData, JSON_NUMERIC_CHECK); ?>
            }]
        });

        //Chart2- Median Salary across different Careers 
        var chart2 = new CanvasJS.Chart("chartContainer2", {
            animationEnabled: true,
            theme: "light2",
            title:{
                text: "Median Salary for Different Tech Careers",
                fontFamily:"Geneva",
                fontWeight:"bold"
            },
            subtitles: [{
                text: "This chart shows the median salary of common technology jobs in NYC. (Source: BMCC Career Coach)",
                fontFamily:"Geneva"
            }],
            axisY: {
                title: "$/perHour (in USD)",
                includeZero: true,
                prefix: "$"
            },
            data: [{
                type: "spline",
                lineThickness: 3,
                yValueFormatString: "$#,##0",
                indexLabel: "{y}",
                indexLabelPlacement: "inside",
                indexLabelFontWeight: "bolder",
                indexLabelFontColor: "white",
                dataPoints: <?php echo json_encode($salaryData , JSON_NUMERIC_CHECK); ?>
                }]
        });

        // Chart3 - popular programming languages by developers!
        var chart3 = new CanvasJS.Chart("chartContainer3", {
            animationEnabled: true,
            theme: "light2",
            title:{
                text: "Most Used Programming Languages Across Industries Worldwide",
                fontFamily:"Geneva",
                fontWeight:"bold"
            },
            subtitles: [{
                text: " As of 2022, JavaScript and HTML/CSS were the most commonly used programming languages among software developers around the world, with more than 65 percent of respondents stating that they used JavaScript and just over 55 percent using HTML/CSS. Python, and SQL rounded out the top four most widely used programming languages around the world (Source: statista.com)",
                fontFamily:"Geneva"
            }],
            axisY: {
                title: "% of People Using Language"
            },
            data: [{
                type: "column",
                yValueFormatString: "##.#0 '%'",
                dataPoints: <?php echo json_encode($plData, JSON_NUMERIC_CHECK); ?>
            }]
        }); 



        chart1.render();
        chart2.render();
        chart3.render();
    
    }
    </script>

    <div class = chartContainer id="chartContainer2" style="height: 400px; width: 70%; margin:auto;"><br></div><br><hr><br>
    <div class = chartContainer  id="chartContainer1" style="height: 500px; width: 100%;"></div><br><hr><br>
    <div class = chartContainer id="chartContainer3" style="height: 350px; width: 85%; margin:auto;"></div><br>
    <script src="https://cdn.canvasjs.com/canvasjs.min.js"></script>



    <!------Footer--------------->
<hr>
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

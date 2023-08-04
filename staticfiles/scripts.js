
const navbar = document.getElementById("navbar");
const navbarToggle = navbar.querySelector(".navbar-toggle");

function openMobileNavbar() {
  navbar.classList.add("opened");
  navbarToggle.setAttribute("aria-expanded", "true");
}

function closeMobileNavbar() {
  navbar.classList.remove("opened");
  navbarToggle.setAttribute("aria-expanded", "false");
}

navbarToggle.addEventListener("click", () => {
  if (navbar.classList.contains("opened")) {
    closeMobileNavbar();
  } else {
    openMobileNavbar();
  }
});

const navbarMenu = navbar.querySelector("#navbar-menu");
const navbarLinksContainer = navbar.querySelector(".navbar-links");

navbarLinksContainer.addEventListener("click", (clickEvent) => {
  clickEvent.stopPropagation();
});

navbarMenu.addEventListener("click", closeMobileNavbar);


// Function to update the course tables based on the returned JSON data
function loadCourseList() {
  const majorSelect = document.getElementById('major');
  const selectedMajorId = majorSelect.value;

  // Fetch the course list for the selected major
  fetch(`/coursePlanner/?majorId=${selectedMajorId}`)
      .then((response) => response.json())
      .then((courseList) => {
          // Update the course tables with the fetched data
          updateTables(courseList);
      })
      .catch((error) => {
          console.error('Error fetching course data:', error);
      });

  // Prevent the form from submitting
  return false;
}

// Fetch the course list for the major with majorId=1
fetch('/coursePlanner/?majorId=1')
    .then((response) => response.json())
    .then((courseList) => {
    // Update the course tables with the fetched data
    updateTables(courseList);
    })
    .catch((error) => {
    console.error('Error fetching course data:', error);
    });
 


 
    function moveCourse() {
    const selectedCourses = document.getElementById('selected-courses');
    const allCourses = document.getElementById('all-courses');

    if (this.parentElement === selectedCourses) {
        // Deselect the course
        allCourses.appendChild(this);
    } else {
        // Select the course
        selectedCourses.appendChild(this);
    }

    updateButtonStates();
    updateTable();
    }

    function moveLeft() {
    const selectedCourses = document.getElementById('selected-courses');
    const allCourses = document.getElementById('all-courses');
    const selectedCourse = selectedCourses.querySelector('.item');

    if (selectedCourse) {
        allCourses.appendChild(selectedCourse);
    }

    updateButtonStates();
    updateTable();
    }

    function moveRight() {
    const selectedCourses = document.getElementById('selected-courses');
    const allCourses = document.getElementById('all-courses');
    const selectedCourse = allCourses.querySelector('.item');

    if (selectedCourse) {
        selectedCourses.appendChild(selectedCourse);
    }

    updateButtonStates();
    updateTable();
    }

    function updateButtonStates() {
    const selectedCourses = document.getElementById('selected-courses');
    const allCourses = document.getElementById('all-courses');
    const leftArrow = document.getElementById('left-arrow');
    const rightArrow = document.getElementById('right-arrow');

    leftArrow.disabled = selectedCourses.children.length === 0;
    rightArrow.disabled = allCourses.children.length === 0;
    }

    function updateTable() {
    const takenCoursesTable = document.getElementById('taken-courses-table');
    const remainingCoursesTable = document.getElementById('remaining-courses-table');
    const remainingCredits = calculateRemainingCredits();

    updateCoursesTable('selected-courses', takenCoursesTable);
    updateCoursesTable('all-courses', remainingCoursesTable);
    document.getElementById('remaining-credits').textContent = remainingCredits;

    // Call the updateDegreeCompletion function
    updateDegreeCompletion();
    }

    function updateCoursesTable(containerId, table) {
    const container = document.getElementById(containerId);
    const courses = container.getElementsByClassName('item');

    table.innerHTML = '';
    const headerRow = table.insertRow();
    headerRow.innerHTML = '<th>Course Name</th><th>Credits</th>';

    for (let i = 0; i < courses.length; i++) {
        const course = courses[i];
        const courseName = course.textContent;
        const credits = course.getAttribute('data-credits');

        const newRow = table.insertRow();
        newRow.innerHTML = `<td>${courseName}</td><td>${credits}</td>`;
    }
    }

    function calculateRemainingCredits() {
    const remainingCourses = document.getElementById('all-courses').getElementsByClassName('item');
    let remainingCredits = 0;
    for (let i = 0; i < remainingCourses.length; i++) {
        const credits = parseInt(remainingCourses[i].getAttribute('data-credits'));
        remainingCredits += credits;
    }
    return remainingCredits;
    }

    function calculateTakenCredits() {
    const takenCourses = document.getElementById('selected-courses').getElementsByClassName('item');
    let takenCredits = 0;
    for (let i = 0; i < takenCourses.length; i++) {
        const credits = parseInt(takenCourses[i].getAttribute('data-credits'));
        takenCredits += credits;
    }
    return takenCredits;
    }

    function updateDegreeCompletion() {
    const takenCoursesTable = document.getElementById('taken-courses-table');
    const remainingCoursesTable = document.getElementById('remaining-courses-table');
    const completionPercentage = document.getElementById('completion-percentage');

    const totalCourses = takenCoursesTable.rows.length - 1 + remainingCoursesTable.rows.length - 1;
    const takenCoursesCount = takenCoursesTable.rows.length - 1;
    const completion = (takenCoursesCount / totalCourses) * 100;

    completionPercentage.textContent = completion.toFixed(2) + '%';
    }
"""
Curated CIS / IT career graph for BMCC-style demos: majors, jobs, skills, courses, internships.

Pairs with `seed_careers_data` management command. Not scraped live — structured for relational integrity
across major ↔ skills ↔ jobs ↔ internship matcher. Optional BMCC HTML fetch can append program blurbs separately.
"""

from __future__ import annotations

# Skills referenced by jobs, majors, and internships — gapfiller powers page2 "how to build"
SKILLS: list[tuple[str, str]] = [
    ("Python", "Take CSC 210 / CIS programming sequence; add LeetCode / HackerRank labs and a GitHub portfolio project."),
    ("SQL", "Enroll in database courses (e.g., CIS 158 / equivalents); practice on PostgreSQL or SQLite side projects."),
    ("JavaScript", "Build a small React or vanilla JS app; use MDN tutorials and CIS web dev coursework."),
    ("Java", "Use BMCC CS Java track; contribute to a small OSS or classroom team project on GitHub."),
    ("HTML/CSS", "Complete responsive layouts in web dev courses; validate with W3C and Lighthouse."),
    ("Git / Version control", "Use GitHub Classroom or personal repos; follow Conventional Commits and branch workflows."),
    ("REST APIs", "Pair backend + frontend courses; document endpoints with OpenAPI; practice Postman."),
    ("Cloud basics (AWS/Azure)", "Finish cloud intro modules; pursue AWS Cloud Foundations or Azure Fundamentals badges."),
    ("Linux / CLI", "Use CSC lab VMs or WSL; automate with shell scripts in homework."),
    ("Networking fundamentals", "Take networking courses; practice with Packet Tracer or lab gear."),
    ("Cybersecurity awareness", "Compete in NCL or CyberStart; study NIST CSF and CIS controls summaries."),
    ("Data analysis", "Use pandas in Python or Excel Power Query; publish a notebook on Kaggle or Colab."),
    ("Machine learning intro", "Complete Andrew Ng–style MOOC alongside stats; keep a Kaggle notebook log."),
    ("Agile / Scrum", "Run sprints in group projects; document stand-ups and retros in README."),
    ("Communication", "Present demos in class; record a 2-minute Loom explaining a project."),
    ("Technical writing", "Write README specs; prepare one-page architecture for a capstone."),
    ("UI/UX basics", "Sketch in Figma; apply Nielsen heuristics to redesign a campus form."),
    ("Docker", "Containerize a simple Flask/Express app; document compose.yml."),
    ("NoSQL / MongoDB", "Contrast with SQL in a side project; cite CAP tradeoffs in write-up."),
    ("Systems design basics", "Diagram a small scalable app; reference Designing Data-Intensive Applications excerpts."),
]

COURSES: list[str] = [
    "CSC 210 – Computer Science I",
    "CSC 220 – Computer Science II",
    "CSC 350 – Data Structures",
    "CIS 100 – Introduction to Computer Applications",
    "CIS 155 – Computer Systems Technology",
    "CIS 158 – Database Management Systems",
    "CIS 165 – Web Design & Development",
    "CIS 255 – Systems Analysis & Design",
    "CIS 365 – Networking Technologies",
    "CIS 385 – Information Security Fundamentals",
    "CIS 395 – Cloud Computing Essentials",
    "MAT 206 – Precalculus",
    "MAT 301 – Statistics for STEM",
    "ENG 101 – Composition",
]

# job_title capped at 100 chars in DB
JOBS: list[tuple[str, tuple[str, ...]]] = [
    ("Software Developer", ("Python", "Git / Version control", "SQL", "REST APIs", "Agile / Scrum", "Communication")),
    ("Web Developer", ("JavaScript", "HTML/CSS", "REST APIs", "Git / Version control", "UI/UX basics")),
    ("Database Administrator", ("SQL", "Linux / CLI", "Cloud basics (AWS/Azure)", "Technical writing")),
    ("Cybersecurity Analyst", ("Cybersecurity awareness", "Networking fundamentals", "Linux / CLI", "Communication")),
    ("Data Analyst", ("SQL", "Data analysis", "Python", "Technical writing")),
    ("Cloud Support Engineer", ("Cloud basics (AWS/Azure)", "Linux / CLI", "Networking fundamentals", "Docker")),
    ("IT Project Coordinator", ("Agile / Scrum", "Communication", "Technical writing", "REST APIs")),
    ("UI/UX Designer", ("UI/UX basics", "HTML/CSS", "JavaScript", "Communication")),
    ("Machine Learning Engineering Assistant", ("Python", "Machine learning intro", "Data analysis", "SQL")),
    ("Network Technician", ("Networking fundamentals", "Linux / CLI", "Cybersecurity awareness")),
    ("Application Support Analyst", ("SQL", "Communication", "Git / Version control", "REST APIs")),
    ("DevOps Intern", ("Docker", "Linux / CLI", "Git / Version control", "Cloud basics (AWS/Azure)", "Python")),
]

MAJORS: list[dict] = [
    {
        "major": "Computer Science AS",
        "description": "Transfer-oriented CS track emphasizing programming, discrete structures, and systems preparation.",
        "skills": (
            "Python",
            "Java",
            "Git / Version control",
            "Data analysis",
            "HTML/CSS",
            "SQL",
            "Communication",
        ),
        "courses": (
            "CSC 210 – Computer Science I",
            "CSC 220 – Computer Science II",
            "CSC 350 – Data Structures",
            "MAT 206 – Precalculus",
            "MAT 301 – Statistics for STEM",
            "CIS 158 – Database Management Systems",
        ),
        "jobs": ("Software Developer", "Web Developer", "Data Analyst", "Machine Learning Engineering Assistant"),
    },
    {
        "major": "Computer Information Systems AS",
        "description": "Applied IT: databases, systems analysis, networking, and business-facing technology.",
        "skills": (
            "SQL",
            "REST APIs",
            "Agile / Scrum",
            "Communication",
            "Cloud basics (AWS/Azure)",
            "Systems design basics",
        ),
        "courses": (
            "CIS 100 – Introduction to Computer Applications",
            "CIS 158 – Database Management Systems",
            "CIS 255 – Systems Analysis & Design",
            "CIS 395 – Cloud Computing Essentials",
            "CIS 155 – Computer Systems Technology",
        ),
        "jobs": (
            "Application Support Analyst",
            "IT Project Coordinator",
            "Database Administrator",
            "Cloud Support Engineer",
        ),
    },
    {
        "major": "Computer Network Technology AAS",
        "description": "Hands-on networking, security fundamentals, and operations skills.",
        "skills": (
            "Networking fundamentals",
            "Linux / CLI",
            "Cybersecurity awareness",
            "Technical writing",
        ),
        "courses": (
            "CIS 155 – Computer Systems Technology",
            "CIS 365 – Networking Technologies",
            "CIS 385 – Information Security Fundamentals",
            "CSC 210 – Computer Science I",
        ),
        "jobs": ("Network Technician", "Cybersecurity Analyst", "Cloud Support Engineer"),
    },
    {
        "major": "Multimedia Programming & Design AAS",
        "description": "Creative technology blending UI, web, and scripting.",
        "skills": (
            "JavaScript",
            "HTML/CSS",
            "UI/UX basics",
            "Git / Version control",
            "Communication",
        ),
        "courses": (
            "CIS 165 – Web Design & Development",
            "CSC 210 – Computer Science I",
            "CIS 158 – Database Management Systems",
            "ENG 101 – Composition",
        ),
        "jobs": ("Web Developer", "UI/UX Designer", "Software Developer"),
    },
]

# Valid https URLs for URLField
INTERNS: list[dict] = [
    {
        "title": "BMCC Tech Learning Community — project sprint",
        "description": "Cross-functional student team delivering a small civic-tech feature with mentorship.",
        "link": "https://www.bmcc.cuny.edu/academics/departments/mathematics-computer-science/",
        "skills": ("Python", "Git / Version control", "Communication", "Agile / Scrum"),
        "courses": ("CSC 210 – Computer Science I", "CSC 220 – Computer Science II"),
    },
    {
        "title": "City agency — data dashboard internship",
        "description": "Support analysts cleaning city datasets and building Tableau / Python dashboards.",
        "link": "https://www.nyc.gov/health",
        "skills": ("SQL", "Data analysis", "Python", "Technical writing"),
        "courses": ("CIS 158 – Database Management Systems", "MAT 301 – Statistics for STEM"),
    },
    {
        "title": "Startup: React frontend internship",
        "description": "Ship UI components with design system; write Storybook docs.",
        "link": "https://developer.mozilla.org/en-US/docs/Learn",
        "skills": ("JavaScript", "HTML/CSS", "Git / Version control", "UI/UX basics", "REST APIs"),
        "courses": ("CIS 165 – Web Design & Development", "CSC 210 – Computer Science I"),
    },
    {
        "title": "Security operations center (SOC) observer",
        "description": "Rotate through alert triage, runbooks, and phishing response drills.",
        "link": "https://www.cisa.gov/",
        "skills": ("Cybersecurity awareness", "Linux / CLI", "Networking fundamentals", "Communication"),
        "courses": ("CIS 385 – Information Security Fundamentals", "CIS 365 – Networking Technologies"),
    },
    {
        "title": "Cloud support desk internship",
        "description": "Assist with IAM tickets and Terraform modules under senior engineers.",
        "link": "https://aws.amazon.com/education/awseducate/",
        "skills": ("Cloud basics (AWS/Azure)", "Linux / CLI", "Docker", "Communication"),
        "courses": ("CIS 395 – Cloud Computing Essentials", "CIS 155 – Computer Systems Technology"),
    },
    {
        "title": "Open-source docs & QA internship",
        "description": "Improve documentation, reproduce issues, and file fixes for a public OSS library.",
        "link": "https://github.com/",
        "skills": ("Git / Version control", "Technical writing", "Python", "Communication"),
        "courses": ("CSC 220 – Computer Science II", "ENG 101 – Composition"),
    },
]

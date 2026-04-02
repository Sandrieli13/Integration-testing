"""
BMCC program ethnicity / mix for DataAnalysisPage pie charts.

Sources (Institutional Research fact sheets):
- Fall 2022: major mix + CS/CIS/CNT/GIS ethnicity where published
  https://bmccprodstroac.blob.core.windows.net/uploads/2023/05/Institutional-Research-Fact-Sheet-Fall-2022-01.pdf
- Spring 2023: Computer Science ethnicity (percent × 1,057 headcount)
  https://bmccprodstroac.blob.core.windows.net/uploads/2024/03/Institutional-Research-Fact-Sheet-Spring-2023-01a.pdf

CIS, CNT, and GIS pies remain Fall 2022: those programs were not in the Spring 2023 top-10 table with ethnicity columns.
"""

# Fall 2022 — matches prior hard-coded pies (sums match fact-sheet headcounts).
ETHNICITY_CHARTS = [
    {
        "domId": "PiechartContainer",
        "title": "CIS-related majors — enrollment mix (Fall 2022)",
        "subtitle": "BMCC Institutional Research fact sheet",
        "points": [
            {"label": "Computer Science", "y": 1026},
            {"label": "Computer Information Systems", "y": 256},
            {"label": "Geographic Information Science", "y": 10},
            {"label": "Computer Network Technology", "y": 157},
        ],
    },
    {
        "domId": "PiechartContainer1",
        "title": "Computer Information Systems — ethnicity (Fall 2022)",
        "subtitle": "Last published program-level breakdown on fact sheet series",
        "points": [
            {"label": "Asian", "y": 85},
            {"label": "Black", "y": 80},
            {"label": "Hispanic", "y": 74},
            {"label": "White", "y": 17},
            {"label": "Native American", "y": 0},
        ],
    },
    {
        "domId": "PiechartContainer2",
        "title": "Computer Science — ethnicity (Spring 2023)",
        "subtitle": "1,057 majors; % from BMCC Spring 2023 fact sheet (rounded)",
        "points": [
            {"label": "Asian", "y": 330},
            {"label": "Black", "y": 326},
            {"label": "Hispanic", "y": 262},
            {"label": "White", "y": 135},
            {"label": "Two or more / not specified", "y": 4},
        ],
    },
    {
        "domId": "PiechartContainer3",
        "title": "Computer Network Technology — ethnicity (Fall 2022)",
        "subtitle": "Last published program-level breakdown on fact sheet series",
        "points": [
            {"label": "Asian", "y": 34},
            {"label": "Black", "y": 52},
            {"label": "Hispanic", "y": 55},
            {"label": "White", "y": 15},
            {"label": "Native American", "y": 1},
        ],
    },
    {
        "domId": "PiechartContainer4",
        "title": "Geographic Information Science — ethnicity (Fall 2022)",
        "subtitle": "Last published program-level breakdown on fact sheet series",
        "points": [
            {"label": "Asian", "y": 2},
            {"label": "Black", "y": 1},
            {"label": "Hispanic", "y": 4},
            {"label": "White", "y": 3},
            {"label": "Native American", "y": 0},
        ],
    },
]

"""
Charts for DataAnalysisPage: enrollment mix, ethnicity breakdowns, and completion snapshot.

Sources (Institutional Research fact sheets):
- Fall 2022: major mix + CIS/CNT/GIS ethnicity where published
  https://bmccprodstroac.blob.core.windows.net/uploads/2023/05/Institutional-Research-Fact-Sheet-Fall-2022-01.pdf
- Spring 2023: Computer Science ethnicity (percent × 1,057 headcount)
  https://bmccprodstroac.blob.core.windows.net/uploads/2024/03/Institutional-Research-Fact-Sheet-Spring-2023-01a.pdf

CIS, CNT, and GIS pies use Fall 2022 (last program-level breakdown in that series for those programs).

Completion mix uses the latest overlapping year in the project’s graduation CSVs (2022).
"""

DATA_ANALYSIS_PIE_SPECS = [
    {
        "slug": "major-mix-fall-2022",
        "title": "Share of enrollment — computing majors (Fall 2022)",
        "subtitle": "BMCC OIRA fact sheet · CS, CIS, CNT, GIS (Data Science A.S. not yet reported in this vintage)",
        "labels": [
            "Computer Science",
            "Computer Information Systems",
            "Computer Network Technology",
            "Geographic Information Science",
        ],
        "values": [1026, 256, 157, 10],
    },
    {
        "slug": "ethnicity-cis-fall-2022",
        "title": "CIS (A.A.S.) — students by race/ethnicity (Fall 2022)",
        "subtitle": "Headcount by category · BMCC fact sheet",
        "labels": [
            "Asian",
            "Black",
            "Hispanic",
            "White",
            "Native American",
        ],
        "values": [85, 80, 74, 17, 0],
    },
    {
        "slug": "ethnicity-cs-spring-2023",
        "title": "Computer Science — students by race/ethnicity (Spring 2023)",
        "subtitle": "1,057 majors · BMCC Spring 2023 fact sheet (rounded)",
        "labels": [
            "Asian",
            "Black",
            "Hispanic",
            "White",
            "Two or more / not specified",
        ],
        "values": [330, 326, 262, 135, 4],
    },
    {
        "slug": "ethnicity-cnt-fall-2022",
        "title": "Computer Network Technology — students by race/ethnicity (Fall 2022)",
        "subtitle": "BMCC fact sheet",
        "labels": [
            "Asian",
            "Black",
            "Hispanic",
            "White",
            "Native American",
        ],
        "values": [34, 52, 55, 15, 1],
    },
    {
        "slug": "ethnicity-gis-fall-2022",
        "title": "Geographic Information Science — students by race/ethnicity (Fall 2022)",
        "subtitle": "Small program (N=10 total enrollment) · interpret slices cautiously",
        "labels": [
            "Asian",
            "Black",
            "Hispanic",
            "White",
            "Native American",
        ],
        "values": [2, 1, 4, 3, 0],
    },
    {
        "slug": "degrees-mix-2022",
        "title": "Degrees awarded — CS, CIS, and CNT (2022)",
        "subtitle": "Completions in project graduation CSVs · Data Science A.S. not yet in extract",
        "labels": [
            "Computer Science",
            "CIS (A.A.S.)",
            "Computer Network Technology",
        ],
        "values": [142, 58, 59],
    },
]

# Legacy flat shape (e.g. old CanvasJS experiments); prefer DATA_ANALYSIS_PIE_SPECS.
ETHNICITY_CHARTS = [
    {
        "domId": "legacy-pie-" + spec["slug"],
        "title": spec["title"],
        "subtitle": spec["subtitle"],
        "points": [
            {"label": lab, "y": val}
            for lab, val in zip(spec["labels"], spec["values"])
        ],
    }
    for spec in DATA_ANALYSIS_PIE_SPECS
]

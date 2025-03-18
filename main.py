from fastapi import FastAPI, UploadFile, File
import pandas as pd
from collections import defaultdict
import io

app = FastAPI()

@app.post("/upload/")
async def upload_excel(file: UploadFile = File(...)):
    # Read Excel file
    contents = await file.read()
    df = pd.read_excel(io.BytesIO(contents))

    # Dictionary to store total scores for each project
    project_scores = defaultdict(int)

    # Process each row and assign points
    for _, row in df.iterrows():
        project_scores[row["First Preference"]] += 3  # 1st preference → 3 points
        project_scores[row["Second Preference"]] += 2  # 2nd preference → 2 points
        project_scores[row["Third Preference"]] += 1  # 3rd preference → 1 point

    # Sorting projects by total score (Descending order)
    sorted_projects = sorted(project_scores.items(), key=lambda x: x[1], reverse=True)

    # Return all projects sorted by votes
    return {
        "All Projects Sorted by Votes": [
            {"Rank": i+1, "Project": p, "Points": s} for i, (p, s) in enumerate(sorted_projects)
        ]
    }

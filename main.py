from fastapi import FastAPI, UploadFile, File
import pandas as pd
from collections import defaultdict
import io

app = FastAPI()

@app.post("/upload/")
async def upload_excel(file: UploadFile = File(...)):
    try:
        # Read Excel file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Debugging: Print column names
        print("Excel Columns:", df.columns.tolist())

        # Strip extra spaces in column names
        df.columns = df.columns.str.strip()

        # Check for required columns
        required_columns = {"First Preference", "Second Preference", "Third Preference"}
        if not required_columns.issubset(set(df.columns)):
            return {"error": "Missing required columns", "found": df.columns.tolist()}

        # Handle missing values
        df = df.fillna("")

        # Dictionary to store total scores for each project
        project_scores = defaultdict(int)

        # Process each row and assign points
        for _, row in df.iterrows():
            if row["First Preference"]:
                project_scores[row["First Preference"]] += 3
            if row["Second Preference"]:
                project_scores[row["Second Preference"]] += 2
            if row["Third Preference"]:
                project_scores[row["Third Preference"]] += 1

        # Sorting projects by total score (Descending order)
        sorted_projects = sorted(project_scores.items(), key=lambda x: x[1], reverse=True)

        # Return all projects sorted by votes
        return {
            "All Projects Sorted by Votes": [
                {"Rank": i+1, "Project": p, "Points": s} for i, (p, s) in enumerate(sorted_projects)
            ]
        }
    except Exception as e:
        print("Error:", e)  # Debugging
        return {"error": str(e)}

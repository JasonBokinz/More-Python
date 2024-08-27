"""Calculate student grades by combining data from many sources.

Using Pandas, this script combines data from the:

* Roster
* Homework & Exam grades
* Quiz grades

to calculate final grades for a class.
"""
# Importing Libraries and Setting Paths
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import glob
import re

HERE = Path(__file__).parent
DATA_FOLDER = HERE / "data"

# Data Importation and Cleaning
roster = pd.read_csv(DATA_FOLDER / "roster.csv", index_col="NetID")
roster.index = roster.index.str.lower()
roster['Email Address'] = roster['Email Address'].str.lower()
roster = roster.loc[:, ~roster.columns.str.contains('Name')]

hw_exam_grades = pd.read_csv(DATA_FOLDER /  "hw_exam_grades.csv", index_col="SID")
hw_exam_grades.index = hw_exam_grades.index.str.lower()
hw_exam_grades = hw_exam_grades.loc[:, ~hw_exam_grades.columns.str.contains('Submission')]

quiz_grades = pd.DataFrame()
quiz_grades_files = glob.glob(str(DATA_FOLDER / "quiz_*_grades.csv"))

for file in quiz_grades_files:
    quiz_data = pd.read_csv(DATA_FOLDER / file)
    file_name = file.split("/")[-1]
    quiz_name = "Quiz " + file_name.split("_")[1]
    quiz_data.rename(columns={"Grade": quiz_name}, inplace=True)
    quiz_data['Email'] = quiz_data['Email'].astype(str)
    
    quiz_grades = pd.concat([quiz_grades, quiz_data.set_index("Email")], axis=1, sort=False)
    quiz_grades = quiz_grades.loc[:, ~quiz_grades.columns.str.contains('First Name')]
    quiz_grades = quiz_grades.loc[:, ~quiz_grades.columns.str.contains('Last Name')]


# Data Merging
merged = pd.merge(roster, hw_exam_grades, left_index=True, right_index=True, how="outer")
final_data = pd.merge(merged, quiz_grades, left_on="Email Address", right_index=True, how="outer")
final_data = final_data.fillna(0)

# Data Processing and Score Calculation
# Exams
n_exams = 3
for i in range(1, n_exams + 1):
    col_name = f"Exam {i}"
    max_points_col = f"Exam {i} - Max Points"
    final_data[col_name + " Score"] = final_data[col_name] / final_data[max_points_col]

# Calculating Total Homework score
homework_scores = [col for col in final_data.columns if re.match(r'^Homework \d+$', col)]
homework_max_points = [col for col in final_data.columns if re.match(r'^Homework \d+ - Max Points$', col)]

sum_of_hw_scores = final_data[homework_scores].sum(axis=1)
sum_of_hw_max = final_data[homework_max_points].sum(axis=1)
final_data["Total Homework"] = sum_of_hw_scores / sum_of_hw_max

# Assign the average homework score to a new column in the DataFrame
homework_scores_values = final_data[homework_scores].values
homework_max_points_values = final_data[homework_max_points].values

homework_ratios = np.divide(homework_scores_values, homework_max_points_values, out=np.zeros_like(homework_scores_values), where=(homework_max_points_values != 0))
sum_of_ratios = homework_ratios.sum(axis=1)
average_homework_score = sum_of_ratios / len(homework_scores)
final_data["Average Homework"] = average_homework_score
final_data["Homework Score"] = final_data[["Total Homework", "Average Homework"]].max(axis=1)

# Calculating Total and Average Quiz Scores:
# Filter the data for Quiz scores
quiz_scores = final_data.filter(like="Quiz")

quiz_max_points = pd.Series(
    {"Quiz 1": 11, "Quiz 2": 15, "Quiz 3": 17, "Quiz 4": 14, "Quiz 5": 12}
)
# Final Quiz Score Calculation:
sum_of_quiz_scores = quiz_scores.sum(axis=1)
sum_of_quiz_max = quiz_max_points.sum()
final_data["Total Quizzes"] = sum_of_quiz_scores / sum_of_quiz_max

average_quiz_scores = quiz_scores / quiz_max_points
final_data["Average Quizzes"] = average_quiz_scores.sum(axis=1) / len(quiz_max_points)
final_data["Quiz Score"] = final_data[["Total Quizzes", "Average Quizzes"]].max(axis=1)

# Calculating the Final Score
weightings = pd.Series({
    "Exam 1 Score": 0.05,
    "Exam 2 Score": 0.1,
    "Exam 3 Score": 0.15,
    "Quiz Score": 0.30,
    "Homework Score": 0.4,
})
exam_score_columns = [f"Exam {i} Score" for i in range(1, 4)]
final_data["Final Score"] = (
    final_data[exam_score_columns[0]] * weightings["Exam 1 Score"] +
    final_data[exam_score_columns[1]] * weightings["Exam 2 Score"] +
    final_data[exam_score_columns[2]] * weightings["Exam 3 Score"] +
    final_data["Quiz Score"] * weightings["Quiz Score"] +
    final_data["Homework Score"] * weightings["Homework Score"]
)

# Rounding Up the Final Score:
final_data["Ceiling Score"] = np.ceil(final_data["Final Score"] * 100)

# Defining Grade Mapping:
grades = {90: 'A', 80: 'B', 70: 'C', 60: 'D', 0: 'F'}

# Applying Grade Mapping to Data
def grade_mapping(value):
    for threshold, grade in grades.items():
        if value >= threshold:
            return grade

letter_grades = final_data["Ceiling Score"].apply(grade_mapping)
final_data["Final Grade"] = pd.Categorical(final_data["Ceiling Score"].apply(grade_mapping), categories=grades.values())

# Processing Data by Sections:
for section, table in final_data.groupby("Section"):
    section_file_path = f"{DATA_FOLDER}/section_{section}_data.csv"
    table.sort_values(by=["Last Name", "First Name"]).to_csv(section_file_path, index=False)
    print(f"In Section {section} there are {len(table)} students saved to file\n{section_file_path}")

# Visualizing Grade Distribution: Get Grade Counts
grade_counts = final_data["Final Grade"].value_counts().sort_index()
grade_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Distribution of Final Grades')
plt.xlabel('Final Grade')
plt.ylabel('Count')
plt.show()

final_data["Final Score"].plot.hist(bins=20, label="Histogram")
final_data["Final Score"].plot.density(linewidth=4, label="Kernel Density Estimate")

# Plotting Normal Distribution:
final_mean = final_data["Final Score"].mean()
final_std = final_data["Final Score"].std()

# Plot the normal distribution of final_mean and final_std
x = np.linspace(final_mean - 5 * final_std, final_mean + 5 * final_std, 1000)
y = scipy.stats.norm.pdf(x, final_mean, final_std)

# Set the linewidth for the normal distribution line
plt.plot(x, y, label="Normal Distribution", color="lightgreen", linewidth=4)

plt.title("Normal Distribution of Final Score")
plt.xlabel("Final Score")
plt.ylabel("Density")
plt.legend()
plt.show()
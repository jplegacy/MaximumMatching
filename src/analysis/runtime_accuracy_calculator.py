import pandas as pd


df = pd.read_csv("src/analysis/data/filtered_d2/course2.csv")

# Group by solver and sum the elapsed time
total_times = df.groupby('Solver')['Elapsed Time (s)'].sum().reset_index()

# Display the result
print(total_times)


# Standardize the 'Success' values
df['Success'] = df['Success'].str.strip().str.upper()

# Group by solver and calculate total and successful tests
accuracy_df = df.groupby('Solver').agg(
    Total_Tests=('Test Number', 'count'),
    Successful_Tests=('Success', lambda x: (x == "TRUE").sum()),
).reset_index()

# Calculate accuracy percentage for each solver
accuracy_df['Accuracy_Percentage'] = (accuracy_df['Successful_Tests'] / (accuracy_df['Total_Tests'])) * 100

# Display the results
print(accuracy_df[['Solver', 'Total_Tests', 'Successful_Tests', 'Accuracy_Percentage']])
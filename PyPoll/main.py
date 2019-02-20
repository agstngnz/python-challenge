# Import os module
import os

# Module for reading CSV files
import csv

#PyBank/Resources/budget_data.csv
csvpath = os.path.join('PyPoll', 'Resources', 'election_data.csv')

# Set variables
Total_Votes = 0.0
Candidate_List = []
Count_List = []
Pct_List = []
Winner = -1
Winner_Vote_Cnt = 0

# Open the CSV
with open(csvpath, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    # Read the header row first
    csv_header = next(csvreader)
    
    # Loop through remaining csv file
    for row in csvreader:

        # Counting Votes
        Total_Votes = Total_Votes + 1

        # Create Candidate List and initialize Count_List and Pct_List
        if len(row) > 0:
            Name = row[2]
            if Name in Candidate_List:
                Candidate_List = Candidate_List
            else:
                Candidate_List.append(Name)
                Count_List.append(0.0)
                Pct_List.append(0.0)

        # Count Candidate Votes
        if len(row) > 0:
            Count_List[Candidate_List.index(Name)] = Count_List[Candidate_List.index(Name)] + 1

# Calculate Candidate vote percentages
for x in Candidate_List:
    Pct_List[Candidate_List.index(x)] = round((Count_List[Candidate_List.index(x)]/Total_Votes)*100,3)
 
# Determine Winner
for x in Count_List:
    if Winner_Vote_Cnt < Count_List[Count_List.index(x)]:
        Winner_Vote_Cnt = Count_List[Count_List.index(x)]
        Winner = Count_List.index(x) 
    
print("```text")
print("Election Results")
print("-------------------------")
print(f"Total Votes: {str(round(Total_Votes))}")
print("-------------------------")
# print(Candidate_List)
# print(Count_List)
# print(Pct_List)
# print(Winner_Vote_Cnt)
# print(Winner)
for x in range(len(Candidate_List)):
    print(f"{Candidate_List[x]}: {round(Pct_List[x],3):.3f}% ({round(Count_List[x])})")
print("-------------------------")
print(f"Winner: {Candidate_List[Winner]}")
print("-------------------------")
print("```")   

# Write results to file
# File to write to
output_path = os.path.join('PyPoll', 'output.txt')

# Opening file using "write" mode.
txtfile = open(output_path, 'w')

# Write header
txtfile.write("```text\n")
txtfile.write("Election Results\n")
txtfile.write("-------------------------\n")

# Write results
txtfile.write(f"Total Votes: {str(round(Total_Votes))}\n")
txtfile.write("-------------------------\n")
for x in range(len(Candidate_List)):
    txtfile.write(f"{Candidate_List[x]}: {round(Pct_List[x],3):.3f}% ({round(Count_List[x])})\n")
txtfile.write(f"Winner: {Candidate_List[Winner]}\n")
txtfile.write("-------------------------\n")

# Write footer
txtfile.write("```\n")

# Close file
txtfile.close()

# Import os module
import os

# Module for reading CSV files
import csv

#PyBank/Resources/budget_data.csv
csvpath = os.path.join('PyBank', 'Resources', 'budget_data.csv')

# Set variables
Total_Months = 0
Total = 0.0
Prior_Amt = 0.0
Row_Change = 0.0
Total_Change = 0.0
Greatest_Increase = ['',-1.0]
Greatest_Decrease = ['',1.0]

# Open the CSV
with open(csvpath, newline="") as csvfile:
    csvreader = csv.reader(csvfile, delimiter=",")

    # Read the header row first
    csv_header = next(csvreader)
    
    # Read first data row
    csv_header = next(csvreader)
    Total_Months = 1
    Total = float(csv_header[1])
    Prior_Amt = float(csv_header[1])
    
    # Loop through remaining csv file
    for row in csvreader:

        # Counting Months
        Total_Months = Total_Months + 1

        # Adding Profit and Losses
        Total = Total + float(row[1])
        
        # Calculate Change
        Row_Change = float(row[1]) - Prior_Amt
        
        # Cumulative Change Sum
        Total_Change = Total_Change + Row_Change
        
        # Define prior row amount
        Prior_Amt = float(row[1])
        
        # Derive Greatest Increase
        if Row_Change > 0 and Row_Change > Greatest_Increase[1]:
            Greatest_Increase = [row[0],Row_Change]
        
        # Derive Greatest Decrease
        if Row_Change < 0 and Row_Change < Greatest_Decrease[1]:
            Greatest_Decrease = [row[0],Row_Change]

# Printing results to Terminal
print("```text")
print("Financial Analysis")
print("----------------------------")
print(f"Total Months: {str(Total_Months)}")
print(f"Total: ${str(round(Total))}")
#print(f"Total_Change: ${str(Total_Change)}")
print(f"Average Change: ${str(round(Total_Change/(Total_Months-1),2))}")
print(f"Greatest Increase in Profits: {str(Greatest_Increase[0])} (${str(round(Greatest_Increase[1]))})")
print(f"Greatest Decrease in Profits: {str(Greatest_Decrease[0])} (${str(round(Greatest_Decrease[1]))})")
print("```")   

# Write results to text file using csv.writer
# File to write to
output_path = os.path.join('PyBank', 'output.txt')

# Opening file using "write" mode. Specify variable to hold contents
with open(output_path, 'w', newline='') as csvfile:

    # Initialize csv.writer
    csvwriter = csv.writer(csvfile, delimiter=',')

    # Write header
    csvwriter.writerow(["```text"])
    csvwriter.writerow(["Financial Analysis"])
    csvwriter.writerow(["----------------------------"])

    # Write results
    csvwriter.writerow([f"Total Months: {str(Total_Months)}"])
    csvwriter.writerow([f"Total: ${str(round(Total))}"])
    csvwriter.writerow([f"Average Change: ${str(round(Total_Change/(Total_Months-1),2))}"])
    csvwriter.writerow([f"Greatest Increase in Profits: {str(Greatest_Increase[0])} (${str(round(Greatest_Increase[1]))})"])
    csvwriter.writerow([f"Greatest Decrease in Profits: {str(Greatest_Decrease[0])} (${str(round(Greatest_Decrease[1]))})"])

    # Write footer
    csvwriter.writerow(["```"])

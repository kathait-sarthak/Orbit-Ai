import matplotlib.pyplot as plt

# Sample data for SDGs (using a subset for readability on the chart)
sdg_goals = [
    "No Poverty", "Zero Hunger", "Good Health", 
    "Quality Education", "Gender Equality", "Clean Water", 
    "Affordable Energy"
]
# Arbitrary values representing hypothetical progress or focus for demonstration
sdg_values = [75, 60, 85, 70, 65, 90, 80]

# Create the bar chart
plt.figure(figsize=(12, 7)) # Increased figure size for better readability
plt.bar(sdg_goals, sdg_values, color='skyblue')

# Add labels and title
plt.xlabel("Sustainable Development Goals")
plt.ylabel("Progress Indicator (Arbitrary Units)")
plt.title("Sample Progress on Sustainable Development Goals")

# Rotate x-axis labels for better visibility
plt.xticks(rotation=45, ha='right') # 'ha' aligns text to the right of the tick

# Adjust layout to prevent labels from overlapping
plt.tight_layout()

# Save the chart
plt.savefig("data_viz\chart.png")

print("Bar chart saved as data_viz\chart.png")

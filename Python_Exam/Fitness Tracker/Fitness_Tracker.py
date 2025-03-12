import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class FitnessTracker:
    def __init__(self):
        self.activities = []

    def log_activity(self, activity_type, duration, calories, date=None):
        """Log a new fitness activity."""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        activity = {"date": date, "activity_type": activity_type, "duration": duration, "calories": calories}
        self.activities.append(activity)
        print(f"Logged: {activity_type} for {duration} minutes on {date}")

    def calculate_metrics(self):
        """Calculate basic metrics."""
        if not self.activities:
            return {"total_calories": 0, "avg_duration": 0, "activity_count": 0}
        df = pd.DataFrame(self.activities)
        return {
            "total_calories": sum(df["calories"]),
            "avg_duration": df["duration"].mean(),
            "activity_count": len(df)
        }

    def filter_activities(self, activity_type=None, start_date=None, end_date=None):
        """Filter activities by type or date."""
        df = pd.DataFrame(self.activities)
        if activity_type:
            df = df[df["activity_type"] == activity_type]
        if start_date:
            df = df[df["date"] >= start_date]
        if end_date:
            df = df[df["date"] <= end_date]
        return df

    def generate_report(self):
        """Generate a simple report."""
        metrics = self.calculate_metrics()
        df = pd.DataFrame(self.activities)
        print("\n=== Fitness Report ===")
        print(f"Total Activities: {metrics['activity_count']}")
        print(f"Total Calories: {metrics['total_calories']:.0f}")
        print(f"Average Duration: {metrics['avg_duration']:.0f} minutes")
        if not df.empty:
            print("\nActivities by Type:", df["activity_type"].value_counts())

    def save_to_csv(self, filename="fitness_activities.csv"):
        """Save activities to a CSV file."""
        df = pd.DataFrame(self.activities)
        if not df.empty:
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

    def load_from_csv(self, filename="fitness_activities.csv"):
        """Load activities from a CSV file."""
        try:
            df = pd.read_csv(filename)
            df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
            df["duration"] = pd.to_numeric(df["duration"])
            df["calories"] = pd.to_numeric(df["calories"])
            self.activities = df.to_dict("records")
            print(f"Loaded {len(self.activities)} activities from {filename}")
            return True
        except:
            print(f"Could not load {filename}. Starting empty.")
            self.activities = []
            return False

    def visualize_fitness_progress(self):
        """Display visualization options."""
        df = pd.DataFrame(self.activities)
        if df.empty:
            print("No data to visualize.")
            return

        while True:
            print("\nSelect a visualization:")
            print("1. Bar Chart: Time spent on each activity type")
            print("2. Line Graph: Calories burned over time")
            print("3. Pie Chart: Percentage distribution of activities")
            print("4. Heatmap: Correlation between duration and calories")
            print("5. Back to Menu")
            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                plt.figure(figsize=(8, 5))
                sns.barplot(x="duration", y="activity_type", hue="activity_type", data=df)
                plt.title("Time Spent on Activities")
                plt.show()
            elif choice == "2":
                df['date'] = pd.to_datetime(df['date'])
                plt.figure(figsize=(8, 5))
                plt.plot(df['date'], df['calories'], marker='o')
                plt.title("Calories Over Time")
                plt.xlabel("Date")
                plt.ylabel("Calories")
                plt.xticks(rotation=45)
                plt.show()
            elif choice == "3":
                activity_counts = df['activity_type'].value_counts()
                plt.figure(figsize=(6, 6))
                plt.pie(activity_counts, labels=activity_counts.index, autopct="%1.0f%%")
                plt.title("Activity Distribution")
                plt.show()
            elif choice == "4":
                plt.figure(figsize=(6, 5))
                sns.heatmap(df[["duration", "calories"]].corr(), annot=True, cmap="coolwarm")
                plt.title("Duration vs Calories Correlation")
                plt.show()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Try again.")

def main():
    tracker = FitnessTracker()
    tracker.load_from_csv()

    while True:
        print("\n=== Fitness Tracker ===")
        print("1. Log Activity")
        print("2. Generate Report")
        print("3. Filter Activities")
        print("4. Load Data")
        print("5. Visualize Data")
        print("6. Save and Exit")
        choice = input("Choose (1-6): ").strip()

        match choice:
            case "1":
                activity_type = input("Activity type: ")
                duration = float(input("Duration (minutes): "))
                calories = float(input("Calories: "))
                date = input("Date (YYYY-MM-DD) or press Enter: ") or None
                tracker.log_activity(activity_type, duration, calories, date)

            case "2":
                tracker.generate_report()

            case "3":
                activity_type = input("Filter by type (or press Enter): ") or None
                start_date = input("Start date (YYYY-MM-DD): ") or None
                end_date = input("End date (YYYY-MM-DD): ") or None
                filtered = tracker.filter_activities(activity_type, start_date, end_date)
                if filtered.empty:
                    print("No matching activities.")
                else:
                    print(filtered)

            case "4":
                filename = input("Enter filename: ") or "fitness_activities.csv"
                if tracker.load_from_csv(filename):
                    if input("Show data? (yes/no): ").lower() == "yes":
                        print(pd.DataFrame(tracker.activities))

            case "5":
                tracker.visualize_fitness_progress()

            case "6":
                tracker.save_to_csv()
                print("Exiting...")
                break

            case _:
                print("Invalid choice.")

if __name__ == "__main__":
    main()
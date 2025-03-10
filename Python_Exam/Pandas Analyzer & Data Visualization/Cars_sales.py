import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class CarsSalesAnalyzer:
    def __init__(self, f_path=None):
        self.df = pd.DataFrame()
        if f_path:
            self.load_data(f_path)

    def load_data(self, f_path):
        try:
            self.df = pd.read_csv(f_path)
            print("Data Loaded Successfully!")
        except FileNotFoundError:
            print("File not found. Please enter a valid file path.")

    def explore_data(self):
        while True:
            print("\n== Explore Data ==")
            print("1. Display the first 5 rows")
            print("2. Display the last 5 rows")
            print("3. Display column names")
            print("4. Display data types")
            print("5. Display basic info")
            print("6. Go back to main menu")
            choice = input("Enter your choice: ")

            match choice:
                case '1':
                    print(self.df.head())
                case '2':
                    print(self.df.tail())
                case '3':
                    print(self.df.columns)
                case '4':
                    print(self.df.dtypes)
                case '5':
                    print(self.df.info())
                case '6':
                    break
                case _:
                    print("Invalid choice. Please try again.")

    def handle_missing_data(self):
        while True:
            print("\n== Handle Missing Data ==")
            print("1. Display rows with missing values")
            print("2. Fill missing values with mean")
            print("3. Drop rows with missing values")
            print("4. Replace missing values with a specific value")
            print("5. Go back to main menu")
            choice = input("Enter your choice: ")

            match choice:
                case '1':
                    missing = self.df[self.df.isnull().any(axis=1)]
                    if missing.empty:
                        print("No missing values found!")
                    else:
                        print(missing)
                case '2':
                    self.df.fillna(self.df.mean(numeric_only=True), inplace=True)
                    print("Missing values filled with mean.")
                case '3':
                    self.df.dropna(inplace=True)
                    print("Rows with missing values dropped.")
                case '4':
                    val = input("Enter value to replace missing values: ")
                    self.df.fillna(val, inplace=True)
                    print(f"Missing values replaced with {val}.")
                case '5':
                    break
                case _:
                    print("Invalid choice. Please try again.")

    def generate_descriptive(self):
        if not self.df.empty:
            print(self.df.describe())
        else:
            print("No data found!")

    def visualize_data(self):
        while True:
            if self.df is not None and not self.df.empty:
                print("\n== Data Visualization ==")
                print("1. Bar Plot")
                print("2. Line Plot")
                print("3. Scatter Plot")
                print("4. Pie Chart")
                print("5. Box Plot")
                print("6. Histogram")
                print("7. Violin Plot")
                print("8. Back to Main Menu")
                choice = input("Enter your choice: ")

                match choice:
                    case "8":
                        return  # Exit the loop

                    case _:
                        col_name = input("Enter column name: ").strip()
                        if col_name not in self.df.columns:
                            print("Invalid column name. Please try again.")
                            continue

                        plt.figure(figsize=(10, 6))

                        # Set up color palette for consistency
                        custom_palette = sns.color_palette("Set2", n_colors=10)

                        match choice:
                            case "1":
                                sns.barplot(x=self.df[col_name].value_counts().index, y=self.df[col_name].value_counts().values, palette=custom_palette)
                                plt.xlabel(col_name)
                                plt.ylabel("Count")
                                plt.title(f"Bar Plot of {col_name}")
                                plt.legend([col_name])

                            case "2":
                                sns.lineplot(data=self.df, x=self.df.index, y=col_name, hue=col_name, palette=custom_palette)
                                plt.xlabel("Index")
                                plt.ylabel(col_name)
                                plt.title(f"Line Plot of {col_name}")

                            case "3":
                                x_col = input("Enter x-axis column name: ").strip()
                                if x_col not in self.df.columns:
                                    print("Invalid x-axis column name.")
                                    continue
                                sns.scatterplot(data=self.df, x=x_col, y=col_name, hue=col_name, palette=custom_palette)
                                plt.xlabel(x_col)
                                plt.ylabel(col_name)
                                plt.title("Scatter Plot")

                            case "4":
                                self.df[col_name].value_counts().plot(kind='pie', autopct='%1.1f%%', startangle=90, colors=custom_palette)
                                plt.title(f"Pie Chart of {col_name}")

                            case "5":
                                sns.boxplot(y=self.df[col_name], palette=custom_palette)
                                plt.ylabel(col_name)
                                plt.title(f"Box Plot of {col_name}")

                            case "6":
                                sns.histplot(self.df[col_name], kde=True, color='skyblue', bins=20)
                                plt.xlabel(col_name)
                                plt.ylabel("Frequency")
                                plt.title(f"Histogram of {col_name}")

                            case "7":
                                sns.violinplot(y=self.df[col_name], palette=custom_palette)
                                plt.ylabel(col_name)
                                plt.title(f"Violin Plot of {col_name}")

                            case _:
                                print("Invalid choice. Please try again.")

                        plt.legend()
                        plt.show()
            else:
                print("No dataset loaded yet!")
                break

    def save_visualization(self):
        if self.df.empty:
            print("No dataset loaded.")
            return

        col = input("Enter column name to save visualization: ").strip()
        if col not in self.df.columns:
            print("Invalid column name.")
            return

        plt.figure(figsize=(10, 6))

        # Custom color for bar plot
        custom_palette = sns.color_palette("Set2", n_colors=10)

        self.df[col].value_counts().plot(kind='bar', color=custom_palette[:len(self.df[col].value_counts())])
        plt.title(f"{col} Visualization")

        f_name = input("Enter file name to save (without extension): ").strip()
        plt.savefig(f"{f_name}.png")
        print(f"Visualization saved as {f_name}.png")

    def dataframe_operations(self):
        while True:
            print("\n== DataFrame Operations ==")
            print("1. Sort Data by a column")
            print("2. Rename Columns")
            print("3. Filter Data by condition")
            print("4. Go back to main menu")
            choice = input("Enter your choice: ")

            match choice:
                case '1':
                    col = input("Enter column name to sort by: ").strip()
                    if col not in self.df.columns:
                        print("Invalid column name.")
                        continue
                    ascending = input("Sort in ascending order? (y/n): ").strip().lower()
                    self.df = self.df.sort_values(by=col, ascending=True if ascending == 'y' else False)
                    print(f"Data sorted by {col}.")
                
                case '2':
                    old_col = input("Enter the column name to rename: ").strip()
                    if old_col not in self.df.columns:
                        print("Invalid column name.")
                        continue
                    new_col = input("Enter the new column name: ").strip()
                    self.df.rename(columns={old_col: new_col}, inplace=True)
                    print(f"Column '{old_col}' renamed to '{new_col}'.")

                case '3':
                    condition_col = input("Enter column to filter by: ").strip()
                    if condition_col not in self.df.columns:
                        print("Invalid column name.")
                        continue
                    condition_val = input(f"Enter the value to filter {condition_col} by: ").strip()
                    filtered_df = self.df[self.df[condition_col] == condition_val]
                    print(f"Filtered DataFrame based on {condition_col} = {condition_val}:")
                    print(filtered_df)

                case '4':
                    break
                case _:
                    print("Invalid choice. Please try again.")


if __name__ == "__main__":
    analyzer = CarsSalesAnalyzer()
    while True:
        print("\n========== Data Analysis & Visualization Program ==========")
        print("Please select an option:")
        print("1. Load Dataset")
        print("2. Explore Data")
        print("3. Perform DataFrame Operations")
        print("4. Handle Missing Data")
        print("5. Generate Descriptive Statistics")
        print("6. Data Visualization")
        print("7. Save Visualization")
        print("8. Exit")
        
        choice = input("Enter your choice: ")

        match choice:
            case '1':
                f_path = input("Enter the path of the dataset (CSV file): ")
                analyzer.load_data(f_path)
            case '2':
                analyzer.explore_data()
            case '3':
                analyzer.dataframe_operations()  # New option to handle DataFrame operations
            case '4':
                analyzer.handle_missing_data()
            case '5':
                analyzer.generate_descriptive()
            case '6':
                analyzer.visualize_data()
            case '7':
                analyzer.save_visualization()
            case '8':
                print("Exiting the program.")
                break
            case _:
                print("Invalid choice. Please try again.")

import pandas as pd

def read_dataset(filename):
  # Reading the CSV file into a pandas DataFrame
  df = pd.read_csv(filename)
  return df

def clean_data(df):
  #Replacing the missing values with "N/A"
  df.fillna("N/A", inplace = True)
  
  #Standardizing gender values to "Male" and "Female"
  df["Gender"] = df["Gender"].replace({"M": "Male", "m": "Male", 
                                       "F": "Female", "f": "Female"})

  return df

def transform_data(df):
  #Converting the "Age" column to numeric, setting errors to Nan
  df["Age"] = pd.to_numeric(df["Age"], errors='coerce') 

  #Calculating the average age for males and females
  male_avg_age = round(df[df['Gender'] == 'Male']['Age'].mean(), 2)
  female_avg_age = round(df[df['Gender'] == 'Female']['Age'].mean(), 2)  

  #Filling missing age values based on gender-specific averages
  df["Age"].fillna(df.groupby("Gender")["Age"].transform("mean"), inplace = True)

  return df

def analyze_data(df):
  #Calculating the overall and gender-specific average ages
  overall_avg_age = round(df['Age'].mean(), 2)
  male_avg_age = round(df[df['Gender'] == 'Male']['Age'].mean(), 2)
  female_avg_age = round(df[df['Gender'] == 'Female']['Age'].mean(), 2)
 
  #Calculating the age ranges for males and females
  male_age_range = (df[df["Gender"] == "Male"]["Age"].max(), df[df["Gender"] == "Male"]["Age"].min())
  female_age_range = (df[df["Gender"] == "Female"]["Age"].max(), df[df["Gender"] == "Female"]["Age"].min())

  #Calculating the distribution of genders
  gender_distribution = df["Gender"].value_counts()

  return {
      "overall_avg_age": overall_avg_age,
      "male_avg_age": male_avg_age,
      "female_avg_age": female_avg_age,
      "male_age_range": male_age_range,        
      "female_age_range": female_age_range,
      "gender_distribution": gender_distribution
    }

def advanced_analysis(df, N):
    #Identifying the top N oldest and youngest individuals
    top_oldest = df.nlargest(N, "Age")
    top_youngest = df.nsmallest(N, "Age")
      
    #Counting the number of individuals within specific age ranges
    age_range_counts = df["Age"].value_counts(bins=10).sort_index()
      
    #Grouping data by occupation
    occupation_groups = df.groupby("Occupation")
      
    return {
        "top_oldest": top_oldest,
        "top_youngest": top_youngest,
        "age_range_counts": age_range_counts,
        "occupation_groups": occupation_groups
    }

#Function to save the cleaned dataset to a new CSV file
def save_dataset(df, filename):
    df.to_csv(filename, index = False)

#Function to load a dataset from a CSV file
def load_dataset(filename):
    return pd.read_csv(filename)

#Class for processing the data
class DataProcessor:
  #Initializing with the datset
  def __init__(self, filename):
    self.df = read_dataset(filename)

  #Cleaning the dataset
  def clean_data(self):
    self.df = clean_data(self.df)

  #Transforming the dataset
  def transform_data(self):
    self.df = transform_data(self.df)

  #Saving the cleaned dataset to a file
  def save_dataset(self, filename):
    save_dataset(self.df, filename)

#Class for analyzing the data, extending DataProcessor
class DataAnalyzer(DataProcessor):

  def analyze_data(self):
    #Performing basic analysis on the dataset
    return analyze_data(self.df)

  def advanced_analysis(self, N = 5):
    #Performing advanced analysis on the dataset
    return advanced_analysis(self.df, N)

def print_report(analysis):
   print(f"Overall Average Age: {analysis['overall_avg_age']}")
   print(f"Male Average Age: {analysis['male_avg_age']}")
   print(f"Female Average Age: {analysis['female_avg_age']}")
   print(f"Male Age Range: {analysis['male_age_range']}")
   print(f"Female Age Range: {analysis['female_age_range']}")
   print(f"Gender Distribution:\n{analysis['gender_distribution']}")

#Main script execution
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:   
      #Checking if the correct number of arguments are provided
      print("Usage: python script.py <filename>")
      sys.exit(1)

    filename = sys.argv[1]
    analyzer = DataAnalyzer(filename)

    #Cleaning and transforming the dataset
    analyzer.clean_data()
    analyzer.transform_data()

    #Performing analysis and printing the report
    analysis = analyzer.analyze_data()
    advanced_analysis = analyzer.advanced_analysis()

    print_report(analysis)

    #Saving the cleaned and transformed dataset
    output_filename = "cleaned_" + filename
    output_filename = filename.replace(".csv","") + "_cleaned.csv"
    analyzer.save_dataset(output_filename)

    print(f"Cleaned dataset saved to {output_filename}")    

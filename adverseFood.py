import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import os

st.title("Exploratory Data Analysis : Adverse Food")
st.header("Dataset Background")
st.write("""
CAERS is a post-market surveillance system that collects reports about adverse events involving CFSAN-regulated products. 
Their database receives both mandatory reports for dietary supplements as well as voluntary reports from both consumers 
and health care practitioners through MedWatch, emails, telephone calls, faxes, letters, and electronic transfers from the 
Office of Regulatory Affairs (ORA) District Offices’ Field Accomplishments and Compliance Tracking System (FACTS).
""")
####################
st.write("The following are the libraries which I will be going to use throughout this project.")
code = """
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
"""
st.code(code, language="python")

####################
#get the dataset
st.header("Get the Dataset")
st.write("To get the dataset, I import and load **Adverse Food** dataset from my local device and create a Pandas dataframe.")
path = os.path.join("Dataset", "CAERS_ASCII_2004_2017Q2.csv")
adFoodDF=pd.read_csv(path)

#Data Pre-processing
st.header("Data Pre-processing")
st.write(" I will use Pandas to do preliminary investigaton.")
st.write("The following are the first 5 rows of the dataset.")
st.dataframe(adFoodDF.head())

st.write("Next, to know each column data type, I will check their information.")
buffer = io.StringIO()
adFoodDF.info(buf=buffer)
info_output = buffer.getvalue()
st.text(info_output)
st.write("I notice that column index 2, 7, and 11 have some missing values. Therefore, I will drop their values.")
adFoodDF.dropna(inplace=True)
missing_values = adFoodDF.isnull().sum()
st.dataframe(missing_values)

st.write("Then , I continuously check if there are any duplicate values inside the dataset.")
# Convert the duplicated count to a DataFrame
duplicated_count = pd.DataFrame({"Metric": ["Duplicated Rows"], "Count": [adFoodDF.duplicated().sum()]})
st.dataframe(duplicated_count)
st.write("Since there are no more missing and duplicate vlaues, I will proceed to explore the data.")

#Data Exploration
st.header("Exploring the data")
st.subheader("1")
st.write("In this part, to visualize the trend, I will figure out the number of adverse events reported over time to identify trends and potential increase in specific periods by using the line chart.")
st.write("Thus, I utilize **RA_CAERS Created Date** and **AEC_Event Start Date** column.")
first_entered_data_count = pd.to_datetime(adFoodDF['RA_CAERS Created Date']).dt.year.value_counts().sort_index().reset_index()
first_entered_data_count.columns = ['Year', 'Count']
plt.figure(figsize=(14, 6))
sns.lineplot(data=first_entered_data_count, x='Year', y='Count', marker='o', color='blue')
plt.title('Number of Adverse Food Events Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Adverse Events')
plt.show()
st.pyplot(plt)

# Extract the year from the AEC_Event Start Date and count events by year
first_experience_data_count = pd.to_datetime(adFoodDF['AEC_Event Start Date']).dt.year.value_counts().sort_index().reset_index()
first_experience_data_count.columns = ['Year', 'Count']
plt.figure(figsize=(14, 6))
sns.lineplot(data=first_experience_data_count, x='Year', y='Count', marker='o', color='red')
plt.title('Number of Adverse Food Events Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Adverse Events')
plt.show()
st.pyplot(plt)

st.write("**Insight received from the two chart:**")
st.write("""To be compare this two annual trend of the number of adverse food events,
the 'RA_CAERS Created Date' shows a more dramatic increase from 2010 onwards whereas The 'AEC_Event Start Date' shows an increase after the late 1990s. 
Thus this suggest that the more the year shifted, the more the nuber of adverse events are more occurred.""")

st.subheader("2")

st.write("To visualize the trend, I will create a bar chart to compare the number of adverse events for different brands or products.")
st.write("""
Thus, I utilize the '**PRI_Reported Brand/Product Name**' feature which are the names of the products that consumer reported it for their experienced adverse event as well as 
the "**PRI_Product Role**" feature which describe the cause status: "Suspect" or "concomitant".""")
brand_role_counts = adFoodDF.groupby(['PRI_Reported Brand/Product Name', 'PRI_Product Role']).size().reset_index(name='Count')
top_brand_roles = brand_role_counts.nlargest(10, 'Count')
plt.figure(figsize=(14, 7))
sns.barplot(data=top_brand_roles, x='PRI_Reported Brand/Product Name', y='Count', hue='PRI_Product Role', palette='Set3')
plt.title('Products/Brands with the Highest Number of Adverse Events by Product Role')
plt.xlabel('Name of Brand/Product')
plt.ylabel('Number of Adverse Events')
plt.xticks(rotation=45,ha="right")
plt.legend(title='Primary Product Role')
plt.show()
st.pyplot(plt)


st.write("**Insight received from the two chart:**")
st.write("""To compare the number of adverse events for different brands or products, 
I noticed that the brand name called "REDACTED" achieved the most highest significant number of adverse events with the suspect status compared to others. 
There are also other brands which are below 500 adverse events with concomitant status such as "VITAMIN D" and "MULTIVITAMIN".""")


st.subheader("3")
st.write("To visualize the trend, I will create a bar chart to visualize the most frequently reported symptoms .")
st.write("Thus, I utilize the '**SYM_One Row Coded Symptoms**' feature which are the collection of symptom(s) experienced by the injured consumer.")
symptom_list=adFoodDF['SYM_One Row Coded Symptoms'].str.split(', ').explode()
symptom_list= symptom_list.value_counts().reset_index()
symptom_list.columns= ['Symptom Name', 'Count']
plt.figure(figsize=(16, 9))
sns.barplot(x='Symptom Name', y='Count', data=symptom_list.head(10), color="skyblue")
plt.title('Most Common Symptoms Reported in Adverse Food Events')
plt.xlabel('Symptom Name')
plt.ylabel('Number of Adverse Events')
plt.xticks(rotation=45,ha="right")  
plt.show()
st.pyplot(plt)


st.write("**Insight received from the two chart:**")
st.write("""
Among the all symptom reported for adverse events, the symptom of "**DIARRHOEA**" happened the most. 
Frenquently, the symptom of **Nausea** and **Vomitting** can be seen in those reported consumer.""")

st.subheader("4")
st.write("""To visualize the trend, I will create a bar chart to show the distribution of different outcomes resulting
from adverse food event.""")

st.write("Thus I use '**AEC_One Row Outcomes**' feature which is the collection of outcome(s) of the adverse event experienced by the injured consumer.")
outcomes_list=adFoodDF['AEC_One Row Outcomes'].str.split(', ').explode()
outcomes_list= outcomes_list.value_counts().reset_index()
outcomes_list.columns= ['Name of Outcomes', 'Count']
plt.figure(figsize=(14, 7))
sns.barplot(y='Name of Outcomes', x='Count', data=outcomes_list.head(10), palette="Paired")
plt.title('Most Common Outcomes Reported in Adverse Food Events')
plt.ylabel('Name of Outcomes')
plt.xlabel('Number of Adverse Events')
plt.show()
st.pyplot(plt)

st.write("**Insight received from the two chart:**")
st.write("""
Among the all outcomes reported for adverse events, 
the outcome of "**important medical events**" occured the most with significant number.
Athough occuring "**Death**" outcome is a rare and lowest one to occur , there are other severe outcomes slightly more than death such as "**Diability**" and  "**Life Thereatening**".""")

st.subheader("5")
st.write("Next, I will create a histogram chart to analyze the age distribution of individuals affected by adverse food events.")
st.write("""Thus, I will use the '**CI_Age at Adverse Event**' feature which has the values of the age of the consumer reported to have experienced the adverse event and '**CI_Age Unit**' feature 
which has the values of the time unit (day, week, month, year) of the age provided in the CI_Age.
While performing, value of the age of every conusmer will be converted to years in accordance with each age unit.""")
def convert_age_to_years(age, unit):
    age = float(age)
    if unit == 'Year(s)':
        return age
    elif unit == 'Month(s)':
        return age / 12
    elif unit == 'Day(s)':
        return age / 365
    else:
        return age / 52

# Apply the function to the DataFrame
adFoodDF['age(Years)'] = adFoodDF.apply(lambda x: convert_age_to_years(x['CI_Age at Adverse Event'], x['CI_Age Unit']), axis=1)
age_bins = [0, 5, 12, 18, 30, 45, 60, 75, 90, 100]
adFoodDF['Age Bins'] = pd.cut(adFoodDF['age(Years)'], bins=age_bins)
adFoodDF['Age Bins'] = adFoodDF['Age Bins'].dropna().astype(str)
age_bin_counts = adFoodDF['Age Bins'].value_counts().sort_index()
st.bar_chart(age_bin_counts)

st.write("**Insight received from the two chart:**")
st.write("""
Among the all age of the reported consumers, 
the majortiy of adverse events occured in age between 45 and 60. 
There is also a significant number of adverse events reported in the age group of 60 to 75 years.
This could possibly due to weaker immune systems or the consumption of supplements or medications that could interact with foods.""")

st.subheader("6")
st.write("""To visualize the trend, I will create a bar chart to compare the number of adverse events reported by gender.
         
         
For this chart, the "**CI_Gender**" feature will be utilized.  """)

gender_counts = adFoodDF['CI_Gender'].value_counts()
data = gender_counts.values
labels = gender_counts.index

plt.figure(figsize=(10, 6))  

sns.barplot(x=labels, y=data, palette='PuRd') 
plt.title('Gender Comparsion in Reported Adverse Food Events')  
plt.xlabel('Gender')
plt.ylabel('Number of Adverse Events')
plt.xticks(rotation=45)  
plt.show() 
st.pyplot(plt)

st.write("**Insight received from the two chart:**")
st.write("""
In this gender comparison pie chart of the reported events,
female consumers reported more than male consumers 
which could be due to various factors such as gender-specific dietary habits, health awareness, or reporting tendencies.""")

st.subheader("7")
st.write("To visualize the trend, I will create a bar chart to analyze the number of adverse events associated with different FDA industry codes.")
st.write("""Thus, I will utilize the "**PRI_FDA Industry  Code**" and "**PRI_FDA Industry Name**" features.""")
industry_counts = adFoodDF.groupby(['PRI_FDA Industry Code', 'PRI_FDA Industry Name']).size().reset_index(name='count')
plt.figure(figsize=(14, 7))
sns.barplot(data=industry_counts, x='PRI_FDA Industry Code', y='count', hue='PRI_FDA Industry Name')
plt.title('FDA Industry Codes Associated with the Most Adverse Events')
plt.xlabel('FDA Industry Code')
plt.ylabel('Number of Adverse Events')
plt.xticks(rotation=45, ha='right')
plt.legend(title='FDA Industry Name', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
st.pyplot(plt)

st.write("**Insight received from the two chart:**")
st.write("""
In this bar chart, the "**Whole Grain/Milled Grain Prod/Starch**" category indicates 
the most occured adversed events compared to other FDA industry. Apart from it,
other industry codes have relatively low numbers of adverse events.""")

st.subheader("8")
st.write("To visualize the trend, I will create a stacked bar chart to compare the outcomes of adverse events for different product roles.")
adFoodDF['AEC_One Row Outcomes'] = adFoodDF['AEC_One Row Outcomes'].str.split(', ').explode().reset_index(drop=True)
stacked_data = adFoodDF.groupby(['PRI_Product Role', 'AEC_One Row Outcomes']).size().unstack(fill_value=0)
plt.figure(figsize=(14, 8))
stacked_data.plot(kind='barh', stacked=True, colormap='Spectral', figsize=(14, 8))
plt.title('Outcomes of adverse events vary by product role ', fontsize=16)
plt.xlabel('Count of Adverse Events', fontsize=12)
plt.ylabel('Product Role', fontsize=12)
plt.legend(title='Adverse Event Outcomes', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

st.pyplot(plt)

st.write("""**Insight received from the two chart:**
         
         
This stacked bar chart indicates that the "**Suspect**" role has a significantly higher number of reported outcomes compared to 
the "Concomitant" role. Various outcomes such as **hospitalization, visited to healthcare provider, and 
serious injuries** are more prevalent in the "Suspect" category.""")

st.subheader("9")
st.write("To visualize the trend, I will create a histogram chart to Analyze the time difference between when an event occurs and when it is reported.")
adFoodDF['TimeLag(Days)'] = (pd.to_datetime(adFoodDF['RA_CAERS Created Date']) - pd.to_datetime(adFoodDF['AEC_Event Start Date'])).dt.days
plt.figure(figsize=(12, 6))
sns.histplot(adFoodDF['TimeLag(Days)'], bins=50, color='mistyrose')
plt.title('Time Lag between Event Start Date and Report Creation Date')
plt.xlabel('Time Lag (Days)')
plt.ylabel('Number of Reports')
plt.show()
st.pyplot(plt)

st.write("""**Insight received from the two chart:**
         
         
This histogram chart indicates that The majority of adverse events are reported as soon as 
after they happen wheras a few report got some delays even years after the event.""")

st.subheader("10")

st.write("To identify the trend, I use the bar chart to observe if certain times of the year have higher occurrences of adverse food events.")
monthly_counts = pd.to_datetime(adFoodDF['AEC_Event Start Date']).dt.month.value_counts().sort_index()
plt.figure(figsize=(12, 6))
sns.lineplot(x=monthly_counts.index, y=monthly_counts.values, marker='o', color='purple')
plt.title('Seasonal Trends in Occurrence of Adverse Food Events')
plt.xlabel('Months')
plt.ylabel('Number of Adverse Events')
month_labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
plt.xticks(ticks=range(1, 13), labels=month_labels)
plt.show()
st.pyplot(plt)

st.write("""**Insight received from the two chart:**
         
         
Among the all months, **January** marked the highest number of adverse food events.
There is a noticeable decline in the number of events from April through June but slightly increase nack om July and August. 
the occurrences drops significantly towards the end of the year.""")
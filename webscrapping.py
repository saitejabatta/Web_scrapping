

#Importing required libraries
import requests
import pandas as pd
from bs4 import BeautifulSoup


#url addresses the webpage url to be extarcted
url = "https://sahitya-akademi.gov.in/awards/akademi samman_suchi.jsp"


#send a get request to the website 
response = requests.get(url)

##Step-1 : Scrapping Data
#parsing the HTML content of the page
soup = BeautifulSoup(response.text,"lxml")

#finds all the <div> elements with the class "matter"
books = soup.find_all("div", class_ = "matter")
book = soup.find("div", class_ = 'matter')

#retrieves all <td> elements within each <div>
headers = book.find_all("td")
headers

languages=[]

# loopes through first 24 elements from extracted information to identify the languges
# and stores them in a list
for i in range(0,24): 
    title = headers[i].text
    languages.append(title)
print(languages)


# Finding all the tables in the page using BEautifulSoup python Library
tables = soup.find_all("table")
print(len(tables))
print(tables)



'''the dataframe takes tables(list of html table tags) and languages(list of the languages)
and returns a dataframe using the extracted information of tables from the given url'''

def dataframe(tables,languages):
    k=0
    
    #list to store dataframes
    dfs = []
    for i, table in enumerate(tables):
        if k>=len(languages):
            return dfs
        if i==0: 
            continue
        else:
            #Convert the HTML table to a DataFrame with the first row as header
            dframe = pd.read_html(str(table),header=0)[0] 
            
            # Add a new column 'Language' to the DataFrame
            column_data = [f'Language_table_{i+1}']*len(dframe)
            dframe['LANGUAGE'] = languages[k]
            k=k+1
            
            # Append the DataFrame to the list
            dfs.append(dframe)
            '''print(f"table {i+1}")
            print(dframe)
            print('/n')'''

#calling function
dfs = dataframe(tables,t)

# Combine all DataFrames into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True)
print(combined_df)


#Step-2 : Cleaning and Transforming the Extracted data
'''the function category takes a string 'arr' an a parameter and finds the text 
inside the parenthesis within the given input text and returns the text'''  

def category(arr):
    if "(" in arr and ")" in arr:
        s=arr.index('(')
        e=arr.index(')')
        return arr[s+1:e]
    
category_data = []
for i in range(len(combined_df['BOOK'])):
    st = combined_df['BOOK'][i]
    category_data.append(category(st))#category function is invoked on every iteration 
    s2 = st.index('(')
    combined_df['BOOK'][i] =  st[:s2] #replacing the updated title of the book
combined_df['CATEGORY'] = category_data #Adding values to new column CATEGORY
 
    
'''The function is passed by a string as parameter and  removes all the special characters if any are present 
in the given text and returns the name of the author'''

def spe_char(arr):
    author = ''
    for i in arr:
        if i not in "!@#$%^&*()`'-_":
            author = author+i
    return author

authors = combined_df['AUTHOR']
for i in range(len(authors)):
	#funcition is invoked on every iteration and updating the names of the author
    combined_df['AUTHOR'][i] = spe_char(authors[i]) 
                                                    
            
lang=[]
for i in range(len(combined_df['LANGUAGE'])):
    lang.append(combined_df['LANGUAGE'][i].capitalize())
combined_df['LANGUAGE'] = lang
print(combined_df)

# converting the extracted data into a specific format
combined_df.to_csv('Extracted_data.csv')
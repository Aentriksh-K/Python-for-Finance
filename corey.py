# reading csv

# Project Scope:
# Analyze the survey data to explore trends among developers, including coding experience, 
# job satisfaction, salary distributions, programming languages, remote work trends, 
# and open-source contributions.

import pandas as pd, numpy as np, matplotlib.pyplot as plt

na_vals = ['NA','Missing']
survey_result_public = pd.read_csv('D:/Python - VS/stack-overflow-developer-survey-2019/survey_results_public.csv', index_col='Respondent', na_values=na_vals)
survey_results_schema = pd.read_csv('D:/Python - VS/stack-overflow-developer-survey-2019/survey_results_schema.csv')


pd.set_option('display.max_columns',85)
pd.set_option('display.max_rows',85)

print(survey_result_public )
print(survey_results_schema)
print(survey_result_public.shape) # (rows*columns)

print(survey_result_public.describe())
print(survey_result_public.info())  
print(survey_results_schema.info())

print(survey_result_public.columns)
print(survey_result_public['Hobbyist']) # shows values in column name - Hobbyist
print(survey_result_public.loc[:,'Hobbyist']) # alternate method
print(survey_result_public.loc[:,'Hobbyist'].value_counts()) # number of Yes and Nos
print(survey_result_public.loc[[2,2,3],'Hobbyist'])
# print(survey_result_public.loc[[:5,30:],'Hobbyist']) # this will not work
print(survey_result_public.loc[1:4,'Hobbyist':'Country']) # all inclusive

print(survey_result_public.loc[:,'Country'].value_counts()) # finding top countries

# Interesting
# salary and programming language in given country list 
country_list = ['United States','India','Germany','United Kingdom']
filt= survey_result_public.loc[:,'Country'].isin(country_list) # this will be row filter
print(filt)
print(survey_result_public.loc[filt, ['Country','ConvertedComp','LanguageWorkedWith'] ])

high_salary = survey_result_public.loc[:,'ConvertedComp'].value_counts() # finding top salaries
print(high_salary)

# Interesting
# show only data with programing language as python
filt2 = survey_result_public.loc[:,'LanguageWorkedWith'].str.contains('Python', na=False)
print(survey_result_public.loc[filt2,'LanguageWorkedWith'])

# Interesting
# converting 'Hobbyist' form Yes/No to True/False using map function
survey_result_public.loc[:,'Hobbyist'] = survey_result_public.loc[:,'Hobbyist'].map({"Yes":True,'No':False})
print(survey_result_public.loc[:,'Hobbyist'])



# Interesting
# finding highest salary in each country , sorting by country name and salary   
survey_result_public.sort_values(by=  ['Country','ConvertedComp'],ascending=[True,False],inplace = True)
print(survey_result_public.loc[:,['Country','ConvertedComp']])


# Interesting
# finding top 10 largest salary earners 
print(survey_result_public['ConvertedComp'].nlargest(10)) # gives only ConvertedComp field
print(survey_result_public.nlargest(10,'ConvertedComp')) # gives whole table

# Grouping and aggregating
m = survey_result_public.loc[:,'ConvertedComp'].mean()
m2 = survey_result_public.loc[:,'ConvertedComp'].median()
print(m,m2,sep='\n')

print(survey_result_public.describe()) # count shows no. of non NaN values

# median salary broken down by country
# groupby always need sum(),mean() etc
median_salary_country = survey_result_public.loc[:,'ConvertedComp'].groupby(survey_result_public['Country']).median()
print(median_salary_country)

# use this instead
median_salary_country = survey_result_public.groupby('Country')['ConvertedComp'].median()
print(median_salary_country)

# finding mean and median both - using aggregate function (agg)
country_salary_agg = survey_result_public.loc[:,'ConvertedComp'].groupby(survey_result_public['Country']).agg(['median','mean'])
print(country_salary_agg)

# finding % of social media usage
norm_social_media = survey_result_public.loc[:,'SocialMedia'].value_counts(normalize=True)*100
print(norm_social_media)

# data grouped by country India
ind_group = survey_result_public.groupby(survey_result_public['Country']).get_group('India')
print(ind_group)

# or
filt = survey_result_public['Country'] == 'India'
ind_group2 = survey_result_public[filt]
print(ind_group2)


# Social Media user grouped by each Country
country_social_media =  survey_result_public.loc[:,'SocialMedia'].groupby(survey_result_public['Country']).value_counts(normalize=True)
print(country_social_media.head(15))


# find social media use in india
social_media_country = survey_result_public.loc[:,'SocialMedia'].groupby(survey_result_public['Country']).get_group('India').value_counts(normalize=True) 
print(social_media_country)

filt = survey_result_public['Country'] == 'India'
social_media_country = survey_result_public.loc[filt,'SocialMedia'].value_counts(normalize=True)*100
print(social_media_country)


# count number of people use python
python_users = survey_result_public.loc[:,'LanguageWorkedWith'].groupby(survey_result_public['Country']).get_group('India').str.contains('Python').value_counts()
print(python_users)

# use get_group('India') when to find only 1 country

# or
filt = survey_result_public['Country'] == 'India'
python_users2 = survey_result_public[filt]['LanguageWorkedWith'].str.contains("Python").sum()
print(python_users2)

# or
python_users2 = survey_result_public.loc[filt,'LanguageWorkedWith'].str.contains('Python').sum()
print(python_users2)

# number of python users in multiple countries (use lambda function inside apply)

python_users3 = survey_result_public.loc[:,'LanguageWorkedWith'].groupby(survey_result_public['Country']).apply(lambda x : x.str.contains('Python').sum())
print(python_users3)

# % of python users in each country (find no of response who selected python,  and no of total responses, and find % of it )
no_of_resp = survey_result_public.loc[:,'Country'].value_counts()
print(no_of_resp)

perc_of_python = pd.concat((python_users3,no_of_resp),axis='columns')
print(perc_of_python)

perc_of_python['% of python'] = perc_of_python.loc[:,'LanguageWorkedWith']/perc_of_python.loc[:,'count'] * 100
print(perc_of_python.sort_values('% of python',ascending = False))


# average of years of code (experience)

print(survey_result_public['YearsCode']) # data type is object (string) data type
survey_result_public['YearsCode'] = survey_result_public['YearsCode'].astype(float) # converting to float because NaN is float type
print(survey_result_public['YearsCode'].mean()) # it will throw error because it has some strings
print(survey_result_public['YearsCode'].unique()) # shows all values
survey_result_public['YearsCode'].replace('Less than 1 year',float(0.5),inplace=True) # float is mandatory
survey_result_public['YearsCode'].replace('More than 50 years',int(51),inplace=True) # int is mandtory
print(survey_result_public['YearsCode'].unique()) # checking the values
survey_result_public['YearsCode']=  survey_result_public['YearsCode'].astype(float) # converting to float
print(survey_result_public['YearsCode'].mean())


# CHAT GPT

#Group salaries by country and experience level
print(survey_results_schema.loc[13:15,:].to_string()) # full string

#does not work as survey_result_public[['Country','YearsCode']] is dataframe. But Groupby needs column name as a list
s = survey_result_public.loc[:,['Country','ConvertedComp','YearsCode']].groupby(survey_result_public[['Country','YearsCode']]).sum()
print(s)

s1 = survey_result_public.groupby(['Country','YearsCode'])['ConvertedComp'].mean()
print(s1)

# Calculate average salary per job role
survey_result_public[[survey_results_schema.iloc[12,0],'ConvertedComp']]
print(survey_result_public.groupby(['DevType'])['ConvertedComp'].mean())

# Find most common programming languages used

lang_split = survey_result_public['LanguageWorkedWith'].str.split(';')
lang_split.replace({np.nan:'No Answer'},inplace=True) # NaN is float, replacing to string
print(lang_split) 

languages = [lang for lst in lang_split for lang in lst] 
print(languages)

lang_df = pd.Series(languages)
bifur = lang_df.value_counts(normalize=True)*100
bifur.info()
# lang_df.value_counts()
bifur.plot(kind='pie',labels=bifur.index, autopct='%1.1f%%', title = 'Most common programming languages ')    
plt.show()


# Analyze remote work vs. in-office work trends

print(list(survey_result_public['WorkRemote'].unique()))
work = survey_result_public['WorkRemote'].value_counts(normalize=True)*100

work.plot( kind = 'pie',autopct='%1.1f%%')
plt.show()

# Employment status distribution (e.g., employed, student, self-employed)
print(survey_result_public['Employment'].unique())
emp = survey_result_public['Employment'].value_counts(normalize=True)*100

emp.plot(kind='pie',autopct = '%1.1f%%',title='Remote work vs. in-office work trends')
plt.show()


# Salary vs. years of professional coding experience

print(survey_result_public.columns)
exp_comp = survey_result_public.loc[:,['YearsCode','ConvertedComp']].dropna()

exp_comp_grp = exp_comp.groupby('YearsCode')['ConvertedComp'].median()

exp_comp_grp.rename(index={'Less than 1 year' : 0.5 ,'More than 50 years':55 }, inplace=True)
exp_comp_grp.index = exp_comp_grp.index.astype(float)
exp_comp_grp = exp_comp_grp.sort_index()

print(exp_comp_grp)

exp_comp_grp.plot(kind='bar',title='Median Salary vs. years of professional coding experience')
plt.show()

#  countries with the highest and lowest average salaries

count_comp = survey_result_public[['Country','ConvertedComp']]
count_comp_mean = count_comp.groupby('Country')['ConvertedComp'].mean()
count_comp_median = count_comp.groupby('Country')['ConvertedComp'].median()

print(count_comp_median.nlargest(5),count_comp_median.nsmallest(5))

print(survey_result_public['YearsCode'].astype(float).mean())













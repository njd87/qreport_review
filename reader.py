from bs4 import BeautifulSoup
import pandas as pd
import sys

soup = BeautifulSoup()

with open("qreport_2024_spring.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

a = soup.find_all('div', class_='card-body')

print(len(a))


'''
How do I want to split information about each thing?

dictionary:
    department
    link
    hours
    recommendations
    professor
    students
'''

courses = []

for thing in a:
    tmp = thing.find_all('a', href=True)
    for course in tmp:
        curr = {}
        curr['link'] = course['href']
        curr['name'] = course.encode_contents()[4:-80].strip().decode("utf-8")
        courses.append(curr)


df = pd.DataFrame(courses)

df.to_csv('spring_2024_output/coursesSpring_2024.csv')
from bs4 import BeautifulSoup
from helpers import *
import pandas as pd
import time
import sys

def read_html(html_file, save=''):
    with open(html_file) as fp:
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

    if save:
        df.to_csv(save)

    return df

def main(files, save_as='output.txt'):
    newInfo = []

    for file, (semester, year) in files.items():
        # read in course info
        df = read_html(file)

        # walk through each part of the dataframe
        for i in range(len(df)):
            # # sleep to avoid over requesting
            if i % 20 == 0:
                df2 = pd.DataFrame(newInfo)
        
                df2.to_csv(save_as)
            
            # create new dictionary
            curr = {}
            test = df.iloc[i]
            test['requested_info'] = request_page(test['link'])
            test['soup'] = BeautifulSoup(test['requested_info'].content, features='html.parser')

            curr['name'] = test['name']
            curr['link'] = test['link']

            # add information
            curr['hours'] = getMeanHours(test)
            curr['students'] = getStudents(test)
            curr['department'] = getDepartment(test)
            curr['recommendations'] = getRecommendations(test)
            curr['instructor_rating'] = getInstructorRating(test)
            curr['instructor'] = getInstructor(test)
            curr['comments'] = getComments(test)
            curr['semester'] = semester
            curr['year'] = year

            newInfo.append(curr)
            print(f'Collected {i + 1} of {len(df)} courses for {semester} {year}')

        df2 = pd.DataFrame(newInfo)
        
        df2.to_csv(save_as)

    return newInfo

def test():
    test_url = 'https://harvard.bluera.com/harvard/rpv.aspx?lang=eng&redi=1&SelectedIDforPrint=ae715aaaaac9ef9182c1f8c1b885f9646b7b65a7c1253aaf79330cb803fca7088f0a76dc37ea2d5a9d832b776eebb577&ReportType=2&regl=en-US'

    print(getInstructor({'link': test_url}))

def run():
    main({
        'qreport_2022_spring.html' : ['S', 2022],
        'qreport_2021_fall.html': ['F', 2021],
    },
    save_as='qreport_app/data/output_2021_2022.csv'
    )

    main({
        'qreport_2023_spring.html' : ['S', 2023],
        'qreport_2022_fall.html': ['F', 2022],
    },
    save_as='qreport_app/data/output_2022_2023.csv'
    )
    
if __name__ == '__main__':
    run()
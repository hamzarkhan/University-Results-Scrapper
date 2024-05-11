from django.shortcuts import render
from .forms import ResultForm
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup
import mechanize
import requests
from requests.adapters import HTTPAdapter

def scrape_results(result_link, college_code, field_code, year):
    globalbr = mechanize.Browser()
    globalbr.set_handle_robots(False)

    # Your existing web scraping logic
    pre_link = result_link + "?mbstatus&htno="
    row = 1

    college_codes = [college_code]
    field_codes = [field_code]
    results = []

    for field_code in field_codes:
        for college_code in college_codes:
            if not is_valid_combination(college_code, field_code):
                results.append({'error': 'College code and course not matched'})
                continue
            
            for index in range(1, 121):
                hall_ticket = college_code + year + field_code + str(index).zfill(3)
                result = find_result(globalbr, pre_link, field_code, college_code, hall_ticket, int(str(index).zfill(3)))
                results.append(result)

            # Lateral Entry students
            for index in range(301, 313):
                hall_ticket = college_code + year + field_code + str(index).zfill(3)
                result = find_result(globalbr, pre_link, field_code, college_code, hall_ticket, int(str(index).zfill(3)))
                results.append(result)

    return results

def find_result(globalbr, pre_link, field_code, college_code, hall_ticket, index):
    result_link = pre_link + hall_ticket
    session = requests.Session()
    adapter = HTTPAdapter()
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    raw = session.get(result_link)
    soup = BeautifulSoup(raw.content, "html.parser")

    # Find the Name
    table = soup.find('table',id="AutoNumber3")
    if table is None:
        return None
    last_row = table("tr")[2]
    td_list = last_row.find_all("td")
    name = td_list[1].text

    # Find the GPA
    table = soup.find(id="AutoNumber5")
    if table is None:
        return None
    rows = table.find_all("tr")[-1]
    mark_row=rows.find_all('td')[1]
    marks =mark_row.get_text(strip=True)

    # Find subjects with 'F' grade
    f_grade_subjects = extract_subjects_with_f_grade(soup)

    result_data = {
        'college_code': college_code,
        'field_code': field_code,
        'hall_ticket': hall_ticket[-3:],
        'marks': marks,
        'name': name,
        'backlogs': mark_safe('<br>'.join(f_grade_subjects)) if f_grade_subjects else "No Backlogs",
    }

    print("Result Data: ", result_data)
    return result_data

def extract_subjects_with_f_grade(soup):
    table = soup.find(id="AutoNumber4")
    if table is None:
        return []
    rows = table.find_all("tr")[1:]
    f_grade_subjects = []
    for row in rows:
        columns = row.find_all("td")
        sub_code = columns[0].text.strip()
        sub_name = columns[1].text.strip()
        grade = columns[4].text.strip()
        if grade == 'F':
            f_grade_subjects.append(f"{sub_code} - {sub_name}")
    return f_grade_subjects

def is_valid_combination(college_code, field_code):
    # Define a dictionary mapping college codes to the available field codes
    college_field_mapping = {
        '1604': ['748','735','734','737', '750', '736', '733', '732'],  # MJCET
        '1603':['735','736','737','732','734','733'], # DECCAN
        '1605': ['736', '733', '732'],          # ISL
        '1610': ['748', '749', '750', '736', '733', '732'],  # NSAKCET
        '2455': ['748', '733',],          # KMEC
        '2453': ['748','733']   # NGIT
    }

    # Check if the selected field code is available for the chosen college code
    return field_code in college_field_mapping.get(college_code, [])

def index(request):
    results = []

    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result_link = form.cleaned_data['result_link']
            college_code = form.cleaned_data['college_code']
            field_code = form.cleaned_data['field_code']
            year = form.cleaned_data['year']

            # Scraping results
            results = scrape_results(result_link, college_code, field_code, year)

    else:
        form = ResultForm()

    return render(request, 'resultapp/index.html', {'form': form, 'results': results})

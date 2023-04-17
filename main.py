import os
from color import Color
import requests
import csv
from bs4 import BeautifulSoup


def print_b(text):
    # Use print_b to change output color Light Blue
    lightblue = Color.LightBlue
    x = Color.X
    print(f"{lightblue}{text}{x}")


def print_g(text):
    # Use print_g to change output color OK Green
    ok = Color.G
    x = Color.X
    print(f"{ok}{text}{x}")


def print_o(text):
    # Use print_g to change output color Warning orange
    orange = Color.W
    x = Color.X
    print(f"{orange}{text}{x}")


if __name__ == '__main__':
    os.system('clear')  # Clear the screen
    i = 0  # Empty counter
    item_list = []  # Empty Item list
    URLlist = []  # Empty URL list
    URL = "https://impavn.com/"  # Home Page
    MainPage = requests.get(URL)  # Get Full Page
    MainSoup = BeautifulSoup(MainPage.content, "html.parser")  # Change the page using BeautifulSoup
    results = MainSoup.find('div', class_="keys-box col-xs-12")  # find <div class="keys-box col-xs-12">
    for CLum in results.find_all('ul'):  # search for all ul
        for Line in CLum.find_all('li'):  # search for all li in each ul
            i += 1
            URLlist.append(Line.find('a')['href'])  # fill URL List with all URL  Category
    for i in range(len(URLlist)):
        # Category URL
        page = requests.get(URLlist[i])  # <i class="pull-right">297(15/15)</i>
        soup = BeautifulSoup(page.content, "html.parser")  # Change the page using BeautifulSoup
        results = soup.find('i', class_="pull-right")  # find <i class="pull-right">297(15/15)</i>
        PagesCount = int(results.text.rsplit('/', 1)[1][:-1])  # PagesCount = 15
        print(str(i) + "- " + URLlist[i] + "  /  " + str(PagesCount))  # Print Category URL
        for cont in range(1, PagesCount):
            # List URL
            URL_s = URLlist[i] + "?paged=" + str(cont)  # Modify List URL
            print_g(str(i) + "-" + str(cont) + " " + URL_s)  # Print List URL
            page_s = requests.get(URL_s)  # Get List Page
            soup_s = BeautifulSoup(page_s.content, "html.parser")  # Change the page using BeautifulSoup
            results_s = soup.find('table', class_="content-table")  # find <table class="content-table">
            for row in results_s.tbody.find_all('tr'):  # find <tbody> on table
                # find all 'tr' on table
                columns = row.find_all('td')
                if columns:
                    # Grap data and save it in item_list
                    Code = columns[1].text
                    Description = columns[2].text
                    Image = columns[3].contents[1]['src']
                    Unit = columns[4].text.replace(u'\xa0', u'')
                    line_list = [Code, Description, Image, Unit]
                else:
                    continue
            item_list.append(line_list)

    # Save list on CSV  File
    fields = ['Code', 'Description', 'Image', 'Unit']
    with open('GFG', 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        for line in item_list:
            write.writerow(line)

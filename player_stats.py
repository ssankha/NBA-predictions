import requests
from bs4 import BeautifulSoup
from datetime import date
import json

def scrape():
    # get games for current month
    months =["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    day = date.today().day
    month = date.today().month
    year = date.today().year

    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_games-" + months[month - 1] + ".html"

    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    table = soup.find("tbody")
    html_games = table.find_all("tr")
    
    for html_game in html_games:
        # check if date of game is today
        html_date = html_game.find("th", attrs={"data-stat":"date_game"}).find("a").contents[0]
        
        # remove day of the week and commas from date
        # makes "Mon, Apr 1, 2024" into "Apr 1 2024"
        comma_index = html_date.index(",")
        html_date = html_date[comma_index + 2:]
        html_date = html_date.replace(",", "")
        date_parts = html_date.split(" ")
        
        # check if game is held on same day
        if(date_parts[0].lower() in months[month - 1] and date_parts[1] == str(day) and date_parts[2] == str(year)):
            # get visiting and home teams
            visiting_team = html_game.find("td", attrs={"data-stat":"visitor_team_name"}).find("a").contents[0]
            home_team = html_game.find("td", attrs={"data-stat":"home_team_name"}).find("a").contents[0]
            
            print([visiting_team, home_team])
            # explore players for visiting team
            
            # explore players for home team
            
        
    
    

def main():
    scrape()
    
if __name__ == "__main__":
    main()
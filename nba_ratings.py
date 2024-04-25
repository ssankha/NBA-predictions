import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import Ridge
import requests
from bs4 import BeautifulSoup

def scrape():
    # the url of the website to be scraped
    # the months that have happened
    base_url = 'https://www.basketball-reference.com/leagues/NBA_2023_games-'
    months_played = ['october', 'november', 'december', 'january', 'march', 'april', 'may']
    
    # scrape the match history from the months that have been played
    # place the match history in a CSV file called nba_results.csv
    with open("nba_results.csv", 'w') as nba_results:
        
        # iterate through the months and scrape the data from matches played in that month
        for i in range(len(months_played)):
            response = requests.get(base_url + str(months_played[i]) + ".html")
            #nba_results.write(response.text)

            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', attrs={'id':'schedule'}).find('tbody')
            games = table.find_all('tr')

            # iterate through the rows
            for i in range(len(games)):
                #nba_results.write(str(games[i]) + "\n\n")
                game = games[i]
                
                # get the visitor team
                visitor_team = game.find('td', attrs={'data-stat':"visitor_team_name"}).find('a').contents[0]
                
                # get the visitor's points
                visitor_points = game.find('td', attrs={'data-stat':'visitor_pts'}).contents[0]
                
                # get the home team
                home_team = game.find('td', attrs={'data-stat':"home_team_name"}).find('a').contents[0]
                
                # get the home team's points
                home_points = game.find('td', attrs={'data-stat':'home_pts'}).contents[0]

                # write to the file
                
                
                print(visitor_team, visitor_points, home_team, home_points)
                break
            
            break

            
            









    """
    df = pd.read_csv('nba_results.csv')

    df['date'] = pd.to_datetime(df['date_played'], format='%Y-%m-%d')

    df['point_difference'] = df['home_points'] - df['away_points']

    df['home_win'] = np.where(df['point_difference'] > 0, 1, 0)
    df['home_loss'] = np.where(df['point_difference'] < 0, 1, 0)

    df_visitor = pd.get_dummies(df['away_team'], dtype=np.int64)
    df_home = pd.get_dummies(df['home_team'], dtype=np.int64)

    df_model = df_home.sub(df_visitor) 
    df_model['point_difference'] = df['point_difference']


    lr = Ridge(alpha=0.001) 
    X = df_model.drop(['point_difference'], axis=1)
    y = df_model['point_difference']

    lr.fit(X, y)

    df_ratings = pd.DataFrame(data={'team': X.columns, 'rating': lr.coef_})

    df_srs = pd.read_csv('nba_srs.csv')

    df_ratings = df_ratings.join(df_srs.set_index('team'), on='team')
    df_ratings['elo'] = (df_ratings['rating'] + df_ratings['SRS'])/2
    df_ratings = df_ratings.sort_values(by=['elo'], ascending=False)
    df_ratings = df_ratings.drop(columns=['rating', 'SRS'])

    print(df_ratings)"""

def main():
    scrape()
    
if __name__ == "__main__":
    main()
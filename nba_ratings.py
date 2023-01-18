import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.linear_model import Ridge

df = pd.read_csv('nba_trial.csv')

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

print(df_ratings)
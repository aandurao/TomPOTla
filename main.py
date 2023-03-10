import pandas as pd
import numpy as np
from pandasql import sqldf
import random as rd
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error

pysqldf = lambda q: sqldf(q, globals())

# Loadind data
data= pd.read_csv("./collecte_tompotla.csv")

# Pre-processing
data = data.rename(columns={'Last name':'last_name', 'Want a ticket for the party ?':'party_tickets', 'How many lottery tickets do you want to buy :':'lottery_tickets', 'Academic e-mail address':'mail'})

data = data.replace({'1 ticket':1, '2 tickets':2, '5 tickets':5, '10 tickets':10})

data["ID"] = data[['last_name', 'First name', 'mail']].agg('-'.join, axis=1)

data["lottery_tickets"] = data["lottery_tickets"].fillna(0)
data["party_tickets"] = data["party_tickets"].replace({np.nan:0, 'Télécom (1 lottery ticket included)':1, 'Others (1 lottery ticket included)':1, 'IPP (1 lottery ticket included)':1})


## PROCESSING DATA

q = "SELECT ID, SUM(lottery_tickets) AS tot_lottery_tickets FROM data GROUP BY ID"
group_lottery_tickets = pysqldf(q)
group_lottery_tickets.to_csv("save2.csv")

q = "SELECT ID, SUM(party_tickets) AS tot_party_tickets FROM data GROUP BY ID"
group_party_tickets = pysqldf(q)
group_party_tickets.to_csv("save3.csv")

total_tickets = group_lottery_tickets.copy()
total_tickets =  total_tickets.rename(columns={'tot_lottery_tickets':'tickets'})
total_tickets["tickets"] = total_tickets["tickets"] + group_party_tickets["tot_party_tickets"]
total_tickets.to_csv("final.csv")

repeated_ID_list =  []

for index, row in total_tickets.iterrows():
    for i in range(int(row["tickets"])):
        repeated_ID_list.append(row["ID"])

np.random.shuffle(repeated_ID_list)

## CHOOSING THE WINNER

print("THE WINNER IS :" + repeated_ID_list[np.random.randint(len(repeated_ID_list))])

## Checking consistency of the results
win_dist = total_tickets.copy()
win_dist = win_dist.rename(columns={'tickets':'prob'})
win_dist["prob"] = 0

for i in range(10000):
    win_dist.loc[win_dist["prob"] == repeated_ID_list[np.random.randint(len(repeated_ID_list))], 'prob'] += 1

plt.bar(total_tickets["ID"], total_tickets["tickets"])
plt.savefig("true.jpg")
plt.clf()
plt.bar(win_dist["ID"], win_dist["prob"])
plt.savefig("res.jpg")
import pandas as pd
import numpy as np
from pandasql import sqldf

pysqldf = lambda q: sqldf(q, globals())

# Loadind data
data= pd.read_csv("./collecte(4).csv")

# Pre-processing
data = data.rename(columns={'Want a ticket for the party ?':'party_tickets', 'How many tickets do you want to buy :':'lottery_tickets', 'E-mail address':'mail'})
data = data.replace({'1 ticket':1, '2 tickets':2, '5 tickets':5, '10 tickets':10})

q = "SELECT mail, SUM(lottery_tickets) AS tot_lottery_tickets FROM data WHERE lottery_tickets>0 GROUP BY mail"
group_lottery_tickets = pysqldf(q)
group_lottery_tickets.to_csv("save1.csv")

q = "SELECT mail, lottery_tickets FROM data"
group_lottery_tickets = pysqldf(q)
group_lottery_tickets.to_csv("save.csv")

q = "SELECT mail, party_tickets, COUNT(party_tickets) AS tot_party_tickets FROM data WHERE party_tickets !='NaN' GROUP BY mail"
group_party_tickets = pysqldf(q)
#group_party_tickets.to_csv("save.csv")
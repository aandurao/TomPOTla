import wx
import pandas as pd
import numpy as np
from pandasql import sqldf
import random as rd
from matplotlib import pyplot as plt
import wx

pysqldf = lambda q: sqldf(q, globals())

class MainFrame(wx.Frame):
    data = None
    def __init__(self, parent, d, title):
        super(MainFrame, self).__init__(parent, title=title, size=(400, 200))

        self.data = d
        # Adding a panel to the frame
        panel = wx.Panel(self)

        # Adding a button to trigger the winner selection
        button = wx.Button(panel, label="Select winner", pos=(150, 60))
        button.Bind(wx.EVT_BUTTON, self.on_button_click)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        mainSizer.Add(button, 0, wx.ALL | wx.CENTER, 5)


        # Adding a static text to display the winner
        self.result_text1 = wx.StaticText(panel, label="")
        # Adding a static text to display the winner
        self.result_text2 = wx.StaticText(panel, label="")
        # Adding a static text to display the winner
        self.result_text3 = wx.StaticText(panel, label="")
        # Adding a static text to display the winner
        self.result_text4 = wx.StaticText(panel, label="")
        # Adding a static text to display the winner
        self.result_text5 = wx.StaticText(panel, label="")
        # Adding a static text to display the winner
        self.result_text6 = wx.StaticText(panel, label="")
        # Adding a static text to display the winner
        self.result_text7 = wx.StaticText(panel, label="")

        mainSizer.Add(self.result_text1, 0, wx.ALL | wx.CENTER, 5)
        mainSizer.Add(self.result_text2, 0, wx.ALL | wx.CENTER, 5)
        mainSizer.Add(self.result_text3, 0, wx.ALL | wx.CENTER, 5)
        mainSizer.Add(self.result_text4, 0, wx.ALL | wx.CENTER, 5)
        mainSizer.Add(self.result_text5, 0, wx.ALL | wx.CENTER, 5)
        mainSizer.Add(self.result_text6, 0, wx.ALL | wx.CENTER, 5)
        mainSizer.Add(self.result_text7, 0, wx.ALL | wx.CENTER, 5)

        panel.SetSizer(mainSizer)


        # Centering the frame
        self.Center()
        self.ShowFullScreen(True)

    def on_button_click(self, event):

        q = "SELECT ID, SUM(lottery_tickets) AS tot_lottery_tickets FROM data GROUP BY ID"
        group_lottery_tickets = pysqldf(q)

        q = "SELECT ID, SUM(party_tickets) AS tot_party_tickets FROM data GROUP BY ID"
        group_party_tickets = pysqldf(q)

        total_tickets = group_lottery_tickets.copy()
        total_tickets =  total_tickets.rename(columns={'tot_lottery_tickets':'tickets'})
        total_tickets["tickets"] = total_tickets["tickets"] + group_party_tickets["tot_party_tickets"]


        text_list = ["1st WINNER IS (iPad) : ", "2nd WINNER IS :", "3rd WINNER IS : ", "4th WINNER IS : ","5th WINNER IS : ","6th WINNER IS : ","7th WINNER IS : "]

        label_list = [self.result_text1, self.result_text2, self.result_text3, self.result_text4, self.result_text5, self.result_text6, self.result_text7]

        repeated_ID_list = []

        for index, row in total_tickets.iterrows():
            for i in range(int(row["tickets"])):
                repeated_ID_list.append(row["ID"])


        np.random.shuffle(repeated_ID_list)

        for t,l in zip(text_list, label_list):

            winner = repeated_ID_list[np.random.randint(len(repeated_ID_list))]

            # Displaying the winner in the interface
            l.SetLabel(t + data[data["ID"].str.match(winner)]["last_name"].to_string(header=False, index=False) + " " + data[data["ID"].str.match(winner)]["First name"].to_string(header=False, index=False))

            repeated_ID_list = [id for id in repeated_ID_list if id!=winner]

if __name__ == '__main__':
    if ('app' in globals() or 'app' in locals()) :
        del app
    app = wx.App()
    # Loading data
    data = pd.read_csv("./collecte_tompotla.csv")

    # Pre-processing
    data = data.rename(columns={'Last name':'last_name', 'Want a ticket for the party ?':'party_tickets', 'How many lottery tickets do you want to buy :':'lottery_tickets', 'Academic e-mail address':'mail'})

    data = data.replace({'1 ticket':1, '2 tickets':2, '5 tickets':5, '10 tickets':10})

    data["ID"] = data[['last_name', 'First name', 'mail']].agg('-'.join, axis=1)

    data["lottery_tickets"] = data["lottery_tickets"].fillna(0)
    data["party_tickets"] = data["party_tickets"].replace({np.nan:0, 'Télécom (1 lottery ticket included)':1, 'Others (1 lottery ticket included)':1, 'IPP (1 lottery ticket included)':1})
    frame = MainFrame(None, data, title="TomPOTla Lottery")
    frame.Show()
    app.MainLoop()
    del app
from bs4 import BeautifulSoup
import requests
import time
import csv
from time import sleep 
from random import randint

def randomize_sleep(min, max):
    sleep(randint(min*100, max*100) / 100)

def web_scraper(province_territory):
    province_territory_dict = {
        "Alberta": "AB",
        "British Columbia": "BC",
        "Manitoba": "MB",
        "New Brunswick": "NB",
        "Newfoundland": "NL",
        "Northwest Territories": "NT",
        "Nova Scotia": "NS",
        "Nunavut": "NU",
        "Ontario": "ON",
        "Prince Edward Island": "PE",
        "Québec": "QC",
        "Saskatchewan": "SK",
        "Yukon": "YT"
    }

    url = f'https://churchdirectory.ca/search/?s_city=Any+City&s_province={province_territory_dict[province_territory]}&s_orgname=Any+Church+Name&goButton.x=55&goButton.y=60'
    
    header = {"From": "Daniel Agapov <danielagapov1@gmail.com>"}

    response = requests.get(url, headers=header)
    if response.status_code != 200: print("Failed to get HTML:", response.status_code, response.reason); exit()

    soup = BeautifulSoup(response.text, "html5lib")

    return soup.select("fieldset")

def retrieve_info(church):
    name = church.select("legend")[0].text.replace("Edit ", '')

    


    '''church = church.select("p.address")[0]
    print(church.text)

    details_link = church.select('a')[0]['href']

    header = {"From": "Daniel Agapov <danielagapov1@gmail.com>"}
    
    response = requests.get(details_link, headers=header)
    if response.status_code != 200: print("Failed to get HTML:", response.status_code, response.reason); exit()

    soup = BeautifulSoup(response.text, "html5lib")'''

    return name, city, phone, email, website



def csv_entry(province_territory, churches): 
    churches = web_scraper(province_territory)
    
    #clears spreadsheet
    with open(f"./churches/{province_territory}.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([])

    for church in churches: 
        retrieve_info(church)
        

#this first function may seem redundant, but I need it to pass in these variables for the 
#province_territory so that the index resets for every province_territory entered. 

def scrape(province_territory):
    
    churches = web_scraper(province_territory)
        
    csv_entry(province_territory, churches)

#everything past this point is just for the GUI and doesn't matter for the web scraper. 
#------------------------------------------------------------------------------------------#

import tkinter as tk
from tkinter import ttk


HEIGHT = 768
WIDTH = 1366

def main():
    #initializing module
    root = tk.Tk()
    
    #setting the current screen to start menu
    app = main_screen(root)
    
    #overall GUI loop which will run constantly, accepting input and such
    root.mainloop()


class PlaceholderEntry(ttk.Entry):
    #initializing the arguments passed in
    def __init__(self, container, placeholder, validation, *args, **kwargs):
        super().__init__(container, *args, style="Placeholder.TEntry", **kwargs)
        self.placeholder = placeholder
        self.insert("0", self.placeholder)
        
        #runs the appropriate method for when the user is focused in/out of the element
        self.bind("<FocusIn>", self._clear_placeholder)
        self.bind("<FocusOut>", self._add_placeholder)
        
        #if this argument is given (like for the instagram password, 
        # then the entry box will hide its text with asterisks)
        self.validation = validation

    
    def _clear_placeholder(self, e):
        #deleting all text placed automatically with the placeholder
        if self["style"] == "Placeholder.TEntry":
            self.delete("0", "end")
            self["style"] = "TEntry"
        
        #editing the property of the entry box 'show' to display asterisks ,
        #instead of any of the entered characters
        if self.validation == 'password':
            self['show'] = "*"
        
    def _add_placeholder(self, e):
        #if there isn't any text entered in AND the user isn't focused in 
        #on this, then it'll add the placeholder
        if not self.get():
            self.insert("0", self.placeholder)
            self["style"] = "Placeholder.TEntry"


class main_screen():
    def __init__(self, master):
        #these properties will mostly stay constant throughout all windows
        self.master = master
        self.master.title("Church Scraper GUI")
        self.canvas = tk.Canvas(self.master, height=HEIGHT, width=WIDTH, bg = '#23272a')
        self.canvas.pack()
        self.master.config(bg = "#23272a")
        self.master.resizable(width=False, height=False)

        
        #making the style of this window compatible with my custom entry class
        self.style = ttk.Style(self.master)
        self.style.configure("Placeholder.TEntry", foreground="#d5d5d5")

        global options

        options = [
            "Any Province", 
            "Alberta",
            "British Columbia", 
            "Manitoba",
            "New Brunswick",
            "Newfoundland",
            "Northwest Territories",
            "Nova Scotia",
            "Nunavut",
            "Ontario",
            "Prince Edward Island",
            "Québec",
            "Saskatchewan",
            "Yukon"
        ]

        current_province_territory = tk.StringVar(self.master)
        current_province_territory.set(options[0])

        
        self.province_territory_frame = tk.Frame(self.master, bg="#99aab5", bd=10)
        self.province_territory_frame.place(relx=0.5, rely=0.2, relwidth=0.75, relheight=0.1, anchor='n')

        self.submit_frame = tk.Frame(self.master, bg="#7289da", bd=10)
        self.submit_frame.place(relx=0.5, rely=0.85, relwidth=0.2, relheight=0.1, anchor='n')
        

        global province_territory_entry
        province_territory_entry = tk.OptionMenu(self.province_territory_frame, current_province_territory, *options)
        province_territory_entry.config(width=90, font=('Courier', 28))
        province_territory_entry.place(relheight=1, relwidth=1)

        #button for province_territory entry
        #I only want its command to run once, when it's clicked so I made a 
        #simple lambda that invokes the info_display function
        self.button = tk.Button(self.submit_frame, text="Web Scrape", font=('Courier', 24), bg='white', 
            command=lambda:scrape(str(province_territory_entry['text'])))
        self.button.place(relheight=1, relwidth=1)


        

if __name__ == '__main__':
    main()
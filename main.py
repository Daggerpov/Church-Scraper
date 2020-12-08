from bs4 import BeautifulSoup
import requests
import time
import csv

def web_scraper(province_territory):
    if len(province_territory.split()) == 2: 
        province_territory = province_territory.replace(' ', '-')
    url = f'https://www.uschamber.com/co/chambers/{province_territory.lower()}'
    
    header = {"From":"Daniel Agapov <danielagapov1@gmail.com>"}

    response = requests.get(url, headers=header)
    if response.status_code != 200: print("Failed to get HTML:", response.status_code, response.reason); exit()

    soup = BeautifulSoup(response.text, "html5lib")

    return soup.select(".chamber-finder__item")

def retrieve_info(province_territory, lines, current_chamber, chamber_member_bool_info='', website_info='', phone_number_info='', address_info='', address2_info='', accredited_info=''):
    for line in lines:
        stars = 0
        for star in current_chamber.find_all(class_="icon-star"):
            stars += 1
            accredited_info = f'{stars} / 5'
        
        if 'U.S. Chamber Member' in line:
            chamber_member_bool_info = 'U.S. Chamber Member'
                
        if 'Website—' in line:
            website_info = line.replace('Website—', '').replace(' ', '')

        
        if 'Phone Number—' in line:
            phone_number_info = line.replace('Phone Number—', '').replace(' ', '')


        if 'Address—' in line:
            line_number = lines.index(line)
            split_address = lines[line_number+2:line_number+4]
            address_info = split_address[0].replace('  ', '')
            address2_info = split_address[1].replace('  ', '')

        
    name_not_formatted = lines[2].split()
    name_info = ''
    for i in name_not_formatted:
        name_info += i + ' '

    return name_info, chamber_member_bool_info, website_info, phone_number_info, address_info, address2_info, accredited_info

def csv_entry(province_territory): 
    chambers = web_scraper(province_territory)
    
    #clears spreadsheet
    with open(f"./chambers/{province_territory}.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows([])

    for current_chamber in chambers:
        table = []
        lines = current_chamber.text.split('\n')
        table.append(retrieve_info(province_territory, lines, current_chamber))

        with open(f"./chambers/{province_territory}.csv", "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(table)
        

global index ; index = 0

#this first function may seem redundant, but I need it to pass in these variables for the 
#province_territory so that the index resets for every province_territory entered. 

def scrape(province_territory, city):
    global index ; index = 0
    
    chambers = web_scraper(province_territory)
    current_chamber = chambers[index]
    lines = current_chamber.text.split('\n')
    
    name['text'], chamber_member_bool['text'], website['text'], \
    phone_number['text'], address['text'], address2['text'], \
    accredited_text = retrieve_info(province_territory, lines, current_chamber)
    
    if chamber_member_bool['text'] != '' and accredited_text != '':
        chamber_member_bool['text'] += f'  |  {accredited_text}'
    elif accredited_text != '':
        chamber_member_bool['text'] = accredited_text
    
    csv_entry(province_territory)

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
        

        #fitting the entry and button for weather
        self.weather_frame = tk.Frame(self.master, bg="#99aab5", bd=5)
        self.weather_frame.place(relx=0.5, rely=0.05, relwidth=0.75, relheight=0.1, anchor='n')
        
        #fitting the output
        self.lower_frame = tk.Frame(self.master, highlightcolor="#99aab5", bd=10)
        self.lower_frame.place(relx=0.5, rely=0.20, relwidth=0.75, relheight=0.7, anchor='n')



        name = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        name.place(rely=0, relwidth=1, relheight=0.165)

        chamber_member_bool = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        chamber_member_bool.place(rely=0.165, relwidth=1, relheight=0.165)

        phone_number = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        phone_number.place(rely=0.33, relwidth=1, relheight=0.165)

        website = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        website.place(rely=0.495, relwidth=1, relheight=0.165)

        address = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        address.place(rely=0.66, relwidth=1, relheight=0.165)

        address2 = tk.Label(self.lower_frame, bg="#99aab5", font=('Courier', 24))
        address2.place(rely=0.825, relwidth=1, relheight=0.165)


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
        self.submit_frame.place(relx=0.5, rely=0.85, relwidth=0.15, relheight=0.1, anchor='n')
        

        global province_territory_entry
        province_territory_entry = tk.OptionMenu(self.province_territory_frame, current_province_territory, *options)
        province_territory_entry.config(width=90, font=('Courier', 28))
        province_territory_entry.place(relheight=1, relwidth=1)

        #button for province_territory entry
        #I only want its command to run once, when it's clicked so I made a 
        #simple lambda that invokes the info_display function
        self.button = tk.Button(self.submit_frame, text="Web Scrape", font=('Courier', 24), bg='white', 
            command=lambda:scrape(str(province_territory_entry['text'])))
        self.button.place(relx=0.7, relheight=1, relwidth=0.3)




        #next and prev. buttons for chambers navigation
        
        
'''        #making the picture into a label
        self.previous_pic = tk.PhotoImage(file='./images/previous_pic.png')
        self.previous_pic_label = tk.Label(self.master, image=self.previous_pic)
        self.previous_pic_label.place(relwidth=0.1, relheight=0.17786, rely=0.45, relx=0.0125)

        #putting a button at the same spot as the label, essentially making it into one.
        self.previous_pic_button = tk.Button(self.master, image=self.previous_pic, 
        command=lambda:decrease_index(self.entry.get(), name, website, phone_number, address, address2, chamber_member_bool))
        self.previous_pic_button.place(relwidth=0.1, relheight=0.17786, rely=0.45, relx=0.0125)

        

        self.next_pic = tk.PhotoImage(file='./images/next_pic.png')
        self.next_pic_label = tk.Label(self.master, image=self.next_pic)
        self.next_pic_label.place(relwidth=0.1, relheight=0.17786, rely=0.45, relx=0.885) #1366/768 = 1.7786, so I set height to 
                                                                                        #this so that it'd be proportional to width.

        self.next_pic_button = tk.Button(self.master, image=self.next_pic, 
        command=lambda:increase_index(self.entry.get(), name, website, phone_number, address, address2, chamber_member_bool))
        self.next_pic_button.place(relwidth=0.1, relheight=0.17786, rely=0.45, relx=0.885) '''

        
        

if __name__ == '__main__':
    main()
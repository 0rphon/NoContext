from bs4 import BeautifulSoup
import cloudscraper
import requests
import os
from string import ascii_lowercase,digits
from subprocess import call



#checks if files exist exist and reads progress file
def previous_run_check():
    if os.path.isdir("img")==False:                                     #checks if image file exists
        os.mkdir("img")

    if os.path.isfile("progress.txt")==False:                           #if progress.txt doesnt exist
        progress=0                                                      #sets progress and found to 0
        found=0
        with open("progress.txt", "w") as handler:                      #writes progress file
            handler.write("0 0")
    else:
        with open("progress.txt", "r") as handler:                      #if progress.txt exists
            found, progress=handler.read().split("/")                   #sets found, progress to whats in file

    return int(found), int(progress)                                    #returns found, progress



#gets image url or returns false if image removed
def get_img_url(scraper, image_id):
    url = "https://prnt.sc/"+image_id                                           #puts together url
    page = scraper.get(url).text                                                #gets html
    soup = BeautifulSoup(page, "lxml")                                          #soups html
    img_url = soup.find("img", {"class": "no-click screenshot-image"})["src"]   #finds img_url
    if "https" in img_url: return img_url                                       #if valid url returns url
    else: return False                                                          #else returns false



def main():
    scraper = cloudscraper.create_scraper()                                                     #creates cloudscraper obj
    found, progress=previous_run_check()                                                        #gets found, progress and checks if img dir exists
    attempts=0
    charset = ascii_lowercase+digits                                                            #creates charset
    for a in charset:
        for b in charset:
            for c in charset:
                for d in charset:
                    for e in charset:
                        for f in charset:
                            attempts+=1                                                         #incs attempts
                            if attempts<progress: pass                                          #if attempts less than last progress then passes
                            else:                                                               
                                img_id = a+b+c+d+e+f                                            #creates img_id
                                img_url = get_img_url(scraper, img_id)                          #gets img_url
                                if img_url!=False:                                              #if valid url
                                    found+=1                                                    #incs found
                                    img_data = requests.get(img_url).content                    #gets img_data
                                    with open("img\\"+img_id+".png", "wb") as handler:          #writes img data
                                        handler.write(img_data)
                                with open("progress.txt", "w") as handler:                      #updates progress.txt
                                    string=str(found)+"/"+str(attempts)
                                    handler.write(string)

                                call("cls",shell=True)                                          #displays progress
                                print(img_id+"\nSuccess: "+str(found)+"/"+str(attempts))        
                            



if __name__=="__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()              
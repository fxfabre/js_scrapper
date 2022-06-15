# Get the number of results from a google search

Exploration project to get the number of results from a google search <br />
if you search for `Talentsoft` in [google.com](https://www.google.com/search?q=Talentsoft), 
you should see something like :  
- In french : "Environ 1 310 000 résultats (0,67 secondes)"  
- In english : "About 1,230,000 results (0.54 seconds)"  

This project uses :  
- [selenium](https://github.com/SeleniumHQ/selenium/tree/trunk/py/selenium)  
- [Beautifulsoup](https://pypi.org/project/beautifulsoup4/)  

Launch file `main.py` for a working example <br />
I added some `sleep()` to avoid being blocked by Google <br />
Look at the Dockerfile & docker-compose.yml to have installation instruction or 
to launch a notebook with dependencies already installed

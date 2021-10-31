# Shopping Cart  
A simple E-commerce website using Flask.
  
## Dependencies ##
1. Python3
2. Flask
3. cx_Oracle

## How to run ##
1. Change password in `config.py` file to your database password
2. Set up database by running `database.py` or `db.sql`
3. Run `main.py` or `app.py` (both files have exactly same code)
4. Enter `localhost:5000` in the browser.


# Acknowledgement:
This is not a coompletely original code. I took the starting code from `https://github.com/HarshShah1997/Shopping-Cart` and its explanation can be checked at `https://preettheman.medium.com/lets-build-an-e-commerce-website-with-python-flask-7361d608d171`. If you are unable to open this explanation due to no subscription, copy paste the link in icognito window to view it. He has used the sqlite3 as the backend database. But he also uploaded the database.db (sqlite database file) to the repository. So I was able to view the database tables and their rows and columns. I exported the database as a sql file using a software named `DB Browser`. Then I converted the commands written in the sql file to Oracle commands using `https://www.sqlines.com/online` and put them as a python file named `database.py`.
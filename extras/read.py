import csv
import os
import datetime
import io
import time
import MySQLdb
from pprint import pprint

def get_file_data():
    with open('/Users/emodatt08/downloads/RCBs CLEARING ACCOUNTS AND COMPANY CODES - Copy.csv', 'rb') as csvfile:
        readtrans = csv.DictReader(csvfile)
        for row in readtrans:
          company = row['COMPANY CODE']
          branches = company.replace("GH", "")
          branches_data =  branches[3] + branches[4] + branches[5] + branches[6]
          company_data =  company[2]+ company[3] + company[4] 
          address = row['COMPANY ADDRESS']
          #branch_name = row['COMPANY NAME']
          #print company_data + '  ' + branches_data + '  ' + address
          db = db_conn()

          cur = db.cursor()
          query1 = "SELECT *  from branches"
          cur.execute(query1)
          for dbdata in cur.fetchall():
              query2 = """UPDATE branches SET address = '%s' WHERE company_code = '%s' AND branch_code = '%s' """ % \
                (address, company_data, branches_data)
          result = cur.execute(query2)
          db.autocommit(True)
          pprint(query2+";")
          #write_sql(query2)

#Database connection function
def db_conn():
 return MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="",  # your password
                     db="tfbank1",
                     unix_socket="/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock")        # name of the data base
  

#Csv log writter
def write_sql(query2):
  __timestamp = datetime.datetime.now()
  __directory = os.getcwd()
  ts = time.time()
  with open(os.getcwd() +"/logs/"+ str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')) +".csv","a+") as myfile:
	myfile.write(query2)



#Function to run the process
get_file_data()


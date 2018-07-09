from flask import Flask, jsonify, request, render_template, Markup, json, session, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug import generate_password_hash, check_password_hash
from operations import logall, toJson, getdate

from flaskext.mysql import MySQL
from extras.yelp import Yelp
import random
import hashlib
import datetime
import time
from pprint import pprint
from quotes import funny_quotes


app = Flask(__name__)

app.secret_key = 'aqwertyuiop1234567890'
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'GenPay'
app.config['MYSQL_DATABASE_HOST'] = '127.0.0.1'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


@app.route("/")
def main():
	return render_template('index.html')

@app.route("/signup", methods=['GET'])
def getSignup():
	return render_template('signup.html')


@app.route('/userHome')
def userHome():
    return render_template('userHome.html')


@app.route("/signin", methods=['GET'])
def getSignin():
	return render_template('signin.html')

@app.route("/signin", methods=['POST'])
def signin():
     try:
        __username = request.form['inputName']
        __useremail = request.form['inputEmail']
        __userpassword = request.form['inputPassword']
        __hashed_password = hashlib.sha256(__userpassword).hexdigest()
        if __username and __useremail and __userpassword:
            sql1 = "SELECT * FROM wish_user WHERE username = '"+ __username + "' AND password = '"+ __hashed_password +"'"
            #pprint(sql1)
            if cursor.execute(sql1) > 1: 
                #pprint(cursor.execute(sql1))
                getdata=cursor.fetchone()
                return json.dumps({"username":getdata[1],"data":"This user exists"})
            else:
                sql = """INSERT IGNORE INTO wish_user(username, email, password, created_at) VALUES ('%s', '%s', '%s', '%s')""" % \
                (__username, __useremail, __hashed_password, getdate())

   

        if cursor.execute(sql):
            datas = {"username":__username, "email":__useremail, "password":__userpassword,"hashed password":__hashed_password}
            req_data= []
            getdata=cursor.fetchone()
            logall(str(cursor.execute(sql)),"RESPONSE", 1, json.dumps({"data":datas}))
            conn.commit()
            return json.dumps({'success': 'signup was successful',"username":getdata[1]})
        else:
            conn.rollback()
            return json.dumps({'error': 'Something went wrong'})
    


     except Exception as e:
        return json.dumps({'error':str(e)})
     

		#if __username and __useremail and __userpassword:
			#cursor.callproc('sp_createuser', (__username, __useremail,__hashed_password))
			#_data1 = cursor.fetchall()
			#if len(_data1) is 0:
				#conn.commit()
				#return json.dumps({'message':"Successful signup", 'password': __hashed_password})
			#else:
				#return json.dumps({'error': 'An error occured: ' + str(_data1[0])})	



@app.route("/validate", methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password =  hashlib.sha256(request.form['inputPassword']).hexdigest()
 
 
 
        # connect to mysql
 
        con = mysql.connect()
        cursor = con.cursor()
        sql = "SELECT * FROM wish_user WHERE email = '%s' AND password = '%s' " % (_username, _password)
        cursor.execute(sql)
        data = cursor.fetchall()
        req_data= []
        datas = {'user': _username,'pass': _password}

        logall(data,"REQUEST", 1, toJson(req_data.append(datas)))

        if len(data) > 0:
            for datas in data:
                uname =  datas[1] 
                session['user'] = uname
                return render_template('userHome.html', user = uname)
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.' + str(len(data)))
 
 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()
	





@app.route("/api/funny")
def serve_funny_quote():
	quotes = funny_quotes()
	nr_of_quotes = len(quotes)
	selected_quote = quotes[random.randint(0, nr_of_quotes - 1)]
	return jsonify(quotes)



@app.route('/showWish')
def showAddWish():
    return render_template('addWish.html')






@app.route("/addWish", methods=['POST'])
def addwish():
    try:
        if session.get('user'):
            __title = request.form['inputTitle'] 
            __desc = request.form['inputDescription']
            __user = session.get('user')
            __timestamp = datetime.datetime.now()

            
            sql = "INSERT INTO wishes(wish_title, wish_description,wish_user,time_posted) VALUES ('%s', '%s', '%s', '%s')" % \
            (__title,  __desc, __user, __timestamp)
            conn = mysql.connect()
            cursor =conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            datas = {__title,__desc,__user,__timestamp}
            req_data =[]
            logall(data,"REQUEST", 1, toJson(req_data.append(datas)))

            if len(data) is 0:
                conn.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html', error = "something went wrong")
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/getWish', methods =['GET'])
def getWish():
    try:
        if session.get('user'):
            __user = session.get('user')
            querystring="SELECT * FROM wishes WHERE wish_user = '%s'" % ( __user)
            con = mysql.connect()
            cursor = con.cursor()
           
            cursor.execute(querystring) 
            allWishes = cursor.fetchall()
            wishes_dict = []
            logall(allWishes,"REQUEST", 1, __user)
            for wish in allWishes:
                wish_dict = {
                         'Id': wish[0],
                        'Title': wish[1],
                        'Description':wish[2],
                        'Date': wish[4]}
                wishes_dict.append(wish_dict)
                
            return json.dumps(wishes_dict)
        else: 
            return json.dumps({'status':'unauthorised Access'})
    except Exception as e:
            return json.dumps({'status':str(e)})



    







@app.route("/api/<int:post_id>")
def get_user(post_id):
	return 'Your age is %d' % post_id


@app.route("/getWishById", methods = ['POST'])
def getOneWish():
    try:
        if session.get('user'):
            __id = request.form['id']
            user = session.get('user')
            query = "SELECT * FROM wishes where wish_id = '%s'" % (__id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
            all_data = []
            req_data = []
            for datas in data:
                res_data = {

            'Id': datas[0],
            'Title': datas[1],
            'Description' : datas[2],
            'Time':datas[4]}
            #logall(data,"REQUEST", 1, req_data.append(__id))
            return json.dumps(res_data)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps(str(e))


@app.route("/updateWish", methods=['POST'])
def updateWish():
    try:
        if session.get('user'):
            __title = request.form['Title']
            __description = request.form['Description']
            __id = request.form['Id']
               
            querystring ="Update wish_table SET wish_title = '"+__title +"' AND wish_description ='"+__description +"' WHERE wish_id = '"+__id+"'"
            #querystring = "SELECT * from wish_table WHERE wish_id= '%s'" % (_id)



            conn =mysql.connect()
            cursor = conn.cursor()
            check = cursor.execute(querystring)
            search = cursor.fetchall()
            if check is 1:
                return json.dumps({'status':'OK'})
            else: 
                return json.dumps({"something went wrong"})
    except Exception as e:
            return json.dumps({"status": str(e)})





@app.route("/api/register", methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		return serve_funny_quote()

	else:
		return "not worth it"


@app.route('/hello/', methods=['GET'])
def home():
	return render_template('hello.html')

@app.route('/sign', methods=['POST'])
def signup():
    if request.method == 'POST':
    	 __user = Markup(request.form['user_name']).striptags()
         __email = request.form['user_email']
         __password= hashlib.sha512(request.form['user_password'])
         __age= request.form['user_age']
         __filename = request.files['user_pic']
         __filename.save('static/var/www/uploads/' + secure_filename(__filename.filename))
         return render_template('hello.html', username = __user, email = __email, password = __password, image =  secure_filename(__filename.filename))
        

@app.route('/api/v1/save', methods=['GET','POST'])
def insertsign():
    try:
        #__user = Markup(request.json['username']).striptags()
        __email = request.json['email']
        __first_name = request.json['first_name']
        __last_name = request.json['last_name']
        __password = request.json['password']
        query = """INSERT INTO user(first_name, last_name, email, password)VALUES('%s', '%s', '%s', '%s')""" % \
            (__first_name,  __last_name, __email, __password)
        pprint(query)

        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute(query)
        conn.commit()
        data = cursor.fetchall()
        datas = {__first_name,  __last_name, __email, __password}
        req_data =[]
        logall(data,"REQUEST", 1, toJson(req_data.append(datas)))
        if cursor.execute(query):
            return jsonify({"responseCode":"000", "responseMsg":"Data stored!!", "data": req_data.append(datas)})
        else: 
            return jsonify({"something went wrong"})
    except Exception as e:
            return jsonify({"status": str(e)})

@app.route("/api/v1/users", methods = ['GET'])
def getAllUsers():
    try:
        #__id = request.form['id']
        query = "SELECT * FROM user LIMIT 0, 18"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        all_data = {}
        req_data = []
        for datas in data:
            datas = {

            'first_name': datas[1],
            'age': datas[0],
            'email' : datas[3],
            'last_name':datas[2]}
            req_data.append(datas)
            #logall(data,"REQUEST", 1, req_data.append(__id))
        
        return jsonify({"responseCode":"000", "responseMsg":"Success", "data": req_data})
        
    except Exception as e:
        return json.dumps(str(e))


#endpoint to retrieve all hotels 
@app.route("/api/v1/hotels", methods = ['GET'])
def getHotels():
    try:
        #__id = request.form['id']
        query = "SELECT * FROM hotels LIMIT 0, 18"
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        all_data = {}
        req_data = []
        for datas in data:
            datas = {

            'hotel_name': datas[1],
            'hotel_address': datas[2],
            'hotel_location' : datas[3],
            'hotel_category' : datas[4]
            }
            req_data.append(datas)
            #logall(data,"REQUEST", 1, req_data.append(__id))
        
        return jsonify({"responseCode":"000", "responseMsg":"Success", "data": req_data})
        
    except Exception as e:
        return json.dumps(str(e))

#endpoint to add a hotel 
@app.route('/api/v1/hotels', methods=['POST'])
def inserthotel():
    try:
        request_json     = request.get_json()
        #__user = Markup(request.json['username']).striptags()
        __hotel_name = request_json.get('hotel_name')
        __hotel_address = request_json.get('hotel_address')
        __hotel_location = request_json.get('hotel_location')
        __hotel_category = request_json.get('hotel_category')
        query = """INSERT INTO hotels(hotel_name, hotel_address, hotel_location, hotel_category)VALUES('%s', '%s', '%s', '%s')""" % \
            (__hotel_name,  __hotel_address, __hotel_location, __hotel_category)
        

        conn = mysql.connect()
        cursor =conn.cursor()
        cursor.execute(query)
        conn.commit()
        data = cursor.fetchall()
        datas = {__hotel_name,  __hotel_address, __hotel_location, __hotel_category}
        req_data =[]
        #logall(data,"REQUEST", 1, toJson(req_data.append(datas)))
        if cursor.execute(query):
            return jsonify({"responseCode":"000", "responseMsg":"Data stored!!", "data": req_data.append(datas)})
        else: 
            return jsonify({"responseCode":"777"})
    except Exception as e:
            return jsonify({"status": str(e)})

#endpoint to retrieve YELP Businesses 
@app.route('/api/v1/businesses', methods=['GET'])
def getBusinesses():
    data = []
    req_data = []
    position = request.args.get
    yelp = Yelp()
    details = json.loads(yelp.getBusinesses(position))
    
    for datas in details['businesses']:
        #pprint(datas)
        datas = {
            'name': datas['name'],
            'image_url': datas['image_url'],
            'review_count' : datas['review_count'],
            'rating' : datas['rating'],
            'distance': datas['distance'],
            'longitude': datas['coordinates']['longitude'],
            'latitude': datas['coordinates']['latitude'],
            'display_address' : datas['location']['display_address']
            }
        req_data.append(datas)
         
    return jsonify({"responseCode":"000", "responseMsg":"Success", "businesses": req_data})



#endpoint to retrieve TEDX Talks 
@app.route('/api/v1/talks', methods=['GET'])
def getTalks():
    data = []
    req_data = []
    position = request.args.get
    rssdata = Yelp()
    details = json.loads(rssdata.rss())
    return details   
    #return jsonify({"responseCode":"000", "responseMsg":"Success", "businesses": details})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response



if __name__ == "__main__":
	app.run(debug =True)


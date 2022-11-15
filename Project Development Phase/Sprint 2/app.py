from dotenv import load_dotenv
from flask import Flask,render_template,request,session, redirect,url_for
from flask_session import Session
import ibm_db
import os

load_dotenv()

app = Flask(__name__)
app.config['SESSION_TYPE']= 'filesystem'
Session(app)
app.secret_key= os.getenv("SECRET_KEY")

#Cloud COnnection values
database_name = os.getenv("DATABASE")
host_name = os.getenv("HOSTNAME")
port = os.getenv("PORT")
uid = os.getenv("UID")
password = os.getenv("PASSWORD")

try:
    conn = ibm_db.connect(
        f"DATABASE={database_name};HOSTNAME={host_name};PORT={port};SECURITY=SSL;SSLServiceCertificate=DigiCertGlobalRootCA.crt;UID={uid};PWD={password}",'',''
    )
    print(conn)
    print("connection successful...")
except:
    print("Connection Failed")
    print(ibm_db.conn_error())
    

 
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/forgot')
def forgot():
    return render_template('forgotten-password.html')

@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        # conn = connection()
         try:
            sql = "INSERT INTO user_data VALUES('{}','{}','{}','{}')".format(request.form["name"],request.form["email"],request.form["phone"],request.form["password"])
            ibm_db.exec_immediate(conn,sql)
            print('success')
            #flash("successfully Registered !")
            return render_template('login.html')
         except:
            #flash("Account already exists! ")
            print("fail")
            return render_template('signup.html')
    else:
            return render_template('signup.html')
        # name = request.form['name']
         #email = request.form['email']
         #phone = request.form['phone']
         #password = request.form['password']
        
         #sql ="INSERT INTO users VALUES (?,?,?,?)"
         #stmt = ibm_db.prepare(conn,sql)
         #ibm_db.bind_param(stmt, 1, name)
         #ibm_db.bind_param(stmt, 2, email)
         #ibm_db.bind_param(stmt, 3, phone)
         #ibm_db.bind_param(stmt, 4, password)
         #ibm_db.execute(stmt)
   # return render_template('signup.html')

@app.route('/login', methods=['POST','GET'])
def login():
     if request.method == 'POST':
       # conn =connection()
        email = request.form["email"]
        password = request.form["password"]
        sql = "SELECT COUNT(*) FROM user_data WHERE EMAIL=? AND PASSWORD=?"
        stmt = ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        res = ibm_db.fetch_assoc(stmt)
        if res['1'] == 1:
            session['loggedin'] = True
            session['email'] = email
            return render_template('userpage.html')
        else:
            #flash("email/ Password isincorrect! ")
            return render_template('login.html')
     else:
            return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))

        #email = request.form['email']
        #password = request.form['password']
  

        #sql = "SELECT * FROM users WHERE email=%s AND password=%s"
        #stmt = ibm_db.prepare(conn, sql)
        #ibm_db.bind_param(stmt,1,email)
        #ibm_db.bind_param(stmt,2,password)
       # user = ibm_db.execute(stmt).fetchone()
        
  #    return render_template('login.html' ,msg="success")

if __name__=='__main__':
    app.run(debug=True)

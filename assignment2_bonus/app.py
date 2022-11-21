from flask import Flask, redirect, render_template, request, url_for, session
import psycopg2
from sqlalchemy import create_engine, text

con = psycopg2.connect(database="testdata", user="postgres", password="12345", host="127.0.0.1", port="5432")

engine = create_engine("postgresql+psycopg2://postgres:12345@localhost/testdata", echo=False)
app = Flask(__name__, template_folder='template', static_folder='static')
app.secret_key = "12345"



@app.route('/')
def main():
     return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != '12345':
            error = 'Invalid Data. Please try again.'
        else:
            return redirect('/home')
    return render_template('login.html', error=error)

@app.route('/home', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
    if request.form['action'] == 'User':
      return redirect('/user')
    elif request.form['action'] == 'Disease':
      return redirect('/disease')
    elif request.form['action'] == 'Data':
      return redirect('/record')
    elif request.form['action'] == 'Query':
      return redirect('/query')
  return render_template('home.html')

@app.route('/query', methods=['GET','POST'])
def query():
   if request.method == 'GET':
      return render_template("getquery.html")
   if request.method == 'POST':
    query = request.form['query']
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(query)
    data = cur.fetchall()
    return render_template('showquery.html', user = data, query=query)

@app.route('/user')
def users():  
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM Users ")
    usersdata = cursor.fetchall()
    cursor.execute("SELECT * FROM Doctor ")
    doctordata = cursor.fetchall()
    cursor.execute("SELECT * FROM PublicServant ")
    pservantdata = cursor.fetchall()
    return render_template("userinfo.html", usersdata = usersdata, doctordata=doctordata, pservantdata=pservantdata)

@app.route('/searchuser', methods=['GET','POST'])
def searchuser():
   if request.method == 'GET':
      return render_template("get.html", user = {})
   if request.method == 'POST':
    email = request.form['email']
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Users WHERE email = '{0}'".format(email))
    usersdata = cur.fetchall()
    return render_template('show.html', user = usersdata[0])

@app.route('/disease')
def disease():  
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM Disease ")
    diseasedata = cursor.fetchall()
    cursor.execute("SELECT * FROM DiseaseType ")
    dtypedata = cursor.fetchall()
    cursor.execute("SELECT * FROM Discover ")
    discoverdata = cursor.fetchall()
    return render_template("disease.html", diseasedata = diseasedata, dtypedata=dtypedata, discoverdata=discoverdata)

@app.route('/searchdis', methods=['GET','POST'])
def searchdis():
   if request.method == 'GET':
      return render_template("getdis.html", user = {})
   if request.method == 'POST':
    disease_code = request.form['disease_code']
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Disease WHERE disease_code = '{0}'".format(disease_code))
    disdata = cur.fetchall()
    return render_template('showquery.html', user = disdata)

@app.route('/record')
def record():  
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT * FROM Record ")
    recorddata = cursor.fetchall()
    cursor.execute("SELECT * FROM Specialize ")
    specializedata = cursor.fetchall()
    cursor.execute("SELECT * FROM Country ")
    countrydata = cursor.fetchall()
    return render_template("rec.html", recorddata =  recorddata, specializedata=specializedata, countrydata=countrydata)

@app.route('/searchrec', methods=['GET','POST'])
def searchrec():
   if request.method == 'GET':
      return render_template("getrec.html", user = {})
   if request.method == 'POST':
    email = request.form['email']
    cname = request.form['cname']
    disease_code = request.form['disease_code']
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Record WHERE email = '{a}'  AND cname = '{b}' AND disease_code = '{c}'".format(**{'a':email, 'b':cname, 'c':disease_code}))
    disdata = cur.fetchall()
    return render_template('showrec.html', user = disdata[0])

@app.route('/createuser', methods=['GET','POST'])
def createuser():
   if request.method == 'GET':
      return render_template("createuser.html", user = {})
   cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
    email = request.form['email']
    name = request.form['name']
    surname = request.form['surname']
    salary = int(request.form['salary'])
    phone = request.form['phone']
    cname = request.form['cname']
    sql = ('''INSERT INTO Users (email, name, surname, salary, phone, cname) VALUES (%s,%s,%s, %s,%s,%s) ''')
    val = (email,name, surname, salary, phone, cname)
    cursor.execute(sql,val)
    con.commit()
    return redirect('/user')

@app.route('/createdtype', methods=['GET','POST'])
def createdtype():
   if request.method == 'GET':
      return render_template("createdtype.html", dtype = {})
   cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
    id = int(request.form['id'])
    description = request.form['description']
    sql = ('''INSERT INTO DiseaseType (id, description) VALUES (%s,%s) ''')
    val = (id, description)
    cursor.execute(sql,val)
    con.commit()
    return redirect('/disease')

@app.route('/createdis', methods=['GET','POST'])
def createdis():
   if request.method == 'GET':
      return render_template("createdis.html", dis = {})
   cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
    disease_code = request.form['disease_code']
    pathogen = request.form['pathogen']
    description = request.form['description']
    id = int(request.form['id'])
    sql = ('''INSERT INTO Disease (disease_code, pathogen, description, id) VALUES (%s,%s,%s,%s) ''')
    val = (disease_code, pathogen, description, id)
    cursor.execute(sql,val)
    con.commit()
    return redirect('/disease')

@app.route('/creatediscover', methods=['GET','POST'])
def creatediscover():
   if request.method == 'GET':
      return render_template("creatediscover.html", dis = {})
   cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
    cname = request.form['cname']
    disease_code = request.form['disease_code']
    first_enc_date = request.form['first_enc_date']
    sql = ('''INSERT INTO Discover (cname, disease_code, first_enc_date) VALUES (%s,%s,%s) ''')
    val = (cname, disease_code, first_enc_date)
    cursor.execute(sql,val)
    con.commit()
    return redirect('/disease')

@app.route('/createdoctor', methods=['GET','POST'])
def createdoctor():
   if request.method == 'GET':
      return render_template("createdoctor.html", user = {})
   cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
    email = request.form['email']
    name = request.form['name']
    surname = request.form['surname']
    salary = int(request.form['salary'])
    phone = request.form['phone']
    cname = request.form['cname']
    degree = request.form['degree']
    sql = ('''INSERT INTO Users (email, name, surname, salary, phone, cname) VALUES (%s,%s,%s, %s,%s,%s) ''')
    val = (email,name, surname, salary, phone, cname)
    cursor.execute(sql,val)
    sql = ('''INSERT INTO Doctor (email, degree) VALUES (%s,%s) ''')
    val = (email,degree)
    cursor.execute(sql,val)
    con.commit()
    return redirect('/user')

@app.route('/createservant', methods=['GET','POST'])
def createservant():
   if request.method == 'GET':
      return render_template("createservant.html", user = {})
   cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
    email = request.form['email']
    name = request.form['name']
    surname = request.form['surname']
    salary = int(request.form['salary'])
    phone = request.form['phone']
    cname = request.form['cname']
    department = request.form['department']
    sql = ('''INSERT INTO Users (email, name, surname, salary, phone, cname) VALUES (%s,%s,%s, %s,%s,%s) ''')
    val = (email,name, surname, salary, phone, cname)
    cursor.execute(sql,val)
    sql = ('''INSERT INTO PublicServant (email, department) VALUES (%s,%s) ''')
    val = (email,department)
    cursor.execute(sql,val)
    con.commit()
    return redirect('/user')

@app.route('/createrec', methods=['GET','POST'])
def createurec():
   if request.method == 'GET':
      return render_template("createrec.html", user = {})
   cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
    email = request.form['email']
    cname = request.form['cname']
    disease_code = request.form['disease_code']
    total_deaths = int(request.form['total_deaths'])
    total_patients = int(request.form['total_patients'])
    sql = ('''INSERT INTO Record (email, cname, disease_code, total_deaths, total_patients) VALUES (%s,%s,%s,%s,%s) ''')
    val = (email,cname, disease_code, total_deaths, total_patients)
    cursor.execute(sql,val)
    con.commit()
    return redirect('/record')

@app.route('/addcountry', methods=['GET','POST'])
def addcountry():
   if request.method == 'GET':
      return render_template("addcountry.html", user = {})
   cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
    cname = request.form['cname']
    population = int(request.form['population'])
    sql = ('''INSERT INTO Country (cname, population) VALUES (%s,%s) ''')
    val = (cname, population)
    cursor.execute(sql,val)
    con.commit()
    return redirect('/record')

@app.route('/createspec', methods=['GET','POST'])
def createuspec():
   if request.method == 'GET':
      return render_template("createspec.html", user = {})
   cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
   if request.method == 'POST':
    id = int(request.form['id'])
    email = request.form['email']
    sql = ('''INSERT INTO Specialize (id, email) VALUES (%s,%s) ''')
    val = (id,email)
    cursor.execute(sql,val)
    con.commit()
    return redirect('/record')

@app.route('/edit/<string:email>', methods = ['GET', 'POST'])
def get_user(email):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Users WHERE email = '{0}'".format(email))
    usersdata = cur.fetchall()
    # print(usersdata[0])
    return render_template('edit.html', user = usersdata[0])

@app.route('/editdoctor/<string:email>', methods = ['GET', 'POST'])
def get_doctor(email):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Users WHERE email = '{0}'".format(email))
    usersdata = cur.fetchall()
    cur.execute("SELECT degree FROM Doctor WHERE email = '{0}'".format(email))
    doctordata = cur.fetchall()
    return render_template('editdoctor.html', user = usersdata[0], doctor = doctordata[0])

@app.route('/editservant/<string:email>', methods = ['GET', 'POST'])
def get_servant(email):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Users WHERE email = '{0}'".format(email))
    usersdata = cur.fetchall()
    cur.execute("SELECT department FROM PublicServant WHERE email = '{0}'".format(email))
    servantdata = cur.fetchall()
    return render_template('editservant.html', user = usersdata[0], servant = servantdata[0])

@app.route('/editdtype/<id>', methods = ['GET', 'POST'])
def get_dtype(id):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM DiseaseType WHERE id = '{0}'".format(id))
    data = cur.fetchall()
    return render_template('editdtype.html', user = data[0])

@app.route('/editdiscover/<string:disease_code>/<string:cname>', methods = ['GET', 'POST'])
def get_discover(disease_code, cname):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Discover WHERE disease_code = '{a}' AND cname = '{b}'".format(**{'a':disease_code, 'b':cname}))
    data = cur.fetchall()
    return render_template('editdiscover.html', user = data[0])

@app.route('/editdis/<string:disease_code>', methods = ['GET', 'POST'])
def get_dis(disease_code):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Disease WHERE disease_code = '{0}'".format(disease_code))
    data = cur.fetchall()
    return render_template('editdis.html', user = data[0])

@app.route('/editrec/<string:email>/<string:cname>/<string:disease_code>', methods = ['GET', 'POST'])
def get_rec(email, cname, disease_code):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Record WHERE email = '{a}'  AND cname = '{b}' AND disease_code = '{c}'".format(**{'a':email, 'b':cname, 'c':disease_code}))
    data = cur.fetchall()
    return render_template('editrec.html', user = data[0])

@app.route('/editcountry/<string:cname>', methods = ['GET', 'POST'])
def get_country(cname):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM Country WHERE cname = '{0}'".format(cname))
    data = cur.fetchall()
    return render_template('editcountry.html', user = data[0])

@app.route('/update/<string:email>', methods=['POST'])
def update(email):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        salary = int(request.form['salary'])
        phone = request.form['phone']
        cname = request.form['cname']
        cur.execute("""
            UPDATE Users SET name = %s, surname = %s, salary = %s, phone = %s, cname = %s WHERE email = %s""", (name, surname, salary, phone, cname, email))
        con.commit()
        return redirect(url_for('users'))

@app.route('/updatedoctor/<string:email>', methods=['POST'])
def update_doctor(email):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        salary = int(request.form['salary'])
        phone = request.form['phone']
        cname = request.form['cname']
        degree = request.form['degree']
        cur.execute("""
            UPDATE Users SET name = %s, surname = %s, salary = %s, phone = %s, cname = %s WHERE email = %s""", (name, surname, salary, phone, cname, email))
        con.commit()
        cur.execute("""
            UPDATE Doctor SET degree = %s WHERE email = %s""", (degree, email))
        con.commit()
        return redirect(url_for('users'))

@app.route('/updateservant/<string:email>', methods=['POST'])
def update_servant(email):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        salary = int(request.form['salary'])
        phone = request.form['phone']
        cname = request.form['cname']
        department = request.form['department']
        cur.execute("""
            UPDATE Users SET name = %s, surname = %s, salary = %s, phone = %s, cname = %s WHERE email = %s""", (name, surname, salary, phone, cname, email))
        con.commit()
        cur.execute("""
            UPDATE PublicServant SET department = %s WHERE email = %s""", (department, email))
        con.commit()
        return redirect(url_for('users'))

@app.route('/updatedtype/<id>', methods=['POST'])
def updatedtype(id):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        description = request.form['description']
        cur.execute("""
            UPDATE DiseaseType SET description = %s WHERE id = %s""", (description, id))
        con.commit()
        return redirect(url_for('disease'))

@app.route('/updatedis/<string:disease_code>', methods=['POST'])
def updatedis(disease_code):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        pathogen = request.form['pathogen']
        description = request.form['description']
        id = int(request.form['id'])
        cur.execute("""
            UPDATE Disease SET pathogen = %s, description = %s, id = %s WHERE disease_code = %s""", (pathogen, description, id, disease_code))
        con.commit()
        return redirect(url_for('disease'))

@app.route('/updatediscover/<string:disease_code>/<string:cname>', methods=['POST'])
def updatediscover(disease_code, cname):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        first_enc_date = request.form['first_enc_date']
        cur.execute("""
            UPDATE Discover SET first_enc_date = %s WHERE disease_code = %s AND cname = %s""", (first_enc_date, disease_code, cname))
        con.commit()
        return redirect(url_for('disease'))

@app.route('/updaterec/<string:email>/<string:cname>/<string:disease_code>', methods=['POST'])
def updaterec(email, cname, disease_code):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        total_deaths = int(request.form['total_deaths'])
        total_patients = int(request.form['total_patients'])
        cur.execute("""
            UPDATE Record SET total_deaths = %s, total_patients = %s WHERE email = %s AND cname = %s AND disease_code = %s""", (total_deaths, total_patients, email, cname, disease_code))
        con.commit()
        return redirect(url_for('record'))

@app.route('/updatecountry/<string:cname>', methods=['POST'])
def updatecountry(cname):
    cur = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        population = int(request.form['population'])
        cur.execute("""
            UPDATE Country SET population = %s WHERE cname = %s""", (population, cname))
        con.commit()
        return redirect(url_for('record'))

@app.route('/delete/<string:email>', methods = ['POST','GET'])
def delete_student(email):
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("ALTER TABLE Doctor DROP CONSTRAINT doctor_email_fkey")
    cursor.execute("ALTER TABLE Doctor ADD CONSTRAINT doctor_email_fkey FOREIGN KEY (email) REFERENCES Users (email) ON DELETE CASCADE ")
    cursor.execute("ALTER TABLE PublicServant DROP CONSTRAINT publicservant_email_fkey ")
    cursor.execute("ALTER TABLE PublicServant ADD CONSTRAINT publicservant_email_fkey FOREIGN KEY (email) REFERENCES Users (email) ON DELETE CASCADE ")
    cursor.execute("ALTER TABLE Specialize DROP CONSTRAINT specialize_email_fkey ")
    cursor.execute("ALTER TABLE Specialize ADD CONSTRAINT specialize_email_fkey FOREIGN KEY (email) REFERENCES Users (email) ON DELETE CASCADE ")
    cursor.execute("ALTER TABLE Record DROP CONSTRAINT record_email_fkey ")
    cursor.execute("ALTER TABLE Record ADD CONSTRAINT record_email_fkey FOREIGN KEY (email) REFERENCES Users (email) ON DELETE CASCADE ")
    cursor.execute("DELETE FROM Users WHERE email = '{0}'".format(email))
    con.commit()
    return redirect(url_for('users'))

@app.route('/deletedtype/<id>', methods = ['POST','GET'])
def deletedtype(id):
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("ALTER TABLE Disease DROP CONSTRAINT disease_id_fkey")
    cursor.execute("ALTER TABLE Disease ADD CONSTRAINT disease_id_fkey FOREIGN KEY (id) REFERENCES DiseaseType (id) ON DELETE CASCADE ")
    cursor.execute("ALTER TABLE Discover DROP CONSTRAINT discover_disease_code_fkey")
    cursor.execute("ALTER TABLE Discover ADD CONSTRAINT discover_disease_code_fkey FOREIGN KEY (disease_code) REFERENCES Disease (disease_code) ON DELETE CASCADE ")
    cursor.execute("ALTER TABLE Record DROP CONSTRAINT record_disease_code_fkey")
    cursor.execute("ALTER TABLE Record ADD CONSTRAINT record_disease_code_fkey FOREIGN KEY (disease_code) REFERENCES Disease (disease_code) ON DELETE CASCADE ")
    cursor.execute("ALTER TABLE Specialize DROP CONSTRAINT specialize_id_fkey ")
    cursor.execute("ALTER TABLE Specialize ADD CONSTRAINT specialize_id_fkey FOREIGN KEY (id) REFERENCES DiseaseType (id) ON DELETE CASCADE ")
    cursor.execute("DELETE FROM DiseaseType WHERE id = '{0}'".format(id))
    con.commit()
    return redirect(url_for('disease'))

@app.route('/deletedis/<string:disease_code>', methods = ['POST','GET'])
def deletedis(disease_code):
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("ALTER TABLE Discover DROP CONSTRAINT discover_disease_code_fkey")
    cursor.execute("ALTER TABLE Discover ADD CONSTRAINT discover_disease_code_fkey FOREIGN KEY (disease_code) REFERENCES Disease (disease_code) ON DELETE CASCADE ")
    cursor.execute("ALTER TABLE Record DROP CONSTRAINT record_disease_code_fkey")
    cursor.execute("ALTER TABLE Record ADD CONSTRAINT record_disease_code_fkey FOREIGN KEY (disease_code) REFERENCES Disease (disease_code) ON DELETE CASCADE ")
    cursor.execute("DELETE FROM Disease WHERE disease_code = '{0}'".format(disease_code))
    con.commit()
    return redirect(url_for('disease'))

@app.route('/deletediscover/<string:disease_code>/<string:cname>', methods = ['POST','GET'])
def deletediscover(disease_code, cname):
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("DELETE FROM Discover WHERE disease_code = '{a}' AND cname = '{b}'".format(**{'a':disease_code, 'b':cname}))
    con.commit()
    return redirect(url_for('disease'))

@app.route('/deleterec/<string:email>/<string:cname>/<string:disease_code>', methods = ['POST','GET'])
def deleterec(email, cname, disease_code):
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("DELETE FROM Record WHERE email = '{a}'  AND cname = '{b}' AND disease_code = '{c}'".format(**{'a':email, 'b':cname, 'c':disease_code}))
    con.commit()
    return redirect(url_for('record'))

@app.route('/deletespec/<id>/<string:email>', methods = ['POST','GET'])
def deletespec(id, email):
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("DELETE FROM Specialize WHERE email = '{a}'  AND id = '{b}' ".format(**{'a':email, 'b':id}))
    con.commit()
    return redirect(url_for('record'))

@app.route('/deletecountry/<string:cname>', methods = ['POST','GET'])
def deletecountry(cname):
    cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("ALTER TABLE Discover DROP CONSTRAINT discover_cname_fkey")
    cursor.execute("ALTER TABLE Discover ADD CONSTRAINT discover_cname_fkey FOREIGN KEY (cname) REFERENCES Country (cname) ON DELETE CASCADE ")
    cursor.execute("ALTER TABLE Record DROP CONSTRAINT record_cname_fkey")
    cursor.execute("ALTER TABLE Record ADD CONSTRAINT record_cname_fkey FOREIGN KEY (cname) REFERENCES Country (cname) ON DELETE CASCADE ")
    cursor.execute("ALTER TABLE Users DROP CONSTRAINT users_cname_fkey")
    cursor.execute("ALTER TABLE Users ADD CONSTRAINT users_cname_fkey FOREIGN KEY (cname) REFERENCES Country (cname) ON DELETE CASCADE ")
    cursor.execute("DELETE FROM Country WHERE cname = '{0}' ".format(cname))
    con.commit()
    return redirect(url_for('record'))

if __name__ == "__main__":
  with app.app_context():
    app.run(debug=True)




# @app.route('/query1')
# def query():  
#     cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute("SELECT D.disease_code, D.description "
#             "FROM Disease D, Discover Y "
#             "WHERE D.disease_code = Y.disease_code "
#             "AND D.pathogen = 'bacteria' "
#             "AND EXTRACT(YEAR FROM Y.first_enc_date) < 1990 ")
#     usersdata = cursor.fetchall()
#     return render_template("index.html", usersdata = usersdata)

# @app.route('/query2')
# def query2():  
#     cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute("SELECT DISTINCT U.name, U.surname, D.degree "
#             "FROM Users U, Doctor D, Specialize S, DiseaseType T "
#             "WHERE U.email = D.email AND D.email = S.email AND S.id = T.id AND T.description != 'infectious diseases' ")
#     usersdata = cursor.fetchall()
#     return render_template("index.html", usersdata = usersdata)

# @app.route('/query3')
# def query3():  
#     cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute("SELECT U.name, U.surname, D.degree "
#             "FROM Users U, Doctor D, Specialize S, DiseaseType T "
#             "WHERE U.email = D.email AND D.email = S.email AND S.id = T.id "
#             "GROUP BY D.email, U.name, U.surname, D.degree "
#             "HAVING COUNT(T.id) > 2 ")
#     usersdata = cursor.fetchall()
#     return render_template("index.html", usersdata = usersdata)

# @app.route('/query4')
# def query4():  
#     cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute("SELECT Cou.cname, COALESCE(sal, 0) "
#             "FROM Country Cou LEFT JOIN "
#                 "(SELECT C.cname, AVG(U.salary) AS sal "
#                 "FROM (Country C LEFT JOIN Users U ON C.cname = U.cname "
#                 "LEFT JOIN Doctor D ON U.email = D.email "
#                 "LEFT JOIN Specialize S ON S.email = D.email "
#                 "LEFT JOIN DiseaseType T ON T.id = S.id) "
#             "WHERE T.description = 'virology' "
#             "GROUP BY C.cname) Tab ON Cou.cname = Tab.cname ")
#     usersdata = cursor.fetchall()
#     return render_template("index.html", usersdata = usersdata)

# @app.route('/query5')
# def query5():  
#     cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute("SELECT P.department, COUNT(DISTINCT P.email) "
#             "FROM PublicServant P, Record R "
#             "WHERE P.email = R.email AND R.disease_code = 'covid-19' "
#             "GROUP BY P.department, P.email "
#             "HAVING COUNT(R.cname) > 1 ")
#     usersdata = cursor.fetchall()
#     return render_template("index.html", usersdata = usersdata)

# @app.route('/query6')
# def query6():  
#     cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute("UPDATE Users "
#             "SET salary = salary * 2 "
#             "WHERE email = (SELECT DISTINCT R.email "
#                 "FROM PublicServant P, Record R "
#                 "WHERE P.email = R.email AND R.disease_code = 'covid-19' "
#                 "GROUP BY R.email "
#                 "HAVING COUNT(R.cname) > 3) ")
#     cursor.execute("SELECT * FROM Users ")
#     usersdata = cursor.fetchall()
#     return render_template("index.html", usersdata = usersdata)

# @app.route('/query78')
# def query78():  
#     cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute("ALTER TABLE Doctor DROP CONSTRAINT doctor_email_fkey")
#     cursor.execute("ALTER TABLE Doctor ADD CONSTRAINT doctor_email_fkey FOREIGN KEY (email) REFERENCES Users (email) ON DELETE CASCADE ")
#     cursor.execute("ALTER TABLE PublicServant DROP CONSTRAINT publicservant_email_fkey ")
#     cursor.execute("ALTER TABLE PublicServant ADD CONSTRAINT publicservant_email_fkey FOREIGN KEY (email) REFERENCES Users (email) ON DELETE CASCADE ")
#     cursor.execute("ALTER TABLE Specialize DROP CONSTRAINT specialize_email_fkey ")
#     cursor.execute("ALTER TABLE Specialize ADD CONSTRAINT specialize_email_fkey FOREIGN KEY (email) REFERENCES Users (email) ON DELETE CASCADE ")
#     cursor.execute("ALTER TABLE Record DROP CONSTRAINT record_email_fkey ")
#     cursor.execute("ALTER TABLE Record ADD CONSTRAINT record_email_fkey FOREIGN KEY (email) REFERENCES Users (email) ON DELETE CASCADE ")
#     cursor.execute("DELETE FROM Users WHERE LOWER(name) LIKE '%bek%' OR LOWER(name) LIKE '%gul%' ")
#     cursor.execute("CREATE INDEX idxpathogen ON Disease (pathogen) ")
#     cursor.execute("SELECT * FROM Users ")
#     usersdata = cursor.fetchall()
#     return render_template("index.html", usersdata = usersdata)

# @app.route('/query9')
# def query9():  
#     cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute("SELECT DISTINCT P.email, U.name, P.department "
#             "FROM PublicServant P, Users U, Record R "
#             "WHERE P.email = U.email AND R.email = P.email AND R.total_patients BETWEEN 100000 AND 999999 ")
#     cursor.execute("SELECT * FROM Users ")
#     usersdata = cursor.fetchall()
#     return render_template("index.html", usersdata = usersdata)

# @app.route('/query10')
# def query10():  
#     cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute("SELECT C.cname "
#             "FROM Country C, Record R "
#             "WHERE C.cname = R.cname "
#             "GROUP BY C.cname "
#             "ORDER BY SUM(R.total_patients) DESC "
#             "LIMIT 5 ")
#     usersdata = cursor.fetchall()
#     return render_template("index.html", usersdata = usersdata)

# @app.route('/query11')
# def query11():  
#     cursor = con.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     cursor.execute("SELECT type.description, coalesce(treated_patients, 0) as treated_patients "
#             "FROM DiseaseType type LEFT JOIN "
#                 "(SELECT T.id, SUM(R.total_patients - R.total_deaths) as treated_patients "
#                 "FROM DiseaseType T, Disease D, Record R "
#                 "WHERE D.id = T.id AND R.disease_code = D.disease_code "
#                 "GROUP BY T.id) AS sub "
#             "ON type.id = sub.id ")
#     usersdata = cursor.fetchall()
#     return render_template("index.html", usersdata = usersdata)

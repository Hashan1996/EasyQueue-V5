import app as app
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, Response
from flask_mysqldb import MySQL, MySQLdb
import bcrypt
import pickle

#mysql://b162ac8e76ea0c:78509c42@us-cdbr-east-02.cleardb.com/heroku_887dd6c2b40c1c7?reconnect=true

app = Flask(__name__)
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'us-cdbr-east-02.cleardb.com'
app.config['MYSQL_USER'] = 'b162ac8e76ea0c'
app.config['MYSQL_PASSWORD'] = '78509c42'
app.config['MYSQL_DB'] = 'heroku_887dd6c2b40c1c7'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


model = pickle.load(open('model.pkl', 'rb'))

#Home Page
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('login/login.html')



#UserLogin
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM tb_regi WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        
        if len(user) > 0:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['loggedin'] = True
                session['Fname'] = user['Fname']
                session['email'] = user['email']
                session['desig'] = user['desig']

                if session['desig'] == 'Super Admin':
                    return redirect(url_for('superadmin'))

                if session['desig'] == 'Head of Department':
                    return render_template('hod/ColBranchAdmin.html')

                if session['desig'] == 'Staff Member':
                    return redirect(url_for('staffMember'))  

            else:
                flash ("Incorrect Password or Email !", "danger")
                return render_template("login/login.html")

    else:
        return render_template("login/login.html")
                 
#Password Forgot
@app.route('/passwordForgot', methods=['GET', 'POST'])
def passwordForgot():
    if request.method == 'POST':
        inputEmail = request.form['inputEmail']
        inputPassword = request.form['inputPassword'].encode('utf-8')
        hash_password = bcrypt.hashpw(inputPassword, bcrypt.gensalt())
        inputReEnterPassword= request.form['inputReEnterPassword'].encode('utf-8')
        cursor = mysql.connection.cursor()
        cursor.execute(""" UPDATE tb_regi SET password=%s, Rpassword=%s WHERE email=%s""", (hash_password, inputReEnterPassword,inputEmail))
        flash("Password Changed Successfully", "success")
        mysql.connection.commit()
        return render_template('login/forgot_password.html')
    
    else:
         return render_template("login/forgot_password.html")

#Logout
@app.route('/logout') 
def logout(): 
    session.pop('Fname', None) 
    session.pop('email', None) 
    session.pop('desig', None) 
    return redirect(url_for('login')) 

#User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("login/register.html")
    else:
        Fname = request.form['Fname']
        Lname = request.form['Lname']
        email = request.form['email']
       
        desig = request.form['desig']
        phnNo = request.form['phnNo']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
        Rpassword = request.form['Rpassword']

         # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tb_regi WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash ("Account already exists!", "danger")
            return render_template('login/register.html')

        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tb_regi (Fname,Lname,email,desig,phnNo,password,Rpassword) VALUES (%s, %s, %s, %s, %s, %s, %s)",(Fname, Lname, email, desig, phnNo, hash_password, Rpassword,))
            mysql.connection.commit()
            session['Fname'] = Fname
            session['email'] = email
            return redirect(url_for("login"))


#superadmin page
@app.route('/superadmin', methods=['GET', 'POST'])
def superadmin():
    return render_template('superadmin/index.html')

#newBranchAllDetails page
@app.route('/newBranch', methods=['GET', 'POST'])
def newBranch():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT sa_user_id, branch_code, district_name, branch_name,branch_MobileNo FROM tb_branch") 
    if resultValue > 0:
        branchDetails = cur.fetchall()
        return render_template('superadmin/newBranch.html', branchDetails=branchDetails)
    return render_template('superadmin/newBranch.html')

#updatBranch
@app.route('/updatBranch',methods=['POST','GET'])
def updatBranch():

    if request.method == 'POST':
        inputBranchCode = request.form['inputBranchCode']
        inputBranchName = request.form['inputBranchName']
        inputBranchPhnNo = request.form['inputBranchPhnNo']
        cursor = mysql.connection.cursor()
        cursor.execute("""
               UPDATE tb_branch 
               SET branch_code=%s, branch_name=%s, branch_MobileNo =%s
               WHERE branch_code=%s
            """, (inputBranchCode, inputBranchName, inputBranchPhnNo,inputBranchCode))
        flash("Data Updated Successfully", "success")
        mysql.connection.commit()
        return redirect(url_for('newBranch'))

#HOD page       
@app.route('/headofDepartment', methods=['GET'])
def headofDepartment():
    return render_template('hod/ColBranchAdmin.html')


#newDepartmentAllDetails page
@app.route('/newDepartment', methods=['GET', 'POST'])
def newDepartment():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT hod_scsm_user_id,dp_branch_code, department_code, department_name, department_PhoneNo FROM tb_department") 
    if resultValue > 0:
        departmentDetails = cur.fetchall()
        return render_template('hod/newDepartment.html', departmentDetails=departmentDetails)
    return render_template('hod/newDepartment.html')



#updateDep
@app.route('/updateDep',methods=['POST','GET'])
def updateDep():

    if request.method == 'POST':
        inputDepartmentCode = request.form['inputDepartmentCode']
        inputDepartmentName = request.form['inputDepartmentName']
        inputDepartmentPhnNo = request.form['inputDepartmentPhnNo']
        cursor = mysql.connection.cursor()
        cursor.execute("""
               UPDATE tb_department 
               SET department_code=%s, department_name=%s, department_PhoneNo=%s
               WHERE department_code=%s
            """, (inputDepartmentCode, inputDepartmentName, inputDepartmentPhnNo,inputDepartmentCode))
        flash("Data Updated Successfully", "success")
        mysql.connection.commit()
        return redirect(url_for('newDepartment'))

#HOD New Department Save
@app.route('/departmentSave', methods=['GET', 'POST'])
def departmentSave():
    if request.method == 'GET':
        return render_template("hod/newDepartment.html")
         
    else:
        inputDepartmentCode = request.form['inputDepartmentCode']
        inputUserId = request.form['inputUserId']
        inputBranchCode = request.form['inputBranchCode']
        inputDepartmentName = request.form['inputDepartmentName']
        inputDepartmentPhnNo = request.form['inputDepartmentPhnNo']

          # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tb_department WHERE department_code = %s', (inputDepartmentCode,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash ("Deaprtment already exists!", "danger")
            return render_template('hod/newDepartment.html')

        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tb_department(department_code, hod_scsm_user_id,dp_branch_code, department_name, department_PhoneNo) VALUES (%s, %s, %s, %s, %s)",(inputDepartmentCode, inputUserId, inputBranchCode, inputDepartmentName, inputDepartmentPhnNo, ))
            mysql.connection.commit()
            session['inputDepartmentCode'] = inputDepartmentCode
            session['inputUserId'] = inputUserId
            flash ("Department save successfully!", "success")
            return redirect(url_for("newDepartment"))


#staffmember page
@app.route('/staffMember', methods=['GET', 'POST'])
def staffMember():
    return render_template('staffMember/ColBranchStaff.html')



#Customer Report Genarate page STAFF
@app.route('/customerCountDetails')
def customerCountDetails():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM tb_cusinfo") 
    if resultValue > 0:
        customerDetails = cur.fetchall()
        return render_template('staffMember/CusReport.html', customerDetails=customerDetails)


#Customer details Genarate page HOD
@app.route('/HODcustomerReportDelaits')
def HODcustomerReportDelaits():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT CusInfo_id, date,day,cus_dp_code,timeRange,TtlCus FROM tb_cusinfo WHERE cus_dp_code = 'BORELLA_WIDTH_01' ") 
    if resultValue > 0:
        customerDetailsHOD = cur.fetchall()
        return render_template('hod/HODcustomerReportDelaits.html', customerDetailsHOD=customerDetailsHOD)





#Colombo Branch Infor
@app.route('/colomboBranchInfo')
def colomboBranchInfo():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT sa_user_id, branch_code,  branch_name, branch_MobileNo FROM tb_branch WHERE district_name = 'Colombo'") 
    if resultValue > 0:
        oneBranchDetails = cur.fetchall()
        return render_template('superadmin/oneBranchInfor.html', oneBranchDetails=oneBranchDetails)

#Gampaha Branch Infor
@app.route('/gampahaBranchInfo')
def gampahaBranchInfo():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT sa_user_id, branch_code,  branch_name, branch_MobileNo FROM tb_branch WHERE district_name = 'Gampaha'") 
    if resultValue > 0:
        oneBranchDetails = cur.fetchall()
        return render_template('superadmin/oneBranchInfor.html', oneBranchDetails=oneBranchDetails)


#Staff Member Customer Details Save
@app.route('/customerDetailsSave', methods=['GET', 'POST'])
def customerDetailsSave():
    if request.method == 'GET':
        return render_template("staffMember/ColBranchStaff.html")
         
    else:
        inputuserid = request.form['inputuserid']
        inputDate = request.form['inputDate']
        inputDay = request.form['inputDay']
        inputDepCode = request.form['inputDepCode']
        inputTime = request.form['inputTime']
        intCus = request.form['intCus']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tb_cusinfo(scsm_user_id, date,day,cus_dp_code,timeRange,TtlCus) VALUES (%s, %s, %s, %s, %s, %s)",(inputuserid, inputDate, inputDay, inputDepCode, inputTime, intCus,))
        mysql.connection.commit()
        session['inputuserid'] = inputuserid
        session['inputDate'] = inputDate
        return redirect(url_for("staffMember"))


#Super Admin New Branch Save
@app.route('/branchSave', methods=['GET', 'POST'])
def branchSave():
    if request.method == 'GET':
        return render_template("superadmin/newBranch.html")
         
    else:
        inputBranchCode = request.form['inputBranchCode']
        inputUserId = request.form['inputUserId']
        inputDistrictName = request.form['inputDistrictName']
        inputBranchName = request.form['inputBranchName']
        inputBranchPhnNo = request.form['inputBranchPhnNo']

          # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tb_branch WHERE branch_code = %s', (inputBranchCode,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash ("Branch already exists!", "danger")
            return render_template('superadmin/newBranch.html')

        else:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO tb_branch(branch_code, sa_user_id,district_name, branch_name,branch_MobileNo) VALUES (%s, %s, %s, %s, %s)",(inputBranchCode, inputUserId, inputDistrictName, inputBranchName, inputBranchPhnNo, ))
            mysql.connection.commit()
            session['inputBranchCode'] = inputBranchCode
            session['inputUserId'] = inputUserId
            flash ("Branch save successfully!", "success")
            return redirect(url_for("newBranch"))






#CSV Download Button
@app.route('/csvDownload', methods=['GET', 'POST'])
def csvDownload():
    flash ("Download Successfully!", "success")
    return redirect(url_for("HODcustomerReportDelaits"))
    #return render_template('hod/HODcustomerReportDelaits.html')


#HOD Customer Cout Prediction with ML
@app.route('/predict', methods=['POST'])
def predict():
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    output = round(prediction[0], 2)

    return render_template('hod/ColBranchAdmin.html', prediction_text='{}'.format(output))



@app.route('/results', methods=['POST'])
def results():
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == "__main__":
    app.secret_key = "012#ApaAjaBoleh)(*^%"
    app.run(debug=True)

# -*- coding=utf-8 -*-
# python code from：https://github.com/orion-orion/Takeaways-Order-Sys
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import pymysql
import os
import argparse
import sys
import importlib

importlib.reload(sys)

app = Flask(__name__)
mysql_pwd = "11235813"
db_name = "appDB"
# Define global variable
username = ""
# TODO: Assignment of username variable Method 1: Global variable implementation, modified with login Method 2: Pass username to each page
userRole = ""
notFinishedNum = 0
# Directory to store uploaded files
UPLOAD_FOLDER = '/static/images/'
# A collection of file extensions that are allowed to be uploaded
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/index')
# Homepage
def indexpage():
    return render_template('index.html')


# Register
@app.route('/register', methods=['GET', 'POST'])
def registerPage():
    global username
    global userRole
    msg = ""
    if request.method == 'GET':
        return render_template('Register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        phone = request.form.get('phone')
        addr = request.form.get('addr')
        userRole = request.form.get('userRole')
        print(userRole)
        print(username)
        # Connect to the database, default database username root, password empty
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')

        if userRole == 'RESTAURANT':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT * from RESTAURANT where username = '{}' ".format(username)
            cursor.execute(sql1)
            db.commit()
            res1 = cursor.fetchall()
            num = 0
            for row in res1:
                num = num + 1
            # If the merchant already exists
            if num == 1:
                print("Failed! Merchant is registered！")
                msg = "fail1"
            else:
                sql2 = "insert into RESTAURANT (username, password, address, phone) values ('{}', '{}', '{}', '{}') ".format(username, password, addr, phone)

                try:
                    cursor.execute(sql2)
                    db.commit()
                    print("Merchant Registration Success")
                    msg = "done1"
                except ValueError as e:
                    print("--->", e)
                    print("Registration error, failed")
                    msg = "fail1"
            return render_template('Register.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'CUSTOMER':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql1 = "SELECT * from CUSTOMER where username = '{}'".format(username)
            cursor.execute(sql1)
            db.commit()
            res1 = cursor.fetchall()
            num = 0
            for row in res1:
                num = num + 1
            # If the user already exists
            if num == 1:
                print("The user is registered! Please login directly。")
                msg = "fail2"
            else:
                sql2 = "insert into CUSTOMER (username, password, address, phone) values ('{}', '{}', '{}', '{}') ".format(username, password, addr, phone)

                try:
                    cursor.execute(sql2)
                    db.commit()
                    print("Merchant Registration Success")
                    msg = "done2"
                except ValueError as e:
                    print("--->", e)
                    print("Registration error, failed")
                    msg = "fail2"
            return render_template('Register.html', messages=msg, username=username, userRole=userRole)


# Log in
@app.route('/logIn', methods=['GET', 'POST'])
def logInPage():
    global username
    global userRole
    msg = ""
    if request.method == 'GET':
        return render_template('logIn.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        userRole = request.form.get('userRole')
        print(userRole)
        print(username)
        # To connect to the database, the default database user name is root and the password is empty
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')

        if userRole == 'ADMIN':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from ADMIN where username = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # If the administrator exists and the password is correct, administrator part
            if num == 1:
                print("Login successful! Welcome admins!")
                msg = "done1"
            else:
                print("You do not have administrator rights or your login information is incorrect.")
                msg = "fail1"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'RESTAURANT':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from RESTAURANT where username = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # If the merchant exists and the password is correct, restaurant manager part
            if num == 1:
                print("Login successful! Welcome restaurant manager！")
                msg = "done2"
            else:
                print("You do not have restaurant manager rights or your login information is incorrect.")
                msg = "fail2"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

        elif userRole == 'CUSTOMER':
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "SELECT * from CUSTOMER where username = '{}' and password='{}'".format(username, password)
            cursor.execute(sql)
            db.commit()
            res = cursor.fetchall()
            num = 0
            for row in res:
                num = num + 1
            # If the user exists and the password is correct
            if num == 1:
                print("Login successful! Welcome users！")
                msg = "done3"
            else:
                print("You do not have user rights, are not registered, or your login information is incorrect.")
                msg = "fail3"
            return render_template('logIn.html', messages=msg, username=username, userRole=userRole)

# Administrator's store listing page
@app.route('/adminRestList', methods=['GET', 'POST'])
def adminRestListPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # Connecting to the database
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        #Query
        sql = "SELECT * FROM RESTAURANT"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('adminRestList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('adminRestList.html', username=username, messages=msg)
    elif request.form["action"] == "移除":
        RESTName = request.form.get('RESTName')
        # database connection
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # TODO: Click Remove and it says Remove Successful, but it's not deleted from the database.
        # delete it from DISHES table
        sql1 = "DELETE FROM DISHES WHERE restaurant = '{}'".format(RESTName)
        cursor.execute(sql1)
        db.commit()
        # delete it from the order table
        sql2 = "DELETE FROM ORDER_COMMENT WHERE restaurant = '{}'".format(RESTName)
        cursor.execute(sql2)
        db.commit()
        # delete it from cart
        sql3 = "DELETE FROM WHERE restaurant = '{}'".format(RESTName)
        cursor.execute(sql3)
        db.commit()
        # delete from the restaurant list
        sql4 = "DELETE FROM RESTAURANT WHERE username = '{}'".format(RESTName)
        cursor.execute(sql4)
        db.commit()
        print(sql4)

        msg = "delete"
        print(msg)

        return render_template('adminRestList.html', username=username, messages=msg)


# Administrator View Comments List
@app.route('/adminCommentList', methods=['GET', 'POST'])
def adminCommentPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # Connect to the database, default database username root, password empty
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # Query
        sql = "SELECT * FROM ORDER_COMMENT WHERE isFinished = 1 and text <> ''"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('adminCommentList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('adminCommentList.html', username=username, messages=msg)
    elif request.form["action"] == "Sort by rating":
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE isFinished = 1 AND text is not null Order BY c_rank"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('adminCommentList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('adminCommentList.html', username=username, messages=msg)

# Show restaurant list after user login
@app.route('/UserRestList',methods=['GET', 'POST'])
def UserRestListPage():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # Connect to the database, default database username root, password empty
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        # query
        sql = "SELECT * FROM RESTAURANT"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            return render_template('UserRestList.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('UserRestList.html', username=username, messages=msg)

#Select a merchant to enter its menu list
@app.route('/Menu',methods=['GET', 'POST'])
def menu():
    msg = ""
    global restaurant
    if request.form["action"] == "Enter":
        restaurant = request.form['restaurant']
        print(restaurant)
        msg = ""
        # database connection
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # sql to do the query
        sql = "SELECT * FROM DISHES WHERE restaurant = '%s'" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)
    elif request.form["action"] == "Signature dish":
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM DISHES WHERE restaurant = '%s' AND isSpecialty = 1" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)
    elif request.form["action"] == "Sort by sales":
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM DISHES WHERE restaurant = '%s' Order BY sales DESC" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)
    elif request.form["action"] == "Sort by price":
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM DISHES WHERE restaurant = '%s' Order BY price DESC" % restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('Menu.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('Menu.html', username=username, RESTAURANT=restaurant, messages=msg)

#View the comments relates to restaurant
@app.route('/ResComment',methods=['GET','POST'])
def resComment():
    msg = ""
    global restaurant
    if request.form["action"] == "View comments":
        restaurant = request.form['restaurant']
        print(restaurant)
        msg = ""
        # database connection
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # SQL sentence to do the query
        sql = "SELECT * FROM ORDER_COMMENT WHERE restaurant = '%s' AND isFinished = 1 AND text <> '' "% restaurant
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('ResComment.html', username=username, RESTAURANT=restaurant, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('ResComment.html', username=username, RESTAURANT=restaurant, messages=msg)

#Restuarant manager veiwing the comments(imcompleted)
@app.route('/ResCommentList', methods=['GET', 'POST'])
def ResCommentList():
    msg = ""
    # database connection
    restaurant=username
    print(restaurant)
    db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
    cursor = db.cursor()
    try:
        cursor.execute("use appDB")
    except:
        print("Error: unable to use database!")
    # query
    sql = "SELECT * FROM ORDER_COMMENT WHERE restaurant = '%s' AND isFinished = 1 AND text <> '' " % restaurant
    cursor.execute(sql)
    res = cursor.fetchall()
    # print(res)
    # print(len(res))
    if len(res) != 0:
        msg = "done"
        print(msg)
        print(len(res))
        return render_template('ResCommentList.html', username=username, RESTAURANT=restaurant, result=res,
                                   messages=msg)
    else:
        print("NULL")
        msg = "none"
    return render_template('ResCommentList.html', username=username, RESTAURANT=restaurant, messages=msg)

#turning to the 404 page
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

# cart management
@app.route('/myOrder',methods=['GET', 'POST'])
def shoppingCartPage():
    if request.method == 'GET':
        print("myOrder-->GET")
        db =  pymysql.connect(host="localhost", user="root", password=mysql_pwd, database=db_name,charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # query
        sql = "SELECT * FROM SHOPPINGCART"
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('myOrder.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('myOrder.html', username=username, messages=msg)
    elif request.form["action"] == "Add to cart":
        print("myOrder-->add to cart")
        restaurant = request.form['restaurant']
        dishname = request.form['dishname']
        price = (float)(request.form['price'])
        img_res = request.form['img_res']
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql1 = "insert into  SHOPPINGCART (username,restaurant,dishname,price,img_res) values ('{}','{}','{}',{},'{}') ".format(username,restaurant,dishname,price,img_res)
        cursor.execute(sql1)
        sql = "SELECT * FROM SHOPPINGCART"
        cursor.execute(sql)
        res = cursor.fetchall()
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('myOrder.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
        return render_template('myOrder.html', username=username, messages=msg)

    elif request.form["action"] == "Confirm":
        print("Confirm!")
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
       
        restaurant = request.form['restaurant']
        print(restaurant)
        dishname = request.form['dishname']
        price = request.form['price']
        img_res = request.form['img_res']
        mode = request.form['mode']
        print("************************************************")
        print("==*==")
        print(mode)

        if mode == 1:
            print("onsite")

        else:
            print("takeaway")
        return render_template('index.html')
    else:
        print("what is happend")
        return render_template('index.html')


# personal profile page
@app.route('/personal')
def personalPage():
    return render_template('personal.html')


# modify customer personal profile
@app.route('/ModifyPersonalInfo', methods=['GET', 'POST'])
def ModifyPersonalInfo():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPersonalInfo.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        address = request.form['address']
        phonenum = request.form['phonenum']
        # databse connection
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "Update {} SET address = '{}', phone = '{}' where username = '{}'".format(userRole, address, phonenum,
                                                                                        username)
        try:
            cursor.execute(sql)
            db.commit()
            # print("succesfully changed")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("failed")
            msg = "fail"
        return render_template('ModifyPersonalInfo.html', messages=msg, username=username)


# Modify the password
@app.route('/ModifyPassword', methods=['GET', 'POST'])
def ModifyPassword():
    msg = ""
    if request.method == 'GET':
        return render_template('ModifyPassword.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # checked two passwords is matched or not 
        if psw1 == psw2:
            # database connection
            db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "Update {} SET password = '{}' where username = '{}'".format(userRole, psw1, username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("changement made")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("failed")
                msg = "fail"
            return render_template('ModifyPassword.html', messages=msg, username=username)
        else:
            msg = "not equal"
            return render_template('ModifyPassword.html', messages=msg, username=username)

# order management(incompleted version)
@app.route('/OrderPage', methods=['GET', 'POST'])
def OrderPage():
    msg = ""
    global notFinishedNum
    if request.method == 'GET':
        msg = ""
        # database connection
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # view the orders that has not completed yet
        presql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # view more information
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s'" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('OrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "Sort by time":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY transactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "Sort by price":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "In process order":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('OrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('OrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "确认收货":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        print("received confirm")
        orderID = request.form['orderID']
        print(orderID)
        sql1 = "Update ORDER_COMMENT SET isFinished = 1, text = '' WHERE orderID = '%s' " % orderID
        print(sql1)
        cursor.execute(sql1)
        db.commit()

        sql2 = "select * from ORDER_COMMENT WHERE orderID = '%s' " % orderID
        cursor.execute(sql2)
        res1 = cursor.fetchone()
        restaurant = res1[1]
        dishname = res1[2]
        print("{} {} sales+1".format(dishname, restaurant))

        sql = "Update DISHES SET sales = sales+1 WHERE dishname = '{}' AND restaurant = '{}'" .format(dishname, restaurant)
        print(sql)
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        msg = "UpdateSucceed"
        return render_template('OrderPage.html', username=username, messages=msg)

    else:
        return render_template('OrderPage.html', username=username, messages=msg)

# comments management (incompleted version)
@app.route('/MyComments', methods=['GET', 'POST'])
def MyCommentsPage():
    msg = ""
    global notFinishedNum

    if request.method == 'GET':
        msg = ""
        # database connection
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # Check the number of unfilled and uncommented orders
        presql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' " % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # Search for additional information
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' and isFinished = 1 and text <> '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('MyComments.html', username=username, messages=msg)
    elif request.form["action"] == "Sort by time":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text is not null Order BY transactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg)
    elif request.form["action"] == "Sort by price":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text is not null Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MyComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MyComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "Order waiting for commenting":
        # Unrated orders jump to writing a review
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print("MyCommentsPage - orders with no comments: {}".format(len(res)))
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("MyCommentsPage - orders waiting for commenting - NULL")
            msg = "none"
            return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=len(res))

    else:
        return render_template('MyComments.html', username=username, messages=msg)

# post comments function(incompleted version)
@app.route('/WriteComments', methods=['GET', 'POST'])
def WriteCommentsPage():
    msg=""
    if request.method == 'GET':
        # database connection
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # view incompletd orders' detail
        # presql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0" % username
        # cursor.execute(presql)
        # res1 = cursor.fetchall()
        # notFinishedNum = len(res1)
        # view more detail
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg)
        else:
            print("WriteCommentsPage - GET - NULL")
            msg = "none"
            return render_template('WriteComments.html', username=username, messages=msg)
    elif request.form["action"] == "Sort by transaction time":
        # TODO: After sorting the display is empty and the problem of not displaying is not solved
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        print(username)
        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' Order BY transactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg)
        else:
            print("WriteCommentsPage - Sort by transaction time -NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg)
    elif request.form["action"] == "Sort by price":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 1 AND text = '' Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("WriteCommentsPage - Sort by price - NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "In process order":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 AND text = '' " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('WriteComments.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("WriteCommentsPage - Unfinished orders - NULL")
            msg = "none"
        return render_template('WriteComments.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    else:
        return render_template('WriteComments.html', username=username, messages=msg)

# write comment function（incomplete version）
@app.route('/CommentForm', methods=['GET', 'POST'])
def CommentFormPage():
    msg = ""
    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "写评论":
        orderID = request.form['orderID']
        print(orderID)
        msg = "WriteRequest"
        print(msg)
        return render_template('CommentForm.html', username=username, orderID=orderID, messages=msg)
    elif request.form["action"] == "Submit comment":
        print("Submit comment!")
        orderID = request.form.get('orderID')
        c_rank = request.form.get('rank')
        text = request.form.get('text')
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql = "Update ORDER_COMMENT SET text = '{}', c_rank = {} where orderID = '{}'".format(text, c_rank, orderID)
        print(sql)
        try:
            cursor.execute(sql)
            db.commit()
            print("successfully comment an order")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("failed")
            msg = "fail"
        return render_template('CommentForm.html', messages = msg, username=username)

#Restaurant manager view item detail
@app.route('/MerchantMenu',methods=['GET', 'POST'])
def MerchantMenu():
    msg = ""
    if request.method == 'GET':
        msg = ""
        # database connection
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # query
        sql = "SELECT * FROM DISHES WHERE restaurant = '%s'" % username

        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res) != 0:
            msg = "done"
            print(msg)
            print(len(res))
            return render_template('MerchantMenu.html', username=username, result=res, messages=msg)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantMenu.html', username=username, messages=msg)
    if request.method == 'POST':
        if request.form["action"] == "Delete this item":
            dishname = request.form.get('dishname')
            rest = request.form.get('restaurant')
            print(rest)
            db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "DELETE FROM DISHES where dishname = '{}' and restaurant = '{}'".format(dishname,rest)
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
                print("successfully removed an item")
                dmsg = "done"
            except ValueError as e:
                print("--->", e)
                print("fail to remove")
                dmsg = "fail"
            return render_template('MerchantMenu.html', dishname=dishname, rest=rest, dmessages=dmsg)
        elif request.form["action"] == "Sort by sales":
            db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")

            sql = "SELECT * FROM DISHES WHERE restaurant = '%s' Order BY sales DESC" % username
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
            print(len(res))
            if len(res):
                msg = "done"
                print(msg)
                return render_template('MerchantMenu.html',username=username, result=res, messages=msg)
            else:
                print("NULL")
                msg = "none"
            return render_template('MerchantMenu.html', username=username, messages=msg)
        elif request.form["action"] == "Sort by price":
            db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")

            sql = "SELECT * FROM DISHES WHERE restaurant = '%s' Order BY price DESC" % username
            cursor.execute(sql)
            res = cursor.fetchall()
            print(res)
            print(len(res))
            if len(res):
                msg = "done"
                print(msg)
                return render_template('MerchantMenu.html', username=username, result=res, messages=msg)
            else:
                print("NULL")
                msg = "none"
            return render_template('MerchantMenu.html', username=username,messages=msg)

#Restaurant manage modify the specific item 
@app.route('/MenuModify', methods=['GET', 'POST'])
def MenuModify():
    msg = ""

    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "Modify item info":
        dishname = request.form['dishname']#pass item name
        rest = request.form['restaurant']#pass restaurant name
        dishinfo = request.form['dishinfo']
        nutriention = request.form.get('nutriention')
        price = request.form.get('price')
        isSpecialty = request.form.get('isSpecialty')
        #imagesrc = request.form['imagesrc']
        print(dishname)
        print(isSpecialty)
        print(type(isSpecialty))
        
		
        return render_template('MenuModify.html', dishname=dishname, rest=rest, dishinfo=dishinfo, nutriention=nutriention, price=price, username=username, messages=msg,isSpecialty=isSpecialty)
    elif request.form["action"] == "Confirm modification":

        dishname = request.form.get('dishname')
        rest = request.form.get('rest')

        dishinfo = request.form['dishinfo']
        nutriention = request.form.get('nutriention')
        price = request.form.get('price')
        isSpecialty = int(request.form.get('isSpecialty'))
        f = request.files['imagesrc']
        filename = ''
		
        if f !='' and allowed_file(f.filename):
            filename = secure_filename(f.filename)
			
        if filename != '':
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename
		
		
        print(isSpecialty)
        print(type(isSpecialty))
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        if filename == '':
            sql = "Update DISHES SET dishinfo = '{}', nutriention = '{}', price = {} , isSpecialty = {} where dishname = '{}' and restaurant = '{}'".format(dishinfo,nutriention,price,isSpecialty,dishname,rest)
        else:
            sql = "Update DISHES SET dishinfo = '{}', nutriention = '{}', price = {} ,imgsrc = '{}', isSpecialty = {} where dishname = '{}' and restaurant = '{}'".format(dishinfo,nutriention,price,imgsrc,isSpecialty,dishname,rest)
        print(sql)
		
        try:
            cursor.execute(sql)
            db.commit()
            print("Item info changed")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("fail to editing")
            msg = "fail"
        return render_template('MenuModify.html',dishname=dishname, rest=rest, username=username, messages=msg) 
 
 
#function to add new item to the menu 
@app.route('/MenuAdd',methods=['GET','POST'])
def MenuAdd():
    msg = ""
    rest= ""
    print(request.method)
    # print(request.form["action"])
    if request.form["action"] == "Add new item":
        rest = request.form['restaurant']#pass restaurant name
        return render_template('MenuAdd.html',rest=rest)
    elif request.form["action"] == "New item confirm":
        dishname = request.form.get('dishname')
        rest = request.form.get('rest')
        dishinfo = request.form.get('dishinfo')
        nutriention = request.form.get('nutriention')
        price = request.form.get('price')
        f = request.files['imagesrc']
        print(f)
        isSpecialty = int(request.form.get('isSpecialty'))
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')

        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        sql1 = "SELECT * from DISHES where dishname = '{}' ".format(dishname)
        cursor.execute(sql1)
        db.commit()
        res1 = cursor.fetchall()
        num = 0
        for row in res1:
            num = num + 1
        # if it has already exist
        if num == 1:
            print("failed")
            msg = "fail1"
        else:
            sql2 = "insert into DISHES  values ('{}', '{}','{}', '{}',{}, {},'{}', {}) ".format(dishname,rest,dishinfo,nutriention,price,0,imgsrc,isSpecialty)
            print(sql2)
            try:
                cursor.execute(sql2)
                db.commit()
                print("successfully adding")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("failed")
                msg = "fail"
        return render_template('MenuAdd.html', messages=msg, username=username)



@app.route('/MerchantIndex')

def Merchantindexpage():
    return render_template('MerchantIndex.html')


# restaurant manager page
@app.route('/MerchantPersonal')
def MpersonalPage():
    return render_template('MerchantPersonal.html')


# Restaurant manager profile modification function
@app.route('/MerchantModifyPerInfo', methods=['GET', 'POST'])
def MerchantModifyPerInfo():
    msg = ""
    if request.method == 'GET':
        return render_template('MerchantModifyPerInfo.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        address = request.form['address']
        phonenum = request.form['phonenum']
		
        f = request.files['imagesrc']
        filename = ''
		
        if f !='' and allowed_file(f.filename):
            filename = secure_filename(f.filename)
			
        if filename != '':
            f.save('static/images/' + filename)
        imgsrc = 'static/images/' + filename
		
		
		
        # Connect to the database, default database username root, password empty
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
			
        if filename == '':	
            sql = "Update {} SET address = '{}', phone = '{}' where username = '{}'".format(userRole, address, phonenum,
                                                                                        username)
        else:
            sql = "Update {} SET address = '{}', phone = '{}',img_res = '{}' where username = '{}'".format(userRole, address, phonenum, imgsrc,
                                                                                        username)
        try:
            cursor.execute(sql)
            db.commit()
            print("Modify personal information successfully")
            msg = "done"
        except ValueError as e:
            print("--->", e)
            print("Failure to modify personal information")
            msg = "fail"
        return render_template('MerchantModifyPerInfo.html', messages=msg, username=username)


# Modify previous password
@app.route('/MerchantModifyPwd', methods=['GET', 'POST'])
def MerModifyPassword():
    msg = ""
    if request.method == 'GET':
        return render_template('MerchantModifyPwd.html', username=username)
    if request.method == 'POST':
        # username = request.form['username']
        psw1 = request.form['psw1']
        psw2 = request.form['psw2']
        # Check whether the two passwords are the same
        if psw1 == psw2:
            # To connect to the database, the default database user name is root and the password is empty
            db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
            cursor = db.cursor()
            try:
                cursor.execute("use appDB")
            except:
                print("Error: unable to use database!")
            sql = "Update {} SET password = '{}' where username = '{}'".format(userRole, psw1, username)
            try:
                cursor.execute(sql)
                db.commit()
                # print("Sucessfully changed")
                msg = "done"
            except ValueError as e:
                print("--->", e)
                print("Changement failed")
                msg = "fail"
            return render_template('MerchantModifyPwd.html', messages=msg, username=username)
        else:
            msg = "not equal"
            return render_template('MerchantModifyPwd.html', messages=msg, username=username)

#restaurant manager view the order
@app.route('/MerchantOrderPage', methods=['GET', 'POST'])
def MerchantOrderPage():
    msg = ""
    global notFinishedNum
    if request.method == 'GET':
        msg = ""
        # database connection
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")
        # view incompeleted orders
        presql = "SELECT * FROM ORDER_COMMENT WHERE restaurant = '%s' AND isFinished = 0" % username
        cursor.execute(presql)
        res1 = cursor.fetchall()
        notFinishedNum = len(res1)
        # view other info
        sql = "SELECT * FROM ORDER_COMMENT WHERE restaurant = '%s'" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        # print(res)
        # print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
            return render_template('MerchantOrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "Sort by time":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY transactiontime DESC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg)
    elif request.form["action"] == "Sort by price":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' Order BY cost ASC" % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=notFinishedNum)
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    elif request.form["action"] == "In process order":
        db = pymysql.connect(host="localhost", user="root", password=mysql_pwd, db=db_name, charset='utf8')
        cursor = db.cursor()
        try:
            cursor.execute("use appDB")
        except:
            print("Error: unable to use database!")

        sql = "SELECT * FROM ORDER_COMMENT WHERE username = '%s' AND isFinished = 0 " % username
        cursor.execute(sql)
        res = cursor.fetchall()
        print(res)
        print(len(res))
        if len(res):
            msg = "done"
            print(msg)
            return render_template('MerchantOrderPage.html', username=username, result=res, messages=msg,
                                   notFinishedNum=len(res))
        else:
            print("NULL")
            msg = "none"
        return render_template('MerchantOrderPage.html', username=username, messages=msg, notFinishedNum=notFinishedNum)
    else:
        return render_template('MerchantOrderPage.html', username=username, messages=msg)




def parse_args():
    """parse the command line args

    Returns:
        args: a namespace object including args
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--mysql_pwd',
        help='the mysql root password',
        default="11235813"
    )
    parser.add_argument(
        '--db_name',
        help='which database to use',
        default="appDB"
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    mysql_pwd = args.mysql_pwd
    db_name = args.db_name
    app.run(host='localhost', port='9090')

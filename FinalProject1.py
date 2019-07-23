# -*- coding: utf-8 -*-
# Form implementation generated from reading ui file 'FinalProject1.ui'
# Created by: PyQt4 UI code generator 4.11.4
# WARNING! All changes made in this file will be lost!

import csv
import sys
import MySQLdb
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_LoginWindow(object):

    def printReceipt(self):
	custid= self.lineEdit_3.text()
	if custid == "":
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText("Enter the customer id")
		msg.setInformativeText("Enter correct customer id")
		msg.setWindowTitle("Customer ID not found")
		msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		retval = msg.exec_()
	else:
		fname=self.lineEdit.text()
		lname=self.lineEdit_2.text()
		db = MySQLdb.connect("localhost", "root", "sne", "testdb")
		cursor = db.cursor()
		query = "select cust_id, start_date, end_date,amount,pending_amount from cust_gym_details "
		cursor.execute(query)
		result = cursor.fetchall()
		for row_number,row_data	in enumerate(result):
			if(row_data[0] == custid):	
				startdate = row_data[1]
				enddate = row_data[2]
				amt=row_data[3]
				pendamt = row_data[4]
				strmsg = "\n\n********** BILL ********** \n\n Cust ID : " + custid + "\n First Name: " +fname + "\n Last Name: " + lname + "\n\n Start Date : " + startdate + "\n End Date : " + enddate + "\n\n Total Amount : " + amt + "\n Pending Amount : " + pendamt + "\n\n\n**************************\n"
				fo = open(custid + ".txt", "w+")
				fo.write(strmsg);
				fo.close()
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText("Receipt Printed")
		msg.setWindowTitle("SYSTEM MESSAGE")
		msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		retval = msg.exec_()
		self.lineEdit.setText("");
		self.lineEdit_2.setText("");
		self.lineEdit_3.setText("");
		self.plainTextEdit_4.setPlainText("")


    def generateBill(self):
	custid= self.lineEdit_3.text()
	if custid == "":
		msg = QMessageBox()
		msg.setIcon(QMessageBox.Information)
		msg.setText("Enter the customer id")
		msg.setInformativeText("Enter correct customer id")
		msg.setWindowTitle("Customer ID not found")
		msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		retval = msg.exec_()
	else:
		db = MySQLdb.connect("localhost", "root", "sne", "testdb")
		cursor = db.cursor()
		query = "SELECT firstname,lastname,cust_id from cust_personal "
		cursor.execute(query)
		result = cursor.fetchall()
		flag = 'False'
		rowno = 0;
		for row_number,row_data	in enumerate(result):
			if(row_data[2] == custid):
				flag = 'True'	
				rowno = row_number;
				fname = row_data[0]
				lname = row_data[1]
				self.lineEdit.setText(fname);
				self.lineEdit_2.setText(lname);
				break;
				
		if flag == 'False':
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Information)
			msg.setText("Enter the Correct Customer ID")
			msg.setWindowTitle("Customer ID not found")
			msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
			retval = msg.exec_()
		else:
			query = "select cust_id, start_date, end_date,amount from cust_gym_details "
			cursor.execute(query)
			result = cursor.fetchall()


			flag = 'False'
			for row_number,row_data	in enumerate(result):
				if(row_data[0] == custid):
					flag = 'True'	
					startdate = row_data[1]
					enddate = row_data[2]
					date1 = startdate.split("-")
					month1 = int(date1[1])
					date2 = enddate.split("-")
					month2 = int(date2[1])
					pendamt = str((month2 - month1)*500+int(row_data[3]));
					strmsg = "********** BILL ********** \n Cust ID : " + custid +"\n Start Date : " + startdate + "\n End Date : " + enddate + "\n Fees : " + pendamt + "\n**************************\n"
					self.plainTextEdit_4.setPlainText(strmsg)


    def insertBatch(self):
        bid = self.batchIdLineEdit.text()
        btime=self.batchtimeLineEdit.text()
        bstrength = self.batchstrengthLineEdit.text()
        btrainer = self.batchtrainerLineEdit.text()
     	db = MySQLdb.connect("localhost", "root", "sne", "testdb")
        cursor = db.cursor()
        try:

            cursor.execute("""INSERT INTO batch VALUES (%s,%s,%s,%s)""",
                           (bid,btime,bstrength,btrainer))

        except:
            db.rollback()
	db.commit()
	db.close()
	self.batchIdLineEdit.clear()
	self.batchtimeLineEdit.clear()
	self.batchstrengthLineEdit.clear()
	self.batchtrainerLineEdit.clear()  
 
    def showBatchData(self):
        db = MySQLdb.connect("localhost", "root", "sne", "testdb")
        cursor = db.cursor()
        query = "select * from batch"
        cursor.execute(query)
        result = cursor.fetchall()
        self.batchtable.setRowCount(0)
        if (len(result) > 0):
            for row_number, row_data in enumerate(result):
                self.batchtable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.batchtable.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(data)))
        else:
            print("error")
        db.close()

    def storedata(self):
        firstname = self.lastNameLineEdit_4.text()
        lastname = self.firstNameLineEdit_4.text()
        gender = self.genderLineEdit_4.text()
        email = self.emailLineEdit_4.text()
        dob = self.dateOfBirthLineEdit_4.text()
        occupation = self.occupationLineEdit.text()
        contact = self.contactNumberLineEdit_4.text()
        address = self.addressLineEdit_3.text()
        height = self.heightInCmLineEdit.text()
        weight = self.weightInKgLineEdit.text()
        bmi = (int(weight)*10000) / (int(height)*int(height))

        subscription= self.lastNameLineEdit_3.text()
        start_date=self.firstNameLineEdit_3.text()
        end_date=self.genderLineEdit_3.text()
        amount=self.emailLineEdit_3.text()
        amount_status=self.dateOfBirthLineEdit_3.text()
        pending_amount=self.occupationLineEdit_2.text()
        trainer=self.contactNumberLineEdit_3.text()
        cust_id=self.customerIDLineEdit.text()
        batch_id = self.customerIDLineEdit_4.text()
        
        db = MySQLdb.connect("localhost", "root", "sne", "testdb")
        cursor = db.cursor()
        try:

            cursor.execute("""INSERT INTO cust_personal VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(firstname, lastname, gender, email, dob, occupation, contact, address, height, weight,cust_id))
            cursor.execute("""INSERT INTO cust_gym_details VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)""",(subscription,start_date,end_date,amount,amount_status,pending_amount,trainer,cust_id,batch_id))
	    cursor.execute("""INSERT INTO progress VALUES(%s,%s,%s,%s,%s)""",(cust_id,start_date,height,weight,bmi))
              
        except:
            db.rollback()

        db.commit()
	db.close()
	self.lastNameLineEdit_4.clear()
	self.firstNameLineEdit_4.clear()
	self.genderLineEdit_4.clear()
	self.emailLineEdit_4.clear()
	self.dateOfBirthLineEdit_4.clear()
	self.occupationLineEdit.clear()
	self.contactNumberLineEdit_4.clear()
	self.addressLineEdit_3.clear()
	self.heightInCmLineEdit.clear()
	self.weightInKgLineEdit.clear()



	self.lastNameLineEdit_3.clear()
	self.firstNameLineEdit_3.clear()
	self.genderLineEdit_3.clear()
	self.emailLineEdit_3.clear()
	self.dateOfBirthLineEdit_3.clear()
	self.occupationLineEdit_2.clear()
	self.contactNumberLineEdit_3.clear()
	self.customerIDLineEdit.clear() 
        self.customerIDLineEdit_4.clear()              
        
    def showcustdata(self):
        db = MySQLdb.connect("localhost", "root", "sne", "testdb")
        cursor = db.cursor()
        query = "select cust_id,subscription,start_date,end_date,amount,amount_status,pending_amount,trainer from cust_gym_details"
        cursor.execute(query)
        result = cursor.fetchall()
        self.tableWidget.setRowCount(0)
        if (len(result) > 0):
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(data)))
        else:
            print("error")
        db.close()  
                         
    def resetall(self):
                   self.lastNameLineEdit_4.clear()
                   self.firstNameLineEdit_4.clear()
                   self.genderLineEdit_4.clear()
                   self.emailLineEdit_4.clear()
                   self.dateOfBirthLineEdit_4.clear()
                   self.occupationLineEdit.clear()
                   self.contactNumberLineEdit_4.clear()
                   self.addressLineEdit_3.clear()
                   self.heightInCmLineEdit.clear()
                   self.weightInKgLineEdit.clear()
                  
                   self.lastNameLineEdit_3.clear()
                   self.firstNameLineEdit_3.clear()
                   self.genderLineEdit_3.clear()
                   self.emailLineEdit_3.clear()
                   self.dateOfBirthLineEdit_3.clear()
                   self.occupationLineEdit_2.clear()
                   self.contactNumberLineEdit_3.clear()
                   self.customerIDLineEdit.clear()



    def showemp(self):
        db = MySQLdb.connect("localhost", "root", "sne", "testdb")
        cursor = db.cursor()
        query = "select * from emp"
        cursor.execute(query)
        result = cursor.fetchall()
        self.tableWidget_4.setRowCount(0)
        if (len(result) > 0):
            for row_number, row_data in enumerate(result):
                self.tableWidget_4.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_4.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(data)))
        else:
            print("error")
        db.close()



    def addemp(self):
        firstname = self.lastNameLineEdit_13.text()
        lastname=self.firstNameLineEdit_13.text()
        gender = self.genderLineEdit_11.text()
        email = self.emailLineEdit_11.text()
        dob = self.dateOfBirthLineEdit_11.text()
        contact = self.contactNumberLineEdit_11.text()
        address = self.addressLineEdit_10.text()
        experience=self.newlineedit_9.text()
        db = MySQLdb.connect("localhost", "root", "sne", "testdb")
        cursor = db.cursor()
        try:
	    cursor.execute("""INSERT INTO emp VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
                           (firstname, lastname, gender, email, dob, contact, address,experience))

        except:
            db.rollback()
	db.commit()
	db.close()
	self.lastNameLineEdit_13.clear()
	self.firstNameLineEdit_13.clear()
	self.genderLineEdit_11.clear()
	self.emailLineEdit_11.clear()
	self.dateOfBirthLineEdit_11.clear()
	self.contactNumberLineEdit_11.clear()
	self.addressLineEdit_10.clear()
	self.newlineedit_9.clear()


    def showequipment(self):
        db = MySQLdb.connect("localhost", "root", "sne", "testdb")
        cursor = db.cursor()
        query = "select * from instrument"
        cursor.execute(query)
        result = cursor.fetchall()
        self.tableWidget_2.setRowCount(0)
        if (len(result) > 0):
            for row_number, row_data in enumerate(result):
                self.tableWidget_2.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_2.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(data)))
        db.close()


    def addinstrument(self):
         name=self.equipmentNameLineEdit.text()
         dateofpurchase=self.dateOfPurchaseLineEdit.text()
         cost=self.costLineEdit.text()
         quantity=self.quantityLineEdit.text()
	 db = MySQLdb.connect("localhost", "root", "sne", "testdb")
         cursor = db.cursor()
         try:
	     cursor.execute("""INSERT INTO instrument VALUES (%s,%s,%s,%s)""",
                            (name,dateofpurchase,cost,quantity))
	 except:
             db.rollback()
	 db.commit()
	 db.close()
	 self.equipmentNameLineEdit.clear()
	 self.dateOfPurchaseLineEdit.clear()
	 self.costLineEdit.clear()
	 self.quantityLineEdit.clear()


    def loadvalues(self):
	fname=self.firstNameLineEdit_6.text()
	lname=self.lastNameLineEdit_6.text()
	cust_id=""
	db = MySQLdb.connect("localhost", "root", "sne", "testdb")
	cursor = db.cursor()
	try:
	    cursor.execute("select p.cust_id,max(date) from cust_personal p inner join progress pg on p.cust_id=pg.cust_id where firstname=%s and lastname=%s group by cust_id",(fname,lname))
	    
	    result=cursor.fetchall()

	    for row_number, row_data in enumerate(result):
	     	cust_id=row_data[0]
		jd=row_data[1]
	    
	    self.customerIDLineEdit_2.setText(cust_id)
	    self.lasteDateLineEdit.setText(jd)
	except:
	                      db.rollback()
	db.commit()
	db.close()



    def addprogressfunction(self):
                      cust_id=self.customerIDLineEdit_2.text()
                      ed=self.progressEntryDateLineEdit.text()
                      ht=self.heightLineEdit.text()
                      wt=self.weightLineEdit.text()

                      if(wt!="" and ht!=""):
                                            bmi = (int(wt)*10000) / (int(ht)*int(ht))
                                            db = MySQLdb.connect("localhost", "root", "sne", "testdb")
                                            cursor = db.cursor()
                      try:
                                            cursor.execute("""INSERT INTO progress VALUES (%s,%s,%s,%s,%s)""",(cust_id,ed,ht,wt,bmi))
			
                      except:
                                            db.rollback()
                      db.commit()
                      db.close()
	 	      self.firstNameLineEdit_6.clear()
		      self.lastNameLineEdit_6.clear()
		      self.customerIDLineEdit_2.clear()
		      self.lasteDateLineEdit.clear()
		      self.progressEntryDateLineEdit.clear()
		      self.heightLineEdit.clear()
		      self.weightLineEdit.clear()



    def loadcid(self):
	fname=self.firstNameLineEdit_7.text()
	lname=self.lastNameLineEdit_7.text()
	cust_id=""

	db = MySQLdb.connect("localhost", "root", "sne", "testdb")
	cursor = db.cursor()
	try:
	    cursor.execute("select cust_id from cust_personal where firstname=%s and lastname=%s",(fname,lname))
	    result=cursor.fetchall()

	    for row_number, row_data in enumerate(result):
	     	cust_id=row_data[0]

	    self.customerIDLineEdit_3.setText(cust_id)
	except:
	    db.rollback()
	db.commit()
	db.close()



    def trackbmi(self):
	cust_id=self.customerIDLineEdit_3.text()

	db=MySQLdb.connect("localhost","root","sne","testdb")
	cursor=db.cursor()
	cursor.execute("select date,bmi from progress where cust_id='%s'"%(cust_id))
	result = cursor.fetchall()

	objects = []
	pbmi=[]
	x=[]

	for row_number, row_data in enumerate(result):
		objects.append(row_data[0])
		pbmi.append(int(row_data[1]))

	x = [dt.datetime.strptime(d,'%d-%m-%Y').date() for d in objects] 	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.xaxis_date()

	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=15))
	plt.plot(x,pbmi)
	plt.gcf().autofmt_xdate()

	for i,j in zip(x,pbmi):
    		ax.annotate('(%s, %s)' %(i,j), xy=(i,j),xytext=(i,j), textcoords='data')
	plt.ylabel('BMI')	
	plt.xlabel('DATE')
	plt.title('BMI Progress Report')
	plt.show()
	db.close()


    def trackwt(self):
	cust_id=self.customerIDLineEdit_3.text()
	db=MySQLdb.connect("localhost","root","sne","testdb")
	cursor=db.cursor()
	cursor.execute("select date,weight from progress where cust_id='%s'"%(cust_id))
	result = cursor.fetchall()
	objects = []
	pwt=[]
	x=[]
	for row_number, row_data in enumerate(result):
		objects.append(row_data[0])
		pwt.append(int(row_data[1]))
	x = [dt.datetime.strptime(d,'%d-%m-%Y').date() for d in objects] 
	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.xaxis_date()	
	
	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=15))
	plt.plot(x,pwt)
	plt.gcf().autofmt_xdate()

	for i,j in zip(x,pwt):
    		ax.annotate('(%s, %s)' %(i,j), xy=(i,j),xytext=(i,j), textcoords='data')
	plt.ylabel('WEIGHT')	
	plt.xlabel('DATE')
	plt.title('Weight Progress Report')
	plt.show()
	db.close()


    def trackht(self):
	cust_id=self.customerIDLineEdit_3.text()
	db=MySQLdb.connect("localhost","root","sne","testdb")
	cursor=db.cursor()
	cursor.execute("select date,height from progress where cust_id='%s'"%(cust_id))
	result = cursor.fetchall()

	objects = []
	pht=[]
	x=[]
	for row_number, row_data in enumerate(result):
		objects.append(row_data[0])
		pht.append(int(row_data[1]))
	x = [dt.datetime.strptime(d,'%d-%m-%Y').date() for d in objects]

	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.xaxis_date() 	

	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
	plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=15))
	plt.plot(x,pht)
	plt.gcf().autofmt_xdate()

	for i,j in zip(x,pht):
    		ax.annotate('(%s, %s)' %(i,j), xy=(i,j),xytext=(i,j), textcoords='data')
	plt.ylabel('HEIGHT')	
	plt.xlabel('Dates')
	plt.title('Height Progress Report')
	plt.show()
	db.close()


    def showprogdata(self):
        db = MySQLdb.connect("localhost", "root", "sne", "testdb")
        cursor = db.cursor()
        query = "select * from progress order by cust_id"
        cursor.execute(query)
        result = cursor.fetchall()

        self.tableWidget_3.setRowCount(0)
        if (len(result) > 0):

            for row_number, row_data in enumerate(result):
                self.tableWidget_3.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget_3.setItem(row_number, column_number, QtGui.QTableWidgetItem(str(data)))
        else:
            print("Show progress error")
        db.close()



    def getgraphofgenders(self):
	db=MySQLdb.connect("localhost","root","sne","testdb")
	cursor=db.cursor()
	cursor.execute("select gender, count(gender) from cust_personal group by gender")
	result = cursor.fetchall()
	objects = []
	number = []

	for row_number, row_data in enumerate(result):
		objects.append(row_data[0])
		number.append(int(row_data[1]))
	y_pos = np.arange(len(objects))	
	plt.bar(y_pos, number, align='center', color="blue")
	plt.xticks(y_pos, objects)
	plt.ylabel('number')	
	plt.xlabel('Gender')
	plt.show()
	db.close() 

    def getgraphofbmi(self):
	db=MySQLdb.connect("localhost","root","sne","testdb")
	cursor=db.cursor()
	cursor.execute("select weight,height from cust_personal")
	result = cursor.fetchall()

	objects = ['< 18','18-21','> 21']	
	number = [0,0,0]

	for row_number, row_data in enumerate(result):
		bmi = (int(row_data[0])*10000) / (int(row_data[1])*int(row_data[1]))
		if(bmi<18):
			number[0] = number[0] + 1
		if(bmi>21):
			number[2] = number[2] + 1
		else:
			number[1] = number[1] + 1

	y_pos = np.arange(len(objects))
	plt.bar(y_pos, number, align='center', color="blue")
	plt.xticks(y_pos, objects)
	plt.ylabel('number')	
	plt.xlabel('BMI')
	plt.show()
	db.close()     
	

    def getMonthWiseBookingGraph(self):
	db=MySQLdb.connect("localhost","root","sne","testdb")
	cursor=db.cursor()
	cursor.execute("select start_date from cust_gym_details")
	result = cursor.fetchall()

	objects = {1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0,11:0,12:0}

	for row_number, row_data in enumerate(result):
		date = row_data[0].split("-")
		month = int(date[1])
		objects[month] = objects[month] + 1
	plt.bar(range(len(objects)), objects.values(), align='center')
	plt.xticks(range(len(objects)), objects.keys())
	plt.show()
	db.close()  



    def logincheck(self):
        flag='False'
        username= self.lineEditUsername.text()
        password=self.lineEditPassword.text()
        
        with open('logindetails.csv', 'rb') as f:
                      reader = csv.reader(f)
                      for row in reader:
                                            if(row[0] == username and row[1] == password):
                                                                  flag='True'
                                                                  self.lineEditUsername.setText("")
                                                                  self.lineEditPassword.setText("")
                                                                  self.stackedWidget.setCurrentIndex(1)
                                                                  break
                      if (flag == 'False'):
                                            msg = QMessageBox()
                                            msg.setIcon(QMessageBox.Information)
                                            msg.setText("Incorrect Username and password!!!")
                                            msg.setInformativeText("Enter correct username and password.")
                                            msg.setWindowTitle("Authentication Fail!")
                                            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                                            retval = msg.exec_()
                                            
                                            

    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName(_fromUtf8("LoginWindow"))
        LoginWindow.resize(1250, 900)
        self.centralwidget = QtGui.QWidget(LoginWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.stackedWidget = QtGui.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(0, 0, 1250, 900))
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.buttonCancel = QtGui.QPushButton(self.page)
        self.buttonCancel.setGeometry(QtCore.QRect(680, 530, 99, 31))
        self.buttonCancel.setStyleSheet(_fromUtf8("background-color: rgb(111, 111, 111);\n"
"background-color: rgb(59, 119, 179);\n"
"font: 14pt \"OpenSymbol\";\n"
"color: rgb(255, 255, 255);"))
        self.buttonCancel.setObjectName(_fromUtf8("buttonCancel"))
        self.label_9 = QtGui.QLabel(self.page)
        self.label_9.setGeometry(QtCore.QRect(430, 460, 131, 41))
        self.label_9.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"font:  14pt \"Ubuntu\";\n"
"\n"
""))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_4 = QtGui.QLabel(self.page)
        self.label_4.setGeometry(QtCore.QRect(0, 0, 1261, 881))
        self.label_4.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 170, 255);"))
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setPixmap(QtGui.QPixmap(_fromUtf8("ekg-monitor.jpg")))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_2 = QtGui.QLabel(self.page)
        self.label_2.setGeometry(QtCore.QRect(320, 290, 611, 371))
        self.label_2.setStyleSheet(_fromUtf8("background-color: rgba(255,255,255,55);\n"
"border-color: rgb(44, 89, 134);"))
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_6 = QtGui.QLabel(self.page)
        self.label_6.setGeometry(QtCore.QRect(70, 150, 1121, 101))
        self.label_6.setStyleSheet(_fromUtf8("\n"
"font: 72pt \"Ubuntu\";\n"
"background-color: rgba(0, 147, 221,0);\n"
"color: rgb(255, 255, 255);"))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.username = QtGui.QLabel(self.page)
        self.username.setGeometry(QtCore.QRect(400, 430, 131, 41))
        self.username.setStyleSheet(_fromUtf8("color: rgb(255,255, 255);\n"
"font:  14pt \"Ubuntu\";\n"
"\n"
""))
        self.username.setObjectName(_fromUtf8("username"))
        self.lineEditPassword = QtGui.QLineEdit(self.page)
        self.lineEditPassword.setGeometry(QtCore.QRect(540, 480, 251, 31))
        self.lineEditPassword.setObjectName(_fromUtf8("lineEditPassword"))
        self.lineEditPassword.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEditUsername = QtGui.QLineEdit(self.page)
        self.lineEditUsername.setGeometry(QtCore.QRect(540, 430, 251, 31))
        self.lineEditUsername.setObjectName(_fromUtf8("lineEditUsername"))
        self.buttonCancel_2 = QtGui.QPushButton(self.page)
        self.buttonCancel_2.setGeometry(QtCore.QRect(690, 560, 99, 31))
        self.buttonCancel_2.setStyleSheet(_fromUtf8("background-color: rgb(111, 111, 111);\n"
"background-color: rgb(59, 119, 179);\n"
"font: 14pt \"OpenSymbol\";\n"
"color: rgb(255, 255, 255);"))
        self.buttonCancel_2.setObjectName(_fromUtf8("buttonCancel_2"))
        self.password = QtGui.QLabel(self.page)
        self.password.setGeometry(QtCore.QRect(400, 470, 131, 41))
        self.password.setStyleSheet(_fromUtf8("color: rgb(255,255, 255);\n"
"font:  14pt \"Ubuntu\";\n"
"\n"
""))
        self.password.setObjectName(_fromUtf8("password"))
        self.buttonLogin = QtGui.QPushButton(self.page)
        self.buttonLogin.setGeometry(QtCore.QRect(550, 560, 99, 31))
        self.buttonLogin.setStyleSheet(_fromUtf8("background-color: rgb(111, 111, 111);\n"
"background-color: rgb(59, 119, 179);\n"
"font: 14pt \"OpenSymbol\";\n"
"color: rgb(255, 255, 255);"))
        self.buttonLogin.setObjectName(_fromUtf8("buttonLogin"))
        self.label_5 = QtGui.QLabel(self.page)
        self.label_5.setGeometry(QtCore.QRect(560, 350, 71, 41))
        self.label_5.setStyleSheet(_fromUtf8("color: rgb(255, 255, 255);\n"
"text-decoration: underline;\n"
"font: 16pt \"OpenSymbol\";"))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.label = QtGui.QLabel(self.page_2)
        self.label.setGeometry(QtCore.QRect(0, 0, 1251, 191))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Palladio L"))
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setStyleSheet(_fromUtf8("background-color: rgb(0, 0, 106);\n"
""))
        self.label.setFrameShape(QtGui.QFrame.Box)
        self.label.setFrameShadow(QtGui.QFrame.Plain)
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("ekg-monitor.jpg")))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_12 = QtGui.QLabel(self.page_2)
        self.label_12.setGeometry(QtCore.QRect(70, 50, 301, 91))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("URW Gothic L"))
        font.setPointSize(25)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet(_fromUtf8("background-color: rgba(0, 0, 106,0);\n"
"font: 63 bold 25pt \"URW Gothic L\";\n"
""))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.logout = QtGui.QPushButton(self.page_2)
        self.logout.setGeometry(QtCore.QRect(1140, 40, 81, 31))
        self.logout.setStyleSheet(_fromUtf8("background-color: rgba(255,255,255,80);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
"border:1.5px solid white\n"
""))
        self.logout.setObjectName(_fromUtf8("logout"))
        self.label_8 = QtGui.QLabel(self.page_2)
        self.label_8.setGeometry(QtCore.QRect(980, 30, 141, 41))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.stackedWidget_3 = QtGui.QStackedWidget(self.page_2)
        self.stackedWidget_3.setGeometry(QtCore.QRect(0, 190, 1241, 681))
        self.stackedWidget_3.setObjectName(_fromUtf8("stackedWidget_3"))
        self.BatchesPage = QtGui.QWidget()
        self.BatchesPage.setObjectName(_fromUtf8("BatchesPage"))
        self.BatchesWidget = QtGui.QTabWidget(self.BatchesPage)
        self.BatchesWidget.setGeometry(QtCore.QRect(0, 0, 1251, 691))
        self.BatchesWidget.setStyleSheet(_fromUtf8("color: rgb(0, 0, 106);\n"
"background-color: rgb(255, 255, 255);"))
        self.BatchesWidget.setObjectName(_fromUtf8("BatchesWidget"))
        self.AddbatchTab = QtGui.QWidget()
        self.AddbatchTab.setObjectName(_fromUtf8("AddbatchTab"))
        self.formLayoutWidget = QtGui.QWidget(self.AddbatchTab)
        self.formLayoutWidget.setGeometry(QtCore.QRect(430, 120, 281, 181))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.batchform = QtGui.QFormLayout(self.formLayoutWidget)
        self.batchform.setObjectName(_fromUtf8("batchform"))
        self.batchIdLabel = QtGui.QLabel(self.formLayoutWidget)
        self.batchIdLabel.setObjectName(_fromUtf8("batchIdLabel"))
        self.batchform.setWidget(0, QtGui.QFormLayout.LabelRole, self.batchIdLabel)
        self.batchIdLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.batchIdLineEdit.setObjectName(_fromUtf8("batchIdLineEdit"))
        self.batchform.setWidget(0, QtGui.QFormLayout.FieldRole, self.batchIdLineEdit)
        self.timeLabel = QtGui.QLabel(self.formLayoutWidget)
        self.timeLabel.setObjectName(_fromUtf8("timeLabel"))
        self.batchform.setWidget(1, QtGui.QFormLayout.LabelRole, self.timeLabel)
        self.batchtimeLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.batchtimeLineEdit.setObjectName(_fromUtf8("batchtimeLineEdit"))
        self.batchform.setWidget(1, QtGui.QFormLayout.FieldRole, self.batchtimeLineEdit)
        self.strengthLabel = QtGui.QLabel(self.formLayoutWidget)
        self.strengthLabel.setObjectName(_fromUtf8("strengthLabel"))
        self.batchform.setWidget(2, QtGui.QFormLayout.LabelRole, self.strengthLabel)
        self.batchstrengthLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.batchstrengthLineEdit.setObjectName(_fromUtf8("batchstrengthLineEdit"))
        self.batchform.setWidget(2, QtGui.QFormLayout.FieldRole, self.batchstrengthLineEdit)
        self.trainerLabel = QtGui.QLabel(self.formLayoutWidget)
        self.trainerLabel.setObjectName(_fromUtf8("trainerLabel"))
        self.batchform.setWidget(3, QtGui.QFormLayout.LabelRole, self.trainerLabel)
        self.batchtrainerLineEdit = QtGui.QLineEdit(self.formLayoutWidget)
        self.batchtrainerLineEdit.setObjectName(_fromUtf8("batchtrainerLineEdit"))
        self.batchform.setWidget(3, QtGui.QFormLayout.FieldRole, self.batchtrainerLineEdit)
        self.addbatchbutton = QtGui.QPushButton(self.AddbatchTab)
        self.addbatchbutton.setGeometry(QtCore.QRect(520, 340, 101, 31))
        self.addbatchbutton.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold  11pt \"Ubuntu\";\n"
""))
        self.addbatchbutton.setObjectName(_fromUtf8("addbatchbutton"))
        self.BatchesWidget.addTab(self.AddbatchTab, _fromUtf8(""))
        self.batch = QtGui.QWidget()
        self.batch.setObjectName(_fromUtf8("batch"))
        self.batchtable = QtGui.QTableWidget(self.batch)
        self.batchtable.setGeometry(QtCore.QRect(200, 90, 800, 300))
        self.batchtable.setObjectName(_fromUtf8("batchtable"))
        self.batchtable.setColumnCount(4)
        self.batchtable.setRowCount(4)
        item = QtGui.QTableWidgetItem()
        self.batchtable.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.batchtable.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.batchtable.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.batchtable.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.batchtable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.batchtable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.batchtable.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.batchtable.setHorizontalHeaderItem(3, item)
        self.batchtable.horizontalHeader().setDefaultSectionSize(200)
        self.loadbatchbutton = QtGui.QPushButton(self.batch)
        self.loadbatchbutton.setGeometry(QtCore.QRect(560, 410, 121, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.loadbatchbutton.setFont(font)
        self.loadbatchbutton.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.loadbatchbutton.setObjectName(_fromUtf8("loadbatchbutton"))
        self.BatchesWidget.addTab(self.batch, _fromUtf8(""))
        self.stackedWidget_3.addWidget(self.BatchesPage)
        self.CustomerPage = QtGui.QWidget()
        self.CustomerPage.setObjectName(_fromUtf8("CustomerPage"))
        self.CustomerWidget = QtGui.QTabWidget(self.CustomerPage)
        self.CustomerWidget.setGeometry(QtCore.QRect(0, 0, 1261, 691))
        self.CustomerWidget.setStyleSheet(_fromUtf8("color: rgb(0, 0, 106);\n"
"background-color: rgb(255, 255, 255);"))
        self.CustomerWidget.setObjectName(_fromUtf8("CustomerWidget"))
        self.AddCustomer = QtGui.QWidget()
        self.AddCustomer.setObjectName(_fromUtf8("AddCustomer"))
        self.submitCustomerButton = QtGui.QPushButton(self.AddCustomer)
        self.submitCustomerButton.setGeometry(QtCore.QRect(840, 420, 110, 40))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.submitCustomerButton.setFont(font)
        self.submitCustomerButton.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.submitCustomerButton.setObjectName(_fromUtf8("submitCustomerButton"))
        self.gymInfoBox = QtGui.QGroupBox(self.AddCustomer)
        self.gymInfoBox.setGeometry(QtCore.QRect(610, 40, 441, 341))
        self.gymInfoBox.setFlat(False)
        self.gymInfoBox.setCheckable(False)
        self.gymInfoBox.setObjectName(_fromUtf8("gymInfoBox"))
        self.formLayoutWidget_4 = QtGui.QWidget(self.gymInfoBox)
        self.formLayoutWidget_4.setGeometry(QtCore.QRect(30, 30, 371, 391))
        self.formLayoutWidget_4.setObjectName(_fromUtf8("formLayoutWidget_4"))
        self.formLayout_3 = QtGui.QFormLayout(self.formLayoutWidget_4)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.lastNameLabel_3 = QtGui.QLabel(self.formLayoutWidget_4)
        self.lastNameLabel_3.setObjectName(_fromUtf8("lastNameLabel_3"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.lastNameLabel_3)
        self.lastNameLineEdit_3 = QtGui.QLineEdit(self.formLayoutWidget_4)
        self.lastNameLineEdit_3.setObjectName(_fromUtf8("lastNameLineEdit_3"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.FieldRole, self.lastNameLineEdit_3)
        self.firstNameLabel_3 = QtGui.QLabel(self.formLayoutWidget_4)
        self.firstNameLabel_3.setObjectName(_fromUtf8("firstNameLabel_3"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.LabelRole, self.firstNameLabel_3)
        self.firstNameLineEdit_3 = QtGui.QLineEdit(self.formLayoutWidget_4)
        self.firstNameLineEdit_3.setObjectName(_fromUtf8("firstNameLineEdit_3"))
        self.formLayout_3.setWidget(1, QtGui.QFormLayout.FieldRole, self.firstNameLineEdit_3)
        self.genderLabel_3 = QtGui.QLabel(self.formLayoutWidget_4)
        self.genderLabel_3.setObjectName(_fromUtf8("genderLabel_3"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.genderLabel_3)
        self.genderLineEdit_3 = QtGui.QLineEdit(self.formLayoutWidget_4)
        self.genderLineEdit_3.setObjectName(_fromUtf8("genderLineEdit_3"))
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.FieldRole, self.genderLineEdit_3)
        self.emailLabel_3 = QtGui.QLabel(self.formLayoutWidget_4)
        self.emailLabel_3.setObjectName(_fromUtf8("emailLabel_3"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.LabelRole, self.emailLabel_3)
        self.emailLineEdit_3 = QtGui.QLineEdit(self.formLayoutWidget_4)
        self.emailLineEdit_3.setObjectName(_fromUtf8("emailLineEdit_3"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.FieldRole, self.emailLineEdit_3)
        self.dateOfBirthLabel_3 = QtGui.QLabel(self.formLayoutWidget_4)
        self.dateOfBirthLabel_3.setObjectName(_fromUtf8("dateOfBirthLabel_3"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.LabelRole, self.dateOfBirthLabel_3)
        self.dateOfBirthLineEdit_3 = QtGui.QLineEdit(self.formLayoutWidget_4)
        self.dateOfBirthLineEdit_3.setObjectName(_fromUtf8("dateOfBirthLineEdit_3"))
        self.formLayout_3.setWidget(4, QtGui.QFormLayout.FieldRole, self.dateOfBirthLineEdit_3)
        self.occupationLabel_2 = QtGui.QLabel(self.formLayoutWidget_4)
        self.occupationLabel_2.setObjectName(_fromUtf8("occupationLabel_2"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.LabelRole, self.occupationLabel_2)
        self.occupationLineEdit_2 = QtGui.QLineEdit(self.formLayoutWidget_4)
        self.occupationLineEdit_2.setObjectName(_fromUtf8("occupationLineEdit_2"))
        self.formLayout_3.setWidget(5, QtGui.QFormLayout.FieldRole, self.occupationLineEdit_2)
        self.contactNumberLabel_3 = QtGui.QLabel(self.formLayoutWidget_4)
        self.contactNumberLabel_3.setObjectName(_fromUtf8("contactNumberLabel_3"))
        self.formLayout_3.setWidget(6, QtGui.QFormLayout.LabelRole, self.contactNumberLabel_3)
        self.contactNumberLineEdit_3 = QtGui.QLineEdit(self.formLayoutWidget_4)
        self.contactNumberLineEdit_3.setObjectName(_fromUtf8("contactNumberLineEdit_3"))
        self.formLayout_3.setWidget(6, QtGui.QFormLayout.FieldRole, self.contactNumberLineEdit_3)
        self.customerIDLabel = QtGui.QLabel(self.formLayoutWidget_4)
        self.customerIDLabel.setObjectName(_fromUtf8("customerIDLabel"))
        self.formLayout_3.setWidget(7, QtGui.QFormLayout.LabelRole, self.customerIDLabel)
        self.customerIDLineEdit = QtGui.QLineEdit(self.formLayoutWidget_4)
        self.customerIDLineEdit.setObjectName(_fromUtf8("customerIDLineEdit"))
        self.formLayout_3.setWidget(7, QtGui.QFormLayout.FieldRole, self.customerIDLineEdit)
        self.customerIDLabel_4 = QtGui.QLabel(self.formLayoutWidget_4)
        self.customerIDLabel_4.setObjectName(_fromUtf8("customerIDLabel_4"))
        self.formLayout_3.setWidget(8, QtGui.QFormLayout.LabelRole, self.customerIDLabel_4)
        self.customerIDLineEdit_4 = QtGui.QLineEdit(self.formLayoutWidget_4)
        self.customerIDLineEdit_4.setObjectName(_fromUtf8("customerIDLineEdit_4"))
        self.formLayout_3.setWidget(8, QtGui.QFormLayout.FieldRole, self.customerIDLineEdit_4)
        self.personalInfoBox = QtGui.QGroupBox(self.AddCustomer)
        self.personalInfoBox.setGeometry(QtCore.QRect(70, 40, 481, 421))
        self.personalInfoBox.setFlat(False)
        self.personalInfoBox.setCheckable(False)
        self.personalInfoBox.setObjectName(_fromUtf8("personalInfoBox"))
        self.formLayoutWidget_5 = QtGui.QWidget(self.personalInfoBox)
        self.formLayoutWidget_5.setGeometry(QtCore.QRect(30, 30, 401, 371))
        self.formLayoutWidget_5.setObjectName(_fromUtf8("formLayoutWidget_5"))
        self.formLayout_4 = QtGui.QFormLayout(self.formLayoutWidget_5)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.lastNameLineEdit_4 = QtGui.QLineEdit(self.formLayoutWidget_5)
        self.lastNameLineEdit_4.setObjectName(_fromUtf8("lastNameLineEdit_4"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.lastNameLineEdit_4)
        self.firstNameLineEdit_4 = QtGui.QLineEdit(self.formLayoutWidget_5)
        self.firstNameLineEdit_4.setObjectName(_fromUtf8("firstNameLineEdit_4"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.firstNameLineEdit_4)
        self.genderLabel_4 = QtGui.QLabel(self.formLayoutWidget_5)
        self.genderLabel_4.setObjectName(_fromUtf8("genderLabel_4"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.LabelRole, self.genderLabel_4)
        self.genderLineEdit_4 = QtGui.QLineEdit(self.formLayoutWidget_5)
        self.genderLineEdit_4.setObjectName(_fromUtf8("genderLineEdit_4"))
        self.formLayout_4.setWidget(3, QtGui.QFormLayout.FieldRole, self.genderLineEdit_4)
        self.emailLabel_4 = QtGui.QLabel(self.formLayoutWidget_5)
        self.emailLabel_4.setObjectName(_fromUtf8("emailLabel_4"))
        self.formLayout_4.setWidget(4, QtGui.QFormLayout.LabelRole, self.emailLabel_4)
        self.emailLineEdit_4 = QtGui.QLineEdit(self.formLayoutWidget_5)
        self.emailLineEdit_4.setObjectName(_fromUtf8("emailLineEdit_4"))
        self.formLayout_4.setWidget(4, QtGui.QFormLayout.FieldRole, self.emailLineEdit_4)
        self.dateOfBirthLabel_4 = QtGui.QLabel(self.formLayoutWidget_5)
        self.dateOfBirthLabel_4.setObjectName(_fromUtf8("dateOfBirthLabel_4"))
        self.formLayout_4.setWidget(5, QtGui.QFormLayout.LabelRole, self.dateOfBirthLabel_4)
        self.dateOfBirthLineEdit_4 = QtGui.QLineEdit(self.formLayoutWidget_5)
        self.dateOfBirthLineEdit_4.setObjectName(_fromUtf8("dateOfBirthLineEdit_4"))
        self.formLayout_4.setWidget(5, QtGui.QFormLayout.FieldRole, self.dateOfBirthLineEdit_4)
        self.occupationLabel = QtGui.QLabel(self.formLayoutWidget_5)
        self.occupationLabel.setObjectName(_fromUtf8("occupationLabel"))
        self.formLayout_4.setWidget(6, QtGui.QFormLayout.LabelRole, self.occupationLabel)
        self.occupationLineEdit = QtGui.QLineEdit(self.formLayoutWidget_5)
        self.occupationLineEdit.setObjectName(_fromUtf8("occupationLineEdit"))
        self.formLayout_4.setWidget(6, QtGui.QFormLayout.FieldRole, self.occupationLineEdit)
        self.contactNumberLabel_4 = QtGui.QLabel(self.formLayoutWidget_5)
        self.contactNumberLabel_4.setObjectName(_fromUtf8("contactNumberLabel_4"))
        self.formLayout_4.setWidget(7, QtGui.QFormLayout.LabelRole, self.contactNumberLabel_4)
        self.contactNumberLineEdit_4 = QtGui.QLineEdit(self.formLayoutWidget_5)
        self.contactNumberLineEdit_4.setObjectName(_fromUtf8("contactNumberLineEdit_4"))
        self.formLayout_4.setWidget(7, QtGui.QFormLayout.FieldRole, self.contactNumberLineEdit_4)
        self.addressLabel_3 = QtGui.QLabel(self.formLayoutWidget_5)
        self.addressLabel_3.setObjectName(_fromUtf8("addressLabel_3"))
        self.formLayout_4.setWidget(8, QtGui.QFormLayout.LabelRole, self.addressLabel_3)
        self.addressLineEdit_3 = QtGui.QLineEdit(self.formLayoutWidget_5)
        self.addressLineEdit_3.setObjectName(_fromUtf8("addressLineEdit_3"))
        self.formLayout_4.setWidget(8, QtGui.QFormLayout.FieldRole, self.addressLineEdit_3)
        self.heightInCmLabel = QtGui.QLabel(self.formLayoutWidget_5)
        self.heightInCmLabel.setObjectName(_fromUtf8("heightInCmLabel"))
        self.formLayout_4.setWidget(9, QtGui.QFormLayout.LabelRole, self.heightInCmLabel)
        self.heightInCmLineEdit = QtGui.QLineEdit(self.formLayoutWidget_5)
        self.heightInCmLineEdit.setObjectName(_fromUtf8("heightInCmLineEdit"))
        self.formLayout_4.setWidget(9, QtGui.QFormLayout.FieldRole, self.heightInCmLineEdit)
        self.weightInKgLabel = QtGui.QLabel(self.formLayoutWidget_5)
        self.weightInKgLabel.setObjectName(_fromUtf8("weightInKgLabel"))
        self.formLayout_4.setWidget(10, QtGui.QFormLayout.LabelRole, self.weightInKgLabel)
        self.weightInKgLineEdit = QtGui.QLineEdit(self.formLayoutWidget_5)
        self.weightInKgLineEdit.setObjectName(_fromUtf8("weightInKgLineEdit"))
        self.formLayout_4.setWidget(10, QtGui.QFormLayout.FieldRole, self.weightInKgLineEdit)
        self.firstNameLabel_4 = QtGui.QLabel(self.formLayoutWidget_5)
        self.firstNameLabel_4.setObjectName(_fromUtf8("firstNameLabel_4"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.firstNameLabel_4)
        self.lastNameLabel_4 = QtGui.QLabel(self.formLayoutWidget_5)
        self.lastNameLabel_4.setObjectName(_fromUtf8("lastNameLabel_4"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.lastNameLabel_4)
        self.resetButton = QtGui.QPushButton(self.AddCustomer)
        self.resetButton.setGeometry(QtCore.QRect(660, 420, 110, 40))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.resetButton.setFont(font)
        self.resetButton.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.resetButton.setObjectName(_fromUtf8("resetButton"))
        self.CustomerWidget.addTab(self.AddCustomer, _fromUtf8(""))
        self.ViewCustomer = QtGui.QWidget()
        self.ViewCustomer.setObjectName(_fromUtf8("ViewCustomer"))
        self.loadButton_cust = QtGui.QPushButton(self.ViewCustomer)
        self.loadButton_cust.setGeometry(QtCore.QRect(510, 410, 110, 40))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.loadButton_cust.setFont(font)
        self.loadButton_cust.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.loadButton_cust.setObjectName(_fromUtf8("loadButton_cust"))
        self.tableWidget = QtGui.QTableWidget(self.ViewCustomer)
        self.tableWidget.setGeometry(QtCore.QRect(160, 50, 871, 341))
        self.tableWidget.setRowCount(10)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(120)
        self.CustomerWidget.addTab(self.ViewCustomer, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.label_11 = QtGui.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(90, 50, 151, 21))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_13 = QtGui.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(130, 120, 91, 21))
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.label_14 = QtGui.QLabel(self.tab)
        self.label_14.setGeometry(QtCore.QRect(130, 170, 81, 21))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.lineEdit = QtGui.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(240, 120, 113, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(self.tab)
        self.lineEdit_2.setGeometry(QtCore.QRect(240, 170, 113, 27))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))
        self.loadButton_cust_2 = QtGui.QPushButton(self.tab)
        self.loadButton_cust_2.setGeometry(QtCore.QRect(180, 340, 141, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.loadButton_cust_2.setFont(font)
        self.loadButton_cust_2.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.loadButton_cust_2.setObjectName(_fromUtf8("loadButton_cust_2"))
        self.plainTextEdit_4 = QtGui.QPlainTextEdit(self.tab)
        self.plainTextEdit_4.setGeometry(QtCore.QRect(620, 30, 481, 380))
        self.plainTextEdit_4.setObjectName(_fromUtf8("plainTextEdit_4"))
        self.receiptButton = QtGui.QPushButton(self.tab)
        self.receiptButton.setGeometry(QtCore.QRect(810, 430, 99, 27))
        self.receiptButton.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.receiptButton.setObjectName(_fromUtf8("receiptButton"))
        self.lineEdit_3 = QtGui.QLineEdit(self.tab)
        self.lineEdit_3.setGeometry(QtCore.QRect(240, 50, 113, 27))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))
        self.CustomerWidget.addTab(self.tab, _fromUtf8(""))
        self.stackedWidget_3.addWidget(self.CustomerPage)
        self.EmpDetailsPage = QtGui.QWidget()
        self.EmpDetailsPage.setObjectName(_fromUtf8("EmpDetailsPage"))
        self.EmpDetailsWidget = QtGui.QTabWidget(self.EmpDetailsPage)
        self.EmpDetailsWidget.setGeometry(QtCore.QRect(0, 0, 1291, 691))
        self.EmpDetailsWidget.setStyleSheet(_fromUtf8("color: rgb(0, 0, 106);\n"
"background-color: rgb(255, 255, 255);"))
        self.EmpDetailsWidget.setObjectName(_fromUtf8("EmpDetailsWidget"))
        self.AddEmpTab = QtGui.QWidget()
        self.AddEmpTab.setObjectName(_fromUtf8("AddEmpTab"))
        self.formLayoutWidget_14 = QtGui.QWidget(self.AddEmpTab)
        self.formLayoutWidget_14.setGeometry(QtCore.QRect(360, 110, 391, 317))
        self.formLayoutWidget_14.setObjectName(_fromUtf8("formLayoutWidget_14"))
        self.formLayout_14 = QtGui.QFormLayout(self.formLayoutWidget_14)
        self.formLayout_14.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_14.setObjectName(_fromUtf8("formLayout_14"))
        self.firstNameLabel_13 = QtGui.QLabel(self.formLayoutWidget_14)
        self.firstNameLabel_13.setObjectName(_fromUtf8("firstNameLabel_13"))
        self.formLayout_14.setWidget(0, QtGui.QFormLayout.LabelRole, self.firstNameLabel_13)
        self.lastNameLineEdit_13 = QtGui.QLineEdit(self.formLayoutWidget_14)
        self.lastNameLineEdit_13.setObjectName(_fromUtf8("lastNameLineEdit_13"))
        self.formLayout_14.setWidget(0, QtGui.QFormLayout.FieldRole, self.lastNameLineEdit_13)
        self.lastNameLabel_13 = QtGui.QLabel(self.formLayoutWidget_14)
        self.lastNameLabel_13.setObjectName(_fromUtf8("lastNameLabel_13"))
        self.formLayout_14.setWidget(1, QtGui.QFormLayout.LabelRole, self.lastNameLabel_13)
        self.firstNameLineEdit_13 = QtGui.QLineEdit(self.formLayoutWidget_14)
        self.firstNameLineEdit_13.setObjectName(_fromUtf8("firstNameLineEdit_13"))
        self.formLayout_14.setWidget(1, QtGui.QFormLayout.FieldRole, self.firstNameLineEdit_13)
        self.genderLabel_11 = QtGui.QLabel(self.formLayoutWidget_14)
        self.genderLabel_11.setObjectName(_fromUtf8("genderLabel_11"))
        self.formLayout_14.setWidget(3, QtGui.QFormLayout.LabelRole, self.genderLabel_11)
        self.genderLineEdit_11 = QtGui.QLineEdit(self.formLayoutWidget_14)
        self.genderLineEdit_11.setObjectName(_fromUtf8("genderLineEdit_11"))
        self.formLayout_14.setWidget(3, QtGui.QFormLayout.FieldRole, self.genderLineEdit_11)
        self.emailLabel_11 = QtGui.QLabel(self.formLayoutWidget_14)
        self.emailLabel_11.setObjectName(_fromUtf8("emailLabel_11"))
        self.formLayout_14.setWidget(4, QtGui.QFormLayout.LabelRole, self.emailLabel_11)
        self.emailLineEdit_11 = QtGui.QLineEdit(self.formLayoutWidget_14)
        self.emailLineEdit_11.setObjectName(_fromUtf8("emailLineEdit_11"))
        self.formLayout_14.setWidget(4, QtGui.QFormLayout.FieldRole, self.emailLineEdit_11)
        self.dateOfBirthLabel_11 = QtGui.QLabel(self.formLayoutWidget_14)
        self.dateOfBirthLabel_11.setObjectName(_fromUtf8("dateOfBirthLabel_11"))
        self.formLayout_14.setWidget(5, QtGui.QFormLayout.LabelRole, self.dateOfBirthLabel_11)
        self.dateOfBirthLineEdit_11 = QtGui.QLineEdit(self.formLayoutWidget_14)
        self.dateOfBirthLineEdit_11.setObjectName(_fromUtf8("dateOfBirthLineEdit_11"))
        self.formLayout_14.setWidget(5, QtGui.QFormLayout.FieldRole, self.dateOfBirthLineEdit_11)
        self.contactNumberLabel_11 = QtGui.QLabel(self.formLayoutWidget_14)
        self.contactNumberLabel_11.setObjectName(_fromUtf8("contactNumberLabel_11"))
        self.formLayout_14.setWidget(6, QtGui.QFormLayout.LabelRole, self.contactNumberLabel_11)
        self.contactNumberLineEdit_11 = QtGui.QLineEdit(self.formLayoutWidget_14)
        self.contactNumberLineEdit_11.setObjectName(_fromUtf8("contactNumberLineEdit_11"))
        self.formLayout_14.setWidget(6, QtGui.QFormLayout.FieldRole, self.contactNumberLineEdit_11)
        self.addressLabel_10 = QtGui.QLabel(self.formLayoutWidget_14)
        self.addressLabel_10.setObjectName(_fromUtf8("addressLabel_10"))
        self.formLayout_14.setWidget(7, QtGui.QFormLayout.LabelRole, self.addressLabel_10)
        self.addressLineEdit_10 = QtGui.QLineEdit(self.formLayoutWidget_14)
        self.addressLineEdit_10.setObjectName(_fromUtf8("addressLineEdit_10"))
        self.formLayout_14.setWidget(7, QtGui.QFormLayout.FieldRole, self.addressLineEdit_10)
        self.newlabel_9 = QtGui.QLabel(self.formLayoutWidget_14)
        self.newlabel_9.setObjectName(_fromUtf8("newlabel_9"))
        self.formLayout_14.setWidget(8, QtGui.QFormLayout.LabelRole, self.newlabel_9)
        self.newlineedit_9 = QtGui.QLineEdit(self.formLayoutWidget_14)
        self.newlineedit_9.setObjectName(_fromUtf8("newlineedit_9"))
        self.formLayout_14.setWidget(8, QtGui.QFormLayout.FieldRole, self.newlineedit_9)
        self.label_15 = QtGui.QLabel(self.AddEmpTab)
        self.label_15.setGeometry(QtCore.QRect(270, 70, 171, 31))
        self.label_15.setStyleSheet(_fromUtf8("font: 75 bold 12pt \"Ubuntu\";"))
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.submitEmployeeButton = QtGui.QPushButton(self.AddEmpTab)
        self.submitEmployeeButton.setGeometry(QtCore.QRect(510, 420, 99, 27))
        self.submitEmployeeButton.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.submitEmployeeButton.setObjectName(_fromUtf8("submitEmployeeButton"))
        self.EmpDetailsWidget.addTab(self.AddEmpTab, _fromUtf8(""))
        self.ViewEmpTab = QtGui.QWidget()
        self.ViewEmpTab.setObjectName(_fromUtf8("ViewEmpTab"))
        self.tableWidget_4 = QtGui.QTableWidget(self.ViewEmpTab)
        self.tableWidget_4.setGeometry(QtCore.QRect(210, 90, 821, 271))
        self.tableWidget_4.setObjectName(_fromUtf8("tableWidget_4"))
        self.tableWidget_4.setColumnCount(8)
        self.tableWidget_4.setRowCount(4)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_4.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_4.setHorizontalHeaderItem(7, item)
        self.submitEmployeeButton_2 = QtGui.QPushButton(self.ViewEmpTab)
        self.submitEmployeeButton_2.setGeometry(QtCore.QRect(530, 410, 99, 27))
        self.submitEmployeeButton_2.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.submitEmployeeButton_2.setObjectName(_fromUtf8("submitEmployeeButton_2"))
        self.EmpDetailsWidget.addTab(self.ViewEmpTab, _fromUtf8(""))
        self.stackedWidget_3.addWidget(self.EmpDetailsPage)
        self.EqipDetailsPage = QtGui.QWidget()
        self.EqipDetailsPage.setObjectName(_fromUtf8("EqipDetailsPage"))
        self.EqipDetailsWidget = QtGui.QTabWidget(self.EqipDetailsPage)
        self.EqipDetailsWidget.setGeometry(QtCore.QRect(0, 0, 1251, 701))
        self.EqipDetailsWidget.setStyleSheet(_fromUtf8("color: rgb(0, 0, 106);\n"
"background-color: rgb(255, 255, 255);"))
        self.EqipDetailsWidget.setObjectName(_fromUtf8("EqipDetailsWidget"))
        self.AddEquipmenttab = QtGui.QWidget()
        self.AddEquipmenttab.setObjectName(_fromUtf8("AddEquipmenttab"))
        self.formLayoutWidget_7 = QtGui.QWidget(self.AddEquipmenttab)
        self.formLayoutWidget_7.setGeometry(QtCore.QRect(400, 140, 391, 151))
        self.formLayoutWidget_7.setObjectName(_fromUtf8("formLayoutWidget_7"))
        self.formLayout_6 = QtGui.QFormLayout(self.formLayoutWidget_7)
        self.formLayout_6.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_6.setObjectName(_fromUtf8("formLayout_6"))
        self.equipmentNameLabel = QtGui.QLabel(self.formLayoutWidget_7)
        self.equipmentNameLabel.setObjectName(_fromUtf8("equipmentNameLabel"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.LabelRole, self.equipmentNameLabel)
        self.dateOfPurchaseLabel = QtGui.QLabel(self.formLayoutWidget_7)
        self.dateOfPurchaseLabel.setObjectName(_fromUtf8("dateOfPurchaseLabel"))
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.LabelRole, self.dateOfPurchaseLabel)
        self.dateOfPurchaseLineEdit = QtGui.QLineEdit(self.formLayoutWidget_7)
        self.dateOfPurchaseLineEdit.setObjectName(_fromUtf8("dateOfPurchaseLineEdit"))
        self.formLayout_6.setWidget(1, QtGui.QFormLayout.FieldRole, self.dateOfPurchaseLineEdit)
        self.costLabel = QtGui.QLabel(self.formLayoutWidget_7)
        self.costLabel.setObjectName(_fromUtf8("costLabel"))
        self.formLayout_6.setWidget(2, QtGui.QFormLayout.LabelRole, self.costLabel)
        self.costLineEdit = QtGui.QLineEdit(self.formLayoutWidget_7)
        self.costLineEdit.setObjectName(_fromUtf8("costLineEdit"))
        self.formLayout_6.setWidget(2, QtGui.QFormLayout.FieldRole, self.costLineEdit)
        self.quantityLabel = QtGui.QLabel(self.formLayoutWidget_7)
        self.quantityLabel.setObjectName(_fromUtf8("quantityLabel"))
        self.formLayout_6.setWidget(3, QtGui.QFormLayout.LabelRole, self.quantityLabel)
        self.quantityLineEdit = QtGui.QLineEdit(self.formLayoutWidget_7)
        self.quantityLineEdit.setObjectName(_fromUtf8("quantityLineEdit"))
        self.formLayout_6.setWidget(3, QtGui.QFormLayout.FieldRole, self.quantityLineEdit)
        self.equipmentNameLineEdit = QtGui.QLineEdit(self.formLayoutWidget_7)
        self.equipmentNameLineEdit.setObjectName(_fromUtf8("equipmentNameLineEdit"))
        self.formLayout_6.setWidget(0, QtGui.QFormLayout.FieldRole, self.equipmentNameLineEdit)
        self.submitButton_5 = QtGui.QPushButton(self.AddEquipmenttab)
        self.submitButton_5.setGeometry(QtCore.QRect(530, 320, 110, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.submitButton_5.setFont(font)
        self.submitButton_5.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.submitButton_5.setObjectName(_fromUtf8("submitButton_5"))
        self.EqipDetailsWidget.addTab(self.AddEquipmenttab, _fromUtf8(""))
        self.ViewEquipmenttab = QtGui.QWidget()
        self.ViewEquipmenttab.setObjectName(_fromUtf8("ViewEquipmenttab"))
        self.load_dataButton = QtGui.QPushButton(self.ViewEquipmenttab)
        self.load_dataButton.setGeometry(QtCore.QRect(560, 400, 110, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.load_dataButton.setFont(font)
        self.load_dataButton.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.load_dataButton.setObjectName(_fromUtf8("load_dataButton"))
        self.tableWidget_2 = QtGui.QTableWidget(self.ViewEquipmenttab)
        self.tableWidget_2.setGeometry(QtCore.QRect(330, 50, 600, 311))
        self.tableWidget_2.setRowCount(10)
        self.tableWidget_2.setColumnCount(4)
        self.tableWidget_2.setObjectName(_fromUtf8("tableWidget_2"))
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(138)
        self.EqipDetailsWidget.addTab(self.ViewEquipmenttab, _fromUtf8(""))
        self.stackedWidget_3.addWidget(self.EqipDetailsPage)
        self.ProgressPage = QtGui.QWidget()
        self.ProgressPage.setObjectName(_fromUtf8("ProgressPage"))
        self.ProgressWidget = QtGui.QTabWidget(self.ProgressPage)
        self.ProgressWidget.setGeometry(QtCore.QRect(0, 0, 1261, 671))
        self.ProgressWidget.setStyleSheet(_fromUtf8("color: rgb(0, 0, 106);\n"
"background-color: rgb(255, 255, 255);"))
        self.ProgressWidget.setObjectName(_fromUtf8("ProgressWidget"))
        self.AddProgresstab = QtGui.QWidget()
        self.AddProgresstab.setObjectName(_fromUtf8("AddProgresstab"))
        self.formLayoutWidget_8 = QtGui.QWidget(self.AddProgresstab)
        self.formLayoutWidget_8.setGeometry(QtCore.QRect(420, 50, 351, 241))
        self.formLayoutWidget_8.setObjectName(_fromUtf8("formLayoutWidget_8"))
        self.formLayout_7 = QtGui.QFormLayout(self.formLayoutWidget_8)
        self.formLayout_7.setObjectName(_fromUtf8("formLayout_7"))
        self.firstNameLabel_6 = QtGui.QLabel(self.formLayoutWidget_8)
        self.firstNameLabel_6.setObjectName(_fromUtf8("firstNameLabel_6"))
        self.formLayout_7.setWidget(0, QtGui.QFormLayout.LabelRole, self.firstNameLabel_6)
        self.firstNameLineEdit_6 = QtGui.QLineEdit(self.formLayoutWidget_8)
        self.firstNameLineEdit_6.setObjectName(_fromUtf8("firstNameLineEdit_6"))
        self.formLayout_7.setWidget(0, QtGui.QFormLayout.FieldRole, self.firstNameLineEdit_6)
        self.lastNameLabel_6 = QtGui.QLabel(self.formLayoutWidget_8)
        self.lastNameLabel_6.setObjectName(_fromUtf8("lastNameLabel_6"))
        self.formLayout_7.setWidget(1, QtGui.QFormLayout.LabelRole, self.lastNameLabel_6)
        self.lastNameLineEdit_6 = QtGui.QLineEdit(self.formLayoutWidget_8)
        self.lastNameLineEdit_6.setObjectName(_fromUtf8("lastNameLineEdit_6"))
        self.formLayout_7.setWidget(1, QtGui.QFormLayout.FieldRole, self.lastNameLineEdit_6)
        self.customerIDLabel_2 = QtGui.QLabel(self.formLayoutWidget_8)
        self.customerIDLabel_2.setObjectName(_fromUtf8("customerIDLabel_2"))
        self.formLayout_7.setWidget(2, QtGui.QFormLayout.LabelRole, self.customerIDLabel_2)
        self.customerIDLineEdit_2 = QtGui.QLineEdit(self.formLayoutWidget_8)
        self.customerIDLineEdit_2.setObjectName(_fromUtf8("customerIDLineEdit_2"))
        self.formLayout_7.setWidget(2, QtGui.QFormLayout.FieldRole, self.customerIDLineEdit_2)
        self.lasteDateLabel = QtGui.QLabel(self.formLayoutWidget_8)
        self.lasteDateLabel.setObjectName(_fromUtf8("lasteDateLabel"))
        self.formLayout_7.setWidget(3, QtGui.QFormLayout.LabelRole, self.lasteDateLabel)
        self.lasteDateLineEdit = QtGui.QLineEdit(self.formLayoutWidget_8)
        self.lasteDateLineEdit.setObjectName(_fromUtf8("lasteDateLineEdit"))
        self.formLayout_7.setWidget(3, QtGui.QFormLayout.FieldRole, self.lasteDateLineEdit)
        self.progressEntryDateLabel = QtGui.QLabel(self.formLayoutWidget_8)
        self.progressEntryDateLabel.setObjectName(_fromUtf8("progressEntryDateLabel"))
        self.formLayout_7.setWidget(4, QtGui.QFormLayout.LabelRole, self.progressEntryDateLabel)
        self.progressEntryDateLineEdit = QtGui.QLineEdit(self.formLayoutWidget_8)
        self.progressEntryDateLineEdit.setObjectName(_fromUtf8("progressEntryDateLineEdit"))
        self.formLayout_7.setWidget(4, QtGui.QFormLayout.FieldRole, self.progressEntryDateLineEdit)
        self.heightLabel = QtGui.QLabel(self.formLayoutWidget_8)
        self.heightLabel.setObjectName(_fromUtf8("heightLabel"))
        self.formLayout_7.setWidget(5, QtGui.QFormLayout.LabelRole, self.heightLabel)
        self.heightLineEdit = QtGui.QLineEdit(self.formLayoutWidget_8)
        self.heightLineEdit.setObjectName(_fromUtf8("heightLineEdit"))
        self.formLayout_7.setWidget(5, QtGui.QFormLayout.FieldRole, self.heightLineEdit)
        self.weightLabel = QtGui.QLabel(self.formLayoutWidget_8)
        self.weightLabel.setObjectName(_fromUtf8("weightLabel"))
        self.formLayout_7.setWidget(6, QtGui.QFormLayout.LabelRole, self.weightLabel)
        self.weightLineEdit = QtGui.QLineEdit(self.formLayoutWidget_8)
        self.weightLineEdit.setObjectName(_fromUtf8("weightLineEdit"))
        self.formLayout_7.setWidget(6, QtGui.QFormLayout.FieldRole, self.weightLineEdit)
        self.load_dataButton_2 = QtGui.QPushButton(self.AddProgresstab)
        self.load_dataButton_2.setGeometry(QtCore.QRect(470, 390, 110, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.load_dataButton_2.setFont(font)
        self.load_dataButton_2.setStyleSheet(_fromUtf8("background-color: rgba(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.load_dataButton_2.setObjectName(_fromUtf8("load_dataButton_2"))
        self.load_dataButton_3 = QtGui.QPushButton(self.AddProgresstab)
        self.load_dataButton_3.setGeometry(QtCore.QRect(600, 390, 110, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.load_dataButton_3.setFont(font)
        self.load_dataButton_3.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.load_dataButton_3.setObjectName(_fromUtf8("load_dataButton_3"))
        self.ProgressWidget.addTab(self.AddProgresstab, _fromUtf8(""))
        self.Trackprogrsstab = QtGui.QWidget()
        self.Trackprogrsstab.setObjectName(_fromUtf8("Trackprogrsstab"))
        self.formLayoutWidget_9 = QtGui.QWidget(self.Trackprogrsstab)
        self.formLayoutWidget_9.setGeometry(QtCore.QRect(460, 50, 271, 131))
        self.formLayoutWidget_9.setObjectName(_fromUtf8("formLayoutWidget_9"))
        self.formLayout_8 = QtGui.QFormLayout(self.formLayoutWidget_9)
        self.formLayout_8.setObjectName(_fromUtf8("formLayout_8"))
        self.firstNameLabel_7 = QtGui.QLabel(self.formLayoutWidget_9)
        self.firstNameLabel_7.setObjectName(_fromUtf8("firstNameLabel_7"))
        self.formLayout_8.setWidget(0, QtGui.QFormLayout.LabelRole, self.firstNameLabel_7)
        self.firstNameLineEdit_7 = QtGui.QLineEdit(self.formLayoutWidget_9)
        self.firstNameLineEdit_7.setObjectName(_fromUtf8("firstNameLineEdit_7"))
        self.formLayout_8.setWidget(0, QtGui.QFormLayout.FieldRole, self.firstNameLineEdit_7)
        self.lastNameLabel_7 = QtGui.QLabel(self.formLayoutWidget_9)
        self.lastNameLabel_7.setObjectName(_fromUtf8("lastNameLabel_7"))
        self.formLayout_8.setWidget(1, QtGui.QFormLayout.LabelRole, self.lastNameLabel_7)
        self.lastNameLineEdit_7 = QtGui.QLineEdit(self.formLayoutWidget_9)
        self.lastNameLineEdit_7.setObjectName(_fromUtf8("lastNameLineEdit_7"))
        self.formLayout_8.setWidget(1, QtGui.QFormLayout.FieldRole, self.lastNameLineEdit_7)
        self.customerIDLabel_3 = QtGui.QLabel(self.formLayoutWidget_9)
        self.customerIDLabel_3.setObjectName(_fromUtf8("customerIDLabel_3"))
        self.formLayout_8.setWidget(2, QtGui.QFormLayout.LabelRole, self.customerIDLabel_3)
        self.customerIDLineEdit_3 = QtGui.QLineEdit(self.formLayoutWidget_9)
        self.customerIDLineEdit_3.setObjectName(_fromUtf8("customerIDLineEdit_3"))
        self.formLayout_8.setWidget(2, QtGui.QFormLayout.FieldRole, self.customerIDLineEdit_3)
        self.load_dataButton_4 = QtGui.QPushButton(self.Trackprogrsstab)
        self.load_dataButton_4.setGeometry(QtCore.QRect(510, 230, 161, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.load_dataButton_4.setFont(font)
        self.load_dataButton_4.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.load_dataButton_4.setObjectName(_fromUtf8("load_dataButton_4"))
        self.load_dataButton_5 = QtGui.QPushButton(self.Trackprogrsstab)
        self.load_dataButton_5.setGeometry(QtCore.QRect(310, 380, 191, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.load_dataButton_5.setFont(font)
        self.load_dataButton_5.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.load_dataButton_5.setObjectName(_fromUtf8("load_dataButton_5"))
        self.load_dataButton_6 = QtGui.QPushButton(self.Trackprogrsstab)
        self.load_dataButton_6.setGeometry(QtCore.QRect(530, 380, 191, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.load_dataButton_6.setFont(font)
        self.load_dataButton_6.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.load_dataButton_6.setObjectName(_fromUtf8("load_dataButton_6"))
        self.load_dataButton_7 = QtGui.QPushButton(self.Trackprogrsstab)
        self.load_dataButton_7.setGeometry(QtCore.QRect(750, 380, 191, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.load_dataButton_7.setFont(font)
        self.load_dataButton_7.setStyleSheet(_fromUtf8("background-color: rgb(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.load_dataButton_7.setObjectName(_fromUtf8("load_dataButton_7"))
        self.ProgressWidget.addTab(self.Trackprogrsstab, _fromUtf8(""))
        self.ViewAllProgresstab = QtGui.QWidget()
        self.ViewAllProgresstab.setObjectName(_fromUtf8("ViewAllProgresstab"))
        self.tableWidget_3 = QtGui.QTableWidget(self.ViewAllProgresstab)
        self.tableWidget_3.setGeometry(QtCore.QRect(150, 50, 800, 300))
        self.tableWidget_3.setObjectName(_fromUtf8("tableWidget_3"))
        self.tableWidget_3.setColumnCount(5)
        self.tableWidget_3.setRowCount(4)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(4, item)
        self.tableWidget_3.horizontalHeader().setDefaultSectionSize(160)
        self.load_dataButton_8 = QtGui.QPushButton(self.ViewAllProgresstab)
        self.load_dataButton_8.setGeometry(QtCore.QRect(470, 410, 110, 31))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setPointSize(11)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.load_dataButton_8.setFont(font)
        self.load_dataButton_8.setStyleSheet(_fromUtf8("background-color: rgba(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.load_dataButton_8.setObjectName(_fromUtf8("load_dataButton_8"))
        self.ProgressWidget.addTab(self.ViewAllProgresstab, _fromUtf8(""))
        self.stackedWidget_3.addWidget(self.ProgressPage)
        self.ReportsPage = QtGui.QWidget()
        self.ReportsPage.setObjectName(_fromUtf8("ReportsPage"))
        self.ReportsWidget = QtGui.QTabWidget(self.ReportsPage)
        self.ReportsWidget.setGeometry(QtCore.QRect(0, 0, 1231, 671))
        self.ReportsWidget.setStyleSheet(_fromUtf8("color: rgb(0, 0, 106);\n"
"background-color: rgb(255, 255, 255);"))
        self.ReportsWidget.setObjectName(_fromUtf8("ReportsWidget"))
        self.Membertab = QtGui.QWidget()
        self.Membertab.setObjectName(_fromUtf8("Membertab"))
        self.pushButton_8 = QtGui.QPushButton(self.Membertab)
        self.pushButton_8.setGeometry(QtCore.QRect(510, 390, 141, 31))
        self.pushButton_8.setStyleSheet(_fromUtf8("background-color: rgba(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.label_3 = QtGui.QLabel(self.Membertab)
        self.label_3.setGeometry(QtCore.QRect(420, 90, 371, 41))
        self.label_3.setStyleSheet(_fromUtf8("font: 75 bold 22pt \"Ubuntu\";"))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.plainTextEdit = QtGui.QPlainTextEdit(self.Membertab)
        self.plainTextEdit.setGeometry(QtCore.QRect(280, 220, 691, 101))
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.ReportsWidget.addTab(self.Membertab, _fromUtf8(""))
        self.MonthWisetab = QtGui.QWidget()
        self.MonthWisetab.setObjectName(_fromUtf8("MonthWisetab"))
        self.pushButton_9 = QtGui.QPushButton(self.MonthWisetab)
        self.pushButton_9.setGeometry(QtCore.QRect(510, 390, 141, 31))
        self.pushButton_9.setStyleSheet(_fromUtf8("background-color: rgba(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.plainTextEdit_2 = QtGui.QPlainTextEdit(self.MonthWisetab)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(280, 220, 701, 131))
        self.plainTextEdit_2.setObjectName(_fromUtf8("plainTextEdit_2"))
        self.label_7 = QtGui.QLabel(self.MonthWisetab)
        self.label_7.setGeometry(QtCore.QRect(420, 90, 381, 41))
        self.label_7.setStyleSheet(_fromUtf8("font: 75 bold 22pt \"Ubuntu\";"))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.ReportsWidget.addTab(self.MonthWisetab, _fromUtf8(""))
        self.BMItab = QtGui.QWidget()
        self.BMItab.setObjectName(_fromUtf8("BMItab"))
        self.pushButton_10 = QtGui.QPushButton(self.BMItab)
        self.pushButton_10.setGeometry(QtCore.QRect(510, 390, 141, 31))
        self.pushButton_10.setStyleSheet(_fromUtf8("background-color: rgba(0,0,106);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
""))
        self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
        self.plainTextEdit_3 = QtGui.QPlainTextEdit(self.BMItab)
        self.plainTextEdit_3.setGeometry(QtCore.QRect(290, 220, 691, 101))
        self.plainTextEdit_3.setObjectName(_fromUtf8("plainTextEdit_3"))
        self.label_10 = QtGui.QLabel(self.BMItab)
        self.label_10.setGeometry(QtCore.QRect(430, 90, 371, 41))
        self.label_10.setStyleSheet(_fromUtf8("font: 75 bold 22pt \"Ubuntu\";"))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.ReportsWidget.addTab(self.BMItab, _fromUtf8(""))
        self.stackedWidget_3.addWidget(self.ReportsPage)
        self.pushButton_6 = QtGui.QPushButton(self.page_2)
        self.pushButton_6.setGeometry(QtCore.QRect(1140, 150, 99, 35))
        self.pushButton_6.setStyleSheet(_fromUtf8("background-color: rgba(255,255,255,80);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
"border:1.5px solid white\n"
""))
        self.pushButton_6.setObjectName(_fromUtf8("pushButton_6"))
        self.pushButton_5 = QtGui.QPushButton(self.page_2)
        self.pushButton_5.setGeometry(QtCore.QRect(880, 150, 141, 35))
        self.pushButton_5.setStyleSheet(_fromUtf8("background-color: rgba(255,255,255,80);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
"border:1.5px solid white\n"
""))
        self.pushButton_5.setObjectName(_fromUtf8("pushButton_5"))
        self.pushButton_4 = QtGui.QPushButton(self.page_2)
        self.pushButton_4.setGeometry(QtCore.QRect(1030, 150, 99, 35))
        self.pushButton_4.setStyleSheet(_fromUtf8("background-color: rgba(255,255,255,80);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
"border:1.5px solid white\n"
""))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.pushButton = QtGui.QPushButton(self.page_2)
        self.pushButton.setGeometry(QtCore.QRect(510, 150, 99, 35))
        self.pushButton.setStyleSheet(_fromUtf8("background-color: rgba(255,255,255,80);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
"border:1.5px solid white\n"
""))
        icon = QtGui.QIcon.fromTheme(_fromUtf8("note"))
        self.pushButton.setIcon(icon)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.page_2)
        self.pushButton_2.setGeometry(QtCore.QRect(620, 150, 99, 35))
        self.pushButton_2.setStyleSheet(_fromUtf8("background-color: rgba(255,255,255,80);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
"border:1.5px solid white\n"
""))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.page_2)
        self.pushButton_3.setGeometry(QtCore.QRect(730, 150, 141, 35))
        self.pushButton_3.setStyleSheet(_fromUtf8("background-color: rgba(255,255,255,80);\n"
"color: rgb(255,255,255);\n"
"font: 75 bold 11pt \"Ubuntu\";\n"
"border:1.5px solid white\n"
""))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.stackedWidget.addWidget(self.page_2)
        LoginWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(LoginWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.stackedWidget_3.setCurrentIndex(0)
        self.BatchesWidget.setCurrentIndex(0)
        self.CustomerWidget.setCurrentIndex(0)
        self.EmpDetailsWidget.setCurrentIndex(0)
        self.EqipDetailsWidget.setCurrentIndex(0)
        self.ProgressWidget.setCurrentIndex(0)
        self.ReportsWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)
        
        
        self.buttonLogin.clicked.connect(self.logincheck)
        self.logout.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.pushButton.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(0))
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(1))
        self.pushButton_3.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(2))
        self.pushButton_4.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(4))
        self.pushButton_5.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(3))
        self.pushButton_6.clicked.connect(lambda: self.stackedWidget_3.setCurrentIndex(5))
        self.pushButton_8.clicked.connect(self.getgraphofgenders)
        self.pushButton_9.clicked.connect(self.getMonthWiseBookingGraph)
        self.pushButton_10.clicked.connect(self.getgraphofbmi)
        self.submitButton_5.clicked.connect(self.addinstrument)
        self.load_dataButton.clicked.connect(self.showequipment)
        self.loadButton_cust_2.clicked.connect(self.generateBill)
        self.receiptButton.clicked.connect(self.printReceipt)
        self.load_dataButton_3.clicked.connect(self.addprogressfunction)
        self.load_dataButton_2.clicked.connect(self.loadvalues)
        self.load_dataButton_4.clicked.connect(self.loadcid)
        self.load_dataButton_5.clicked.connect(self.trackbmi)
        self.load_dataButton_6.clicked.connect(self.trackwt)
        self.load_dataButton_7.clicked.connect(self.trackht)         
        self.load_dataButton_8.clicked.connect(self.showprogdata)
        self.submitEmployeeButton.clicked.connect(self.addemp)  # added line       
        self.submitEmployeeButton_2.clicked.connect(self.showemp)  # added line       
        self.submitCustomerButton.clicked.connect(self.storedata)           
        self.resetButton.clicked.connect(self.resetall)        
        self.addbatchbutton.clicked.connect(self.insertBatch)
        self.loadbatchbutton.clicked.connect(self.showBatchData)
	self.loadButton_cust.clicked.connect(self.showcustdata)

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(_translate("LoginWindow", "MainWindow", None))
        self.buttonCancel.setText(_translate("LoginWindow", "Cancel", None))
        self.label_9.setText(_translate("LoginWindow", "Password", None))
        self.label_6.setText(_translate("LoginWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:48pt;\">FitnessPro</span></p></body></html>", None))
        self.username.setText(_translate("LoginWindow", "User Name", None))
        self.buttonCancel_2.setText(_translate("LoginWindow", "Cancel", None))
        self.password.setText(_translate("LoginWindow", "Password", None))
        self.buttonLogin.setText(_translate("LoginWindow", "Login", None))
        self.label_5.setText(_translate("LoginWindow", "LOGIN", None))
        self.label_12.setText(_translate("LoginWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:36pt; color:#ffffff;\">FitnessPro</span></p></body></html>", None))
        self.logout.setText(_translate("LoginWindow", "Logout", None))
        self.label_8.setText(_translate("LoginWindow", "<html><head/><body><p><span style=\" font-weight:600; color:#ffffff;\">Welcome, Admin </span></p></body></html>", None))
        self.batchIdLabel.setText(_translate("LoginWindow", "Batch Id :", None))
        self.timeLabel.setText(_translate("LoginWindow", "Time :", None))
        self.strengthLabel.setText(_translate("LoginWindow", "Strength :", None))
        self.trainerLabel.setText(_translate("LoginWindow", "Trainer :", None))
        self.addbatchbutton.setText(_translate("LoginWindow", "Add", None))
        self.BatchesWidget.setTabText(self.BatchesWidget.indexOf(self.AddbatchTab), _translate("LoginWindow", "Add Batch", None))
        item = self.batchtable.verticalHeaderItem(0)
        item.setText(_translate("LoginWindow", "1", None))
        item = self.batchtable.verticalHeaderItem(1)
        item.setText(_translate("LoginWindow", "2", None))
        item = self.batchtable.verticalHeaderItem(2)
        item.setText(_translate("LoginWindow", "3", None))
        item = self.batchtable.verticalHeaderItem(3)
        item.setText(_translate("LoginWindow", "4", None))
        item = self.batchtable.horizontalHeaderItem(0)
        item.setText(_translate("LoginWindow", "Batch Id", None))
        item = self.batchtable.horizontalHeaderItem(1)
        item.setText(_translate("LoginWindow", "Strength", None))
        item = self.batchtable.horizontalHeaderItem(2)
        item.setText(_translate("LoginWindow", "Time", None))
        item = self.batchtable.horizontalHeaderItem(3)
        item.setText(_translate("LoginWindow", "Trainer", None))
        self.loadbatchbutton.setText(_translate("LoginWindow", "Load", None))
        self.BatchesWidget.setTabText(self.BatchesWidget.indexOf(self.batch), _translate("LoginWindow", "View Batch", None))
        self.submitCustomerButton.setText(_translate("LoginWindow", "Submit", None))
        self.gymInfoBox.setTitle(_translate("LoginWindow", "Gym information", None))
        self.lastNameLabel_3.setText(_translate("LoginWindow", "Subscription :", None))
        self.firstNameLabel_3.setText(_translate("LoginWindow", "Start Date :", None))
        self.genderLabel_3.setText(_translate("LoginWindow", "End date : ", None))
        self.emailLabel_3.setText(_translate("LoginWindow", "Amount :", None))
        self.dateOfBirthLabel_3.setText(_translate("LoginWindow", "Amount Status :", None))
        self.occupationLabel_2.setText(_translate("LoginWindow", "Pending Amount :", None))
        self.contactNumberLabel_3.setText(_translate("LoginWindow", "Personal Trainer :", None))
        self.customerIDLabel.setText(_translate("LoginWindow", "Customer ID :", None))
        self.customerIDLabel_4.setText(_translate("LoginWindow", "Batch ID :", None))
        self.personalInfoBox.setTitle(_translate("LoginWindow", "Personal information", None))
        self.genderLabel_4.setText(_translate("LoginWindow", "Gender :", None))
        self.emailLabel_4.setText(_translate("LoginWindow", "Email :", None))
        self.dateOfBirthLabel_4.setText(_translate("LoginWindow", "Date of Birth :", None))
        self.occupationLabel.setText(_translate("LoginWindow", "Occupation", None))
        self.contactNumberLabel_4.setText(_translate("LoginWindow", "Contact Number :", None))
        self.addressLabel_3.setText(_translate("LoginWindow", "Address", None))
        self.heightInCmLabel.setText(_translate("LoginWindow", "Height(in cm) :", None))
        self.weightInKgLabel.setText(_translate("LoginWindow", "Weight (in kg)", None))
        self.firstNameLabel_4.setText(_translate("LoginWindow", "First name :", None))
        self.lastNameLabel_4.setText(_translate("LoginWindow", "Last Name :", None))
        self.resetButton.setText(_translate("LoginWindow", "Reset", None))
        self.CustomerWidget.setTabText(self.CustomerWidget.indexOf(self.AddCustomer), _translate("LoginWindow", "Add Customer", None))
        self.loadButton_cust.setText(_translate("LoginWindow", "Load", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("LoginWindow", "Cutomer Id", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("LoginWindow", "Subscription", None))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("LoginWindow", "Start Date", None))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("LoginWindow", "End Date", None))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("LoginWindow", "Amount", None))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("LoginWindow", "Amount Status", None))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("LoginWindow", "Pending Amount", None))
        self.CustomerWidget.setTabText(self.CustomerWidget.indexOf(self.ViewCustomer), _translate("LoginWindow", "View Customer", None))
        self.label_11.setText(_translate("LoginWindow", "Select Customer Id", None))
        self.label_13.setText(_translate("LoginWindow", "First Name", None))
        self.label_14.setText(_translate("LoginWindow", "Last Name", None))
        self.loadButton_cust_2.setText(_translate("LoginWindow", "Generate Bill", None))
        self.receiptButton.setText(_translate("LoginWindow", "Print Receipt", None))
        self.CustomerWidget.setTabText(self.CustomerWidget.indexOf(self.tab), _translate("LoginWindow", "Generate Custmer Bill", None))
        self.firstNameLabel_13.setText(_translate("LoginWindow", "First name :", None))
        self.lastNameLabel_13.setText(_translate("LoginWindow", "Last Name :", None))
        self.genderLabel_11.setText(_translate("LoginWindow", "Gender :", None))
        self.emailLabel_11.setText(_translate("LoginWindow", "Email :", None))
        self.dateOfBirthLabel_11.setText(_translate("LoginWindow", "Date of Birth :", None))
        self.contactNumberLabel_11.setText(_translate("LoginWindow", "Contact Number :", None))
        self.addressLabel_10.setText(_translate("LoginWindow", "Address", None))
        self.newlabel_9.setText(_translate("LoginWindow", "Experience: ", None))
        self.label_15.setText(_translate("LoginWindow", "Personal Information :", None))
        self.submitEmployeeButton.setText(_translate("LoginWindow", "Submit", None))
        self.EmpDetailsWidget.setTabText(self.EmpDetailsWidget.indexOf(self.AddEmpTab), _translate("LoginWindow", "Add Employee", None))
        item = self.tableWidget_4.verticalHeaderItem(0)
        item.setText(_translate("LoginWindow", "1", None))
        item = self.tableWidget_4.verticalHeaderItem(1)
        item.setText(_translate("LoginWindow", "2", None))
        item = self.tableWidget_4.verticalHeaderItem(2)
        item.setText(_translate("LoginWindow", "3", None))
        item = self.tableWidget_4.verticalHeaderItem(3)
        item.setText(_translate("LoginWindow", "4", None))
        item = self.tableWidget_4.horizontalHeaderItem(0)
        item.setText(_translate("LoginWindow", "First Name", None))
        item = self.tableWidget_4.horizontalHeaderItem(1)
        item.setText(_translate("LoginWindow", "Last Name", None))
        item = self.tableWidget_4.horizontalHeaderItem(2)
        item.setText(_translate("LoginWindow", "Gender", None))
        item = self.tableWidget_4.horizontalHeaderItem(3)
        item.setText(_translate("LoginWindow", "Email", None))
        item = self.tableWidget_4.horizontalHeaderItem(4)
        item.setText(_translate("LoginWindow", "Date of Birth", None))
        item = self.tableWidget_4.horizontalHeaderItem(5)
        item.setText(_translate("LoginWindow", "Contact", None))
        item = self.tableWidget_4.horizontalHeaderItem(6)
        item.setText(_translate("LoginWindow", "Address", None))
        item = self.tableWidget_4.horizontalHeaderItem(7)
        item.setText(_translate("LoginWindow", "Experience", None))
        self.submitEmployeeButton_2.setText(_translate("LoginWindow", "Load", None))
        self.EmpDetailsWidget.setTabText(self.EmpDetailsWidget.indexOf(self.ViewEmpTab), _translate("LoginWindow", "View Employee", None))
        self.equipmentNameLabel.setText(_translate("LoginWindow", "Equipment Name :", None))
        self.dateOfPurchaseLabel.setText(_translate("LoginWindow", "Date Of Purchase", None))
        self.costLabel.setText(_translate("LoginWindow", "Cost :", None))
        self.quantityLabel.setText(_translate("LoginWindow", "Quantity", None))
        self.submitButton_5.setText(_translate("LoginWindow", "Submit", None))
        self.EqipDetailsWidget.setTabText(self.EqipDetailsWidget.indexOf(self.AddEquipmenttab), _translate("LoginWindow", "Add Equipments", None))
        self.load_dataButton.setText(_translate("LoginWindow", "Load", None))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("LoginWindow", "Name", None))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("LoginWindow", "Date Of Purchase", None))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("LoginWindow", "Cost", None))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("LoginWindow", "Quantity", None))
        self.EqipDetailsWidget.setTabText(self.EqipDetailsWidget.indexOf(self.ViewEquipmenttab), _translate("LoginWindow", "View Equipments", None))
        self.firstNameLabel_6.setText(_translate("LoginWindow", "First Name ", None))
        self.lastNameLabel_6.setText(_translate("LoginWindow", "Last Name", None))
        self.customerIDLabel_2.setText(_translate("LoginWindow", "Customer ID", None))
        self.lasteDateLabel.setText(_translate("LoginWindow", "Last Entry Date", None))
        self.progressEntryDateLabel.setText(_translate("LoginWindow", "Progress Entry Date", None))
        self.heightLabel.setText(_translate("LoginWindow", "Height", None))
        self.weightLabel.setText(_translate("LoginWindow", "Weight", None))
        self.load_dataButton_2.setText(_translate("LoginWindow", "Load", None))
        self.load_dataButton_3.setText(_translate("LoginWindow", "Add", None))
        self.ProgressWidget.setTabText(self.ProgressWidget.indexOf(self.AddProgresstab), _translate("LoginWindow", "Add Progress", None))
        self.firstNameLabel_7.setText(_translate("LoginWindow", "First Name", None))
        self.lastNameLabel_7.setText(_translate("LoginWindow", "Last Name", None))
        self.customerIDLabel_3.setText(_translate("LoginWindow", "Customer ID", None))
        self.load_dataButton_4.setText(_translate("LoginWindow", "Load Customer ID", None))
        self.load_dataButton_5.setText(_translate("LoginWindow", "Generate BMI Report", None))
        self.load_dataButton_6.setText(_translate("LoginWindow", "Generate Weight Report", None))
        self.load_dataButton_7.setText(_translate("LoginWindow", "Generate Height report", None))
        self.ProgressWidget.setTabText(self.ProgressWidget.indexOf(self.Trackprogrsstab), _translate("LoginWindow", "Track Progress", None))
        item = self.tableWidget_3.verticalHeaderItem(0)
        item.setText(_translate("LoginWindow", "1", None))
        item = self.tableWidget_3.verticalHeaderItem(1)
        item.setText(_translate("LoginWindow", "2", None))
        item = self.tableWidget_3.verticalHeaderItem(2)
        item.setText(_translate("LoginWindow", "3", None))
        item = self.tableWidget_3.verticalHeaderItem(3)
        item.setText(_translate("LoginWindow", "4", None))
        item = self.tableWidget_3.horizontalHeaderItem(0)
        item.setText(_translate("LoginWindow", "Customer ID", None))
        item = self.tableWidget_3.horizontalHeaderItem(1)
        item.setText(_translate("LoginWindow", "Date", None))
        item = self.tableWidget_3.horizontalHeaderItem(2)
        item.setText(_translate("LoginWindow", "Height", None))
        item = self.tableWidget_3.horizontalHeaderItem(3)
        item.setText(_translate("LoginWindow", "Weight", None))
        item = self.tableWidget_3.horizontalHeaderItem(4)
        item.setText(_translate("LoginWindow", "BMI", None))
        self.load_dataButton_8.setText(_translate("LoginWindow", "Load", None))
        self.ProgressWidget.setTabText(self.ProgressWidget.indexOf(self.ViewAllProgresstab), _translate("LoginWindow", "View All Progress", None))
        self.pushButton_8.setText(_translate("LoginWindow", "Show Graph", None))
        self.label_3.setText(_translate("LoginWindow", "Member Analysis Report", None))
        self.plainTextEdit.setPlainText(_translate("LoginWindow", "FitneessPro is a unisex Gym Management System. Member Analysis report displays the statistical data of the number of male and female customers who joined the gym  ", None))
        self.ReportsWidget.setTabText(self.ReportsWidget.indexOf(self.Membertab), _translate("LoginWindow", "Member Analysis", None))
        self.pushButton_9.setText(_translate("LoginWindow", "Show Graph", None))
        self.plainTextEdit_2.setPlainText(_translate("LoginWindow", "Every month number of customers join the Gym. This report displays the statistical data of how many customers join gym in each month.\n"
"\n"
"This record also helps to keep track of the business i.e. whether more marketing is needed or are there some improvements to be done, if the enrollments are decreasing.\nWe can also use it to track whether a newly added service is able to attract more customers,etc.", None))
        self.label_7.setText(_translate("LoginWindow", "Monthwise Analysis Report", None))
        self.ReportsWidget.setTabText(self.ReportsWidget.indexOf(self.MonthWisetab), _translate("LoginWindow", "Monthwise Report", None))
        self.pushButton_10.setText(_translate("LoginWindow", "Show Graph", None))
        self.plainTextEdit_3.setPlainText(_translate("LoginWindow", "FitnessPro mainly focuses on maintaining BMI of each and every customer.BMI is nothing but Body Mass Index which is calculated on the basis of formula (Weight x 10000 )/ Height^2.This report categorize customers according to Low BMI,Average BMI and High BMI.", None))
        self.label_10.setText(_translate("LoginWindow", "BMI Analysis Report", None))
        self.ReportsWidget.setTabText(self.ReportsWidget.indexOf(self.BMItab), _translate("LoginWindow", "BMI Analysis", None))
        self.pushButton_6.setText(_translate("LoginWindow", "Reports", None))
        self.pushButton_5.setText(_translate("LoginWindow", "Equipment Details", None))
        self.pushButton_4.setText(_translate("LoginWindow", "Progress", None))
        self.pushButton.setText(_translate("LoginWindow", "Batches", None))
        self.pushButton_2.setText(_translate("LoginWindow", "Customer", None))
        self.pushButton_3.setText(_translate("LoginWindow", "Employee Details", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    LoginWindow = QtGui.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec_())


"""
mysql> show tables;
+-------------------+
| Tables_in_project |
+-------------------+
| batch             |
| cust_gym_details  |
| cust_personal     |
| emp               |
| instrument        |
| progress          |
+-------------------+
6 rows in set (0.00 sec)

mysql> desc batch;
+----------+-------------+------+-----+---------+-------+
| Field    | Type        | Null | Key | Default | Extra |
+----------+-------------+------+-----+---------+-------+
| batchid  | varchar(10) | YES  |     | NULL    |       |
| time     | varchar(10) | YES  |     | NULL    |       |
| strength | varchar(10) | YES  |     | NULL    |       |
| trainer  | varchar(20) | YES  |     | NULL    |       |
+----------+-------------+------+-----+---------+-------+
4 rows in set (0.00 sec)

mysql> desc cust_gym_details;
+---------------+-------------+------+-----+---------+-------+
| Field         | Type        | Null | Key | Default | Extra |
+---------------+-------------+------+-----+---------+-------+
| subscription  | varchar(20) | YES  |     | NULL    |       |
| start_date    | varchar(15) | YES  |     | NULL    |       |
| end_date      | varchar(15) | YES  |     | NULL    |       |
| amount        | varchar(10) | YES  |     | NULL    |       |
| amount_status | varchar(10) | YES  |     | NULL    |       |
| pending_amount| varchar(10) | YES  |     | NULL    |       |
| trainer       | varchar(20) | YES  |     | NULL    |       |
| cust_id       | varchar(10) | YES  |     | NULL    |       |
| batch_id      | varchar(10) | YES  |     | NULL    |       |
+---------------+-------------+------+-----+---------+-------+
9 rows in set (0.00 sec)

mysql> desc cust_personal;
+------------+-------------+------+-----+---------+-------+
| Field      | Type        | Null | Key | Default | Extra |
+------------+-------------+------+-----+---------+-------+
| firstname  | varchar(20) | YES  |     | NULL    |       |
| lastname   | varchar(20) | YES  |     | NULL    |       |
| gender     | varchar(5)  | YES  |     | NULL    |       |
| email      | varchar(15) | YES  |     | NULL    |       |
| dob        | varchar(10) | YES  |     | NULL    |       |
| occupation | varchar(10) | YES  |     | NULL    |       |
| contact    | varchar(10) | YES  |     | NULL    |       |
| address    | varchar(10) | YES  |     | NULL    |       |
| height     | varchar(10) | YES  |     | NULL    |       |
| weight     | varchar(10) | YES  |     | NULL    |       |
| cust_id    | varchar(10) | YES  |     | NULL    |       |
+------------+-------------+------+-----+---------+-------+
11 rows in set (0.01 sec)

mysql> desc emp;
+------------+-------------+------+-----+---------+-------+
| Field      | Type        | Null | Key | Default | Extra |
+------------+-------------+------+-----+---------+-------+
| firstname  | varchar(15) | YES  |     | NULL    |       |
| lastname   | varchar(15) | YES  |     | NULL    |       |
| gender     | varchar(10) | YES  |     | NULL    |       |
| email      | varchar(25) | YES  |     | NULL    |       |
| dob        | varchar(10) | YES  |     | NULL    |       |
| contact    | varchar(10) | YES  |     | NULL    |       |
| address    | varchar(20) | YES  |     | NULL    |       |
| experience | varchar(15) | YES  |     | NULL    |       |
+------------+-------------+------+-----+---------+-------+
8 rows in set (0.00 sec)

mysql> desc instrument;
+----------------+-------------+------+-----+---------+-------+
| Field          | Type        | Null | Key | Default | Extra |
+----------------+-------------+------+-----+---------+-------`+
| name           | varchar(15) | YES  |     | NULL    |       |
| dateofpurchase | varchar(10) | YES  |     | NULL    |       |
| cost           | varchar(10) | YES  |     | NULL    |       |
| quantity       | varchar(10) | YES  |     | NULL    |       |
+----------------+-------------+------+-----+---------+-------+
4 rows in set (0.01 sec)

mysql> desc progress;
+---------+-------------+------+-----+---------+-------+
| Field   | Type        | Null | Key | Default | Extra |
+---------+-------------+------+-----+---------+-------+
| cust_id | varchar(10) | YES  |     | NULL    |       |
| date   | varchar(15) | YES  |     | NULL    |       |
| height  | varchar(10) | YES  |     | NULL    |       |
| weight  | varchar(10) | YES  |     | NULL    |       |
| bmi     | varchar(10) | YES  |     | NULL    |       |
+---------+-------------+------+-----+---------+-------+


"""

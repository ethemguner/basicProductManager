from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import datetime
import sqlite3
from PyQt5.QtWidgets import QMessageBox


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.setWindowTitle("Product Manager")
        
        self.setTheme() ## set app. theme.
        self.setDisableButtons() ## set all buttons and line edits disable until user connect to db correctly.
        self.createProductTable() ## db connection and creating table.
        self.listProducts() ## set all product into the combo box.
        
    def createProductTable(self):
        ## Database connection / creating table.
        self.dbConn = sqlite3.connect("products.db")
        self.cursor = self.dbConn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS myProducts (serial_number INT, name TEXT, model TEXT, info TEXT, price INT, amount INT, op_time TEXT)")
        self.dbConn.commit() ## ready.

    ## will use for administrator connection.
    def adminControl(self, admin_id, admin_pass):
        ## Database connection.
        self.dbConn = sqlite3.connect("products.db")
        self.cursor = self.dbConn.cursor()
        ## Create a table which includes administrator ID and PASSWORD.
        self.cursor.execute("CREATE TABLE IF NOT EXISTS administrator (id TEXT, password TEXT)")
        self.dbConn.commit()
        ## With fetchone, we take admin ID from administrator table.
        self.cursor.execute("SELECT id FROM administrator")
        self.adminID = self.cursor.fetchone()[0] ## defined as adminID.
        ## With fetchone, we take admin PASS from administrator table.
        self.cursor.execute("SELECT password FROM administrator")
        self.adminPASS = self.cursor.fetchone()[0] ## defined as adminPASS.
        
        
        if admin_id != self.adminID or admin_pass != self.adminPASS:
                 self.db_status_label.setStyleSheet("QLabel {color: #FF2D00;}")
                 self.db_status_label.setText("not connected")
                 self.msg_box.setIcon(QtWidgets.QMessageBox.Critical)
                 self.msg_box.setText("Connection failed! ID or password is incorrect.")
                 self.msg_box.setWindowTitle("Failure")
                 self.msg_box.exec_()
                 self.setDisableButtons()
                 ## Giving an error and running setEnableButton. 
        else:
            self.db_status_label.setStyleSheet("QLabel {color: #00FF49;}")
            self.db_status_label.setText("connected successfuly")
            self.admin_id_lineedit.setEnabled(False)
            self.admin_pass_lineedit.setEnabled(False)
            self.adminConnectButton.setEnabled(False)
            
            self.msg_box.setIcon(QtWidgets.QMessageBox.Information)
            self.msg_box.setText("Connection successful. Database operations are enable.")
            self.msg_box.setWindowTitle("Succeed.")
            self.msg_box.exec_()
            
            self.productAmount_lineedit.setEnabled(True)
            self.productName_lineedit.setEnabled(True)
            self.productSerial_lineedit.setEnabled(True)
            self.productModel_lineedit.setEnabled(True)
            self.productInfo_lineedit.setEnabled(True)
            self.productPrice_lineedit.setEnabled(True)
            self.addDatabaseButton.setEnabled(True)
            self.editProductsButton.setEnabled(True)
            self.deleteProductButton.setEnabled(True)
            self.product_cb.setEnabled(True)
            self.saveButton.setEnabled(True)
            ## Set green db status label color.
            ## Clear admin id and pass line edits.
            ## Giving a message box, saying that connection successful.
            ## Set all line edits and buttons enable.
        
    def init_ui(self):
        
        ## Message box for warnings.
        self.msg_box = QtWidgets.QMessageBox()        
        ## Labels here.
        self.admin_label = QtWidgets.QLabel("Database Connection")
        self.admin_id_label = QtWidgets.QLabel("Administrator ID:")
        self.admin_pass_label = QtWidgets.QLabel("Administrator Password:")
        self.product_title_label = QtWidgets.QLabel("ADD PRODUCT")
        self.productName_label = QtWidgets.QLabel("Product name:")
        self.productSerial_label = QtWidgets.QLabel("Product serial number:")
        self.productModel_label = QtWidgets.QLabel("Product model:")
        self.productInfo_label = QtWidgets.QLabel("Product description:")
        self.productPrice_label = QtWidgets.QLabel("Product price:")
        self.productAmount_label = QtWidgets.QLabel("Prodcut amount:")
        ## LineEdits here.
        self.admin_id_lineedit = QtWidgets.QLineEdit()
        self.admin_pass_lineedit = QtWidgets.QLineEdit()
        self.admin_pass_lineedit.setEchoMode(QtWidgets.QLineEdit.Password) ## password mode.
        self.productName_lineedit = QtWidgets.QLineEdit()
        self.productSerial_lineedit = QtWidgets.QLineEdit()
        self.productModel_lineedit = QtWidgets.QLineEdit()
        self.productInfo_lineedit = QtWidgets.QLineEdit()
        self.productPrice_lineedit = QtWidgets.QLineEdit()
        self.productAmount_lineedit = QtWidgets.QLineEdit()
        ## Push buttons here.
        self.adminConnectButton = QtWidgets.QPushButton("Connect Database")
        self.addDatabaseButton = QtWidgets.QPushButton("Add Product to Database")
        ## vbox2 WIDGET AREA ---------------------------------------------------------------
        ## vbox2 labels.
        self.editProducts_title_label = QtWidgets.QLabel("EDIT PRODUCTS")
        self.productName_label2 = QtWidgets.QLabel("Product name:")
        self.productSerial_label2 = QtWidgets.QLabel("Product serial number:")
        self.productModel_label2 = QtWidgets.QLabel("Product model:")
        self.productInfo_label2 = QtWidgets.QLabel("Product description:")
        self.productPrice_label2 = QtWidgets.QLabel("Product price:")
        self.productAmount_label2 = QtWidgets.QLabel("Prodcut amount:")
        self.welcome_label = QtWidgets.QLabel("You can edit your products at this area.")
        self.db_con_label = QtWidgets.QLabel("Database connection:")
        self.db_status_label = QtWidgets.QLabel("not connected")
        ## vbox2 LineEdits.
        self.productName_lineedit2 = QtWidgets.QLineEdit()
        self.productSerial_lineedit2 = QtWidgets.QLineEdit()
        self.productModel_lineedit2 = QtWidgets.QLineEdit()
        self.productInfo_lineedit2 = QtWidgets.QLineEdit()
        self.productPrice_lineedit2 = QtWidgets.QLineEdit()
        self.productAmount_lineedit2 = QtWidgets.QLineEdit()
        ## vbox2 buttons.
        self.editProductsButton = QtWidgets.QPushButton("Edit Product")
        self.deleteProductButton = QtWidgets.QPushButton("Delete Product")
        self.saveButton = QtWidgets.QPushButton("Save Edits")
        ## Combobox and its settings.
        self.product_cb = QtWidgets.QComboBox()
        
        ## Vertical layout boxes.
        vbox = QtWidgets.QVBoxLayout()
        vbox2 = QtWidgets.QVBoxLayout()
        
        ## Admin connection.
        vbox.addWidget(self.admin_label)
        vbox.addWidget(self.admin_id_label)
        vbox.addWidget(self.admin_id_lineedit)
        vbox.addWidget(self.admin_pass_label)
        vbox.addWidget(self.admin_pass_lineedit)
        vbox.addWidget(self.adminConnectButton)
        ## Add Product.
        vbox.addWidget(self.product_title_label)
        vbox.addWidget(self.productName_label)
        vbox.addWidget(self.productName_lineedit)
        vbox.addWidget(self.productSerial_label)
        vbox.addWidget(self.productSerial_lineedit)
        vbox.addWidget(self.productModel_label)
        vbox.addWidget(self.productModel_lineedit)
        vbox.addWidget(self.productInfo_label)
        vbox.addWidget(self.productInfo_lineedit)
        vbox.addWidget(self.productPrice_label)
        vbox.addWidget(self.productPrice_lineedit)
        vbox.addWidget(self.productAmount_label)
        vbox.addWidget(self.productAmount_lineedit)
        vbox.addWidget(self.addDatabaseButton)
        ## vbox2 AREA -------------------------------------------
        vbox2.addWidget(self.editProducts_title_label)
        vbox2.addWidget(self.welcome_label)
        vbox2.addWidget(self.db_con_label)
        vbox2.addWidget(self.db_status_label)
        vbox2.addWidget(self.product_cb)
        vbox2.addWidget(self.productName_label2)
        vbox2.addWidget(self.productName_lineedit2)
        vbox2.addWidget(self.productSerial_label2)
        vbox2.addWidget(self.productSerial_lineedit2)
        vbox2.addWidget(self.productModel_label2)
        vbox2.addWidget(self.productModel_lineedit2)
        vbox2.addWidget(self.productInfo_label2)
        vbox2.addWidget(self.productInfo_lineedit2)
        vbox2.addWidget(self.productPrice_label2)
        vbox2.addWidget(self.productPrice_lineedit2)
        vbox2.addWidget(self.productAmount_label2)
        vbox2.addWidget(self.productAmount_lineedit2)
        vbox2.addWidget(self.editProductsButton)
        vbox2.addWidget(self.saveButton)
        vbox2.addWidget(self.deleteProductButton)

        ## Buttons are connecting their functions.
        self.adminConnectButton.clicked.connect(lambda : self.adminControl(self.admin_id_lineedit.text(), self.admin_pass_lineedit.text()))
        self.addDatabaseButton.clicked.connect(lambda: self.confirmProductData(self.productSerial_lineedit.text(), 
                                                                               self.productName_lineedit.text(),
                                                                               self.productModel_lineedit.text(), 
                                                                               self.productInfo_lineedit.text(),
                                                                               self.productPrice_lineedit.text(), 
                                                                               self.productAmount_lineedit.text()))
        self.editProductsButton.clicked.connect(self.editingProcess)
        self.saveButton.clicked.connect(self.updateProducts)
        self.deleteProductButton.clicked.connect(self.deleteProcess)
        
        ## Horizontal layout box
        hbox = QtWidgets.QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addLayout(vbox2)
        

        self.setLayout(hbox)
        self.show() ## user interface loaded.
        
    ## Disable all buttons and line edits.
    def setDisableButtons(self):
        self.addDatabaseButton.setEnabled(False)
        self.productAmount_lineedit.setEnabled(False)
        self.productName_lineedit.setEnabled(False)
        self.productSerial_lineedit.setEnabled(False)
        self.productModel_lineedit.setEnabled(False)
        self.productInfo_lineedit.setEnabled(False)
        self.productPrice_lineedit.setEnabled(False)
        ## vbox2 disable line edits and buttons.
        self.productAmount_lineedit2.setEnabled(False)
        self.productName_lineedit2.setEnabled(False)
        self.productSerial_lineedit2.setEnabled(False)
        self.productModel_lineedit2.setEnabled(False)
        self.productInfo_lineedit2.setEnabled(False)
        self.productPrice_lineedit2.setEnabled(False)
        self.editProductsButton.setEnabled(False)
        self.deleteProductButton.setEnabled(False)
        self.product_cb.setEnabled(False)
        self.saveButton.setEnabled(False)
        
    ## Bring product list into the combo box.
    def listProducts(self):
        self.product_cb.clear()
        self.dbConn = sqlite3.connect("products.db")
        self.cursor = self.dbConn.cursor()

        self.dbConn = sqlite3.connect("products.db")
        self.cursor = self.dbConn.cursor()
        
        self.cursor.execute("SELECT name FROM myProducts")
        self.productList = self.cursor.fetchall()
        self.productLength = len(self.productList)
        
        for i in range(0, self.productLength):
            self.productList = list(map(str, self.productList))
            product = self.productList[i].replace(",","").replace("(","").replace(")","").replace("'","")
            self.product_cb.addItems([product])

    def editingProcess(self):
        
        ## Set free line edits for edit.
        self.productAmount_lineedit2.setEnabled(True)
        self.productName_lineedit2.setEnabled(True)
        self.productSerial_lineedit2.setEnabled(True)
        self.productModel_lineedit2.setEnabled(True)
        self.productInfo_lineedit2.setEnabled(True)
        self.productPrice_lineedit2.setEnabled(True)
        
        ## DB connection.
        self.dbConn = sqlite3.connect("products.db")
        self.cursor = self.dbConn.cursor()
        
        self.cursor.execute("SELECT name FROM myProducts")
        productList = self.cursor.fetchall()
        productList_length = len(productList)
        cbText = self.product_cb.currentText()
        ## Listed product names. Also take length of name column.
        ## Define combobox current text. Will use for if condition.
        
        for i in range(0,productList_length):
            ## Mapping and clear the data that comes from name column.
            productList = list(map(str, productList))
            product = productList[i].replace(",","").replace("(","").replace(")","").replace("'","") ## all clear.
            
            ## If selected product name matched with product name:
            if cbText == product:
                ## Taking all data about this product name. serial_number, model, info, price, amount.
                self.cursor.execute("SELECT serial_number FROM myProducts WHERE name= ?",[product])
                self.serial_number = self.cursor.fetchall()
                self.serial_number = list(map(str, self.serial_number))
                self.sn = self.serial_number[0].replace(",","").replace("(","").replace(")","").replace("'","")
                
                self.cursor.execute("SELECT name FROM myProducts WHERE name= ?",[product])
                self.name = self.cursor.fetchall()
                self.name = list(map(str, self.name))
                self.produtName = self.name[0].replace(",","").replace("(","").replace(")","").replace("'","")
                
                self.cursor.execute("SELECT model FROM myProducts WHERE name= ?",[product])
                self.model = self.cursor.fetchall()
                self.model = list(map(str, self.model))
                self.productModel = self.model[0].replace(",","").replace("(","").replace(")","").replace("'","")

                self.cursor.execute("SELECT info FROM myProducts WHERE name= ?",[product])
                self.info = self.cursor.fetchall()
                self.info = list(map(str, self.info))
                self.productDescription = self.info[0].replace(",","").replace("(","").replace(")","").replace("'","")

                self.cursor.execute("SELECT price FROM myProducts WHERE name= ?",[product])
                self.price = self.cursor.fetchall()
                self.price = list(map(str, self.price))
                self.productPrice = self.price[0].replace(",","").replace("(","").replace(")","").replace("'","")
                
                self.cursor.execute("SELECT amount FROM myProducts WHERE name= ?",[product])
                self.amount = self.cursor.fetchall()
                self.amount = list(map(str, self.amount))
                self.productAmount = self.amount[0].replace(",","").replace("(","").replace(")","").replace("'","")
                
                ## Set all data onto line edits.
                self.productAmount_lineedit2.setText(str(self.productAmount))
                self.productName_lineedit2.setText(str(self.produtName))
                self.productSerial_lineedit2.setText(str(self.sn))
                self.productModel_lineedit2.setText(str(self.productModel))
                self.productInfo_lineedit2.setText(str(self.productDescription))
                self.productPrice_lineedit2.setText(str(self.productPrice))
                
                ## With that for loop, we show selected product's data on the ui -line edits- so, that way
                ## user can edit and can see old information about product.
        
    def updateProducts(self):
        
        self.V2inputControls()
        if self.isEverythingOK2 == True:
            ## DB connection.
            self.dbConn = sqlite3.connect("products.db")
            self.cursor = self.dbConn.cursor()
            
            self.cursor.execute("SELECT name FROM myProducts")
            productList = self.cursor.fetchall()
            productList_length = len(productList)
            cbText = self.product_cb.currentText()
            ## Listed product names. Also take length of name column.
            ## Define combobox current text. Will use for if condition.
            
            for i in range(0,productList_length):
                ## Mapping and clear the data that comes from name column.
                productList = list(map(str, productList))
                product = productList[i].replace(",","").replace("(","").replace(")","").replace("'","") ## all clear.
                
                ## If selected product name matched with product name:
                if cbText == product:
                    ## Taking all data about this product name. serial_number, model, info, price, amount.
                    self.cursor.execute("SELECT serial_number FROM myProducts WHERE name= ?",[product])
                    self.serial_number = self.cursor.fetchall()
                    self.serial_number = list(map(str, self.serial_number))
                    self.sn = self.serial_number[0].replace(",","").replace("(","").replace(")","").replace("'","")
                    
                    self.cursor.execute("SELECT name FROM myProducts WHERE name= ?",[product])
                    self.name = self.cursor.fetchall()
                    self.name = list(map(str, self.name))
                    self.produtName = self.name[0].replace(",","").replace("(","").replace(")","").replace("'","")
                    
                    self.cursor.execute("SELECT model FROM myProducts WHERE name= ?",[product])
                    self.model = self.cursor.fetchall()
                    self.model = list(map(str, self.model))
                    self.productModel = self.model[0].replace(",","").replace("(","").replace(")","").replace("'","")
    
                    self.cursor.execute("SELECT info FROM myProducts WHERE name= ?",[product])
                    self.info = self.cursor.fetchall()
                    self.info = list(map(str, self.info))
                    self.productDescription = self.info[0].replace(",","").replace("(","").replace(")","").replace("'","")
    
                    self.cursor.execute("SELECT price FROM myProducts WHERE name= ?",[product])
                    self.price = self.cursor.fetchall()
                    self.price = list(map(str, self.price))
                    self.productPrice = self.price[0].replace(",","").replace("(","").replace(")","").replace("'","")
                    
                    self.cursor.execute("SELECT amount FROM myProducts WHERE name= ?",[product])
                    self.amount = self.cursor.fetchall()
                    self.amount = list(map(str, self.amount))
                    self.productAmount = self.amount[0].replace(",","").replace("(","").replace(")","").replace("'","")
                    
                    self.cursor.execute("SELECT op_time FROM myProducts WHERE name= ?",[product])
                    self.op_time = self.cursor.fetchall()
                    self.op_time = list(map(str, self.amount))
                    self.productOpTime = self.op_time[0].replace(",","").replace("(","").replace(")","").replace("'","")
                    
                    ## For record operation time.
                    self.now = datetime.datetime.now()
                    self.today = self.now.strftime("%d/%m/%y")
                    self.hour_minute = self.now.strftime("%H:%M")
                    dt = self.hour_minute + " " + self.today
                    
                    ## Update all columns.
                    self.cursor.execute("UPDATE myProducts SET op_time = ? WHERE name = ?",(dt, self.produtName))
                    self.dbConn.commit()
                    self.cursor.execute("UPDATE myProducts SET serial_number = ? WHERE serial_number = ?",(self.productSerial_lineedit2.text(), self.sn))
                    self.dbConn.commit()
                    self.cursor.execute("UPDATE myProducts SET name = ? WHERE name = ?",(self.productName_lineedit2.text(), self.produtName))
                    self.dbConn.commit()
                    self.cursor.execute("UPDATE myProducts SET model = ? WHERE model = ?",(self.productModel_lineedit2.text(), self.productModel))
                    self.dbConn.commit()
                    self.cursor.execute("UPDATE myProducts SET info = ? WHERE info = ?",(self.productInfo_lineedit2.text(), self.productDescription))
                    self.dbConn.commit()
                    self.cursor.execute("UPDATE myProducts SET price = ? WHERE price = ?",(self.productPrice_lineedit2.text(), self.productPrice))
                    self.dbConn.commit()
                    self.cursor.execute("UPDATE myProducts SET amount = ? WHERE amount = ?",(self.productAmount_lineedit2.text(), self.productAmount))
                    self.dbConn.commit()
                    
                    self.listProducts() ## For update our combo box list. Otherwise, we may see duplicates in our combo box.
        else:
            self.msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg_box.setText("Fill all inputs please.")
            self.msg_box.setWindowTitle("An error occured.")
            self.msg_box.exec_()
    
    ## will use for insert data into our database.
    def confirmProductData(self,sn, name, model, info, price, amount): ## taking product information as parameter.
        self.V1inputControls() ## It controls inputs length if some of them is 0, it will return False
        
        ## If all inputs are fill.
        if self.isEverythingOK == True:
            
            ## At this point, we will control same product inputs. We don't want same product in our database.
            ## At least, we want different serial numbers. So, we control serial numbers.
            self.cursor.execute("SELECT serial_number FROM myProducts")
            self.fetch_sn = self.cursor.fetchall()  ## they're in here.
            fetch_sn_length = len(self.fetch_sn)  ## length of serial_number column.
            

            self.isSameProduct = bool  ## a boolean variable, we will define it later.
            
            if fetch_sn_length == 0:
                self.isSameProduct = False
            else:
                for k in range(0,fetch_sn_length):
                    self.fetch_sn = list(map(str, self.fetch_sn))
                    serial_numbers = self.fetch_sn[k].replace(",","").replace("(","").replace(")","").replace("'","")
                    print(fetch_sn_length)
                    
                    if serial_numbers == self.productSerial_lineedit.text():
                        self.isSameProduct = True
                    else:
                        self.isSameProduct = False
                
            if self.isSameProduct == False:
                ## We will take current date time and put it into the our database while product add.
                self.now = datetime.datetime.now()
                self.today = self.now.strftime("%d/%m/%y")
                self.hour_minute = self.now.strftime("%H:%M")
                dt = self.hour_minute + " " + self.today
                
                self.cursor.execute("INSERT INTO myProducts VALUES(?,?,?,?,?,?,?)", (sn, name, model, info, price, amount, dt))
                self.dbConn.commit() ## insert operation done.
                
                self.listProducts()
            else:
                self.msg_box.setIcon(QtWidgets.QMessageBox.Warning)
                self.msg_box.setText("Cannot add same product. Please enter different serial number.")
                self.msg_box.setWindowTitle("An error occured.")
                self.msg_box.exec_()
                
                ## First, we look length of column. If there is no column, we let the user add the product. 585.statment.
                ## In 593.statment, we compare our serial number and user serial number. If they are same, we don't add the product.
                ## Of course, we defined isSameProduct as True. So with that way, we control same products easily.
        else:
            self.msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg_box.setText("Fill all inputs please.")
            self.msg_box.setWindowTitle("An error occured.")
            self.msg_box.exec_()
            ## If there is any empty inputs.
            
    def deleteProcess(self):
        
        ## First we ask.
        self.questionMsgBox = QMessageBox.question(self, 'Warning', "Do you really want to delete the product?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        ## If the answer is yes->
        if self.questionMsgBox == QMessageBox.Yes:
            ## DB connection.
            self.dbConn = sqlite3.connect("products.db")
            self.cursor = self.dbConn.cursor()
            
            self.cursor.execute("SELECT name FROM myProducts")
            productList = self.cursor.fetchall()
            productList_length = len(productList)
            cbText = self.product_cb.currentText()
            
            for i in range(0,productList_length):
                ## Mapping and clear the data that comes from name column.
                productList = list(map(str, productList))
                product = productList[i].replace(",","").replace("(","").replace(")","").replace("'","") ## all clear.
                
                ## If selected product name matched with product name:
                if cbText == product:
                    ## Taking all data about this product name. serial_number, model, info, price, amount.
                    self.cursor.execute("DELETE FROM myProducts WHERE name = ?",[product])
                    self.dbConn.commit()
                    self.listProducts()
                else:
                    pass
        else:
            pass
        
    def V1inputControls(self):
            
        self.all_v1_inputs = [self.productAmount_lineedit.text(), self.productName_lineedit.text(),
                              self.productSerial_lineedit.text(), self.productModel_lineedit.text(),
                              self.productInfo_lineedit.text(), self.productPrice_lineedit.text()]
        
        self.isEverythingOK = bool
        for i in self.all_v1_inputs:
            if len(i) == 0:
                self.isEverythingOK = False
                break
            else:
                self.isEverythingOK = True
                
    def V2inputControls(self):
    
        self.all_v2_inputs = [self.productName_lineedit2.text(), self.productAmount_lineedit2.text(),
                              self.productSerial_lineedit2.text(), self.productModel_lineedit2.text(),
                              self.productInfo_lineedit2.text(), self.productPrice_lineedit2.text()]
        
        self.isEverythingOK2 = bool
        for j in self.all_v2_inputs:
            if len(j) == 0:
                self.isEverythingOK2 = False
                break
            else:
                self.isEverythingOK2 = True        
                
    def setTheme(self):
        ## Creating fonts.
        self.labelFonts = QtGui.QFont("Trebuchet MS", 11, QtGui.QFont.Bold)
        self.titleLabel = QtGui.QFont("Trebuchet MS", 13, QtGui.QFont.Bold)
        self.lineEditFonts = QtGui.QFont("Trebuchet MS", 9, QtGui.QFont.Bold)
        self.buttonFonts = QtGui.QFont("Corbel", 11, QtGui.QFont.Bold)
        self.infoLabelFonts = QtGui.QFont("Trebuchet MS", 8, QtGui.QFont.Bold)
        
        ## Titles fonts.
        self.admin_label.setFont(self.titleLabel)
        self.product_title_label.setFont(self.titleLabel)
        ## Labels fonts.
        self.admin_id_label.setFont(self.labelFonts)
        self.admin_pass_label.setFont(self.labelFonts)
        self.productName_label.setFont(self.labelFonts)
        self.productSerial_label.setFont(self.labelFonts)
        self.productModel_label.setFont(self.labelFonts)
        self.productInfo_label.setFont(self.labelFonts)
        self.productPrice_label.setFont(self.labelFonts)
        self.productAmount_label.setFont(self.labelFonts)
        ## Line edits fonts.
        self.admin_id_lineedit.setFont(self.lineEditFonts)
        self.admin_pass_lineedit.setFont(self.lineEditFonts)
        self.productName_lineedit.setFont(self.lineEditFonts)
        self.productSerial_lineedit.setFont(self.lineEditFonts)
        self.productModel_lineedit.setFont(self.lineEditFonts)
        self.productInfo_lineedit.setFont(self.lineEditFonts)
        self.productPrice_lineedit.setFont(self.lineEditFonts)
        self.productAmount_lineedit.setFont(self.lineEditFonts)
        ## Buttons fonts.
        self.adminConnectButton.setFont(self.buttonFonts)
        self.addDatabaseButton.setFont(self.buttonFonts)
        ## Tite styleSheet.
        self.admin_label.setStyleSheet("QLabel {color: #FFD700;}")
        self.product_title_label.setStyleSheet("QLabel {color: #FFD700;}")
        ## Labels styleSheet.
        self.admin_id_label.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.admin_pass_label.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.productName_label.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.productSerial_label.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.productModel_label.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.productInfo_label.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.productPrice_label.setStyleSheet("QLabel {color: #FFFFFF;}")        
        self.productAmount_label.setStyleSheet("QLabel {color: #FFFFFF;}")
        ## Line edits styleSheet.
        self.admin_id_lineedit.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        self.admin_pass_lineedit.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        self.productName_lineedit.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        self.productSerial_lineedit.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        self.productModel_lineedit.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        self.productInfo_lineedit.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        self.productPrice_lineedit.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        self.productAmount_lineedit.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        ## Buttons styleSheet.
        self.adminConnectButton.setStyleSheet("QPushButton {background: #3F4041; color: #FFD700}")  
        self.addDatabaseButton.setStyleSheet("QPushButton {background: #3F4041; color: #FFD700}")
            
        ## --------------------------------------------------------------------------------------------------
        ## vbox2 AREA
        
        ## Titles fonts.
        self.editProducts_title_label.setFont(self.titleLabel)
        ## Combobox font.
        self.product_cb.setFont(self.lineEditFonts)
        ## Labels fonts.
        self.productName_label2.setFont(self.labelFonts)
        self.productSerial_label2.setFont(self.labelFonts)
        self.productModel_label2.setFont(self.labelFonts)
        self.productInfo_label2.setFont(self.labelFonts)
        self.productPrice_label2.setFont(self.labelFonts)
        self.productAmount_label2.setFont(self.labelFonts)
        self.welcome_label.setFont(self.labelFonts)
        self.db_con_label.setFont(self.labelFonts)
        self.db_status_label.setFont(self.labelFonts)
        ## Line edits fonts.
        self.productName_lineedit2.setFont(self.lineEditFonts)
        self.productSerial_lineedit2.setFont(self.lineEditFonts)
        self.productModel_lineedit2.setFont(self.lineEditFonts)
        self.productInfo_lineedit2.setFont(self.lineEditFonts)
        self.productPrice_lineedit2.setFont(self.lineEditFonts)
        self.productAmount_lineedit2.setFont(self.lineEditFonts)
        ## Buttons fonts.
        self.editProductsButton.setFont(self.buttonFonts)
        self.deleteProductButton.setFont(self.buttonFonts)
        self.saveButton.setFont(self.buttonFonts)
        ## Tite styleSheet.
        self.editProducts_title_label.setStyleSheet("QLabel {color: #FFD700;}")
        ## Labels styleSheet.
        self.productName_label2.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.productSerial_label2.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.productModel_label2.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.productInfo_label2.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.productPrice_label2.setStyleSheet("QLabel {color: #FFFFFF;}")        
        self.productAmount_label2.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.welcome_label.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.db_con_label.setStyleSheet("QLabel {color: #FFFFFF;}")
        self.db_status_label.setStyleSheet("QLabel {color: #FF2D00;}")
        ## Line edits styleSheet.
        self.productName_lineedit2.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        self.productSerial_lineedit2.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        self.productModel_lineedit2.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        self.productInfo_lineedit2.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        self.productPrice_lineedit2.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        self.productAmount_lineedit2.setStyleSheet("QLineEdit {background: #A2CDF3; color: 'black'}")
        ## Buttons styleSheet.
        self.editProductsButton.setStyleSheet("QPushButton {background: #3F4041; color: #FFD700}")  
        self.deleteProductButton.setStyleSheet("QPushButton {background: #3F4041; color: #FFD700}")
        self.saveButton.setStyleSheet("QPushButton {background: #3F4041; color: #FFD700}")
            
        ## Alignments.
        self.admin_label.setAlignment(QtCore.Qt.AlignCenter)
        self.product_title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.editProducts_title_label.setAlignment(QtCore.Qt.AlignCenter)
        
app = QtWidgets.QApplication(sys.argv)
window = Window()
window.move(700, 120)
app.setStyle("Fusion")
window.setFixedSize(620, 660)
window.setStyleSheet("Window {background : #000080;}")
sys.exit(app.exec_())


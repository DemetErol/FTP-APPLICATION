from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import*
import ftplib
import os
from PyQt5.uic.properties import QtGui


class loadUi_example(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("ftpapp.ui",self)
        self.setWindowTitle("FTP APP.")
        self.login.clicked.connect(self.login_)
        self.msg = QMessageBox()

    def ftp_list(self,ftp):
        lst = ftp.nlst()
        # dosyaları list widget ile göster
        for each in lst:
            item=QListWidgetItem(each)
            if self.is_dir(each):
                 item.setForeground(Qt.red)
            self.list_ftp.addItem(item)

    def os_list(self):
        # os dosyaları list widget ile göster
        try:
            for each in os.listdir():
                item2 = QListWidgetItem(each)
                if os.path.isdir(each):
                    item2.setForeground(Qt.red)
                self.list_.addItem(item2)
        except:
            self.msg.setText("Directory is empty")
            self.msg.exec()

    def os_start(self):
        self.p = os.getcwd()
        #root klasörden başlat
        try:
            os.chdir(self.p.split(":\\")[0]+":\\")
        except:
            os.chdir(self.p)

    def login_(self):
        #eğer üçü de boş değilse(şifre kullanıcı adı ve ip)
        if self.user.text() and self.pswrd.text() and self.ip.text():
            try:
                #bağlan
                self.ftp=ftplib.FTP(self.ip.text(), self.user.text(), self.pswrd.text())

                if self.ftp:
                    loadUi("ftp_.ui", self)
                    self.setWindowTitle("FTP APPLICATION")
                    self.ftp_list(self.ftp) #ftp dosyaları listele
                    self.os_start() #os root klasöre gel
                    self.os_list() #os dosyaları listele
                    self.upload.clicked.connect(self.upload_)
                    self.download.clicked.connect(self.download_)
                    self.remove.clicked.connect(self.remove_)
                    self.rename.clicked.connect(self.rename_)
                    self.list_ftp.itemDoubleClicked.connect(self.go_ftp)
                    self.list_.itemDoubleClicked.connect(self.go_os)
                    self.create_dir.clicked.connect(self.create_d)
                    self.back.clicked.connect(self.back_ftp)
                    self.back_o.clicked.connect(self.back_os)
                    self.close.clicked.connect(self.close_)
            except:
                self.msg.setText("Login Failed")
                self.msg.exec()

        else:
            self.msg.setText("Fields cannot be empty")
            self.msg.exec()

    def upload_(self):

        # options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        # self.fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        # if self.fileName:
        #
        #     try:
        #         self.ftp.storbinary('STOR ' + os.path.split(self.fileName)[1], open(self.fileName, 'rb'))
        #         self.msg.setText("File uploaded successfully")
        #         self.msg.exec()
        #         self.list_ftp.clear()
        #         self.ftp_list(self.ftp)
        #     except:
        #         self.msg.setText("Don't select directory")
        #         self.msg.exec()


        self.filename= self.list_.currentItem().text()
        if os.path.isdir(self.filename):
            self.msg.setText("Don't select directory")
            self.msg.exec()
        else:
            try:
                with open(self.filename, "rb") as file:
                    self.ftp.storbinary("STOR "+self.filename, file)
                    self.msg.setText("File uploaded successfully")
                    self.msg.exec()
            except:
                self.msg.setText("Please, select a file")
                self.msg.exec()
            self.list_ftp.clear()
            self.ftp_list(self.ftp)


    def download_(self):
        try:
            self.filename= self.list_ftp.currentItem().text()
            if self.is_dir(self.filename):
                self.msg.setText("Don't select directory")
                self.msg.exec()
            else:
                self.ftp.retrbinary('RETR ' + self.filename, open(self.filename, 'wb').write, 1024)
                self.msg.setText("File downloaded successfully")
                self.msg.exec()

                self.list_.clear()
                self.os_list()

        except:
            self.msg.setText("Please, select a file")
            self.msg.exec()

    def remove_(self):
        #seçili dosyayı sil
        try:
            self.filename = self.list_ftp.currentItem().text()

            if self.is_dir(self.filename):
                try:
                    self.ftp.rmd(self.filename) #klasör sil
                    self.msg.setText("removed successfully")
                    self.msg.exec()
                except:
                    self.msg.setText("Directory is not empty, firstly delete files inside")
                    self.msg.exec()
            else:
                self.ftp.delete(self.filename) #file sil

            self.list_ftp.clear()
            self.ftp_list(self.ftp)
        except:
            self.msg.setText("Please,Select a file or an empty directory")
            self.msg.exec()

    def rename_(self):
        #yeniden adlandır
        try:
            self.filename = self.list_ftp.currentItem().text()
            if self.new_name.text():
                self.ftp.rename(self.filename,self.new_name.text())
                self.list_ftp.clear()
                self.ftp_list(self.ftp)
            else:
                self.msg.setText("Write a new name")
                self.msg.exec()
        except:
            self.msg.setText("Please, select a file")
            self.msg.exec()

    def go_ftp(self): #seçilen klasöre gir
        self.parent = self.ftp.pwd()
        try:
            self.ftp.cwd(self.list_ftp.currentItem().text())
        except:
            self.ftp.cwd(self.parent)
            self.msg.setText("This is a file, not a directory")
            self.msg.exec()
        self.list_ftp.clear()
        self.ftp_list(self.ftp)

    def create_d(self): #klasör oluştur.
        if self.dir.text():
            try:
                self.ftp.mkd(self.dir.text())
                self.msg.setText("created successfully")
                self.msg.exec()
            except:
                self.msg.setText("There is a folder with this name")
                self.msg.exec()
            self.list_ftp.clear()
            self.ftp_list(self.ftp)

    def back_ftp(self):
        try:
            self.ftp.cwd('..')
            self.list_ftp.clear()
            self.ftp_list(self.ftp)
        except:
            self.msg.setText("This is root directory")
            self.msg.exec()

    def is_dir(self,n): #klasör mü, dosya mı? klasör ise return true
        current = self.ftp.pwd()
        try:
            self.ftp.cwd(n)
        except:
            self.ftp.cwd(current)
            return False
        self.ftp.cwd(current)
        return True


    def go_os(self):
        #os seçilen klasöre gir
        self.p = os.getcwd()
        try:
            os.chdir(self.list_.currentItem().text())
        except:
            os.chdir(self.p)
            self.msg.setText("This is a file, not a directory")
            self.msg.exec()
        self.list_.clear()
        self.os_list()


    def back_os(self):
        #üst klasöre git
        try:
            os.chdir(os.path.abspath('..'))
            self.list_.clear()
            self.os_list()
        except:
            self.msg.setText("This is root directory")
            self.msg.exec()

    def close_(self):

        self.ftp.close()
        window.exec_()


app = QApplication([])
window = loadUi_example()
window.show()
app.exec_()






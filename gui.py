import wx
import subprocess
import searchencrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
import os
import sys
import json
from getpass import getpass
from base64 import b64encode, b64decode
import mysql.connector

########################################################################
class LoginDialog(wx.Dialog):
    """
    Class to define login dialog
    """
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Dialog.__init__(self, None, title="Login")
        self.logged_in = False
        
        # user info
        user_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        user_lbl = wx.StaticText(self, label="Username:")
        user_sizer.Add(user_lbl, 0, wx.ALL|wx.CENTER, 5)
        self.user = wx.TextCtrl(self)
        user_sizer.Add(self.user, 0, wx.ALL, 5)
        
        # pass info
        p_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        p_lbl = wx.StaticText(self, label="Password:")
        p_sizer.Add(p_lbl, 0, wx.ALL|wx.CENTER, 5)
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        self.password.Bind(wx.EVT_TEXT_ENTER, self.onLogin)
        p_sizer.Add(self.password, 0, wx.ALL, 5)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(user_sizer, 0, wx.ALL, 5)
        main_sizer.Add(p_sizer, 0, wx.ALL, 5)
        
        btn = wx.Button(self, label="Login")
        btn.Bind(wx.EVT_BUTTON, self.onLogin)
        main_sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        
        self.SetSizer(main_sizer)
        
    #----------------------------------------------------------------------
    def onLogin(self, event):
        """
        Check credentials and login
        """
        username= "symmetric"
        password = "encryption"
        user = self.user.GetValue()
        user_password = self.password.GetValue()
        if user_password == password and user==username:
            print ("You are now logged in!")
            self.logged_in = True
            self.Close()
        else:
            print ("Username or password is incorrect!")
            
########################################################################
class MyPanel(wx.Panel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        
    
########################################################################


class MainFrame(wx.Frame):
    """"""
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Searchable Symmetric Encryption")
        panel = MyPanel(self)

   #################################

        k_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        k_lbl = wx.StaticText(self, label="Keyword:")
        k_sizer.Add(k_lbl, 0, wx.ALL|wx.CENTER, 5)
        #self.keyword = wx.TextCtrl(self, style=wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        #self.keyword.Bind(wx.EVT_TEXT_ENTER, self.search)
        self.keyword = wx.TextCtrl(self)
        k_sizer.Add(self.keyword, 0, wx.ALL, 5)
        
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(k_sizer, 0, wx.ALL, 5)
        
        btn = wx.Button(self, label="Search")
        btn.Bind(wx.EVT_BUTTON, self.search)
        main_sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
        
        self.SetSizer(main_sizer)    


   ################################

        
        # Ask user to login
        dlg = LoginDialog()
        dlg.ShowModal()
        authenticated = dlg.logged_in
        if not authenticated:
            self.Close()
        
        self.Show()

    def search(self,event):    
        keyword = self.keyword.GetValue()
        db = searchencrypt.connectToDB('cloudstorage.cwyqmpoiw0xl.us-east-1.rds.amazonaws.com', 'symmetric', 'encryption', 'world')
        res=searchencrypt.search_by_blindindex(db, keyword, searchencrypt.idxkey)
        print(res)

        ##output to GUI

        #wx.MessageBox("hi" , res)
        wx.MessageBox("%s" %res, "search result")
        

        
        
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()

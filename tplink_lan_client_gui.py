#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

In this LanClientGUI, we create three toggle buttons.
They will control the background color of a 
QtGui.QFrame. 

author: Jan Bodnar
website: zetcode.com 
last edited: September 2011
"""

import sys
from PyQt4 import QtGui
import tplink_dhcp_client_scrape as tpscrape

class LanClientGUI(QtGui.QWidget):
    
    def __init__(self):
        super(LanClientGUI, self).__init__()
        
        self.initUI()
    
    #ip from host name
    host_ip_dict = {}
    #button from host name
    host_but_dict ={}

    def initUI(self):      

        self.col = QtGui.QColor(0, 0, 0) 
       
        hbox = QtGui.QHBoxLayout()

        refresh_but = QtGui.QPushButton("Refresh",self)
        hbox.addWidget(refresh_but)
        refresh_but.clicked.connect(self.generate_list)
        
        self.clbox = QtGui.QVBoxLayout()
        hbox.addLayout(self.clbox)

        self.scrape = tpscrape.TPLINK_DHCP_LIST()
        self.generate_list()



        self.setGeometry(300, 300, 280, 170)
        self.setLayout(hbox)
        self.setWindowTitle('TPLINK LAN Client Lister')
        self.show()

        
    def generate_list(self):
        scrape_list = self.scrape.req_and_parse()
        # remove old buttons
        for hn in  self.host_but_dict:
            but = self.host_but_dict[hn]
            but.close()
        
        for entry_dict in scrape_list:
            if entry_dict:
                hname = entry_dict['hostName']
                ip = entry_dict['IPAddress']
                
                self.host_ip_dict[hname]=ip
                
                but = QtGui.QPushButton(hname,self)
                self.host_but_dict[hname]=but

                self.clbox.addWidget(but)
                but.clicked.connect(self.click_host)
            
    def click_host(self):
        sender = self.sender()
        dkey = str(sender.text().toAscii())
        # get the ip from the button name
        host_ip = self.host_ip_dict[dkey]

        cb = QtGui.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(host_ip, mode=cb.Clipboard)



        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = LanClientGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()  
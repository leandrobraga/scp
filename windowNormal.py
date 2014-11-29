# -*- coding: utf-8 -*-

#Copyright 2012 Leandro Quadros Durães Braga

#Este arquivo é parte do programa Sistema de Controle de Paciente(SCP)
#Sistema de Controle de Paciente(SCP) é um software livre; você pode redistribui-lo e/ou
#modifica-lo dentro dos termos da Licença Pública Geral GNU como
#publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença.
#Este programa é distribuido na esperança que possa ser  util,
#mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
#MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
#Você deve ter recebido uma cópia da Licença Pública Geral GNU
#junto com este programa, se não, escreva para a Fundação do Software
#Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import wx
import wx.grid
import shutil
import os

from datetime import date

ID_TOOLBAR_REGISTER_PATIENT = 100
ID_TOOLBAR_REGISTER_USER = 101
ID_TOOLBAR_BACKUP = 102
ID_TOOLBAR_RESTORE_BACKUP = 103

class WindowNormal(wx.Frame):

    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,'Sistema de Cadastro de Pacientes - ',size=(600,400),style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_WINDOW_MENU  )


        self.ico=wx.Icon("./imagens/thooth_.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.ico)

        self.panelManagerWindow = wx.Panel(self,1)
        self.panelManagerWindow.SetBackgroundColour(wx.WHITE)

        self.status = self.CreateStatusBar(number=4)
        self.status.SetStatusText(u"Usuário: "+user.name,1)
        self.status.SetStatusText("Login: "+user.login,2)
        self.status.SetStatusText(date.today().strftime("%d/%m/%Y"),3)

        self.toolBar = wx.ToolBar(self,id=wx.ID_ANY,pos=wx.DefaultPosition,size=wx.DefaultSize,style=wx.TB_TEXT)
        self.toolBar.AddLabelTool(ID_TOOLBAR_REGISTER_PATIENT,"Cadastro de Paciente", wx.Bitmap("./imagens/patient.png"),shortHelp='Cadastro de Pacientes')


        self.Bind(wx.EVT_MENU,self.registerPatientWindow,id=ID_TOOLBAR_REGISTER_PATIENT)
        self.Bind(wx.EVT_CLOSE,self.quit)

        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.Maximize()
        self.Show()

    def registerPatientWindow(self,event):

        import patientWindow
        patientWindow.PatientWindow(self)


    def quit(self,event):
        close_dial = wx.MessageDialog(None, 'Tem certeza que deseja sair?', 'Sair',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = close_dial.ShowModal()
        if ret == wx.ID_YES:
            self.MakeModal(False)
            self.Destroy()
        else:
            event.Veto()


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

#from models import User
from datetime import date

ID_TOOLBAR_REGISTER_PATIENT = 100
ID_TOOLBAR_REGISTER_USER = 101
ID_TOOLBAR_BACKUP = 102
ID_TOOLBAR_RESTORE_BACKUP = 103

class WindowMain(wx.Frame):

    def __init__(self,user):
        wx.Frame.__init__(self,None,-1,'Sistema de Cadastro de Pacientes - ',size=(600,400),style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_NO_WINDOW_MENU  )

        self.ico=wx.Icon("./imagens/thooth_.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.ico)

        self.panelManagerWindow = wx.Panel(self,1)
        self.panelManagerWindow.SetBackgroundColour(wx.WHITE)
        #self.panelManagerWindow.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        #self.bmp = wx.Image("./imagens/brasil.png", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        #self.bitmap1 = wx.StaticBitmap(self.panelManagerWindow, -1, self.bmp, (10,73))
        #self.panelManagerWindow.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        #dc = wx.ClientDC(self)
        #dc.DrawBitmap(self.bmp, 0,0, True)

        self.status = self.CreateStatusBar(number=4)
        self.status.SetStatusText(u"Usuário: "+user.name,1)
        self.status.SetStatusText("Login: "+user.login,2)
        self.status.SetStatusText(date.today().strftime("%d/%m/%Y"),3)

        self.toolBar = wx.ToolBar(self,id=wx.ID_ANY,pos=wx.DefaultPosition,size=wx.DefaultSize,style=wx.TB_TEXT)
        self.toolBar.AddLabelTool(ID_TOOLBAR_REGISTER_PATIENT,"Cadastro de Paciente", wx.Bitmap("./imagens/patient.png"),shortHelp='Cadastro de Pacientes')
        self.toolBar.AddLabelTool(ID_TOOLBAR_REGISTER_USER,"Cadastro de Usuário", wx.Bitmap("./imagens/users.png"),shortHelp='Cadastro de Usuário')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()

        self.toolBar.AddLabelTool(ID_TOOLBAR_BACKUP,"Backup", wx.Bitmap("./imagens/down.png"),shortHelp='Realiza processo de Backup da base de dados')
        self.toolBar.AddLabelTool(ID_TOOLBAR_RESTORE_BACKUP,"Restauração de Backup", wx.Bitmap("./imagens/upload.png"),shortHelp='Realiza restauração da base de dados a partir de um arquivo de backup gerado pelo sistema')


        self.Bind(wx.EVT_MENU,self.registerPatientWindow,id=ID_TOOLBAR_REGISTER_PATIENT)
        self.Bind(wx.EVT_MENU,self.registerUserWindow,id=ID_TOOLBAR_REGISTER_USER)
        self.Bind(wx.EVT_MENU,self.backup,id=ID_TOOLBAR_BACKUP)
        self.Bind(wx.EVT_MENU,self.restoreBackup,id=ID_TOOLBAR_RESTORE_BACKUP)
        self.Bind(wx.EVT_CLOSE,self.quit)


        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.Maximize()

        self.Show()


    def registerPatientWindow(self,event):
        import patientWindow
        patientWindow.PatientWindow(self)

    def registerUserWindow(self,event):
        #self.toolBar.EnableTool(ID_TOOLBAR_REGISTER_PATIENT,False)
        #self.toolBar.EnableTool(ID_TOOLBAR_REGISTER_USER,False)
        import userWindow
        userWindow.UserWindow(self)

    def backup(self,event):
        self.message = wx.MessageDialog(None, 'Para realizar o backup da base de dados é altamente recomendado,por motivos de segurança,que você escolha uma unidade diferente de onde está instalada a aplicação!', 'Info', wx.OK)
        self.message.ShowModal()

        dlgDir = wx.DirDialog(None,message="Escolha um diretório")
        if dlgDir.ShowModal() == wx.ID_OK:
            try:
                shutil.copy(os.getcwd()+'/db/database.sqlite',dlgDir.GetPath())
            except:
                self.message = wx.MessageDialog(None, 'Houve um erro na realização do seu backup!Por favor tente novamente!', 'Info', wx.OK)
                self.message.ShowModal()
                return 0
            self.message = wx.MessageDialog(None,'Backup realizado com sucesso!Um arquivo database.sqlite foi gerado no diretório escolhido!', 'Info', wx.OK)
            self.message.ShowModal()

    def restoreBackup(self,event):
        dlgDirFile = wx.FileDialog(None,message="Selecione o arquivo...",wildcard="*.sqlite")
        if dlgDirFile.ShowModal() == wx.ID_OK:
            if dlgDirFile.GetFilename() == 'database.sqlite':
                try:
                    shutil.copy(dlgDirFile.GetPath(),os.getcwd()+'/db')
                except:
                    self.message = wx.MessageDialog(None, 'Houve um erro na inesperado na restauração do seu backup!Por favor tente novamente!', 'Info', wx.OK)
                    self.message.ShowModal()
                    return 0
                self.message = wx.MessageDialog(None,'A restauração do Backup foi realizado com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()
            else:
                self.message = wx.MessageDialog(None,'O arquivo de backup deve ter EXATAMENTE o nome:\n\ndatabase.sqlite\n\n Caso este esteja alterado renome-o e repita o processo de Resauração de Backup !', 'Info', wx.OK)
                self.message.ShowModal()

    def quit(self,event):
        close_dial = wx.MessageDialog(None, 'Tem certeza que deseja sair?', 'Sair',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = close_dial.ShowModal()
        if ret == wx.ID_YES:
            self.MakeModal(False)
            self.Destroy()
        else:
            event.Veto()


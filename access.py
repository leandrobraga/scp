#!/usr/bin/python
# -*- coding: utf-8 -*-

#Copyright 2012 Leandro Quadros Durães Braga

#Este arquivo é parte do programa Sistema de Controle de Paciente(SCP)
#Sistema de Controle de Paciente(SCP) é um software livre;
#você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU como
#publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença.
#Este programa é distribuido na esperança que possa ser  util,
#mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
#MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
#Você deve ter recebido uma cópia da Licença Pública Geral GNU
#junto com este programa, se não, escreva para a Fundação do Software
#Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


import wx
import hashlib
from models import *
setup_all()

class Login(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,parent=None,id=wx.ID_ANY,title='Cadastro de Pacientes',style=  wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.Centre(wx.BOTH)

        self.ico=wx.Icon("./imagens/thooth_.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.ico)

        panelLogin = wx.Panel(self,1)

        self.vBox1 = wx.BoxSizer(wx.VERTICAL)
        self.hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hBox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hBox3 = wx.BoxSizer(wx.HORIZONTAL)

        self.labelUser = wx.StaticText(panelLogin,-1,'Usuário: ',pos=(5,34),style=wx.ALIGN_LEFT)
        self.inputUser = wx.TextCtrl(panelLogin,-1,pos=(60,30),size=(180,-1),style=wx.ALIGN_LEFT)

        self.hBox1.Add(self.labelUser,1,wx.LEFT,1)
        self.hBox1.Add(self.inputUser,1,8)

        self.vBox1.Add(self.hBox1,0, wx.EXPAND | wx.ALL, 10)

        self.labelPass = wx.StaticText(panelLogin,-1,'Senha: ',pos=(5,65),style=wx.ALIGN_LEFT)
        self.inputPass = wx.TextCtrl(panelLogin,-1,pos=(60,61),size=(180,-1),style=wx.ALIGN_LEFT|wx.TE_PASSWORD)

        self.hBox2.Add(self.labelPass,1,wx.LEFT,1)
        self.hBox2.Add(self.inputPass,1,8)

        self.vBox1.Add(self.hBox2,0, wx.EXPAND | wx.ALL, 10)

        self.btnEntrar = wx.Button(panelLogin,wx.ID_OK,label="Entrar",pos=(40,100))
        self.btnSair = wx.Button(panelLogin,wx.ID_EXIT,label="Sair",pos=(130,100))
        self.Bind(wx.EVT_BUTTON,self.valida,self.btnEntrar)
        self.Bind(wx.EVT_BUTTON,self.quit,self.btnSair)

        self.hBox3.Add(self.btnEntrar,1,wx.LEFT,1)
        self.hBox3.Add(self.btnSair,1,8)

        self.vBox1.Add(self.hBox3,0, wx.EXPAND | wx.ALL, 10)

        self.Bind(wx.EVT_CLOSE, self.closeWindow)

        self.SetSize((250,170))
        self.Show()

    def closeWindow(self,event):
        self.Destroy()

    def valida(self,event):
        user =  User.query.filter(User.login.like(self.inputUser.GetValue())).first()

        if user != None:
            if user.password == hashlib.sha1(self.inputPass.GetValue()).hexdigest():
                if user.level ==0:
                    self.Destroy()
                    import windowMain
                    windowMain.WindowMain(user)
                else:
                    self.Destroy()
                    import windowNormal
                    windowNormal.WindowNormal(user)

            else:
                self.errorLogin()
        else:
            self.errorLogin()

    def quit(self,event):
        self.Close(True)

    def errorLogin(self):
        self.dialog = wx.MessageDialog(self, "Nome do usuário ou senha inválidos.\nDigite-os novamente.", "Acesso Negado", wx.YES_DEFAULT| wx.ICON_INFORMATION)
        self.dialog.ShowModal()
        self.inputUser.SetValue('')
        self.inputPass.SetValue('')
        self.inputUser.SetFocus()

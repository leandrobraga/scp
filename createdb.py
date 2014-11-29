#!/usr/bin/python
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


from models import *
from elixir import *
import os
import shutil
import hashlib
import sys
import wx
import stat




class CreateUserMaster(wx.Frame):

    def __init__(self):

        dbDir = os.getcwd()+'/db'
        if os.path.exists(dbDir):
            shutil.rmtree(dbDir)
        os.makedirs(dbDir)

        setup_all()
        create_all()
        dir = dbDir+'/database.sqlite'


        wx.Frame.__init__(self,None,id=wx.ID_ANY,size=(560,300),pos=(300,170),title=u"Cadastro do Administrador do Sistema",style= wx.SYSTEM_MENU | wx.CAPTION | wx.CLIP_CHILDREN)
        self.panelUser = wx.Panel(self, wx.ID_ANY)

        self.welcomeStaticText = wx.StaticText(self.panelUser,-1,u'Antes de finalizar o processo de instalação é necessário fazer o cadastro de um usuário administrador.\nInforme os campos abaixo para fazer o cadastro deste usuário!',pos=(10,10),style=wx.ALIGN_LEFT)
        wx.StaticText(self.panelUser,-1,u'Nome',pos=(10,50),style=wx.ALIGN_LEFT)
        self.nameTextCtrl = wx.TextCtrl(self.panelUser,-1,pos=(10,70),size=(190,-1))
        wx.StaticText(self.panelUser,-1,u'Login',pos=(10,100),style=wx.ALIGN_LEFT)
        self.loginTextCtrl = wx.TextCtrl(self.panelUser,-1,pos=(10,120),size=(120,-1))
        self.loginTextCtrl.SetValue(u"administrador")
        wx.StaticText(self.panelUser,-1,u'Senha',pos=(10,160),style=wx.ALIGN_LEFT)
        self.passTextCtrl = wx.TextCtrl(self.panelUser,-1,pos=(10,180),size=(90,-1),style=wx.TE_PASSWORD)
        wx.StaticText(self.panelUser,-1,u'Confirma Senha',pos=(120,160),style=wx.ALIGN_LEFT)
        self.confirmpassTextCtrl = wx.TextCtrl(self.panelUser,-1,pos=(120,180),size=(90,-1),style=wx.TE_PASSWORD)

        self.okBtn = wx.Button(self.panelUser,wx.ID_OK,label=u"Cadastrar",pos=(180,220))
        self.okBtn.Bind(wx.EVT_BUTTON,self.save)
#-------------END BINDS--------------------------------------------------------------------

        self.MakeModal(True)
        self.Show()


    def save(self,event):
        if self.validaPassword(self.passTextCtrl.GetValue(),self.confirmpassTextCtrl.GetValue(),self.nameTextCtrl.GetValue(),self.loginTextCtrl.GetValue()):
            user1 = User(name=unicode(self.nameTextCtrl.GetValue()),login=unicode(self.loginTextCtrl.GetValue()),
                 password=unicode(hashlib.sha1(self.passTextCtrl.GetValue()).hexdigest()),
                 level=u'0')
            session.commit()
            self.message = wx.MessageDialog(None, u'Usuário cadastrado com sucesso!', u'Info', wx.OK)
            self.message.ShowModal()
            self.Destroy()


    def validaPassword(self,password,confirmPassword,name,login):
        if login =='':
            self.message = wx.MessageDialog(None, u'O campo login deve ser preenchido!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        if name =='':
            self.message = wx.MessageDialog(None, u'O campo nome deve ser preenchido!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        if len(password) <6:
            self.message = wx.MessageDialog(None, u'A senha deve ter no mínimo 6 caracteres!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        if password != confirmPassword:
            self.message = wx.MessageDialog(None, u'O campo Senha e Confirma Senha devem ser iguais!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        return 1
if __name__ == "__main__":
    app = wx.App()
    access = CreateUserMaster()
    app.MainLoop()





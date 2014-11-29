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
from wx.lib import masked
from models import Patient
from elixir import *

setup_all()

#ID para toolbar da janela de administrador
ID_TOOLBAR_PATIENT_NEW = 501
ID_TOOLBAR_PATIENT_SAVE = 502
ID_TOOLBAR_PATIENT_REMOVE = 503
ID_TOOLBAR_PATIENT_FIND = 504
ID_TOOLBAR_PATIENT_EDIT = 505
ID_TOOLBAR_PATIENT_CANCEL = 510
ID_TOOLBAR_PATIENT_FIRST = 506
ID_TOOLBAR_PATIENT_LAST = 507
ID_TOOLBAR_PATIENT_NEXT = 508
ID_TOOLBAR_PATIENT_PREVIOUS = 509

#ID para o dialog localizar
ID_FIND_SEARCH = 5041

current_index = 0

class PatientWindow(wx.MiniFrame):

    def __init__(self,parent):

        wx.MiniFrame.__init__(self,parent,id=wx.ID_ANY,size=(670,400),pos=(250,140),title="Cadastro de Pacientes",style=wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)

        self.currentIndex = 0
        self.totalIndex = len(Patient.query.all())-1


        self.parent = parent
        self.panelPatient = wx.Panel(self, wx.ID_ANY)

        self.ico=wx.Icon("./imagens/patient.ico", wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.ico)

        self.toolBar = wx.ToolBar(self,id=wx.ID_ANY,pos=wx.DefaultPosition,size=wx.DefaultSize,style=wx.TB_TEXT)

        self.toolBar.AddLabelTool(ID_TOOLBAR_PATIENT_FIRST,u"Primeiro", wx.Bitmap("./imagens/first.png"),shortHelp='Ir para o primeiro registro')
        self.toolBar.AddLabelTool(ID_TOOLBAR_PATIENT_PREVIOUS,u"Anterior", wx.Bitmap("./imagens/previous.png"),shortHelp='Registro anterior')
        self.toolBar.AddLabelTool(ID_TOOLBAR_PATIENT_NEXT,u"Próximo", wx.Bitmap("./imagens/next.png"),shortHelp='Próximo registro')
        self.toolBar.AddLabelTool(ID_TOOLBAR_PATIENT_LAST,u"Último", wx.Bitmap("./imagens/last.png"),shortHelp='Ir para o último registro')
        self.toolBar.AddSeparator()
        self.toolBar.AddSeparator()


        self.toolBar.AddLabelTool(ID_TOOLBAR_PATIENT_NEW,u"Novo (F2)", wx.Bitmap("./imagens/add.png"),shortHelp='Novo Registro')
        self.toolBar.AddLabelTool(ID_TOOLBAR_PATIENT_SAVE,u"Salvar", wx.Bitmap("./imagens/filesave.png"),shortHelp='Grava alterções no registro')
        self.toolBar.AddLabelTool(ID_TOOLBAR_PATIENT_REMOVE,u"Remover", wx.Bitmap("./imagens/remove.png"),shortHelp='Remove o registro atual')
        self.toolBar.AddLabelTool(ID_TOOLBAR_PATIENT_FIND,u"Localizar", wx.Bitmap("./imagens/find.png"),shortHelp='Localiza um Registro')
        self.toolBar.AddLabelTool(ID_TOOLBAR_PATIENT_EDIT,u"ALterar", wx.Bitmap("./imagens/edit.png"),shortHelp='Altera o registro atual')
        self.toolBar.AddLabelTool(ID_TOOLBAR_PATIENT_CANCEL,u"Cancelar", wx.Bitmap("./imagens/cancel.png"),shortHelp='Cancela ação')

        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_SAVE, False)

        self.toolBar.Realize()
        self.SetToolBar(self.toolBar)

        self.vBox1 = wx.BoxSizer(wx.VERTICAL)

        self.hBox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hBox2 = wx.BoxSizer(wx.HORIZONTAL)

        self.idTextCtrl = wx.TextCtrl(self.panelPatient,-1,pos=(10,15),size=(0,0))
        self.hBox2.Add( self.idTextCtrl,1, wx.LEFT,8)

        self.nameStaticText = wx.StaticText(self.panelPatient,-1,u'Nome',pos=(18,30),style=wx.ALIGN_LEFT)
        self.nameTextCtrl = wx.TextCtrl(self.panelPatient,-1,pos=(18,50),size=(400,-1),style=wx.TE_READONLY)
        self.hBox1.Add(self.nameStaticText, 1, wx.LEFT,8)
        self.hBox2.Add( self.nameTextCtrl,1, wx.LEFT,8)

        self.dateOfBirthStaticText = wx.StaticText(self.panelPatient,-1,u'Data de Nasc.',pos=(460,30),style=wx.ALIGN_LEFT)
        self.dateOfBirthTextCtrl = masked.TextCtrl(self.panelPatient,-1,mask="##/##/####")
        self.dateOfBirthTextCtrl.SetSize((90,-1))
        self.dateOfBirthTextCtrl.SetPosition((460,50))
        self.dateOfBirthTextCtrl.SetEditable(False)
        self.hBox1.Add(self.dateOfBirthStaticText,1,8)
        self.hBox2.Add(self.dateOfBirthTextCtrl,1,8)

        self.cpfStaticText = wx.StaticText(self.panelPatient,-1,u'CPF',pos=(18,90),style=wx.ALIGN_LEFT)
        self.cpfTextCtrl = masked.TextCtrl(self.panelPatient,-1,mask="###.###.###-##")
        self.cpfTextCtrl.SetSize((120,-1))
        self.cpfTextCtrl.SetPosition((18,110))
        self.cpfTextCtrl.SetEditable(False)
        self.hBox1.Add(self.cpfStaticText,1,8)
        self.hBox2.Add( self.cpfTextCtrl,1,8)

        self.rgStaticText = wx.StaticText(self.panelPatient,-1,u'RG',pos=(170,90),style=wx.ALIGN_LEFT)
        self.rgTextCtrl = wx.TextCtrl(self.panelPatient,-1,pos=(170,110),size=(120,-1),style=wx.TE_READONLY)
        self.hBox1.Add(self.rgStaticText,1,8)
        self.hBox2.Add( self.rgTextCtrl,1,8)

        self.telephoneStaticText = wx.StaticText(self.panelPatient,-1,u'Telefone',pos=(18,150),style=wx.ALIGN_LEFT)
        self.telephoneTextCtrl =  masked.TextCtrl(self.panelPatient,-1,mask="(##)####-####")
        self.telephoneTextCtrl.SetSize((120,-1))
        self.telephoneTextCtrl.SetPosition((18,170))
        self.telephoneTextCtrl.SetEditable(False)
        self.hBox1.Add(self.telephoneStaticText, 1,8)
        self.hBox2.Add( self.telephoneTextCtrl,1,8)

        self.telephone2StaticText = wx.StaticText(self.panelPatient,-1,u'Telefone 2',pos=(170,150),style=wx.ALIGN_LEFT)
        self.telephone2TextCtrl =  masked.TextCtrl(self.panelPatient,-1,mask="(##)####-####")
        self.telephone2TextCtrl.SetSize((120,-1))
        self.telephone2TextCtrl.SetPosition((170,170))
        self.telephone2TextCtrl.SetEditable(False)
        self.hBox1.Add(self.telephone2StaticText, 1,8)
        self.hBox2.Add( self.telephone2TextCtrl,1,8)

        wx.StaticBox(self.panelPatient,-1,u'Informações Pessoais',pos=(5,5),size=(600,220))

        self.treatmentStartStaticText = wx.StaticText(self.panelPatient,-1,u'Início do Trat.',pos=(18,250),style=wx.ALIGN_LEFT)
        self.treatmentStartTextCtrl = masked.TextCtrl(self.panelPatient,-1,mask="##/##/####")
        self.treatmentStartTextCtrl.SetSize((100,-1))
        self.treatmentStartTextCtrl.SetPosition((18,275))
        self.treatmentStartTextCtrl.SetEditable(False)
        self.hBox1.Add(self.treatmentStartStaticText,1,8)
        self.hBox2.Add(self.treatmentStartTextCtrl,1,8)

        self.budgetByStaticText = wx.StaticText(self.panelPatient,-1,u'Orçado por',pos=(140,250),style=wx.ALIGN_LEFT)
        self.budgetByTextCtrl = wx.TextCtrl(self.panelPatient,-1,pos=(140,275),size=(150,-1),style=wx.TE_READONLY)
        self.hBox1.Add(self.budgetByStaticText, 1, wx.LEFT,8)
        self.hBox2.Add(self.budgetByTextCtrl,1, wx.LEFT,8)

        self.registrationFormStaticText = wx.StaticText(self.panelPatient,-1,u'Ficha',pos=(320,250),style=wx.ALIGN_LEFT)
        self.registrationFormTextCtrl = wx.TextCtrl(self.panelPatient,-1,pos=(320,275),size=(100,-1),style=wx.TE_READONLY)
        self.hBox1.Add(self.registrationFormStaticText, 1,8)
        self.hBox2.Add(self.registrationFormTextCtrl,1,8)

        wx.StaticBox(self.panelPatient,-1,'',pos=(5,230),size=(600,80))

        self.vBox1.Add(self.hBox1,0, wx.EXPAND | wx.ALL, 10)
        self.vBox1.Add(self.hBox2,0, wx.EXPAND | wx.ALL, 10)


#-------------BINDS------------------------------------------------------------------------

        self.Bind(wx.EVT_MENU,self.getFirst,id=ID_TOOLBAR_PATIENT_FIRST)
        self.Bind(wx.EVT_MENU,self.getLast,id=ID_TOOLBAR_PATIENT_LAST)
        self.Bind(wx.EVT_MENU,self.getNext,id=ID_TOOLBAR_PATIENT_NEXT)
        self.Bind(wx.EVT_MENU,self.getPrevious,id=ID_TOOLBAR_PATIENT_PREVIOUS)
        self.Bind(wx.EVT_MENU,self.new,id=ID_TOOLBAR_PATIENT_NEW)
        self.Bind(wx.EVT_MENU,self.cancel,id=ID_TOOLBAR_PATIENT_CANCEL)
        self.Bind(wx.EVT_MENU,self.save,id=ID_TOOLBAR_PATIENT_SAVE)
        self.Bind(wx.EVT_MENU,self.edit,id=ID_TOOLBAR_PATIENT_EDIT)
        self.Bind(wx.EVT_MENU,self.remove,id=ID_TOOLBAR_PATIENT_REMOVE)
        self.Bind(wx.EVT_MENU,self.find,id=ID_TOOLBAR_PATIENT_FIND)
        self.Bind(wx.EVT_CLOSE,self.quit)
#-------------END BINDS--------------------------------------------------------------------
        self.MakeModal(True)
        self.Show()

        if not(self.totalIndex<0):
            self.getFirst(None)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_CANCEL, False)

    def getFirst(self,event):

        if self.totalIndex <0:
            return 0

        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIRST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_LAST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_PREVIOUS, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEXT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_SAVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_REMOVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_EDIT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIND, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_CANCEL, False)

        self.currentIndex = 0

        patient1 = Patient.query.order_by('registrationForm').limit(1).offset(self.currentIndex).first()

        patients12 = Patient.query.order_by('registrationForm').all()

        self.idTextCtrl.SetValue(unicode(patient1.id))
        self.nameTextCtrl.SetValue(unicode(patient1.name))
        self.dateOfBirthTextCtrl.SetValue(unicode(patient1.dateOfBirth))
        self.rgTextCtrl.SetValue(unicode(patient1.rg))
        self.cpfTextCtrl.SetValue(unicode(patient1.cpf))
        self.telephoneTextCtrl.SetValue(unicode(patient1.telephone))
        self.telephone2TextCtrl.SetValue(unicode(patient1.telephone))
        self.treatmentStartTextCtrl.SetValue(unicode(patient1.treatmentStart))
        self.budgetByTextCtrl.SetValue(unicode(patient1.budgetBy))
        self.registrationFormTextCtrl.SetValue(unicode(patient1.registrationForm))

    def getLast(self,event):

        if self.totalIndex <0:
            return 0


        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIRST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_LAST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_PREVIOUS, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEXT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_SAVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_REMOVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_EDIT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIND, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_CANCEL, False)

        self.currentIndex = self.totalIndex

        patient1 = Patient.query.order_by('registrationForm').limit(1).offset(self.currentIndex).first()

        self.idTextCtrl.SetValue(unicode(patient1.id))
        self.nameTextCtrl.SetValue(unicode(patient1.name))
        self.dateOfBirthTextCtrl.SetValue(unicode(patient1.dateOfBirth))
        self.rgTextCtrl.SetValue(unicode(patient1.rg))
        self.cpfTextCtrl.SetValue(unicode(patient1.cpf))
        self.telephoneTextCtrl.SetValue(unicode(patient1.telephone))
        self.telephone2TextCtrl.SetValue(unicode(patient1.telephone2))
        self.treatmentStartTextCtrl.SetValue(unicode(patient1.treatmentStart))
        self.budgetByTextCtrl.SetValue(unicode(patient1.budgetBy))
        self.registrationFormTextCtrl.SetValue(unicode(patient1.registrationForm))

    def getNext(self,event):

        if self.totalIndex <0:
            return 0

        if self.totalIndex == self.currentIndex:
            self.currentIndex = 0
        else:
            self.currentIndex = self.currentIndex+1

        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIRST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_LAST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_PREVIOUS, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEXT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_SAVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_REMOVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_EDIT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIND, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_CANCEL, False)

        patient1 = Patient.query.order_by('registrationForm').limit(1).offset(self.currentIndex).first()

        self.idTextCtrl.SetValue(unicode(patient1.id))
        self.nameTextCtrl.SetValue(unicode(patient1.name))
        self.dateOfBirthTextCtrl.SetValue(unicode(patient1.dateOfBirth))
        self.rgTextCtrl.SetValue(unicode(patient1.rg))
        self.cpfTextCtrl.SetValue(unicode(patient1.cpf))
        self.telephoneTextCtrl.SetValue(unicode(patient1.telephone))
        self.telephone2TextCtrl.SetValue(unicode(patient1.telephone2))
        self.treatmentStartTextCtrl.SetValue(unicode(patient1.treatmentStart))
        self.budgetByTextCtrl.SetValue(unicode(patient1.budgetBy))
        self.registrationFormTextCtrl.SetValue(unicode(patient1.registrationForm))

    def getPrevious(self,event):

        if self.totalIndex <0:
            return 0

        if self.currentIndex == 0:
            self.currentIndex = self.totalIndex
        else:
            self.currentIndex = self.currentIndex-1

        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIRST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_LAST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_PREVIOUS, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEXT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_SAVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_REMOVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_EDIT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIND, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_CANCEL, False)

        patient1 = Patient.query.order_by('registrationForm').limit(1).offset(self.currentIndex).first()

        self.idTextCtrl.SetValue(unicode(patient1.id))
        self.nameTextCtrl.SetValue(unicode(patient1.name))
        self.dateOfBirthTextCtrl.SetValue(unicode(patient1.dateOfBirth))
        self.rgTextCtrl.SetValue(unicode(patient1.rg))
        self.cpfTextCtrl.SetValue(unicode(patient1.cpf))
        self.telephoneTextCtrl.SetValue(unicode(patient1.telephone))
        self.telephone2TextCtrl.SetValue(unicode(patient1.telephone2))
        self.treatmentStartTextCtrl.SetValue(unicode(patient1.treatmentStart))
        self.budgetByTextCtrl.SetValue(unicode(patient1.budgetBy))
        self.registrationFormTextCtrl.SetValue(unicode(patient1.registrationForm))

    def new(self,event):
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIRST, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_LAST, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_PREVIOUS, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEXT, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEW, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_SAVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_REMOVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_EDIT, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIND, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_CANCEL, True)

        self.idTextCtrl.SetValue('')
        self.nameTextCtrl.SetValue('')
        self.nameTextCtrl.SetEditable(True)
        self.dateOfBirthTextCtrl.SetValue('')
        self.dateOfBirthTextCtrl.SetEditable(True)
        self.rgTextCtrl.SetValue('')
        self.rgTextCtrl.SetEditable(True)
        self.cpfTextCtrl.SetValue('')
        self.cpfTextCtrl.SetEditable(True)
        self.telephoneTextCtrl.SetValue('92')
        self.telephoneTextCtrl.SetEditable(True)
        self.telephone2TextCtrl.SetValue('92')
        self.telephone2TextCtrl.SetEditable(True)
        self.treatmentStartTextCtrl.SetValue('')
        self.treatmentStartTextCtrl.SetEditable(True)
        self.budgetByTextCtrl.SetValue('')
        self.budgetByTextCtrl.SetEditable(True)
        self.registrationFormTextCtrl.SetValue('')
        self.registrationFormTextCtrl.SetEditable(True)

        self.nameTextCtrl.SetFocus()

    def cancel(self,event):
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIRST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_LAST, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_PREVIOUS, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEXT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEW, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_SAVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_REMOVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_EDIT, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIND, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_CANCEL, False)

        self.nameTextCtrl.SetEditable(False)
        self.dateOfBirthTextCtrl.SetEditable(False)
        self.rgTextCtrl.SetEditable(False)
        self.cpfTextCtrl.SetEditable(False)
        self.telephoneTextCtrl.SetEditable(False)
        self.telephone2TextCtrl.SetEditable(False)
        self.treatmentStartTextCtrl.SetEditable(False)
        self.budgetByTextCtrl.SetEditable(False)
        self.registrationFormTextCtrl.SetEditable(False)

        if not(self.totalIndex<0):
            self.getFirst(None)

    def save(self,event):
        if self.idTextCtrl.GetValue() != '':

            if self.valida(int(self.idTextCtrl.GetValue()),self.nameTextCtrl.GetValue(),self.dateOfBirthTextCtrl.GetValue(),
                           self.telephoneTextCtrl.GetValue(),self.telephone2TextCtrl.GetValue(),self.treatmentStartTextCtrl.GetValue(),
                           self.budgetByTextCtrl.GetValue(),self.registrationFormTextCtrl.GetValue()):

                patient1 = Patient.get_by(id=self.idTextCtrl.GetValue())

                patient1.name = self.nameTextCtrl.GetValue().title()
                patient1.dateOfBirth = self.dateOfBirthTextCtrl.GetValue()
                patient1.rg = self.rgTextCtrl.GetValue()
                patient1.cpf = self.cpfTextCtrl.GetValue()
                patient1.telephone = self.telephoneTextCtrl.GetValue()
                patient1.telephone2 = self.telephone2TextCtrl.GetValue()
                patient1.treatmentStart = self.treatmentStartTextCtrl.GetValue()
                patient1.budgetBy = self.budgetByTextCtrl.GetValue()
                patient1.registrationForm = self.registrationFormTextCtrl.GetValue()

                session.commit()
                self.refreshIndex(self.idTextCtrl.GetValue())
                self.message = wx.MessageDialog(None, u'Paciente alterado com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()

                self.nameTextCtrl.SetEditable(False)
                self.dateOfBirthTextCtrl.SetEditable(False)
                self.rgTextCtrl.SetEditable(False)
                self.cpfTextCtrl.SetEditable(False)
                self.telephoneTextCtrl.SetEditable(False)
                self.telephone2TextCtrl.SetEditable(False)
                self.treatmentStartTextCtrl.SetEditable(False)
                self.budgetByTextCtrl.SetEditable(False)
                self.registrationFormTextCtrl.SetEditable(False)

                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIRST, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_LAST, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_PREVIOUS, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEXT, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEW, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_SAVE, False)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_REMOVE, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_EDIT, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIND, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_CANCEL, False)
        else:

            if self.valida(self.idTextCtrl.GetValue(),self.nameTextCtrl.GetValue(),self.dateOfBirthTextCtrl.GetValue(),
                           self.telephoneTextCtrl.GetValue(),self.telephone2TextCtrl.GetValue(),self.treatmentStartTextCtrl.GetValue(),
                           self.budgetByTextCtrl.GetValue(),self.registrationFormTextCtrl.GetValue()):

                patient1 = Patient(name=self.nameTextCtrl.GetValue().title(),dateOfBirth=self.dateOfBirthTextCtrl.GetValue(),
                                   rg=self.rgTextCtrl.GetValue(),cpf=self.cpfTextCtrl.GetValue(),
                                   telephone=self.telephoneTextCtrl.GetValue(),telephone2=self.telephone2TextCtrl.GetValue(),
                                   treatmentStart=self.treatmentStartTextCtrl.GetValue(),budgetBy=self.budgetByTextCtrl.GetValue(),
                                   registrationForm=self.registrationFormTextCtrl.GetValue())

                session.commit()

                self.refreshIndex(patient1.id)
                self.idTextCtrl.SetValue(unicode(patient1.id))
                self.message = wx.MessageDialog(None, u'Paciente cadastrado com sucesso!', 'Info', wx.OK)
                self.message.ShowModal()

                self.nameTextCtrl.SetEditable(False)
                self.dateOfBirthTextCtrl.SetEditable(False)
                self.rgTextCtrl.SetEditable(False)
                self.cpfTextCtrl.SetEditable(False)
                self.telephoneTextCtrl.SetEditable(False)
                self.telephone2TextCtrl.SetEditable(False)
                self.treatmentStartTextCtrl.SetEditable(False)
                self.budgetByTextCtrl.SetEditable(False)
                self.registrationFormTextCtrl.SetEditable(False)

                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIRST, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_LAST, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_PREVIOUS, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEXT, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEW, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_SAVE, False)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_REMOVE, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_EDIT, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIND, True)
                self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_CANCEL, False)

    def valida(self,id,name,dateOfBirth,telephone,telephone2,treatmentStart,budgetBy,registrationForm):
        patient1 = Patient.query.filter(Patient.name.like(name)).first()
        if patient1 !=None:
            if (patient1.name.upper() == name.upper()) and ( patient1.id == id):
                return 1
            else:
                self.message = wx.MessageDialog(None, u'Já existe um paciente cadastrado com este nome!', 'Info', wx.OK)
                self.message.ShowModal()
                self.nameTextCtrl.SetFocus()
                self.nameTextCtrl.SelectAll()

                return 0
        if name == '':
            self.message = wx.MessageDialog(None, u'O campo Nome deve ser preenchido!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        if dateOfBirth == '  /  /    ':
            self.message = wx.MessageDialog(None, u'O campo Data de nacimento deve ser preenchido!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0

        if telephone == '(  )    -    ' and len(telephone)!=13:
            self.message = wx.MessageDialog(None, u'O campo Telefone deve ser preenchido coretamente!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        if telephone2 == '(  )    -    ' and len(telephone2)!=13:
            self.message = wx.MessageDialog(None, u'O campo Telefone2 deve ser preenchido coretamente!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        if treatmentStart == '  /  /    ':
            self.message = wx.MessageDialog(None, u'O campo "Início do Tratamento" deve ser preenchido!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        if budgetBy == '':
            self.message = wx.MessageDialog(None, u'O campo "Orçado por" deve ser preenchido!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        if registrationForm == '':
            self.message = wx.MessageDialog(None, u'O campo Ficha deve ser preenchido!', 'Info', wx.OK)
            self.message.ShowModal()
            return 0
        return 1

    def refreshIndex(self,id):
        patients = Patient.query.order_by('registrationForm').all()
        if id != None:
            for index,patient in enumerate(patients):
                if patient.id == id:
                    self.currentIndex = index
                    self.totalIndex = len(patients)-1
                    break
        else:
            self.currentIndex = self.currentIndex-1
            self.totalIndex = len(patients)-1

    def edit(self,event):

        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIRST, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_LAST, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_PREVIOUS, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEXT, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_NEW, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_SAVE, True)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_REMOVE, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_EDIT, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_FIND, False)
        self.toolBar.EnableTool(ID_TOOLBAR_PATIENT_CANCEL, True)

        self.nameTextCtrl.SetEditable(True)
        self.dateOfBirthTextCtrl.SetEditable(True)
        self.rgTextCtrl.SetEditable(True)
        self.cpfTextCtrl.SetEditable(True)
        self.telephoneTextCtrl.SetEditable(True)
        self.telephone2TextCtrl.SetEditable(True)
        self.treatmentStartTextCtrl.SetEditable(True)
        self.budgetByTextCtrl.SetEditable(True)
        self.registrationFormTextCtrl.SetEditable(True)

    def remove(self,event):

        remove_dial = wx.MessageDialog(None, u'Tem certeza que deseja excluir este paciente?', 'Sair',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        ret = remove_dial.ShowModal()
        if ret == wx.ID_YES:
            patient1 = Patient.get_by(id=int(self.idTextCtrl.GetValue()))
            patient1.delete()
            session.commit()
            remove_dial.Destroy()
            self.refreshIndex(None)
            self.getNext(None)

        else:
            event.Veto()

    def find(self,event):

        import sys
        self.findDialog = wx.Dialog(parent=None,id=wx.ID_ANY,pos=(410,180),size=(430,700),title='Localizar Paciente')
        #self.findDialog.Centre(wx.BOTH)

        self.vPatientBox1 = wx.BoxSizer(wx.VERTICAL)

        self.hPatientBox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.listPatient = wx.ListCtrl(self.findDialog,-1,size=(430,280),style=wx.LC_REPORT)
        self.listPatient.InsertColumn(0, u'Nome', width=205)
        self.listPatient.InsertColumn(1, u'Orçado Por', width=75)
        self.listPatient.InsertColumn(2, u'Data de Nasc.', width=90)
        self.listPatient.InsertColumn(3,u'Ficha',width=65)
        self.listPatient.InsertColumn(4,'',width=0)

        self.hPatientBox1.Add(self.listPatient, 1,wx.EXPAND)
        self.vPatientBox1.Add(self.hPatientBox1,0,wx.ALL | wx.EXPAND, 5)
        self.vPatientBox1.Add((-1,10))

        #patients = Patient.query.order_by('name').all()

        #for patient in patients:
        #    index = self.listPatient.InsertStringItem(sys.maxint, patient.name)
        #    self.listPatient.SetStringItem(index, 1, patient.budgetBy)
        #    self.listPatient.SetStringItem(index, 2, patient.registrationForm)
        #    self.listPatient.SetStringItem(index, 3, str(patient.id))

        self.listPatient.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.getSelectedItem,id=-1)

        self.hPatientBox2 = wx.BoxSizer(wx.HORIZONTAL)
        findOptions = [u"Nome",u"Data",u"RG",u"CPF"]
        self.findRadioBox = wx.RadioBox(self.findDialog, -1, u"Localizar por:", (10, 300), wx.DefaultSize,findOptions,2, wx.RA_SPECIFY_COLS)
        self.hPatientBox2.Add(self.findRadioBox,0,wx.RIGHT,8)
        self.vPatientBox1.Add(self.hPatientBox2,0,wx.ALL | wx.EXPAND,5)

        self.findRadioBox.Bind(wx.EVT_RADIOBOX,self.putMaskInFindTextCtrl)

        self.hPatientBox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.findTextCtrl = masked.TextCtrl(self.findDialog,-1,mask="")
        self.findTextCtrl.SetSize((140,40))
        self.findTextCtrl.SetPosition((-1,-1))

        self.searchBtn = wx.BitmapButton(self.findDialog,ID_FIND_SEARCH,wx.Bitmap('./imagens/search.png'))

        self.hPatientBox3.Add(self.findTextCtrl,1, wx.LEFT,0)
        self.hPatientBox3.Add(self.searchBtn,0,5)
        self.vPatientBox1.Add(self.hPatientBox3,0,wx.ALL | wx.EXPAND, 5)

        self.findDialog.Bind(wx.EVT_BUTTON,self.search,self.searchBtn)
        self.findDialog.SetSizerAndFit(self.vPatientBox1)

        self.findDialog.ShowModal()
        self.findDialog.SetFocus()
        self.findDialog.Destroy()

    def putMaskInFindTextCtrl(self,event):

        if event.GetString() == u"Data":
            self.findTextCtrl.SetCtrlParameters(mask="##/##/####")
            self.findTextCtrl.SetFocus()
        elif event.GetString() == u"CPF":
            self.findTextCtrl.SetCtrlParameters(mask="###.###.###-##")
            self.findTextCtrl.SetFocus()
        else:
            self.findTextCtrl.SetCtrlParameters(mask="")
            self.findTextCtrl.SetValue("")
            self.findTextCtrl.Refresh()

    def getSelectedItem(self,event):

        id = self.listPatient.GetItem(event.GetIndex(),4).GetText()
        patientSelected = Patient.query.filter_by(id=id).first()

        self.idTextCtrl.SetValue(unicode(patientSelected.id))
        self.nameTextCtrl.SetValue(unicode(patientSelected.name))
        self.dateOfBirthTextCtrl.SetValue(unicode(patientSelected.dateOfBirth))
        self.rgTextCtrl.SetValue(unicode(patientSelected.rg))
        self.cpfTextCtrl.SetValue(unicode(patientSelected.cpf))
        self.streetTextCtrl.SetValue(unicode(patientSelected.street))
        self.numberTextCtrl.SetValue(unicode(patientSelected.number))
        self.districtTextCtrl.SetValue(unicode(patientSelected.district))
        self.additionalAdressTextCtrl.SetValue(unicode(patientSelected.additionalAdress))
        self.zipCodeTextCtrl.SetValue(unicode(patientSelected.zipCode))
        self.cityTextCtrl.SetValue(unicode(patientSelected.city))
        self.stateChoice.SetValue(unicode(patientSelected.state))
        self.telephoneTextCtrl.SetValue(unicode(patientSelected.telephone))
        self.treatmentStartTextCtrl.SetValue(unicode(patientSelected.treatmentStart))
        self.budgetByTextCtrl.SetValue(unicode(patientSelected.budgetBy))
        self.registrationFormTextCtrl.SetValue(unicode(patientSelected.registrationForm))

        self.refreshIndex(patientSelected.id)
        self.findDialog.Destroy()

    def search(self,event):

        import sys
        self.findTextCtrl.SetFocus()
        self.findTextCtrl.SelectAll()
        self.listPatient.DeleteAllItems()
        self.finderPatient = self.findTextCtrl.GetValue().strip()

        searchFor = self.findRadioBox.GetStringSelection()
        if searchFor == u'Nome':
            patients = Patient.query.filter(Patient.name.like(self.finderPatient+'%'))

            if self.finderPatient == '':
                for patient in patients:
                    index = self.listPatient.InsertStringItem(sys.maxint,patient.name)
                    self.listPatient.SetStringItem(index, 1, patient.budgetBy)
                    self.listPatient.SetStringItem(index, 2, patient.dateOfBirth)
                    self.listPatient.SetStringItem(index, 3, patient.registrationForm)
                    self.listPatient.SetStringItem(index, 4, str(patient.id))
            else:
                for patient in patients:
                    index = self.listPatient.InsertStringItem(sys.maxint,patient.name)
                    self.listPatient.SetStringItem(index, 1, patient.budgetBy)
                    self.listPatient.SetStringItem(index, 2, patient.dateOfBirth)
                    self.listPatient.SetStringItem(index, 3, patient.registrationForm)
                    self.listPatient.SetStringItem(index, 4, str(patient.id))

        if searchFor == u'Data':
            if self.findTextCtrl.GetValue() == '':
                pass
            else:
                patients = Patient.query.filter_by(treatmentStart=self.finderPatient).all()
                for patient in patients :
                    index = self.listPatient.InsertStringItem(sys.maxint,patient.name)
                    self.listPatient.SetStringItem(index, 1, patient.budgetBy)
                    self.listPatient.SetStringItem(index, 2, patient.dateOfBirth)
                    self.listPatient.SetStringItem(index, 3, patient.registrationForm)
                    self.listPatient.SetStringItem(index, 4, str(patient.id))

        if searchFor == u'RG':
            if self.findTextCtrl.GetValue() == '':
                pass
            else:

                patients = Patient.query.filter(Patient.rg.like(self.finderPatient)).all()

                for patient in patients:
                    index = self.listPatient.InsertStringItem(sys.maxint,patient.name)
                    self.listPatient.SetStringItem(index, 1, patient.budgetBy)
                    self.listPatient.SetStringItem(index, 2, patient.dateOfBirth)
                    self.listPatient.SetStringItem(index, 3, patient.registrationForm)
                    self.listPatient.SetStringItem(index, 4, str(patient.id))

        if searchFor == u'CPF':
            if self.findTextCtrl.GetValue() == '':
                pass
            else:
                patients = Patient.query.filter(Patient.cpf.like(self.finderPatient)).all()
                for patient in patients:
                    index = self.listPatient.InsertStringItem(sys.maxint,patient.name)
                    self.listPatient.SetStringItem(index, 1, patient.budgetBy)
                    self.listPatient.SetStringItem(index, 2, patient.dateOfBirth)
                    self.listPatient.SetStringItem(index, 3, patient.registrationForm)
                    self.listPatient.SetStringItem(index, 4, str(patient.id))

    def quit(self,event):

        self.MakeModal(False)
        self.Destroy()


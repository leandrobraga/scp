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


from elixir import *
metadata.bind = 'sqlite:///db/database.sqlite'
metadata.bind.echo = False

class User(Entity):
    name = Field(Unicode(50),required=True)
    login = Field(Unicode(20),required=True)
    password = Field(Unicode(20),required=True)
    level = Field(Integer,required=False)

    def __repr__(self):
        return "%s"%(self.name)

class Patient(Entity):
    name = Field(Unicode(50),required=True)
    dateOfBirth = Field(Unicode(10),required=True)
    cpf = Field(Unicode(14),required=False)
    rg = Field(Unicode(20),required=False)
    telephone = Field(Unicode(15),required=True)
    telephone2 = Field(Unicode(15),required=False)
    treatmentStart = Field(Unicode(10),required=True)
    budgetBy = Field(Unicode(30),required=False)
    registrationForm = Field(Unicode(10),required=True)

    def __repr__(self):
        return "%s"%(self.name)

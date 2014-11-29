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


import wx
import access
if __name__ == '__main__':
    app = wx.App()
    access = access.Login()
    app.MainLoop()

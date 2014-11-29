# -*- coding: iso-8859-1 -*-
#Copyright 2012 Leandro Quadros Dur�es Braga

#Este arquivo � parte do programa Sistema de Controle de Paciente(SCP)
#Sistema de Controle de Paciente(SCP) � um software livre; voc� pode redistribui-lo e/ou
#modifica-lo dentro dos termos da Licen�a P�blica Geral GNU como
#publicada pela Funda��o do Software Livre (FSF); na vers�o 2 da Licen�a.
#Este programa � distribuido na esperan�a que possa ser  util,
#mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUA��O a qualquer
#MERCADO ou APLICA��O EM PARTICULAR. Veja a Licen�a P�blica Geral GNU para maiores detalhes.
#Voc� deve ter recebido uma c�pia da Licen�a P�blica Geral GNU
#junto com este programa, se n�o, escreva para a Funda��o do Software
#Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


from distutils.core import setup
import py2exe


setup(
      windows=[{"script":"createdb.py"}],



       options={"py2exe":{

            "includes":["sqlite3","sqlalchemy.dialects.sqlite","elixir"],
            "excludes":['_ssl','doctest','optparse','bsddb','compiler',
                        'curses','pickle','calendar','antigravity',
                        'cgi','base64','bz2',
                        ],
            "dll_excludes":["msvcr71.dll","API-MS-Win-Core-LocalRegistry-L1-1-0.dll",
    "POWRPROF.dll",
    "w9xpopen.exe"],
            }}
      )

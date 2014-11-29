from models import *
from elixir import *
import os
import shutil
import hashlib
import sys
import wx
import stat
setup_all()


for x in xrange(10000):
    Patient(name="Teste "+str(x),dateOfBirth="25/12/2011",
    rg="123456",cpf="123.456.852-14",
    street="teste",number="321",
    district="manaus",additionalAdress="tr",
    zipCode="39400-356",city="2152",
    state="as",telephone="(92)3698-9632",
    treatmentStart="25/08/2012",budgetBy="teste",
    registrationForm="6565")
    session.commit()

import csv
import zipfile
import os
import numpy
import pandas as pd
import sqlite3
import json
import mysql.connector

from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from decimal import Decimal
from django.template.context_processors import csrf
from .models import *
from .forms import *
from io import BytesIO
from django.conf import settings
from django.utils.encoding import uri_to_iri
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.models import User, Group


@login_required(login_url='/login/')
def index(request):
        return render(request, "mysite/index.html")

@login_required(login_url='/login/')
def about(request):
        return render(request, "mysite/about.html")

@login_required(login_url='/login/')
def bazaznanja_cst(request):
        return render(request, "bazaznanjatechnical/home.html")

@login_required(login_url='/login/')
def troubleshooter(request):
        return render(request, "bazaznanjatechnical/troubleshooter.html")

@login_required(login_url='/login/')
def article_admin(request):
        form = PostForm()
        arg = {"form": form}
        return render(request, "bazaznanjatechnical/article_admin.html", arg)

@login_required(login_url='/login/')
def test(request):
        return render(request, "mysite/test.html")

@login_required(login_url='/login/')
def dekodiranjeadmin(request):
        if request.user.groups.filter(name = 'level_1').exists():
                # u must call every arg so that the page could load all modules
                entry_data = EntryTable.objects.all()
                ace_data = AceTable.objects.all()
                temp_list = []
                trigger = 0
                for row in entry_data:
                        if row.unlock != '' and row.status != 3:
                                temp_list.append([row.kontakt, row.unlock])
                if len(temp_list) == 0:
                        trigger = 1
                        messages.info(request, 'Nema novih zahteva za preuzimanje.')
                arg = {"trigger": trigger, "ace_data": ace_data}
                return render(request, "mysite/dekodiranjeadmin.html", arg)
        else:
             return HttpResponseRedirect('/')


@login_required(login_url='/login/')
def dekodiranjeadminvendorlist(request):
        # u must call every arg so that the page could load all modules
        entry_data = EntryTable.objects.all()
        ace_data = AceTable.objects.all()
        temp_list = []
        list_trigger = 'Nema novih zahteva za preuzimanje!'
        trigger = 0
        for row in entry_data:
                if row.unlock != '' and row.status != 3:
                        temp_list.append([row.kontakt, row.unlock])
        if len(temp_list) == 0:
                trigger = 1
                messages.info(request, 'Nema novih zahteva za preuzimanje.')
        arg = {"trigger": trigger, "ace_data": ace_data, "list_trigger": list_trigger}
        return render(request, "mysite/dekodiranjeadmin.html", arg)

@login_required(login_url='/login/')
def dekodiranjeadminnokialist(request):
        # u must call every arg so that the page could load all modules
        entry_data = EntryTable.objects.all()
        ace_data = AceTable.objects.all()
        temp_list = []
        nokia_trigger = 'Nema novih zahteva za preuzimanje!'
        trigger = 0
        for row in entry_data:
                if row.unlock != '' and row.status != 3:
                        temp_list.append([row.kontakt, row.unlock])
        if len(temp_list) == 0:
                trigger = 1
                messages.info(request, 'Nema novih zahteva za preuzimanje.')
        arg = {"trigger": trigger, "ace_data": ace_data, "nokia_trigger": nokia_trigger}
        return render(request, "mysite/dekodiranjeadmin.html", arg)

@login_required(login_url='/login/')
def dekodiranjeinput(request):
        entry_data = EntryTable.objects.all()
        nokia_model = NokiaModels.objects.all()
        arg = {"entry_data": entry_data, "nokia_model": nokia_model}
        return render(request, "mysite/dekodiranjeinput.html", arg)

@login_required(login_url='/login/')
def dekodiranjeinput_search(request):
        imei_temp = request.POST["imeihidden"]
        proizvodjac_temp_lwr = str.lower(request.POST["proizvodjachidden"])
        proizvodjac_temp = request.POST["proizvodjachidden"]
        model_temp = request.POST["modelhidden"]
        entry_data = EntryTable.objects.all()
        nokia_model = NokiaModels.objects.all()
        arg = {"entry_data": entry_data, "imei": imei_temp, "proizvodjac": proizvodjac_temp, "proizvodjac_lwr": proizvodjac_temp_lwr, "model_temp": model_temp, "nokia_model": nokia_model}
        return render(request, "mysite/dekodiranjeinput.html", arg)

@login_required(login_url='/login/')
def dekodiranjetabela(request):
        entry_data = EntryTable.objects.all()
        paginator = Paginator(entry_data, 25) # Show 25 contacts per page
        page = request.GET.get('page')
        pages = paginator.get_page(page)
        arg = {"pages": pages}
        return render(request, "mysite/dekodiranjetabela.html", arg)

@login_required(login_url='/login/')
def dekodiranjeobradjeni(request):
        data = DataTable.objects.all()
        paginator = Paginator(data, 25) # Show 25 contacts per page
        page = request.GET.get('page')
        pages = paginator.get_page(page)
        arg = {"pages": pages}
        return render(request, "mysite/dekodiranjeobradjeni.html", arg)

@login_required(login_url='/login/')
def dekodiranjepretraga(request):
        entry_data = EntryTable.objects.all()
        arg = {"entry_data": entry_data}
        return render(request, "mysite/dekodiranjepretraga.html", arg)

def sumDig(n):
        a = 0
        while n > 0:
                a = a + n % 10
                n = int(n / 10)
        return a
        # Returns True if n is valid EMEI

def isValidIMEI(n):
        # Converting the number into
        # Sting for finding length
        s = str(n)
        l = len(s)
        # If length is not 15 then IMEI is Invalid
        d = 0
        sum = 0
        for i in range(15, 0, -1):
                d = (int)(n % 10)
                if i % 2 == 0:
                        # Doubling every alternate digit
                        d = 2 * d
                # Finding sum of the digits
                sum = sum + sumDig(d)
                n = n / 10
        return (sum % 10 == 0)

def isie(request):
        return render(request, "mysite/isie.html")

@login_required(login_url='/login/')
def search_unc(request):
        imei = request.POST["imei"]
        unlock_list = []
        entry_data = EntryTable.objects.all()
        validate = '0'
        entry_data = EntryTable.objects.all()
        data = DataTable.objects.all()
        alcatel_data = AlcatelUnlock.objects.all()
        htc_data = HtcUnlock.objects.all()
        huawei_data = HuaweiUnlock.objects.all()
        lg_data = LgUnlock.objects.all()
        lumia_data = LumiaUnlock.objects.all()
        nokia_data = NokiaUnlock.objects.all()
        samsung_data = SamsungUnlock.objects.all()
        sony_data = SonyUnlock.objects.all()
        zte_data = ZteUnlock.objects.all()
        search_data = SearchLog.objects.all()
        winlockpreview = ''
        validate = '0'
        imei_text = ''
        unlock_not_found = None
        temp_proizvodjac = ''
        temp_model = ''
        make_type = ['alcatel', 'htc', 'huawei', 'lg', 'lumia', 'nokia', 'samsung', 'sony', 'zte']
        # check len of IMEI input
        if len(imei) != 15:
                imei_text = uri_to_iri('Broj ' + imei + ' nije unet u ispravnom formatu. IMEI broj sadr%C5%BEi isklju%C4%8Divo numeri%C4%8Dke karaktere i %C4%8Dini ga ta%C4%8Dno 15 cifara.')
                validate = '9'

        try:
                imei_test = int(imei)
                # function in order to validate IMEI
                if isValidIMEI(imei_test):
                        imei_tac = str(imei[:8])
                        tac_data = MyTAC.objects.all()
                        tac = ''
                        cxn = mysql.connector.connect(user='simlock', password='Star333wars',
                              host='simlock.mysql.pythonanywhere-services.com',
                              database='simlock$database')
                        cur = cxn.cursor()
                        for t in tac_data:
                                if t.tac == imei_tac:
                                        tac = str(t.proizvodjac) + ' ' + str(t.model)
                                        temp_proizvodjac = t.proizvodjac
                                        temp_model = t.model

                                        if str.lower(t.proizvodjac) == 'alcatel':
                                                select_user_query = 'SELECT * FROM polls_alcatelunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'htc':
                                                select_user_query = 'SELECT * FROM polls_htcunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'huawei':
                                                select_user_query = 'SELECT * FROM polls_huaweiunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'lg':
                                                select_user_query = 'SELECT * FROM polls_lgunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'lumia':
                                                select_user_query = 'SELECT * FROM polls_lumiaunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'nokia':
                                                select_user_query = 'SELECT * FROM polls_nokiaunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                nokia_data = NokiaModels.objects.all()
                                                for n in nokia_data:
                                                        if n.model == t.model:
                                                                winlock = n.winlock
                                                                winlockversion = n.version
                                                                winaltversion = n.altversion
                                                                if winaltversion != '':
                                                                        winlockpreview = uri_to_iri('Winlock za uređaj ') + str(temp_proizvodjac) + ' ' + str(temp_model) + ' je: ' + str(winlock) + ' - ' + str(winlockversion) + ' (alternativno: ' + str(winlock) + ' - ' + str(winaltversion) + ')'
                                                                else:
                                                                        winlockpreview = uri_to_iri('Winlock za uređaj ') + str(temp_proizvodjac) + ' ' + str(temp_model) + ' je: ' + str(winlock) + ' - ' + str(winlockversion)
                                                                break
                                                        else:
                                                                winlockpreview = uri_to_iri('')

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'samsung':
                                                select_user_query = 'SELECT * FROM polls_samsungunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'sony':
                                                select_user_query = 'SELECT * FROM polls_sonyunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'zte':
                                                select_user_query = 'SELECT * FROM polls_zteunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                else:
                                        tac = str(t.proizvodjac) + ' ' + str(t.model)
                                        validate = '3'
                        for o in data:
                                if o.imei == imei:
                                        validate = '1'
                                        if o.unlock == "":
                                                unlock = uri_to_iri('nije dostupan unlock kod za uređaj ') + tac
                                                unlock_list.append(unlock)
                                                lockstatus = '2'
                                        else:
                                                unlock = str(o.unlock) + ' - SMS poslat'
                                                unlock_list.append(unlock)
                                                lockstatus = '1'
                                        imei_text = uri_to_iri('Kod za uređaj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                        for i in entry_data:
                                if i.imei == imei:
                                        validate = '2'
                                        if i.unlock == "":
                                                unlock_not_found = 'zahtev se nalazi u obradi - strpljenje'
                                                lockstatus = '3'
                                        else:
                                                unlock = str(i.unlock)
                                                unlock_list.append(unlock)
                                                imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                lockstatus = '1'
                                                break
                else:
                        imei_text = uri_to_iri('IMEI broj nije validan!')
                        validate = '9'
        # if IMEI is not integer
        except ValueError:
                imei_text = uri_to_iri('Tekst ' + imei + ' je nevalidan unos! IMEI broj sadr%C5%BEi isklju%C4%8Divo numeri%C4%8Dke karaktere i %C4%8Dini ga ta%C4%8Dno 15 cifara.')
                validate = '9'

        if validate == '0':
                imei_text = uri_to_iri('Nije dostupan kod za ure%C4%91aj ' + tac + ' sa IMEI brojem ' + imei + '.')
                lockstatus = '2'
        if validate == '3':
                imei_text = uri_to_iri('Uređaj sa IMEI brojem ' + imei + ' nije zaključan ili nije deo naše ponude. Ukoliko je uređaj deo naše ponude, potrebno je testirati SIM karticu drugog operatera u korisnikovom uređaju!')
                lockstatus = '0'
        if validate == '4':
                imei_text = uri_to_iri('Uređaj ' + tac + ' sa IMEI brojem ' + imei + ' nije zaključan ili nije deo naše ponude. Ukoliko je uređaj deo naše ponude, potrebno je testirati SIM karticu drugog operatera u korisnikovom uređaju!')
                lockstatus = '0'

        # search log
        username = str(request.user.username)
        usergroup = str(request.user.groups.all()[1])
        search_table = SearchLog(imei=imei, usergroup=usergroup, username=username, lockstatus=lockstatus)
        search_table.save()


        item = Counters.objects.get(pk=1)
        counter_name = 'search_SUM'
        counter_counter = item.counter_01 + 1
        counter_table = Counters(id=1, name_01=counter_name, counter_01=counter_counter)
        counter_table.save()


        arg = {"unlock_list": unlock_list, "imei_query": imei_text, "validate": validate, "imei_temp": imei, "proizvodjac_temp": temp_proizvodjac, "model_temp": temp_model, "unlock_not_found": unlock_not_found, "winlockpreview": winlockpreview}
        return render(request, "mysite/dekodiranjepretraga.html", arg)



def search_unc_ajax(request):
        imei = request.GET.get('imei', None)
        user = request.GET.get('user', None)
        group = request.GET.get('group', None)
        level = request.GET.get('level', None)

        unlock_list = []
        entry_data = EntryTable.objects.all()
        validate = '0'
        entry_data = EntryTable.objects.all()
        data = DataTable.objects.all()
        alcatel_data = AlcatelUnlock.objects.all()
        htc_data = HtcUnlock.objects.all()
        huawei_data = HuaweiUnlock.objects.all()
        lg_data = LgUnlock.objects.all()
        lumia_data = LumiaUnlock.objects.all()
        nokia_data = NokiaUnlock.objects.all()
        samsung_data = SamsungUnlock.objects.all()
        sony_data = SonyUnlock.objects.all()
        zte_data = ZteUnlock.objects.all()
        search_data = SearchLog.objects.all()
        winlockpreview = ''
        validate = '0'
        imei_text = ''
        unlock_not_found = ''
        temp_proizvodjac = ''
        temp_model = ''
        make_type = ['alcatel', 'htc', 'huawei', 'lg', 'lumia', 'nokia', 'samsung', 'sony', 'zte']
        # check len of IMEI input
        if len(imei) != 15:
                imei_text = uri_to_iri('Broj ' + imei + ' nije unet u ispravnom formatu. IMEI broj sadr%C5%BEi isklju%C4%8Divo numeri%C4%8Dke karaktere i %C4%8Dini ga ta%C4%8Dno 15 cifara.')
                validate = '9'

        try:
                imei_test = int(imei)
                # function in order to validate IMEI
                if isValidIMEI(imei_test):
                        imei_tac = str(imei[:8])
                        tac_data = MyTAC.objects.all()
                        tac = ''
                        cxn = mysql.connector.connect(user='simlock', password='Star333wars',
                              host='simlock.mysql.pythonanywhere-services.com',
                              database='simlock$database')
                        cur = cxn.cursor()
                        for t in tac_data:
                                if t.tac == imei_tac:
                                        tac = str(t.proizvodjac) + ' ' + str(t.model)
                                        temp_proizvodjac = t.proizvodjac
                                        temp_model = t.model

                                        if str.lower(t.proizvodjac) == 'alcatel':
                                                select_user_query = 'SELECT * FROM polls_alcatelunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'htc':
                                                select_user_query = 'SELECT * FROM polls_htcunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'huawei':
                                                select_user_query = 'SELECT * FROM polls_huaweiunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'lg':
                                                select_user_query = 'SELECT * FROM polls_lgunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'lumia':
                                                select_user_query = 'SELECT * FROM polls_lumiaunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'nokia':
                                                select_user_query = 'SELECT * FROM polls_nokiaunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                nokia_data = NokiaModels.objects.all()
                                                for n in nokia_data:
                                                        if n.model == t.model:
                                                                winlock = n.winlock
                                                                winlockversion = n.version
                                                                winaltversion = n.altversion
                                                                if winaltversion != '':
                                                                        winlockpreview = uri_to_iri('Winlock za uređaj ') + str(temp_proizvodjac) + ' ' + str(temp_model) + ' je: ' + str(winlock) + ' - ' + str(winlockversion) + ' (alternativno: ' + str(winlock) + ' - ' + str(winaltversion) + ')'
                                                                else:
                                                                        winlockpreview = uri_to_iri('Winlock za uređaj ') + str(temp_proizvodjac) + ' ' + str(temp_model) + ' je: ' + str(winlock) + ' - ' + str(winlockversion)
                                                                break
                                                        else:
                                                                winlockpreview = uri_to_iri('')

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'samsung':
                                                select_user_query = 'SELECT * FROM polls_samsungunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'sony':
                                                select_user_query = 'SELECT * FROM polls_sonyunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'zte':
                                                select_user_query = 'SELECT * FROM polls_zteunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                else:
                                        tac = str(t.proizvodjac) + ' ' + str(t.model)
                                        validate = '3'
                        for o in data:
                                if o.imei == imei:
                                        validate = '1'
                                        if o.unlock == "":
                                                unlock = uri_to_iri('nije dostupan unlock kod za uređaj ') + tac
                                                unlock_list.append(unlock)
                                                lockstatus = '2'
                                        else:
                                                unlock = str(o.unlock) + ' - SMS poslat'
                                                unlock_list.append(unlock)
                                                lockstatus = '1'
                                        imei_text = uri_to_iri('Kod za uređaj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                        for i in entry_data:
                                if i.imei == imei:
                                        validate = '2'
                                        if i.unlock == "":
                                                unlock_not_found = 'zahtev se nalazi u obradi - strpljenje'
                                                lockstatus = '3'
                                        else:
                                                unlock = str(i.unlock)
                                                unlock_list.append(unlock)
                                                imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                lockstatus = '1'
                                                break
                else:
                        imei_text = uri_to_iri('IMEI broj nije validan!')
                        validate = '9'
        # if IMEI is not integer
        except ValueError:
                imei_text = uri_to_iri('Tekst ' + imei + ' je nevalidan unos! IMEI broj sadr%C5%BEi isklju%C4%8Divo numeri%C4%8Dke karaktere i %C4%8Dini ga ta%C4%8Dno 15 cifara.')
                validate = '9'

        if validate == '0':
                imei_text = uri_to_iri('Nije dostupan kod za ure%C4%91aj ' + tac + ' sa IMEI brojem ' + imei + '.')
                lockstatus = '2'
        if validate == '3':
                imei_text = uri_to_iri('Uređaj sa IMEI brojem ' + imei + ' nije zaključan ili nije deo naše ponude. Ukoliko je uređaj deo naše ponude, potrebno je testirati SIM karticu drugog operatera u korisnikovom uređaju!')
                lockstatus = '0'
        if validate == '4':
                imei_text = uri_to_iri('Uređaj ' + tac + ' sa IMEI brojem ' + imei + ' nije zaključan ili nije deo naše ponude. Ukoliko je uređaj deo naše ponude, potrebno je testirati SIM karticu drugog operatera u korisnikovom uređaju!')
                lockstatus = '0'


        # search log
        username = str(user)
        usergroup = str(group)
        lockstatus = str('0')
        search_table = SearchLog(imei=imei, usergroup=usergroup, username=username, lockstatus=lockstatus)
        search_table.save()


        item = Counters.objects.get(pk=1)
        counter_name = 'search_SUM'
        counter_counter = item.counter_01 + 1
        counter_table = Counters(id=1, name_01=counter_name, counter_01=counter_counter)
        counter_table.save()

        data = {
                'unlock_list': unlock_list,
                'imei_query': str(imei_text),
                'unlock_not_found': str(unlock_not_found),
                'proizvodjac_temp': str(temp_proizvodjac),
                'winlockpreview': winlockpreview,
                'validate': validate,
                'imei_temp': imei,
                'model_temp': temp_model,
                'level': level,
        }

        return JsonResponse(data)


def add_new_confirm(request):
        now = datetime.now()
        date_now = now.strftime("%m-%d-%Y_%H-%M-%S")
        kontakt = request.POST["kontakt"]
        proizvodjac = request.POST["proizvodjac"]
        proizvodjac_lwr = str.lower(proizvodjac)
        if proizvodjac_lwr == 'nokia':
                model = request.POST["model"]
                nokia_data = NokiaModels.objects.all()
                for i in nokia_data:
                        if i.model == model:
                                winlock = i.winlock
                                winlockversion = i.version
                                break
                        else:
                                winlock = 'other'
                                winlockversion = 'other'
        else:
                model = ''
                winlock = ''
                winlockversion = ''
        imei = request.POST["imei"]
        log = "createdby_" + str(request.user.username) + "_" + str(date_now) + ";"
        createdby = str(request.user.username)
        createdbygroup = str(request.user.groups.all()[1])
        entry_data = EntryTable.objects.all()
        entry_table = EntryTable(kontakt=kontakt, proizvodjac=proizvodjac_lwr, model=model, imei=imei, log=log, winlock=winlock, winlockversion=winlockversion, createdby=createdby, createdbygroup=createdbygroup)
        entry_table.save()
        return HttpResponseRedirect('/dekodiranjeinput/')
        arg = {"entry_data": entry_data, "model_temp": model}
        return render(request, "mysite/dekodiranjeinput.html", arg)

def add_new(request):
        now = datetime.now()
        date_now = now.strftime("%m-%d-%Y_%H-%M-%S")
        kontakt = request.POST["kontakthidden"]
        proizvodjac = request.POST["proizvodjachidden"]
        proizvodjac_lwr = str.lower(proizvodjac)
        if proizvodjac_lwr == 'nokia':
                model = request.POST["modelhidden"]
        else:
                model = ''
        imei = request.POST["imeihidden"]
        log = "createdby_" + str(request.user.username) + "_" + str(date_now) + ";"
        createdby = str(request.user.username)
        createdbygroup = str(request.user.groups.all()[1])
        unlock_list = []
        entry_data = EntryTable.objects.all()
        data = DataTable.objects.all()
        validate = '0'
        imei_text = ''
        unlock_not_found = None
        # check len of IMEI input
        if len(imei) != 15:
                imei_text = uri_to_iri('Broj ' + imei + ' nije unet u ispravnom formatu. IMEI broj sadr%C5%BEi isklju%C4%8Divo numeri%C4%8Dke karaktere i %C4%8Dini ga ta%C4%8Dno 15 cifara.')
                validate = '9'

        try:
                imei_test = int(imei)
                # function in order to validate IMEI
                if isValidIMEI(imei_test):
                        for o in data:
                                if o.imei == imei:
                                        validate = '1'
                                        if o.unlock == "":
                                                unlock = 'nije dostupan unlock kod'
                                                unlock_list.append(unlock)
                                        else:
                                                unlock = str(o.unlock) + ' - SMS poslat'
                                                unlock_list.append(unlock)
                                        imei_text = uri_to_iri('Kod za uređaj sa IMEI brojem ' + imei + ' je:')
                        for i in entry_data:
                                if i.imei == imei:
                                        validate = '2'
                                        if i.unlock == "":
                                                unlock_not_found = 'zahtev se nalazi u obradi - strpljenje'
                                        else:
                                                unlock = str(i.unlock)
                                                unlock_list.append(unlock)
                                                imei_text = uri_to_iri('Kod za ure%C4%91aj sa IMEI brojem ' + imei + ' je:')
                else:
                        imei_text = uri_to_iri('IMEI broj nije validan!')
                        validate = '9'
        # if IMEI is not integer
        except ValueError:
                imei_text = uri_to_iri('Tekst ' + imei + ' je nevalidan unos! IMEI broj sadr%C5%BEi isklju%C4%8Divo numeri%C4%8Dke karaktere i %C4%8Dini ga ta%C4%8Dno 15 cifara.')
                validate = '9'

        if validate == '0':
                if proizvodjac_lwr == 'nokia':
                        nokia_data = NokiaModels.objects.all()
                        for i in nokia_data:
                                if i.model == model:
                                        winlock = i.winlock
                                        winlockversion = i.version
                                        break
                                else:
                                        winlock = 'other'
                                        winlockversion = 'other'
                        entry_table = EntryTable(kontakt=kontakt, proizvodjac=proizvodjac_lwr, model=model, imei=imei, log=log, winlock=winlock, winlockversion=winlockversion, createdby=createdby, createdbygroup=createdbygroup)
                        entry_table.save()
                else:
                        entry_table = EntryTable(kontakt=kontakt, proizvodjac=proizvodjac_lwr, model=model, imei=imei, log=log, createdby=createdby, createdbygroup=createdbygroup)
                        entry_table.save()


                item = Counters.objects.get(pk=2)
                entry_name = 'entry_SUM'
                entry_counter = item.counter_01 + 1
                entry_table = Counters(id=2, name_01=entry_name, counter_01=entry_counter)
                entry_table.save()
                return HttpResponseRedirect('/dekodiranjeinput/')


        arg = {"entry_data": entry_data, "unlock_list": unlock_list, "imei_query": imei_text, "validate": validate, "unlock_not_found": unlock_not_found, "kontakt_temp": kontakt, "proizvodjac_temp": proizvodjac, "model_temp": model, "imei_temp": imei, "imei": imei, "kontakt": kontakt, "proizvodjac": proizvodjac}
        return render(request, "mysite/dekodiranjeinput.html", arg)

def confirm_new(request):
        now = datetime.now()
        date_now = now.strftime("%m-%d-%Y_%H-%M-%S")
        kontakt = request.POST["kontakt"]
        proizvodjac = request.POST["proizvodjac"]
        model = request.POST["model"]
        imei = request.POST["imei"]
        log = "createdby_" + str(request.user.username) + "_" + str(date_now) + ";"
        createdby = str(request.user.username)
        createdbygroup = str(request.user.groups.all()[1])
        unlock_list = []
        entry_data = EntryTable.objects.all()
        data = DataTable.objects.all()
        nokia_model = NokiaModels.objects.all()
        validate = '0'
        imei_text = ''
        unlock_not_found = None
        alcatel_data = AlcatelUnlock.objects.all()
        htc_data = HtcUnlock.objects.all()
        huawei_data = HuaweiUnlock.objects.all()
        lg_data = LgUnlock.objects.all()
        lumia_data = LumiaUnlock.objects.all()
        nokia_data = NokiaUnlock.objects.all()
        samsung_data = SamsungUnlock.objects.all()
        sony_data = SonyUnlock.objects.all()
        zte_data = ZteUnlock.objects.all()
        search_data = SearchLog.objects.all()
        winlockpreview = ''
        validate = '0'
        temp_proizvodjac = ''
        temp_model = ''
        model_temp = None
        make_type = ['alcatel', 'htc', 'huawei', 'lg', 'lumia', 'nokia', 'samsung', 'sony', 'zte']
        # check len of IMEI input
        if len(imei) != 15:
                imei_text = uri_to_iri('Broj ' + imei + ' nije unet u ispravnom formatu. IMEI broj sadr%C5%BEi isklju%C4%8Divo numeri%C4%8Dke karaktere i %C4%8Dini ga ta%C4%8Dno 15 cifara.')
                validate = '9'

        try:
                imei_test = int(imei)
                # function in order to validate IMEI
                if isValidIMEI(imei_test):
                        imei_tac = str(imei[:8])
                        tac_data = MyTAC.objects.all()
                        tac = ''
                        cxn = mysql.connector.connect(user='simlock', password='Star333wars',
                              host='simlock.mysql.pythonanywhere-services.com',
                              database='simlock$database')
                        cur = cxn.cursor()
                        for t in tac_data:
                                if t.tac == imei_tac:
                                        tac = str(t.proizvodjac) + ' ' + str(t.model)
                                        temp_proizvodjac = t.proizvodjac
                                        temp_model = t.model

                                        if str.lower(t.proizvodjac) == 'alcatel':
                                                select_user_query = 'SELECT * FROM polls_alcatelunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'htc':
                                                select_user_query = 'SELECT * FROM polls_htcunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'huawei':
                                                select_user_query = 'SELECT * FROM polls_huaweiunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'lg':
                                                select_user_query = 'SELECT * FROM polls_lgunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'lumia':
                                                select_user_query = 'SELECT * FROM polls_lumiaunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'nokia':
                                                select_user_query = 'SELECT * FROM polls_nokiaunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                nokia_data = NokiaModels.objects.all()
                                                for n in nokia_data:
                                                        if n.model == t.model:
                                                                model_temp = model
                                                                winlock = n.winlock
                                                                winlockversion = n.version
                                                                winaltversion = n.altversion
                                                                if winaltversion != '':
                                                                        winlockpreview = uri_to_iri('Winlock za uređaj ') + str(temp_proizvodjac) + ' ' + str(temp_model) + ' je: ' + str(winlock) + ' - ' + str(winlockversion) + ' (alternativno: ' + str(winlock) + ' - ' + str(winaltversion) + ')'
                                                                else:
                                                                        winlockpreview = uri_to_iri('Winlock za uređaj ') + str(temp_proizvodjac) + ' ' + str(temp_model) + ' je: ' + str(winlock) + ' - ' + str(winlockversion)
                                                                break
                                                        else:
                                                                winlockpreview = uri_to_iri('')

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'samsung':
                                                select_user_query = 'SELECT * FROM polls_samsungunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'sony':
                                                select_user_query = 'SELECT * FROM polls_sonyunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                        if str.lower(t.proizvodjac) == 'zte':
                                                select_user_query = 'SELECT * FROM polls_zteunlock WHERE imei = "' + str(imei) + '";'
                                                df = pd.read_sql_query(select_user_query, cxn)
                                                df = df['unlock']

                                                if df.empty == False:
                                                        for i in df.values:
                                                                unlock_list.append(i)
                                                        validate = '5'
                                                        imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                        lockstatus = '1'
                                                        break
                                                else:
                                                        validate = '0'
                                                        break
                                                break
                                else:
                                        tac = str(t.proizvodjac) + ' ' + str(t.model)
                                        validate = '3'
                        for o in data:
                                if o.imei == imei:
                                        validate = '1'
                                        if o.unlock == "":
                                                unlock = uri_to_iri('nije dostupan unlock kod za uređaj ') + tac
                                                unlock_list.append(unlock)
                                                lockstatus = '2'
                                        else:
                                                unlock = str(o.unlock) + ' - SMS poslat'
                                                unlock_list.append(unlock)
                                                lockstatus = '1'
                                        imei_text = uri_to_iri('Kod za uređaj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                        for i in entry_data:
                                if i.imei == imei:
                                        validate = '2'
                                        if i.unlock == "":
                                                unlock_not_found = 'zahtev se nalazi u obradi - strpljenje'
                                                lockstatus = '3'
                                        else:
                                                unlock = str(i.unlock)
                                                unlock_list.append(unlock)
                                                imei_text = uri_to_iri('Kod za ure%C4%91aj ') + tac + ' sa IMEI brojem ' + imei + ' je:'
                                                lockstatus = '1'
                                                break
                else:
                        imei_text = uri_to_iri('IMEI broj nije validan!')
                        validate = '9'
        # if IMEI is not integer
        except ValueError:
                imei_text = uri_to_iri('Tekst ' + imei + ' je nevalidan unos! IMEI broj sadr%C5%BEi isklju%C4%8Divo numeri%C4%8Dke karaktere i %C4%8Dini ga ta%C4%8Dno 15 cifara.')
                validate = '9'

        if validate == '0':
                imei_text = uri_to_iri('Nije dostupan kod za ure%C4%91aj ' + tac + ' sa IMEI brojem ' + imei + '.')
                lockstatus = '2'
        if validate == '3':
                imei_text = uri_to_iri('Uređaj sa IMEI brojem ' + imei + ' nije zaključan ili nije deo naše ponude. Ukoliko je uređaj deo naše ponude, potrebno je testirati SIM karticu drugog operatera u korisnikovom uređaju!')
                lockstatus = '0'
        if validate == '4':
                imei_text = uri_to_iri('Uređaj ' + tac + ' sa IMEI brojem ' + imei + ' nije zaključan ili nije deo naše ponude. Ukoliko je uređaj deo naše ponude, potrebno je testirati SIM karticu drugog operatera u korisnikovom uređaju!')
                lockstatus = '0'



        if validate == '0':
                if proizvodjac == 'nokia':
                        nokia_data = NokiaModels.objects.all()
                        for i in nokia_data:
                                if i.model == model:
                                        winlock = i.winlock
                                        winlockversion = i.version
                                        break
                                else:
                                        winlock = 'other'
                                        winlockversion = 'other'
                        entry_table = EntryTable(kontakt=kontakt, proizvodjac=proizvodjac, model=model, imei=imei, log=log, winlock=winlock, winlockversion=winlockversion, createdby=createdby, createdbygroup=createdbygroup)
                        entry_table.save()
                else:
                        entry_table = EntryTable(kontakt=kontakt, proizvodjac=proizvodjac, model=model, imei=imei, log=log, createdby=createdby, createdbygroup=createdbygroup)
                        entry_table.save()


                item = Counters.objects.get(pk=2)
                entry_name = 'entry_SUM'
                entry_counter = item.counter_01 + 1
                entry_table = Counters(id=2, name_01=entry_name, counter_01=entry_counter)
                entry_table.save()
                return HttpResponseRedirect('/dekodiranjeinput/')


        arg = {"entry_data": entry_data, "unlock_list": unlock_list, "imei_query": imei_text, "validate": validate, "unlock_not_found": unlock_not_found, "kontakt_temp": kontakt, "proizvodjac_temp": proizvodjac, "model_temp": model_temp, "imei_temp": imei, "winlockpreview": winlockpreview, "imei": imei, "kontakt": kontakt, "proizvodjac": proizvodjac, "model": model, "nokia_model": nokia_model}
        return render(request, "mysite/dekodiranjeinput.html", arg)

def edit_new(request, item_id):
        now = datetime.now()
        date_now = now.strftime("%m-%d-%Y_%H-%M-%S")
        if request.method == 'POST':
                item = EntryTable.objects.get(pk=item_id)
                kontakt = request.POST["kontakt"]
                proizvodjac = request.POST["proizvodjac"]
                model = request.POST["model"]
                imei = request.POST["imei"]
                unlock = request.POST["unlock"]
                status = item.status
                log = str(item.log) + "editedby_" + str(request.user.username) + "_unlock_" + str(unlock) + "_" + str(date_now) + ";"
                createdby = item.createdby
                createdbygroup = item.createdbygroup
                winlock = item.winlock
                winlockversion = item.winlockversion
                datecreated = item.datecreated
                datemodified = item.datemodified
                entry_table = EntryTable(id=item_id, kontakt=kontakt, proizvodjac=proizvodjac, model=model, imei=imei, unlock=unlock, datecreated=datecreated, datemodified=datemodified, status=status, log=log, winlock=winlock, winlockversion=winlockversion, createdby=createdby, createdbygroup=createdbygroup)
                entry_table.save()
                return HttpResponseRedirect('/dekodiranjeinput/')
                entry_data = EntryTable.objects.all()
                arg = {"entry_data": entry_data}
                return render(request, "mysite/dekodiranjeinput.html", arg)
        else:
                return HttpResponseRedirect('/dekodiranjeinput/')
                entry_data = EntryTable.objects.all()
                arg = {"entry_data": entry_data}
                return render(request, "mysite/dekodiranjeinput.html", arg)

def delete_new(request, item_id):
        now = datetime.now()
        date_now = now.strftime("%m-%d-%Y_%H-%M-%S")
        if request.method == 'POST':
                item = EntryTable.objects.get(pk=item_id)
                kontakt = item.kontakt
                proizvodjac = item.proizvodjac
                model = item.model
                imei = item.imei
                unlock = item.unlock
                status = item.status
                log = str(item.log) + "deletedby_" + str(request.user.username) + "_" + str(date_now) + ";"
                createdby = item.createdby
                createdbygroup = item.createdbygroup
                winlock = item.winlock
                winlockversion = item.winlockversion
                datecreated = item.datecreated
                datemodified = item.datemodified
                entry_table = DeletedTable(kontakt=kontakt, proizvodjac=proizvodjac, model=model, imei=imei, unlock=unlock, datecreated=datecreated, datemodified=datemodified, status=status, log=log, winlock=winlock, winlockversion=winlockversion, createdby=createdby, createdbygroup=createdbygroup)
                entry_table.save()
                item.delete()
                return HttpResponseRedirect('/dekodiranjeinput/')
                entry_data = EntryTable.objects.all()
                arg = {"entry_data": entry_data}
                return render(request, "mysite/dekodiranjeinput.html", arg)
        else:
                return HttpResponseRedirect('/dekodiranjeinput/')
                entry_data = EntryTable.objects.all()
                arg = {"entry_data": entry_data}
                return render(request, "mysite/dekodiranjeinput.html", arg)


def download_list(request):

        now = datetime.now()
        date_now = now.strftime("%m-%d-%Y_%H-%M-%S")
        nokia_trigger = 0

        ### CHECKBOX CHECKER ###

        """
        checkbox_list = ["checkbox0", "checkbox1", "checkbox2", "checkbox3", "checkbox4", "checkbox5", "checkbox6", "checkbox7"]
        name_list = []
        counter = 0


        for checked in checkbox_list:
                try:
                        checked = str(request.POST["name" + str(counter)])
                        counter += 1
                        name_list.append(checked)
                except KeyError:
                        counter += 1
        """

        name_list = request.POST["selected"]
        name_list = name_list.split(',') # making the list out of name_list string

        ### CSV LIST ###

        # new list and loop in order to check if there is something to write in .csv
        csv_list = []

        for checked in name_list:
                # load data from database object
                entry_data = EntryTable.objects.all()
                for i in entry_data:
                        if i.unlock == '' and i.proizvodjac == checked:
                                # append NAME in new list if there is find according to conditions
                                csv_list.append(checked)
                                # break (no need to look furder)
                                break

        list_trigger = 'Nema novih zahteva za slanje!'

        # check if list in not empty - in case it is, than skip and print message
        if len(csv_list) != 0:

                ### CREATE CSVs ###

                entry_data = EntryTable.objects.all()
                list_trigger = ''
                unique_temp = []

                for checked in csv_list:
                        index = []
                        with open('/home/simlock/mysite/polls/static/tmp/' + str(checked) + '.txt', 'w', newline='') as csvfile:
                                filewriter = csv.writer(csvfile, delimiter=',')
                                filewriter.writerow(['IMEI:'])
                                for i in entry_data:
                                        if i.unlock == '' and i.proizvodjac == checked:
                                                if not str(i.imei) in index:
                                                        item = EntryTable.objects.get(id=i.id)
                                                        index.append(str(i.imei))
                                                        filewriter.writerow([str(i.imei)])
                                                        item.status = '1'
                                                        item.log = str(item.log) + "imeidownloadedby_" + str(request.user.username) + "_" + str(date_now) + ";"
                                                        item.save()

                ### ZIPING CSV FILES ###

                filenames = []

                for checked in csv_list:
                        # Files (local path) to put in the .zip
                        filename = ("/home/simlock/mysite/polls/static/tmp/" + str(checked) + ".txt")
                        filenames.append(filename)
                # Folder name in ZIP archive which contains the above files
                zip_subdir = "liste za vendore"
                zip_filename = "%s.zip" % zip_subdir

                # Open StringIO to grab in-memory ZIP contents
                s = BytesIO()

                # The zip compressor
                zf = zipfile.ZipFile(s, "w")
                for fpath in filenames:
                        # Calculate path for file in zip
                        fdir, fname = os.path.split(fpath)
                        zip_path = os.path.join(zip_subdir, fname)

                        # Add file, at correct path
                        zf.write(fpath, zip_path)

                # Must close zip for all contents to be written
                zf.close()

                # Grab ZIP file from in-memory, make response with correct MIME-type
                response = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
                # ..and correct content-disposition
                response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
                return response

                """
                ### NOT IN USE ###
                try:
                        checkbox0 = str(request.POST["name0"])
                except KeyError:
                        checkbox0 = "none"

                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="alcatel.csv"'
                writer = csv.writer(response)
                writer.writerow(['Kontakt', 'Proizvodjac', 'Model telefona', 'IMEI', 'Kod', 'Datum unosa', 'Datum izmene', 'Status'])
                entry_data = EntryTable.objects.all()
                for i in entry_data:
                        if i.status == 0 and i.proizvodjac == 'alcatel':
                                writer.writerow([str(i.kontakt), str(i.proizvodjac), str(i.model), str(i.imei), str(i.unlock), str(i.datecreated),      str(i.datemodified), str(i.status)])

                if checkbox0 == "alcatel":
                        return response
                """
        else:
                entry_data = EntryTable.objects.all()
                ace_data = AceTable.objects.all()
                temp_list = []
                """
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="TEST.csv"'
                writer = csv.writer(response)
                writer.writerow([list_trigger])
                return(response)
                """
                trigger = 0
                for row in entry_data:
                        if row.unlock != '' and row.status != 3:
                                temp_list.append([row.kontakt, row.unlock])
                if len(temp_list) == 0:
                        trigger = 1
                        messages.info(request, 'Nema novih zahteva za preuzimanje.')
                return HttpResponseRedirect('/dekodiranjeadminvendorlist/')
                arg = {"trigger": trigger, "ace_data": ace_data, "list_trigger": list_trigger}
                return render(request, "mysite/dekodiranjeadmin.html", arg)
        return HttpResponseRedirect('/dekodiranjeadminvendorlist/')
        arg = {"trigger": trigger, "ace_data": ace_data, "list_trigger": list_trigger}
        return render(request, "mysite/dekodiranjeadmin.html", arg)

def nokia_list(request):

        now = datetime.now()
        date_now = now.strftime("%m-%d-%Y_%H-%M-%S")
        nokia_trigger = 'Nema novih zahteva za slanje!'
        entry_data = EntryTable.objects.all()
        nokia_data = NokiaModels.objects.all()

        ### CSV LIST ###

        fullwinlock = []
        fullwinlock_list = []
        winlock = []
        winlock_list = []
        wversion = []
        wversion_list = []

        file_list = []

        for i in entry_data:
                if i.proizvodjac == 'nokia' and i.unlock == '':
                        fullwinlock.append(i.winlock + '-' + i.winlockversion)
        for i in fullwinlock:
                if not str(i) in fullwinlock_list:
                        fullwinlock_list.append(str(i))


        winlock_folder_counter = len(fullwinlock_list)

        # check if list in not empty - in case it is, than skip and print message
        if winlock_folder_counter != 0:

                nokia_trigger = ''

                for w in fullwinlock_list:
                        with open('/home/simlock/mysite/polls/static/tmp/' + str(w) + '.txt', 'w', newline='') as csvfile:
                                filewriter = csv.writer(csvfile, delimiter=',')
                                filewriter.writerow(['IMEI:'])
                                for i in entry_data:
                                        if (i.winlock + '-' + i.winlockversion) == w:
                                                item = EntryTable.objects.get(id=i.id)
                                                filewriter.writerow([i.imei])
                                                item.status = '1'
                                                item.log = str(item.log) + "imeidownloadedby_" + str(request.user.username) + "_" + str(date_now) + ";"
                                                item.save()

                ### ZIPING CSV FILES ###

                filenames = []

                for w in fullwinlock_list:
                        # Files (local path) to put in the .zip
                        filename = ("/home/simlock/mysite/polls/static/tmp/" + str(w) + ".txt")
                        filenames.append(filename)
                # Folder name in ZIP archive which contains the above files
                zip_subdir = "Nokia IMEI liste"
                zip_filename = "%s.zip" % zip_subdir

                # Open StringIO to grab in-memory ZIP contents
                s = BytesIO()

                # The zip compressor
                zf = zipfile.ZipFile(s, "w")
                for fpath in filenames:
                        # Calculate path for file in zip
                        fdir, fname = os.path.split(fpath)
                        zip_path = os.path.join(zip_subdir, fname)

                        # Add file, at correct path
                        zf.write(fpath, zip_path)

                # Must close zip for all contents to be written
                zf.close()

                # Grab ZIP file from in-memory, make response with correct MIME-type
                response = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
                # ..and correct content-disposition
                response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
                return response
        else:
                entry_data = EntryTable.objects.all()
                ace_data = AceTable.objects.all()
                temp_list = []
                trigger = 0
                for row in entry_data:
                        if row.unlock != '' and row.status != 3:
                                temp_list.append([row.kontakt, row.unlock])
                if len(temp_list) == 0:
                        trigger = 1
                        messages.info(request, 'Nema novih zahteva za preuzimanje.')
                return HttpResponseRedirect('/dekodiranjeadminnokialist/')
                arg = {"trigger": trigger, "ace_data": ace_data, "nokia_trigger": nokia_trigger}
                return render(request, "mysite/dekodiranjeadmin.html", arg)
        return HttpResponseRedirect('/dekodiranjeadminnokialist/')
        arg = {"trigger": trigger, "ace_data": ace_data, "nokia_trigger": nokia_trigger}
        return render(request, "mysite/dekodiranjeadmin.html", arg)

from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator

csv_list = []
temp_csv_list = []

def upload_csv(request):

        input_text = 'submit'

        if request.method == 'POST' and request.FILES['upload_csv']:
                myfile = request.FILES['upload_csv']
                fs = FileSystemStorage("/home/simlock/mysite/polls/static/tmp/")
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)

                # populate lists
                with open('/home/simlock/mysite/polls/static/tmp/' + filename, 'r', newline='') as csvfile:
                        file_reader = csv.reader(csvfile)
                        for row in file_reader:
                                s = str(row)
                                break
                if ',' in s:
                        with open('/home/simlock/mysite/polls/static/tmp/' + filename, 'r', newline='') as csvfile:
                                temp_csv_list.clear()
                                csv_list.clear()
                                file_reader = csv.reader(csvfile, delimiter=',')
                                for row in file_reader:
                                        temp_csv_list.append(row)
                                        csv_list.append(row)
                elif ';' in s:
                        with open('/home/simlock/mysite/polls/static/tmp/' + filename, 'r', newline='') as csvfile:
                                temp_csv_list.clear()
                                csv_list.clear()
                                file_reader = csv.reader(csvfile, delimiter=';')
                                for row in file_reader:
                                        temp_csv_list.append(row)
                                        csv_list.append(row)

                # remove uploaded file from database
                if os.path.isfile('/home/simlock/mysite/polls/static/tmp/' + filename):
                        os.remove('/home/simlock/mysite/polls/static/tmp/' + filename)

                # paginate
                paginator = Paginator(csv_list, 25) # Show 25 contacts per page
                page = request.GET.get('page')
                pages = paginator.get_page(page)

                entry_data = EntryTable.objects.all()
                ace_data = AceTable.objects.all()
                temp_list = []
                trigger = 0
                for row in entry_data:
                        if row.unlock != '' and row.status != 3:
                                temp_list.append([row.kontakt, row.unlock])
                if len(temp_list) == 0:
                        trigger = 1
                        messages.info(request, 'Nema novih zahteva za preuzimanje.')
                arg = {"csv_list": csv_list, "input_text": input_text, "trigger": trigger, "ace_data": ace_data, "pages": pages}
                return render(request, "mysite/csvupload.html", arg)
        else:
                # paginate
                paginator = Paginator(csv_list, 5) # Show 25 contacts per page
                page = request.GET.get('page')
                pages = paginator.get_page(page)

                entry_data = EntryTable.objects.all()
                ace_data = AceTable.objects.all()
                temp_list = []
                trigger = 0
                for row in entry_data:
                        if row.unlock != '' and row.status != 3:
                                temp_list.append([row.kontakt, row.unlock])
                if len(temp_list) == 0:
                        trigger = 1
                        messages.info(request, 'Nema novih zahteva za preuzimanje.')
                arg = {"csv_list": csv_list, "input_text": input_text, "trigger": trigger, "ace_data": ace_data, "pages": pages}
                return render(request, "mysite/csvupload.html", arg)
        # paginate
        paginator = Paginator(csv_list, 5) # Show 25 contacts per page
        page = request.GET.get('page')
        pages = paginator.get_page(page)
        entry_data = EntryTable.objects.all()
        ace_data = AceTable.objects.all()
        temp_list = []
        trigger = 0
        for row in entry_data:
                if row.unlock != '' and row.status != 3:
                        temp_list.append([row.kontakt, row.unlock])
        if len(temp_list) == 0:
                trigger = 1
                messages.info(request, 'Nema novih zahteva za preuzimanje.')
        arg = {"csv_list": csv_list, "input_text": input_text, "trigger": trigger, "ace_data": ace_data, "pages": pages}
        return render(request, "mysite/csvupload.html", arg)

def csvupload(request):
        return render(request, "mysite/csvupload.html")

def reset_csv(request):
        csv_list.clear()
        if request.method == 'POST':
                if os.path.isfile('/home/simlock/mysite/polls/static/tmp/csv_temp_list.csv'):
                        os.remove('/home/simlock/mysite/polls/static/tmp/csv_temp_list.csv')
                return HttpResponseRedirect('/dekodiranjeadmin/')
                return render(request, "mysite/dekodiranjeadmin.html")
        else:
                entry_data = EntryTable.objects.all()
                ace_data = AceTable.objects.all()
                temp_list = []
                trigger = 0
                for row in entry_data:
                        if row.unlock != '' and row.status != 3:
                                temp_list.append([row.kontakt, row.unlock])
                if len(temp_list) == 0:
                        trigger = 1
                        messages.info(request, 'Nema novih zahteva za preuzimanje.')
                arg = {"trigger": trigger, "ace_data": ace_data}
                return HttpResponseRedirect('/dekodiranjeadmin/')
                return render(request, "mysite/dekodiranjeadmin.html", arg)

def validate_csv(request):
        now = datetime.now()
        date_now = now.strftime("%m-%d-%Y_%H-%M-%S")
        if request.method == 'POST':
                entry_data = EntryTable.objects.all()
                for row in temp_csv_list:
                        for i in entry_data:
                                if row[0] == i.imei and i.unlock == '':
                                        item = i.id
                                        kontakt = i.kontakt
                                        proizvodjac = i.proizvodjac
                                        model = i.model
                                        imei = i.imei
                                        unlock = str(row[1])
                                        if proizvodjac == 'nokia':
                                                unlock = '#pw+' + unlock + '+7#'
                                        if proizvodjac == 'samsung':
                                                if len(str(unlock)) < 8:
                                                        while len(str(unlock)) < 8:
                                                                unlock = '0' + unlock
                                                else:
                                                        pass
                                        status = '2'
                                        log = str(i.log) + "unlockmassupdatedby_" + str(request.user.username) + '_unlock_' + str(i.unlock) + "_" + str(date_now) + ";"
                                        winlock = i.winlock
                                        winlockversion = i.winlockversion
                                        datecreated = i.datecreated
                                        datemodified = i.datemodified
                                        entry_table = EntryTable(id=item, kontakt=kontakt, proizvodjac=proizvodjac, model=model, imei=imei, unlock=unlock, status=status, datecreated=datecreated, datemodified=datemodified, log=log, winlock=winlock, winlockversion=winlockversion)
                                        entry_table.save()
                entry_data = EntryTable.objects.all()
                ace_data = AceTable.objects.all()
                temp_list = []
                trigger = 0
                for row in entry_data:
                        if row.unlock != '' and row.status != 3:
                                temp_list.append([row.kontakt, row.unlock])
                if len(temp_list) == 0:
                        trigger = 1
                        messages.info(request, 'Nema novih zahteva za preuzimanje.')
                arg = {"trigger": trigger, "ace_data": ace_data}
                return HttpResponseRedirect('/dekodiranjeadmin/')
                return render(request, "mysite/dekodiranjeadmin.html", arg)
        entry_data = EntryTable.objects.all()
        ace_data = AceTable.objects.all()
        temp_list = []
        trigger = 0
        for row in entry_data:
                if row.unlock != '' and row.status != 3:
                        temp_list.append([row.kontakt, row.unlock])
        if len(temp_list) == 0:
                trigger = 1
                messages.info(request, 'Nema novih zahteva za preuzimanje.')
        arg = {"trigger": trigger, "ace_data": ace_data}
        return HttpResponseRedirect('/dekodiranjeadmin/')
        return render(request, "mysite/dekodiranjeadmin.html", arg)


from django.contrib import messages
import numpy

def ace_list(request):
        now = datetime.now()
        date_now = now.strftime("%m-%d-%Y_%H-%M-%S")
        if request.method == 'POST':
                now = datetime.now()
                date_now = now.strftime("%m-%d-%Y_%H-%M-%S")
                entry_data = EntryTable.objects.all()
                data = DataTable.objects.all()
                ace_data = AceTable.objects.all()
                temp_list = []
                file_counter = int(0)
                for row in entry_data:
                        if row.unlock != '' and row.status != 3:
                                temp_list.append([row.kontakt, row.unlock])
                # Check if there something in the list and if there is ...
                if len(temp_list) != 0:
                        # Create lists for filtering data
                        unique_value = []
                        duplicate_msisdn = []
                        duplicate_value = []
                        unique_value_stp1 = []
                        index = []
                        name_list = []
                        # Separate duplicate lists (same MSISDN and unlock) from unique lists
                        for f in temp_list:
                                if f in index:
                                        index.append(f)
                                        duplicate_value.append(f)
                                else:
                                        index.append(f)
                                        unique_value_stp1.append(f)

                        # Separate unique MSISDN from duplicate MSISDNs (but different unlock) and reset index list
                        index = []
                        for f in unique_value_stp1:
                                if not f[0] in index:
                                        index.append(f[0])
                                        unique_value.append(f)
                                else:
                                        index.append(f[0])
                                        duplicate_msisdn.append(f)

                        # Check if list is more or less than 500 rows
                        if len(unique_value) > 500:
                                # determine number of max rows per file, round that number and add one
                                y = int(len(unique_value)) / 500
                                z = int(round(y)) + 1
                                l = numpy.array_split(unique_value,z)
                                # set counter
                                c = 0
                                while c < z:
                                        value = l[c]
                                        with open('/home/simlock/mysite/polls/static/tmp/ACE_list_' + date_now + '-0' + str(c) + '.txt', 'w', newline='') as csvfile:
                                                filewriter = csv.writer(csvfile, delimiter=';')
                                                for i in value:
                                                        filewriter.writerow([str('381' + (i[0])[1:]),i[1]])
                                        name = 'ACE_list_' + date_now + '-0' + c + '.txt'
                                        name_list.append(name)
                                        c += 1
                        else:
                                with open('/home/simlock/mysite/polls/static/tmp/ACE_list_' + date_now + '-00.txt', 'w', newline='') as csvfile:
                                        filewriter = csv.writer(csvfile, delimiter=';')
                                        for i in unique_value:
                                                filewriter.writerow([str('381' + (i[0])[1:]),i[1]])
                                name = 'ACE_list_' + date_now + '-00.txt'
                                name_list.append(name)

                        if len(duplicate_msisdn) == 0:
                                pass
                        else:
                                y = int(len(duplicate_msisdn)) / 500
                                z = int(round(y)) + 1
                                l = numpy.array_split(duplicate_msisdn,z)
                                c = 0
                                while c < z:
                                        value = l[c]
                                        with open('/home/simlock/mysite/polls/static/tmp/ACE_duplicates_' + date_now + '-0' + str(c) + '.txt', 'w', newline='') as csvfile:
                                                filewriter = csv.writer(csvfile, delimiter=';')
                                                for i in value:
                                                        filewriter.writerow([str('381' + (i[0])[1:]),i[1]])
                                        name = 'ACE_duplicates_' + date_now + '-0' + str(c) + '.txt'
                                        name_list.append(name)
                                        c += 1

                        ### ZIPING CSV FILES ###

                        filenames = []

                        for checked in name_list:
                                # Files (local path) to put in the .zip
                                filename = ("/home/simlock/mysite/polls/static/tmp/" + str(checked))
                                filenames.append(filename)
                                # Folder name in ZIP archive which contains the above files
                        zip_subdir = "ACE liste " + str(date_now)
                        zip_filename = "%s.zip" % zip_subdir

                        # Open StringIO to grab in-memory ZIP contents
                        s = BytesIO()
                        with open('/home/simlock/mysite/polls/static/acebackup/' + zip_filename,'wb') as out:

                                # The zip compressor: out for save backup at defined folder; s for download attachment
                                zf = zipfile.ZipFile(out, "w")
                                zf_att = zipfile.ZipFile(s, "w")

                                for fpath in filenames:
                                        # Calculate path for file in zip
                                        fdir, fname = os.path.split(fpath)
                                        zip_path = os.path.join(zip_subdir, fname)

                                        # Add file, at correct path
                                        zf.write(fpath, zip_path)
                                        zf_att.write(fpath, zip_path)

                                # Must close zip for all contents to be written
                                zf.close()
                                zf_att.close()

                        name = zip_filename
                        ace_table = AceTable(name=name)
                        ace_table.save()

                        # Grab ZIP file from in-memory, make response with correct MIME-type
                        response = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
                        # ..and correct content-disposition
                        response['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
                        # delete TXT files from tmp folder
                        for checked in name_list:
                                if os.path.isfile('/home/simlock/mysite/polls/static/tmp/' + str(checked)):
                                        os.remove('/home/simlock/mysite/polls/static/tmp/' + str(checked))
                        for row in entry_data:
                                if row.unlock != '' and row.status != 3:
                                        item = row.id
                                        kontakt = row.kontakt
                                        proizvodjac = row.proizvodjac
                                        model = row.model
                                        imei = row.imei
                                        unlock = row.unlock
                                        status = '3'
                                        log = str(row.log) + "acelistdownloadedby_" + str(request.user.username) + '_' + str(date_now) + ";"
                                        winlock = row.winlock
                                        winlockversion = row.winlockversion
                                        datecreated = row.datecreated
                                        data_table = DataTable(kontakt=kontakt, proizvodjac=proizvodjac, model=model, imei=imei,unlock=unlock, status=status, datecreated=datecreated, log=log, winlock=winlock, winlockversion=winlockversion)
                                        data_table.save()
                                        entry = EntryTable.objects.get(pk=item)
                                        entry.delete()
                        return response
                # ... if list is empty
                else:
                        # u must call every arg so page can load all modules
                        entry_data = EntryTable.objects.all()
                        ace_data = AceTable.objects.all()
                        temp_list = []
                        trigger = 0
                        for row in entry_data:
                                if row.unlock != '' and row.status != 3:
                                        temp_list.append([row.kontakt, row.unlock])
                        if len(temp_list) == 0:
                                trigger = 1
                                messages.info(request, 'Nema novih zahteva za preuzimanje.')
                        arg = {"trigger": trigger, "ace_data": ace_data}
                        return HttpResponseRedirect('/dekodiranjeadmin/')
                        return render(request, "mysite/dekodiranjeadmin.html", arg)
        else:
                # u must call every arg so page can load all modules
                entry_data = EntryTable.objects.all()
                ace_data = AceTable.objects.all()
                temp_list = []
                trigger = 0
                for row in entry_data:
                        if row.unlock != '' and row.status != 3:
                                temp_list.append([row.kontakt, row.unlock])
                if len(temp_list) == 0:
                        trigger = 1
                        messages.info(request, 'Nema novih zahteva za preuzimanje.')
                arg = {"trigger": trigger, "ace_data": ace_data}
                return HttpResponseRedirect('/dekodiranjeadmin/')
                return render(request, "mysite/dekodiranjeadmin.html", arg)

def ace_table(request):
        if request.method == 'POST':
                ace_filename = 'polls/static/acebackup/' + str(request.POST["ace_name"])
                if os.path.exists(ace_filename):
                        with open(ace_filename, 'rb') as fh:
                                response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
                                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(ace_filename)
                        return response
                else:
                        # u must call every arg so page can load all modules
                        entry_data = EntryTable.objects.all()
                        ace_data = AceTable.objects.all()
                        temp_list = []
                        trigger = 0
                        for row in entry_data:
                                if row.unlock != '' and row.status != 3:
                                        temp_list.append([row.kontakt, row.unlock])
                        if len(temp_list) == 0:
                                trigger = 1
                                messages.info(request, 'Nema novih zahteva za preuzimanje.')
                        arg = {"trigger": trigger, "ace_data": ace_data}
                        return HttpResponseRedirect('/dekodiranjeadmin/')
                        return render(request, "mysite/dekodiranjeadmin.html", arg)

from django.core.paginator import Paginator

def lista(request):
    entry_data = EntryTable.objects.all()
    paginator = Paginator(entry_data, 25) # Show 25 contacts per page

    page = request.GET.get('page')
    pages = paginator.get_page(page)
    return render(request, 'mysite/list.html', {'pages': pages})


from datetime import datetime
from datetime import timedelta

@login_required(login_url='/login/')
def dashboard(request):
        if request.user.groups.filter(name = 'level_1').exists():

                now = datetime.now()
                thisyear = str(now.year)
                lastyear = str(int(thisyear) - 1)
                thismonth = str(now.month)
                lastmonth = str(int(thismonth) - 1)

                start_date = datetime.now().date() + timedelta( days=1 )
                end_date_today = start_date - timedelta( days=1 )
                today_use = SearchLog.objects.filter(datenow__range=[end_date_today, start_date]).count()

                if thismonth == '1':
                        month_list = ['na', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart', 'februar']
                        januar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).count()
                        decembar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=12).count()
                        novembar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=11).count()
                        oktobar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=10).count()
                        septembar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=9).count()
                        avgust = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=8).count()
                        month_count = ['na', januar, decembar, novembar, oktobar, septembar, avgust]
                elif thismonth =='2':
                        month_list = ['na', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart']
                        februar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).count()
                        januar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=1).count()
                        decembar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=12).count()
                        novembar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=11).count()
                        oktobar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=10).count()
                        septembar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=9).count()
                        month_count = ['na', februar, januar, decembar, novembar, oktobar, septembar]
                elif thismonth =='3':
                        month_list = ['na', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april']
                        mart = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).count()
                        februar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=2).count()
                        januar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=1).count()
                        decembar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=12).count()
                        novembar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=11).count()
                        oktobar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=10).count()
                        month_count = ['na', mart, februar, januar, decembar, novembar, oktobar]
                elif thismonth =='4':
                        month_list = ['na', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj']
                        april = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).count()
                        mart = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=3).count()
                        februar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=2).count()
                        januar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=1).count()
                        decembar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=12).count()
                        novembar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=11).count()
                        month_count = ['na', april, mart, februar, januar, decembar, novembar]
                elif thismonth =='5':
                        month_list = ['na', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun']
                        maj = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).count()
                        april = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=4).count()
                        mart = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=3).count()
                        februar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=2).count()
                        januar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=1).count()
                        decembar = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=12).count()
                        month_count = ['na', maj, april, mart, februar, januar, decembar]
                elif thismonth =='6':
                        month_list = ['na', 'jun', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul']
                        jun = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).count()
                        maj = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=5).count()
                        april = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=4).count()
                        mart = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=3).count()
                        februar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=2).count()
                        januar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=1).count()
                        month_count = ['na', jun, maj, april, mart, februar, januar]
                elif thismonth =='7':
                        month_list = ['na', 'jul', 'jun', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust']
                        jul = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).count()
                        jun = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=6).count()
                        maj = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=5).count()
                        april = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=4).count()
                        mart = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=3).count()
                        februar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=2).count()
                        month_count = ['na', jul, jun, maj, april, mart, februar]
                elif thismonth =='8':
                        month_list = ['na', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar']
                        avgust = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).count()
                        jul = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=7).count()
                        jun = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=6).count()
                        maj = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=5).count()
                        april = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=4).count()
                        mart = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=3).count()
                        month_count = ['na', avgust, jul, jun, maj, april, mart]
                elif thismonth =='9':
                        month_list = ['na', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar']
                        septembar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).count()
                        avgust = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=8).count()
                        jul = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=7).count()
                        jun = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=6).count()
                        maj = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=5).count()
                        april = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=4).count()
                        month_count = ['na', septembar, avgust, jul, jun, maj, april]
                elif thismonth =='10':
                        month_list = ['na', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar']
                        oktobar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).count()
                        septembar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=9).count()
                        avgust = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=8).count()
                        jul = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=7).count()
                        jun = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=6).count()
                        maj = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=5).count()
                        month_count = ['na', oktobar, septembar, avgust, jul, jun, maj]
                elif thismonth =='11':
                        month_list = ['na', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar']
                        novembar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).count()
                        oktobar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=10).count()
                        septembar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=9).count()
                        avgust = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=8).count()
                        jul = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=7).count()
                        jun = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=6).count()
                        month_count = ['na', novembar, oktobar, septembar, avgust, jul, jun]
                elif thismonth =='12':
                        month_list = ['na', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart', 'februar', 'januar']
                        decembar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).count()
                        novembar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=11).count()
                        oktobar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=10).count()
                        septembar = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=9).count()
                        avgust = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=8).count()
                        jul = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=7).count()
                        month_count = ['na', decembar, novembar, oktobar, septembar, avgust, jul]



                if thismonth == '1':
                        month_list = ['na', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart', 'februar']
                        januar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count()
                        decembar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).count()
                        novembar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=11).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=11).count()
                        oktobar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=10).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=10).count()
                        septembar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=9).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=9).count()
                        avgust = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=8).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=8).count()
                        req_month_count = ['na', januar, decembar, novembar, oktobar, septembar, avgust]
                elif thismonth =='2':
                        month_list = ['na', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart']
                        februar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count() + EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count()
                        januar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=1).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=1).count()
                        decembar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).count()
                        novembar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=11).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=11).count()
                        oktobar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=10).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=10).count()
                        septembar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=9).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=9).count()
                        req_month_count = ['na', februar, januar, decembar, novembar, oktobar, septembar]
                elif thismonth =='3':
                        month_list = ['na', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april']
                        mart = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count()
                        februar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=2).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=2).count()
                        januar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=1).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=1).count()
                        decembar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).count()
                        novembar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=11).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=11).count()
                        oktobar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=10).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=10).count()
                        req_month_count = ['na', mart, februar, januar, decembar, novembar, oktobar]
                elif thismonth =='4':
                        month_list = ['na', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj']
                        april = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count()
                        mart = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=3).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=3).count()
                        februar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=2).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=2).count()
                        januar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=1).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=1).count()
                        decembar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).count()
                        novembar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=11).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=11).count()
                        req_month_count = ['na', april, mart, februar, januar, decembar, novembar]
                elif thismonth =='5':
                        month_list = ['na', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun']
                        maj = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count()
                        april = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=4).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=4).count()
                        mart = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=3).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=3).count()
                        februar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=2).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=2).count()
                        januar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=1).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=1).count()
                        decembar = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).count()
                        req_month_count = ['na', maj, april, mart, februar, januar, decembar]
                elif thismonth =='6':
                        month_list = ['na', 'jun', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul']
                        jun = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count()
                        maj = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=5).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=5).count()
                        april = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=4).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=4).count()
                        mart = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=3).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=3).count()
                        februar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=2).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=2).count()
                        januar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=1).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=1).count()
                        req_month_count = ['na', jun, maj, april, mart, februar, januar]
                elif thismonth =='7':
                        month_list = ['na', 'jul', 'jun', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust']
                        jul = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count()
                        jun = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=6).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=6).count()
                        maj = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=5).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=5).count()
                        april = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=4).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=4).count()
                        mart = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=3).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=3).count()
                        februar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=2).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=2).count()
                        req_month_count = ['na', jul, jun, maj, april, mart, februar]
                elif thismonth =='8':
                        month_list = ['na', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar', 'septembar']
                        avgust = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count()
                        jul = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=7).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=7).count()
                        jun = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=6).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=6).count()
                        maj = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=5).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=5).count()
                        april = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=4).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=4).count()
                        mart = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=3).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=3).count()
                        req_month_count = ['na', avgust, jul, jun, maj, april, mart]
                elif thismonth =='9':
                        month_list = ['na', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar', 'oktobar']
                        septembar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count()
                        avgust = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=8).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=8).count()
                        jul = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=7).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=7).count()
                        jun = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=6).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=6).count()
                        maj = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=5).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=5).count()
                        april = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=4).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=4).count()
                        req_month_count = ['na', septembar, avgust, jul, jun, maj, april]
                elif thismonth =='10':
                        month_list = ['na', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar', 'novembar']
                        oktobar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count()
                        septembar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=9).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=9).count()
                        avgust = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=8).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=8).count()
                        jul = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=7).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=7).count()
                        jun = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=6).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=6).count()
                        maj = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=5).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=5).count()
                        req_month_count = ['na', oktobar, septembar, avgust, jul, jun, maj]
                elif thismonth =='11':
                        month_list = ['na', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart', 'februar', 'januar', 'decembar']
                        novembar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count()
                        oktobar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=10).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=10).count()
                        septembar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=9).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=9).count()
                        avgust = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=8).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=8).count()
                        jul = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=7).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=7).count()
                        jun = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=6).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=6).count()
                        req_month_count = ['na', novembar, oktobar, septembar, avgust, jul, jun]
                elif thismonth =='12':
                        month_list = ['na', 'decembar', 'novembar', 'oktobar', 'septembar', 'avgust', 'jul', 'jun', 'maj', 'april', 'mart', 'februar', 'januar']
                        decembar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).count()
                        novembar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=11).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=11).count()
                        oktobar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=10).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=10).count()
                        septembar = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=9).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=9).count()
                        avgust = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=8).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=8).count()
                        jul = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=7).count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=7).count()
                        req_month_count = ['na', decembar, novembar, oktobar, septembar, avgust, jul]




                lockstatus_0 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(lockstatus=0).count()
                lockstatus_1 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(lockstatus=1).count()
                lockstatus_2 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(lockstatus=2).count()
                lockstatus_3 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(lockstatus=3).count()
                lockstatusthismonth = [lockstatus_0, lockstatus_1, lockstatus_2, lockstatus_3]

                group_1 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(usergroup='CS Business Complaint and Support Team').count()
                group_2 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(usergroup='CS Business Contact Center').count()
                group_3 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(usergroup='CS Complaint and Retention Center').count()
                group_4 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(usergroup='CS Online team').count()
                group_5 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(usergroup='CS Residental Contact Center').count()
                group_6 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(usergroup='CS Technical').count()
                group_7 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(usergroup='RCC TNPS team').count()
                group_8 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(usergroup='Sales').count()
                group_9 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(usergroup='Sales and CS content Team').count()
                group_10 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(usergroup='Telesales Team').count()
                group_11 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=thismonth).filter(usergroup='Training Team').count()
                groupthismonth = [group_1, group_2, group_3, group_4, group_5, group_6, group_7, group_8, group_9, group_10, group_11]

                requeststatus_1 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(status=0).count()
                requeststatus_2 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(status=1).count()
                requeststatus_3 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(status=2).count()
                requeststatus_4 = DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(status=3).count()
                requeststatusthismonth = [requeststatus_1, requeststatus_2, requeststatus_3, requeststatus_4]

                reqgroup_1 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='CS Business Complaint and Support Team').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='CS Business Complaint and Support Team').count()
                reqgroup_2 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='CS Business Contact Center').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='CS Business Contact Center').count()
                reqgroup_3 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='CS Complaint and Retention Center').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='CS Complaint and Retention Center').count()
                reqgroup_4 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='CS Online team').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='CS Online team').count()
                reqgroup_5 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='CS Residental Contact Center').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='CS Residental Contact Center').count()
                reqgroup_6 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='CS Technical').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='CS Technical').count()
                reqgroup_7 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='RCC TNPS team').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='RCC TNPS team').count()
                reqgroup_8 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='Sales').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='Sales').count()
                reqgroup_9 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='Sales and CS content Team').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='Sales and CS content Team').count()
                reqgroup_10 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='Telesales Team').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='Telesales Team').count()
                reqgroup_11 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='Training Team').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=thismonth).filter(createdbygroup='Training Team').count()
                reqgroupthismonth = [reqgroup_1, reqgroup_2, reqgroup_3, reqgroup_4, reqgroup_5, reqgroup_6, reqgroup_7, reqgroup_8, reqgroup_9, reqgroup_10, reqgroup_11]

                searchgroup =  (group_1 + group_2 + group_3 + group_4 + group_5 + group_6 + group_7 + group_8 + group_9 + group_10 + group_11)
                reqgroup = (reqgroup_1 + reqgroup_2 + reqgroup_3 + reqgroup_4 + reqgroup_5 + reqgroup_6 + reqgroup_7 + reqgroup_8 + reqgroup_9 + reqgroup_10 + reqgroup_11)
                if searchgroup != 0:
                        FCRthismonth = '%.2f'%((searchgroup-reqgroup)/searchgroup*100)
                else:
                        FCRthismonth = 0

                if thismonth == '1':
                        lockstatus_0 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=12).filter(lockstatus=0).count()
                        lockstatus_1 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=12).filter(lockstatus=1).count()
                        lockstatus_2 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=12).filter(lockstatus=2).count()
                        lockstatus_3 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month=12).filter(lockstatus=3).count()
                        lockstatuslastmonth = [lockstatus_0, lockstatus_1, lockstatus_2, lockstatus_3]

                        group_1 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month='12').filter(usergroup='CS Business Complaint and Support Team').count()
                        group_2 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month='12').filter(usergroup='CS Business Contact Center').count()
                        group_3 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month='12').filter(usergroup='CS Complaint and Retention Center').count()
                        group_4 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month='12').filter(usergroup='CS Online team').count()
                        group_5 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month='12').filter(usergroup='CS Residental Contact Center').count()
                        group_6 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month='12').filter(usergroup='CS Technical').count()
                        group_7 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month='12').filter(usergroup='RCC TNPS team').count()
                        group_8 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month='12').filter(usergroup='Sales').count()
                        group_9 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month='12').filter(usergroup='Sales and CS content Team').count()
                        group_10 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month='12').filter(usergroup='Telesales Team').count()
                        group_11 = SearchLog.objects.filter(datenow__year=lastyear).filter(datenow__month='12').filter(usergroup='Training Team').count()
                        grouplastmonth = [group_1, group_2, group_3, group_4, group_5, group_6, group_7, group_8, group_9, group_10, group_11]

                        requeststatus_1 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).filter(status=0).count()
                        requeststatus_2 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).filter(status=1).count()
                        requeststatus_3 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).filter(status=2).count()
                        requeststatus_4 = DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month=12).filter(status=3).count()
                        requeststatuslastmonth = [requeststatus_1, requeststatus_2, requeststatus_3, requeststatus_4]

                        reqgroup_1 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='CS Business Complaint and Support Team').count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='CS Business Complaint and Support Team').count()
                        reqgroup_2 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='CS Business Contact Center').count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='CS Business Contact Center').count()
                        reqgroup_3 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='CS Complaint and Retention Center').count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='CS Complaint and Retention Center').count()
                        reqgroup_4 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='CS Online team').count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='CS Online team').count()
                        reqgroup_5 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='CS Residental Contact Center').count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='CS Residental Contact Center').count()
                        reqgroup_6 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='CS Technical').count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='CS Technical').count()
                        reqgroup_7 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='RCC TNPS team').count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='RCC TNPS team').count()
                        reqgroup_8 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='Sales').count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='Sales').count()
                        reqgroup_9 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='Sales and CS content Team').count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='Sales and CS content Team').count()
                        reqgroup_10 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='Telesales Team').count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='Telesales Team').count()
                        reqgroup_11 = EntryTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='Training Team').count() + DataTable.objects.filter(datecreated__year=lastyear).filter(datecreated__month='12').filter(createdbygroup='Training Team').count()
                        reqgrouplastmonth = [reqgroup_1, reqgroup_2, reqgroup_3, reqgroup_4, reqgroup_5, reqgroup_6, reqgroup_7, reqgroup_8, reqgroup_9, reqgroup_10, reqgroup_11]

                        searchgroup =  (group_1 + group_2 + group_3 + group_4 + group_5 + group_6 + group_7 + group_8 + group_9 + group_10 + group_11)
                        reqgroup = (reqgroup_1 + reqgroup_2 + reqgroup_3 + reqgroup_4 + reqgroup_5 + reqgroup_6 + reqgroup_7 + reqgroup_8 + reqgroup_9 + reqgroup_10 + reqgroup_11)
                        if searchgroup != 0:
                                FCRlastmonth = '%.2f'%((searchgroup-reqgroup)/searchgroup*100)
                        else:
                                FCRlastmonth = 0
                else:
                        lockstatus_0 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(lockstatus=0).count()
                        lockstatus_1 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(lockstatus=1).count()
                        lockstatus_2 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(lockstatus=2).count()
                        lockstatus_3 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(lockstatus=3).count()
                        lockstatuslastmonth = [lockstatus_0, lockstatus_1, lockstatus_2, lockstatus_3]

                        group_1 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(usergroup='CS Business Complaint and Support Team').count()
                        group_2 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(usergroup='CS Business Contact Center').count()
                        group_3 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(usergroup='CS Complaint and Retention Center').count()
                        group_4 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(usergroup='CS Online team').count()
                        group_5 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(usergroup='CS Residental Contact Center').count()
                        group_6 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(usergroup='CS Technical').count()
                        group_7 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(usergroup='RCC TNPS team').count()
                        group_8 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(usergroup='Sales').count()
                        group_9 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(usergroup='Sales and CS content Team').count()
                        group_10 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(usergroup='Telesales Team').count()
                        group_11 = SearchLog.objects.filter(datenow__year=thisyear).filter(datenow__month=lastmonth).filter(usergroup='Training Team').count()
                        grouplastmonth = [group_1, group_2, group_3, group_4, group_5, group_6, group_7, group_8, group_9, group_10, group_11]

                        requeststatus_1 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(status=0).count()
                        requeststatus_2 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(status=1).count()
                        requeststatus_3 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(status=2).count()
                        requeststatus_4 = DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(status=3).count()
                        requeststatuslastmonth = [requeststatus_1, requeststatus_2, requeststatus_3, requeststatus_4]

                        reqgroup_1 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='CS Business Complaint and Support Team').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='CS Business Complaint and Support Team').count()
                        reqgroup_2 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='CS Business Contact Center').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='CS Business Contact Center').count()
                        reqgroup_3 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='CS Complaint and Retention Center').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='CS Complaint and Retention Center').count()
                        reqgroup_4 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='CS Online team').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='CS Online team').count()
                        reqgroup_5 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='CS Residental Contact Center').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='CS Residental Contact Center').count()
                        reqgroup_6 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='CS Technical').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='CS Technical').count()
                        reqgroup_7 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='RCC TNPS team').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='RCC TNPS team').count()
                        reqgroup_8 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='Sales').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='Sales').count()
                        reqgroup_9 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='Sales and CS content Team').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='Sales and CS content Team').count()
                        reqgroup_10 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='Telesales Team').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='Telesales Team').count()
                        reqgroup_11 = EntryTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='Training Team').count() + DataTable.objects.filter(datecreated__year=thisyear).filter(datecreated__month=lastmonth).filter(createdbygroup='Training Team').count()
                        reqgrouplastmonth = [reqgroup_1, reqgroup_2, reqgroup_3, reqgroup_4, reqgroup_5, reqgroup_6, reqgroup_7, reqgroup_8, reqgroup_9, reqgroup_10, reqgroup_11]

                        searchgroup =  (group_1 + group_2 + group_3 + group_4 + group_5 + group_6 + group_7 + group_8 + group_9 + group_10 + group_11)
                        reqgroup = (reqgroup_1 + reqgroup_2 + reqgroup_3 + reqgroup_4 + reqgroup_5 + reqgroup_6 + reqgroup_7 + reqgroup_8 + reqgroup_9 + reqgroup_10 + reqgroup_11)
                        if searchgroup != 0:
                                FCRlastmonth = '%.2f'%((searchgroup-reqgroup)/searchgroup*100)
                        else:
                                FCRlastmonth = 0

                item_1 = Counters.objects.get(pk=1)
                item_2 = Counters.objects.get(pk=2)
                counter_sum = item_1.counter_01
                entry_sum = item_2.counter_01

                duzina = int(counter_sum)
                eleven = str(counter_sum)

                if duzina == 0:
                        counter_sum_1 = uri_to_iri('izvršeno')
                        counter_sum_2 = uri_to_iri('pretraga')
                elif duzina == 1:
                        counter_sum_1 = uri_to_iri('izvršena')
                        counter_sum_2 = uri_to_iri('pretraga')
                elif eleven[-1] == '1' and eleven[-2] == '1':
                        counter_sum_1 = uri_to_iri('izvršeno')
                        counter_sum_2 = uri_to_iri('pretraga')
                elif eleven[-1] == '1':
                        counter_sum_1 = uri_to_iri('izvršena')
                        counter_sum_2 = uri_to_iri('pretraga')
                elif duzina == 2 or duzina == 3 or duzina == 4:
                        counter_sum_1 = uri_to_iri('izvršene')
                        counter_sum_2 = uri_to_iri('pretrage')
                elif eleven[-1] == '2' and eleven[-2] == '1':
                        counter_sum_1 = uri_to_iri('izvršeno')
                        counter_sum_2 = uri_to_iri('pretraga')
                elif eleven[-1] == '3' and eleven[-2] == '1':
                        counter_sum_1 = uri_to_iri('izvršeno')
                        counter_sum_2 = uri_to_iri('pretraga')
                elif eleven[-1] == '4' and eleven[-2] == '1':
                        counter_sum_1 = uri_to_iri('izvršeno')
                        counter_sum_2 = uri_to_iri('pretraga')
                elif eleven[-1] == '2' or eleven[-1] == '3' or eleven[-1] == '4':
                        counter_sum_1 = uri_to_iri('izvršene')
                        counter_sum_2 = uri_to_iri('pretrage')
                elif duzina > 4:
                        counter_sum_1 = uri_to_iri('izvršeno')
                        counter_sum_2 = uri_to_iri('pretraga')

                duzina = int(entry_sum)
                eleven = str(entry_sum)

                if duzina == 0:
                        entry_sum_1 = uri_to_iri('podneto')
                        entry_sum_2 = uri_to_iri('zahteva')
                elif duzina == 1:
                        entry_sum_1 = uri_to_iri('podnet')
                        entry_sum_2 = uri_to_iri('zahtev')
                elif eleven[-1] == '1' and eleven[-2] == '1':
                        entry_sum_1 = uri_to_iri('podneto')
                        entry_sum_2 = uri_to_iri('zahteva')
                elif eleven[-1] == '1':
                        entry_sum_1 = uri_to_iri('podnet')
                        entry_sum_2 = uri_to_iri('zahtev')
                elif duzina == 2 or duzina == 3 or duzina == 4:
                        entry_sum_1 = uri_to_iri('podneta')
                        entry_sum_2 = uri_to_iri('zahteva')
                elif eleven[-1] == '2' and eleven[-2] == '1':
                        entry_sum_1 = uri_to_iri('podneto')
                        entry_sum_2 = uri_to_iri('zahteva')
                elif eleven[-1] == '3' and eleven[-2] == '1':
                        entry_sum_1 = uri_to_iri('podneto')
                        entry_sum_2 = uri_to_iri('zahteva')
                elif eleven[-1] == '4' and eleven[-2] == '1':
                        entry_sum_1 = uri_to_iri('podneto')
                        entry_sum_2 = uri_to_iri('zahteva')
                elif eleven[-1] == '2' or eleven[-1] == '3' or eleven[-1] == '4':
                        entry_sum_1 = uri_to_iri('podneta')
                        entry_sum_2 = uri_to_iri('zahteva')
                elif duzina > 4:
                        entry_sum_1 = uri_to_iri('podneto')
                        entry_sum_2 = uri_to_iri('zahteva')




                arg = {"today_use": today_use, "lockstatusthismonth": lockstatusthismonth, "lockstatuslastmonth": lockstatuslastmonth, "groupthismonth": groupthismonth,"grouplastmonth": grouplastmonth, "thismonth": thismonth, "thisyear": thisyear, "month_list": month_list, "month_count": month_count, "req_month_count": req_month_count, "counter_sum": counter_sum, "entry_sum": entry_sum, "requeststatusthismonth": requeststatusthismonth, "requeststatuslastmonth": requeststatuslastmonth, "reqgroupthismonth": reqgroupthismonth, "reqgrouplastmonth": reqgrouplastmonth, "FCRthismonth": FCRthismonth, "FCRlastmonth": FCRlastmonth, "counter_sum_1": counter_sum_1, "counter_sum_2": counter_sum_2, "entry_sum_1": entry_sum_1, "entry_sum_2": entry_sum_2}
                return render(request, "mysite/dashboard.html", arg)
        else:
                return HttpResponseRedirect('/')



# napraviti skriptu koja će čuvati TXT ACE liste na serveru i nuditi da se iste skinu (indexiran backup) - DONE
# napraviti alert kada je lista empty - promeniti da bude JS - DONE
# MSISDN mora da bude u 381 formatu - DONE
# ograničiti duplirane zahteve u input formu - DONE
# Tabelu srediti tako da mora da se postuje forma - setovan readonly za sada !!!
# are u sure popup kada se brise unos sa liste - DONE
# ACE Liste moraju da budu ograničene na po 500 redova - DONE
# da se kontrolisu duplikati prilikom kreiranja ACE lista - DONE
# ZIP-uj ACE listu/e - DONE
# da se izvede da se status menja na 3 i da se migracija radi tek kada se download-uje ACE lista - DONE
# sredi da se sada radi backup za ZIP umesto TXT ACE liste - DONE
# prekontrolisati HTML templejte - DONE
# sredi izgled tastera za IPAK PODNESI ZAHTEV - DONE
# napravi Select all za prvi modul "download_list" - DONE
# da ne skida prazan ZIP - DONE
# notifikacija kada se ne obelezi ni jedan checkbutton - DONE
# uveži Search sa obe baze - DONE
# kreiraj stranicu za odvojenu tabelu za Obrađene zahteve i linkuj - DONE
# update all za listu - ne radi se za sada !!!
# napravi paginaciju za tabele - DONE
# forma za unos novih zahteva da bude vise responsive - DONE
# uploaduj Nokia modele - drop down list sa pretragom - DONE
# sredi button za Unos kodova za dekodiranje - DONE
# preslikaj segment realisticne baze u DB - DONE
# preslikaj unlock u db - uvezi sa search - DONE
# sredi logo - DONE
# izmeni About - DONE
# paginacija za CSV upload - DONE
# napravi login - DONE
# mandatory login za svaku stranu - DONE
# nije zakljucan ??
# upload CSV, nokia add #pw+unlock+7#, 8 nula za samsung - DONE
# logovi - DONE
# Nokia da se skida po Winlock-u (npr. Winlock 5 jedan folder) - DONE
# automatsko prepoznavanje uredjaja na osnovu IMEI-ja i adekvatne poruke - DONE
# preslikavanje prepoznatog modela u input - DONE
# sredi da se provera vrsi i za IMEI koji pocinje sa nulom - DONE
# sredi iscitavanje unc kada je iz RATbox tiketinga - DONE
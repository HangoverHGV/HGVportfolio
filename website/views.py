from flask import Blueprint, render_template, request, redirect, url_for, send_file
from flask_login import login_required, current_user
import os
from .models import *
from .calculatorcubaj import Volum
from .convertpdf import CreateAndDelete, convert_pdf2docx
from .ytdownloader import SongDownload, PlaylistDownload
from . import dimension_i7
from . import dimension_electrica

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', user=current_user)

@views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html', user=current_user)




#-------------------------------------------------------------------------------------------------------------------

vol = 0
tot = 0

@views.route('/calculatorcubaj', methods = ["POST", "GET"])
@login_required
def calculate():
    global vol, tot
    context = {}
    if request.method == 'POST':
        vol = 0
        lungime = request.form['lungime']
        diametru = request.form['diametru']


        if lungime.isdigit() and diametru.isdigit():
            dimensions = Rezultate(lungime=lungime, diametru=diametru, volumul=Volum(lungime, diametru),user_id=current_user.id)
            db.session.add(dimensions)
            db.session.commit()
            vol = Volum(lungime, diametru)
        elif lungime == '' or diametru == '':
            alert = 'No Blanks'
            context = {'message': alert}
        elif not lungime.isdigit() and not diametru.isdigit():
            alert = 'All Values must be digits'
            context = {'message': alert}

    elif request.method == 'GET':
        total = 0
        result = Rezultate.query.all()

        for i in result:
            if i.user_id == current_user.id:
                total += float(i.volumul)

        tot = round(total, 3)


    return render_template('calculatorcubaj.html', user=current_user, volum=vol, total=tot, context=context)

@views.route('/delete/<int:id>', methods = ['GET', 'POST'])
def delete(id):
    row_to_delete = Rezultate.query.get(id)
    db.session.delete(row_to_delete)

    db.session.commit()
    return redirect(url_for('views.calculate'))

@views.route('/pdfconvert', methods = ['GET', 'POST'])
def pdfconvert():
    if request.method == 'POST':
        dir_path = r'files'
        CreateAndDelete(dir_path)

        savePath = 'files/'

        file = request.files['pdf']
        if not file:
            return redirect(url_for('views.pdfconvert'))
        file.save(savePath + file.filename)
        filePath = savePath + str(os.path.basename(file.filename))
        fileName, fileextension = os.path.splitext(file.filename)

        destination = 'files/'
        path = 'files/' + fileName + '.docx'
        convert_pdf2docx(filePath, destination)
        print(convert_pdf2docx(filePath, destination))
        var = send_file(path, as_attachment=True)

        return var


    return render_template('pdfconvert.html', user=current_user)

@views.route('/ytdownloader', methods = ['GET', 'POST'])
def ytdownloader():
    if request.method == 'POST':
        link = request.form['link']
        word = 'playlist'
        if word in link:
            download = PlaylistDownload(link)
        else:
            download = SongDownload(link)

        return send_file(download, as_attachment=True)
    return render_template('ytdownloader.html', user = current_user)

@views.route('/cable_dimension', methods = ['GET','POST'])
def CableDimension():

    sigurante = [2, 4, 6, 8, 10, 12, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250]
    siguranta = ''
    putere_D = ''
    lungime_D = ''
    normativ = ''
    tip_material_D = ''
    tip_D = ''
    pozare_D = ''
    curent = ''
    DUp = ''
    DP = ''
    DU = ''
    sectiunea = ''
    rezultat =[]
    red = False
    red_P = False

    if request.method == 'POST':
        n_electrica = ['subteran', 'aerian']
        n_anrei7 = ['subteran_tub', 'aerian_tub', 'aerian_notub']
        pozare = request.form.get('pozare')
        tip_material = request.form.get('tip_material')
        tip = request.form.get('tip')
        putere = request.form['putere']
        lungime = request.form['lungime']

        P = float(putere)
        L = float(lungime)

        if pozare in n_electrica:
            normativ = 'NTE 007'
            if tip_material == 'cu':
                tip_material_D = 'Copper'
                rezultat = dimension_electrica.SectiuneCu(P, L, pozare, tip)
            if tip_material== 'al':
                tip_material_D = 'Aluminium'
                rezultat = dimension_electrica.SectiuneAl(P, L, pozare, tip)

        if pozare in n_anrei7:
            normativ = 'ANRE I7'
            if tip_material == 'cu':
                tip_material_D = 'Copper'
                rezultat = dimension_i7.SectiuneCu(P, L, pozare, tip)
            if tip_material== 'al':
                tip_material_D = 'Aluminium'
                rezultat = dimension_i7.SectiuneAl(P, L, pozare, tip)

        if pozare == n_electrica[0]:
            pozare_D = 'Underground'
        if pozare == n_electrica[1]:
            pozare_D = 'In air'
        if pozare == n_anrei7[0]:
            pozare_D = 'Underground, in tube'
        if pozare == n_anrei7[1]:
            pozare_D = 'Ia air, in tube'
        if pozare == n_anrei7[2]:
            pozare_D = 'In air'

        if tip == 'trifazic':
            tip_D = 'Three Phase'
        elif tip == 'monofazic':
            tip_D = 'One Phase'

        tip_D = tip

        curent = str(round(rezultat[0], 3))
        DUp = str(round(rezultat[1], 3))
        DU = str(round(rezultat[2], 3))
        DP = str(round(rezultat[3], 3))
        sectiunea = str(rezultat[4])
        red = rezultat[-1]

        if float(curent) > sigurante[-1]:
            siguranta = sigurante[-1]
            red_P = True
        putere_D = str(putere)
        lungime_D =str(lungime)
        for s in sigurante:
            if float(curent) < s:
                siguranta = str(s)
                break

    return render_template('cableDimensoin.html', user=current_user, curent=curent, dup=DUp, du=DU, dp=DP, s=sectiunea, sig=siguranta, red=red, red_P=red_P, pozare=pozare_D, tip_material=tip_material_D, tip=tip_D, putere=putere_D, lungime=lungime_D, normativ=normativ)


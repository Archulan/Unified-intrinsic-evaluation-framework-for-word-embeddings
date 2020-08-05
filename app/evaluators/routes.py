from app.evaluators import blueprint
from flask import render_template, redirect, url_for, request, flash
from app.base.util import allowed_file
from werkzeug.utils import secure_filename
import os
import wget
from app.evaluators.distance import similarity
from app.evaluators.word_analogy import analogy
from app.evaluators.OutlierDetection import outlier as out
from app.evaluators.conceptcate import categorize

from flask import jsonify, make_response
import json
from app.base.models import db, Repository


@blueprint.route('/upload-file', methods=['GET', 'POST'])
def upload_file():
    base_dir = 'c:\\users\\hp\\Desktop\\fyp\\data\\Evaluator\\flask\\app\\base\\uploads'

    if request.method == 'POST':
        # check if the post request has the file part
        dim = request.form['dim']
        name = request.form['name']
        # if user does not select file, browser also
        # submit an empty part without filename
        if request.form['modelRadios'] == "option2":
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(base_dir,
                                    filename)
                repofolder = os.path.join(
                    'c:\\users\\hp\\Desktop\\fyp\\data\\Evaluator\\flask\\app\\base\\repository',
                    filename)
                file.save(path)
        else:
            url = request.form['link']
            path = os.path.join(base_dir, name + ".txt")
            wget.download(url, path)
            repofolder = os.path.join(
                'c:\\users\\hp\\Desktop\\fyp\\data\\Evaluator\\flask\\app\\base\\repository',
                name + ".txt")

        result = similarity(path, dim)
        #result1 = analogy(path, dim)
        result2=categorize(path,dim)
        result3= out(path,dim)
        #result.extend(result1)
        result.append(result2)
        result.append(result3)
        sim, rw, synana, semana, ambi, concept, outlier, oop = 0, 0, 0, 0, 0, 0, 0, 0
        for res in result:
            if res["Test"] == "Word similarity":
                sim = res["Score"]
            elif res["Test"] == "RW similarity":
                rw = res["Score"]
            elif res["Test"] == "Syn analogy":
                synana = res["Score"]
            elif res["Test"] == "Sem analogy":
                semana = res["Score"]
            elif res["Test"] == "Concept categorization":
                concept = res["Score"]
            elif res["Test"] == "Outlier Detection":
                outlier = res["Score"]
            elif res["Test"] == "Outlier-oop":
                oop = res["Score"]
            elif res["Test"] == "Ambiguity":
                ambi = res["Score"]

        response_body = {
            "modelname": request.form['name'],
            "description ": request.form['description'],
            "dimension ": request.form['dim'],
            "result": result
        }

        repo = Repository(
            modelname=request.form['name'],
            description=request.form['description'],
            dimension=request.form['dim'],
            wordsimilarity=sim,
            semanalogy=semana,
            synanalogy=synana,
            rw=rw,
            ambiguity=ambi,
            conceptcate=concept,
            outlier=outlier

        )
        db.session.add(repo)
        db.session.commit()
        with open(repofolder, 'w') as outfile:
            json.dump(response_body, outfile)

        cols = ["#", "Test", "Score", "OOV"]
        return render_template('result.html', records=result, colnames=cols, title=response_body["modelname"])
    return ""
    # render_template("result.html")



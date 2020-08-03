# -*- encoding: utf-8 -*-
"""
MIT License
Copyright (c) 2019 - present AppSeed.us
"""

from app.home import blueprint
from flask import render_template, redirect, url_for, request,flash
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from app.base.models import db, Repository
@blueprint.route('/index')
@login_required
def index():

    return render_template('index.html')
@blueprint.route('/ui-tables.html')
def get_repo():
    return render_template('ui-tables.html',repos=Repository.query.all())

@blueprint.route('/result.html/<id>')
def show_result(id):
    result=Repository.query.filter_by(id=id).first()
    return render_template('repo-result.html',repo=result)
@blueprint.route('/<template>')
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        return render_template( template )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500


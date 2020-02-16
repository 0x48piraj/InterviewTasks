from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import sys
import json
import os
import shutil
import MySQLdb
# App config.
#DEBUG = True
app = Flask(__name__)
app.config['SECRET_KEY'] = '3d441f27u331c27333d331k2f3333a'


class ReusableForm(Form):
    name = TextField("What's your Name?")
    reg = TextField("What's your Registration Number?")
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    if len(form.errors) != 0:
       print(form.errors)
    if request.method == 'POST':
        name=request.form['name']
        reg=request.form['reg']
        print("Sending data to the database : ", name, " ", reg, " ")
        conn = MySQLdb.connect(host= "localhost",
                    user="root",
                    passwd="root",
                    db="PT_Intern")
        x = conn.cursor()
        conn.set_character_set('utf8')
        x.execute('SET NAMES utf8;')
        x.execute('SET CHARACTER SET utf8;')
        x.execute('SET character_set_connection=utf8;')
        if len(name) != 0:
            if len(reg) != 0:
                x.execute("""INSERT IGNORE INTO student_data (name, reg) VALUES (%s,%s)""",(name, reg))
                conn.commit()
                flash('Stored!')
                conn.close()
                flash('Thanks for Registering ' + name)
            else:
             flash('Error: `Registration Number` in the form field is required.')

        else:
            flash('Error: `Name` in the form field is required.')
 
    return render_template('index.html', form=form)



if __name__ == "__main__":
    app.run()
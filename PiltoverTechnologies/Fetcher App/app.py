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
    search = TextField("What's your search?")
 
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)
    if len(form.errors) != 0:
       print(form.errors)
    if request.method == 'POST':
        search=request.form['search']
        print("Searching data from the database : ", search, " ")
        db = MySQLdb.connect(host= "localhost",
                    user="root",
                    passwd="root",
                    db="PT_Intern")
        cursor = db.cursor()
        sql_table = "select * from student_data" #additional data
        sql = "select * from student_data where name LIKE " + "'" + str(search) + "'" + "OR reg LIKE " + "'" + str(search) + "'"
        fetch=cursor.execute(sql)
        list_data=[list(i) for i in cursor.fetchmany(fetch)]
        db.close()
        if len(search) != 0:
            if fetch != 0:
                if len(list_data) != 1:
                    flash("More than one entries found.")
                    flash("Here's the log data : " + str(list_data))
                flash("Success!  : ")
                flash("Name : "+ str(list_data[0][0]))
                flash("Registration Number : "+ str(list_data[0][1]))
            else:
             flash('Error: No data exists.')

        else:
            flash('Error: `Search` in the form field is required.')
 
    return render_template('index.html', form=form)




if __name__ == "__main__":
    app.run()
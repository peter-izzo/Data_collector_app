from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:sf49ers@localhost:5432/data_collector'
db=SQLAlchemy(app)

#a group to compare user input eye color to
#if it didn't match one of the values in colors, an error would be given to them
COLORS = ["Blue", "Green", "Brown", "Hazel", "Amber", "Grey", "Red"]

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(120), unique=True)
    height=db.Column(db.Integer)
    color=db.Column(db.String(5))
    pct=db.Column(db.DECIMAL)

def get_avg_height(height):
    return db.session.query(func.avg(height)).scalar()

def is_email_available(email):
    return (db.session.query(Data).filter(Data.email==email).count()==0)


def save_data(email, height, color):
    data=Data(email=email, height=height, color=color)
    db.session.add(data)
    db.session.commit()
    return data


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        email=request.form.get("email_name")
        height=request.form.get("height_name")
        color=request.form.get("color_name")
        color=color.capitalize()

        #if user input color didn't match with any colors in the list
        #error is displayed
        if color not in COLORS:
            return render_template("index.html",
            text="Invalid color, dog!")


        if not is_email_available(email):
            #If email address already received
            return render_template("index.html",
            text="Seems like we've gotten something from that email address already!")


        save_data(email, height, color)
        send_email(email, height, color, pct)
        average_height = get_avg_height(height)
        #thought I could add sql code to python to get the db to create the percentage Column
        #from there I would email the percentage of whatever color user input back to them
        #pct = SELECT color, count(*) AS user_count,
        #COUNT(*) * 100.0/ SUM(COUNT(*)) OVER() as percent
        print(average_height)
        print(pct)
        return render_template("success.html")



     #tried to do the same thing with this one but it didn't work
    #return render_template("index.html",
     #input_value="Seems like you've input an invalid color.")

if __name__ == '__main__':
    app.debug=True
    app.run()

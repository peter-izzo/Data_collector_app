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
    return db.session.query(func.avg(Data.height)).scalar()

#makes sure users can only input unique emails
def is_email_available(email):
    return (db.session.query(Data).filter(Data.email==email).count()==0)

#saves input data
def save_data(email, height, color):
    data=Data(email=email, height=height, color=color)
    db.session.add(data)
    db.session.commit()
    return data

#Function that takes percentage of user input eye color
def find_pct(color):
    return db.session.query(
            db.func.count().filter(Data.color == color) * 100.0 /
            db.func.count()).\
        scalar()


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
        get_avg_height(height)
        #rounded avg of height & eye color percent
        average_height = round(get_avg_height(height))
        count = db.session.query(Data.height).count()
        find_pct(color)
        rounded_pct = round(find_pct(color))
        send_email(email, height, color, average_height, rounded_pct, count)


        return render_template("success.html")



if __name__ == '__main__':
    app.debug=True
    app.run()

from flask import Flask , render_template , request , url_for , make_response , flash , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date , datetime


app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']='your_secret_key'
db=SQLAlchemy(app)

class Expense(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    description=db.Column(db.String(100),nullable=False)
    amount=db.Column(db.Float,nullable=False)
    category=db.Column(db.String(50),nullable=False)
    date=db.Column(db.Date,nullable=False,default=date.today)




with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add",methods=['POST'])
def add():
    
    description=(request.form.get("description") or "").strip()
    amount_str=(request.form.get("amount")or "").strip()
    category=(request.form.get("category")or "").strip()
    date_str=(request.form.get("date")or "").strip()
    
    if not description or not amount_str or not category:
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("index"))
    try:
        amount=float(amount_str)    
        if amount <= 0:
            raise ValueError
    except ValueError:
        flash("Please enter a valid positive amount.", "error")
        return redirect(url_for("index"))
    
    try:
        date_obj=datetime.strptime(date_str,"%Y-%m-%d").date() if date_str else date.today()
    except ValueError:
        date_obj=date.today()    
        
    e=Expense(description=description,amount=amount,category=category,date=date_obj)    
    db.session.add(e)
    db.session.commit()
    
    flash("Expense added successfully!","success")
    return redirect(url_for("index"))
        
         
    
    
    
    
    print("Form received:",dict(request.form))
    return make_response("Form received check the console")



if __name__ == "__main__":
    app.run(debug=True)



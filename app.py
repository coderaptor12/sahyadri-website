from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

# Image Upload Folder
UPLOAD_FOLDER = "static/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# HOME PAGE

@app.route("/")
def home():

    return render_template("index.html")



# CONTACT PAGE

@app.route("/contact")
def contact():

    return render_template("contact.html")



# STAFF LOGIN PAGE

@app.route("/staff")
def staff():

    return render_template("staff_login.html")



# STAFF LOGIN CHECK

@app.route("/login",methods=["POST"])

def login():

    username=request.form["username"]
    password=request.form["password"]

    if username=="staff" and password=="1234":

        return render_template("staff_dashboard.html")

    else:

        return "Wrong Username or Password"



# PRODUCTS PAGE

@app.route("/products")

def products():

    product_list=[]

    try:

        with open("products.csv","r") as f:

            reader=csv.reader(f)

            for row in reader:

                product_list.append(row)

    except:

        pass


    return render_template("products.html",
                           products=product_list)



# PRODUCT UPLOAD

@app.route("/upload",methods=["POST"])

def upload():

    name=request.form["name"]
    price=request.form["price"]
    branch=request.form["branch"]

    image=request.files["image"]

    filename=image.filename

    image.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))


    with open("products.csv","a",newline="") as f:

        writer=csv.writer(f)

        writer.writerow([name,price,branch,filename])


    return redirect("/products")



# ORDER PAGE

@app.route("/orderpage")

def orderpage():

    return render_template("order.html")



# PLACE ORDER

@app.route("/order",methods=["POST"])

def order():

    name=request.form["name"]
    mobile=request.form["mobile"]
    address=request.form["address"]
    product=request.form["product"]
    branch=request.form["branch"]


    orderid=str(len(open("orders.csv").readlines())+1)


    with open("orders.csv","a",newline="") as f:

        writer=csv.writer(f)

        writer.writerow([orderid,name,mobile,address,product,branch,"Processing"])


    return "Your Order ID = "+orderid



# TRACK PAGE

@app.route("/track")

def trackpage():

    return render_template("track.html")



# TRACK ORDER

@app.route("/trackorder",methods=["POST"])

def trackorder():

    orderid=request.form["orderid"]

    try:

        with open("orders.csv","r") as f:

            reader=csv.reader(f)

            for row in reader:

                if row[0]==orderid:

                    return "Order Status = "+row[6]

    except:

        pass


    return "Order Not Found"



# RUN SERVER

app.run(debug=True)
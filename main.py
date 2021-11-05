from flask import *
import cx_Oracle, hashlib, os
import config as cfg
from werkzeug.utils import secure_filename

conn = cx_Oracle.connect(cfg.username, cfg.password, cfg.dsn, encoding=cfg.encoding)
app = Flask(__name__)
app.secret_key = 'random string'
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif'])
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def getLoginDetails():
    cur = conn.cursor()
    loggedIn = False
    firstName = ''
    noOfItems = 0

    try:
        if 'email' not in session:
            pass
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = '{0}'".format(session['email']))
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM kart WHERE userId = '{0}'".format(userId))
            noOfItems = cur.fetchone()[0]
    except:
        pass

    return (loggedIn, firstName, noOfItems)

@app.route("/")
def root():
    loggedIn, firstName, noOfItems = getLoginDetails()
    cur = conn.cursor()
    cur.execute('SELECT productId, name, price, description, image, stock FROM products')
    itemData = cur.fetchall()
    cur.execute('SELECT categoryId, name FROM categories')
    categoryData = cur.fetchall()
    itemData = parse(itemData)   
    return render_template('home.html', itemData=itemData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryData=categoryData)

@app.route("/add")
def admin():
    # cur = conn.cursor()
    # cur.execute("SELECT categoryId, name FROM categories")
    # categories = cur.fetchall()
    return render_template("checktoadd.html")
    # return render_template('add.html', categories=categories)

@app.route("/checktoadd", methods=["GET", "POST"])
def checktoadd():
    ide=""
    password=""
    if request.method == "POST":
        ide = request.form['ide']
        password = request.form['password']
    if (ide == "user@add.com" and password == "password"): #add/update username/password as per your choice
        cur = conn.cursor()
        cur.execute("SELECT categoryId, name FROM categories")
        categories = cur.fetchall()
        return render_template("add.html", categories=categories)
    else:
        error = "Invalid username/password"
        return render_template("checktoadd.html", error=error)


# added to check authority of user to remove posts
@app.route("/checktoremove", methods=["GET", "POST"])
def checktoremove():
    # ide=""
    # password=""
    if request.method == "POST":
        ide = request.form['ide']
        password = request.form['password']
        if (ide == "user@gremove.com" and password == "password"): #add/update username/password as per your choice
            cur = conn.cursor()
            cur.execute('SELECT productId, name, price, description, image, stock FROM products')
            data = cur.fetchall()
            return render_template("remove.html", data=data)
    else:
        error = "Invalid username/password"
        return render_template("checktoremove.html", error=error)z

    
@app.route("/checkout")
def checkOut():
    return "Create the checkout credentials"



@app.route("/addItem", methods=["GET", "POST"])
def addItem():
    global msg
    if request.method == "POST":
        name = request.form['name']
        price = float(request.form['price'])
        description = request.form['description']
        stock = int(request.form['stock'])
        categoryId = int(request.form['category'])

        #Uploading image procedure
        filename = "a"
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            os.makedirs(os.path.join(app.instance_path, 'htmlfi'), exist_ok=True)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(image.filename)))
        imagename = filename

        #creating random productId
        import random
        pid = random.randint(0,10**10)
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO products (name, price, description, image, stock, categoryId, productid) VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(name, price, description, imagename, stock, categoryId, pid))
            conn.commit()
            msg="added successfully"
        except Exception as e:
            msg="error occured"
            conn.rollback()
    
        print(msg)
        return redirect(url_for('root'))

@app.route("/remove")
def remove():
    # cur = conn.cursor()
    # cur.execute('SELECT productId, name, price, description, image, stock FROM products')
    # data = cur.fetchall()
    return render_template('checktoremove.html')
    # return render_template('remove.html', data=data)

@app.route("/removeItem")
def removeItem():
    productId = request.args.get('productId')
    try:
        cur = conn.cursor()
        cur.execute('''DELETE FROM products WHERE productID = '{}' '''.format(productId))
        conn.commit()
        msg = "Deleted successsfully"
    except:
        conn.rollback()
        msg = "Error occured"
     
    print(msg)
    return redirect(url_for('root'))

@app.route("/displayCategory")
def displayCategory():
        loggedIn, firstName, noOfItems = getLoginDetails()
        categoryId = request.args.get("categoryId")
        cur = conn.cursor()
        cur.execute("SELECT products.productId, products.name, products.price, products.image, categories.name FROM products, categories WHERE products.categoryId = categories.categoryId AND categories.categoryId = '{0}'".format(categoryId))
        data = cur.fetchall()         
        categoryName = data[0][4]
        data = parse(data)
        return render_template('displayCategory.html', data=data, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems, categoryName=categoryName)

@app.route("/account/profile")
def profileHome():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template("profileHome.html", loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    cur = conn.cursor()
    cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM users WHERE email = '{}'".format(session['email']))
    profileData = cur.fetchone()
     
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        cur = conn.cursor()
        cur.execute("SELECT userId, password FROM users WHERE email = '{0}'".format(session['email']))
        userId, password = cur.fetchone()
        if (password == oldPassword):
            try:
                cur.execute("UPDATE users SET password = '{}' WHERE userId = '{}'".format(newPassword, userId))
                conn.commit()
                msg="Changed successfully"
            except:
                conn.rollback()
                msg = "Failed"
            return render_template("changePassword.html", msg=msg)
        else:
            msg = "Wrong password"
         
        return render_template("changePassword.html", msg=msg)
    else:
        return render_template("changePassword.html")

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        try:
            cur = conn.cursor()
            cur.execute("UPDATE users SET firstName = '{}', lastName = '{}', address1 = '{}', address2 = '{}', zipcode = '{}', city = '{}', state = '{}', country = '{}', phone = '{}' WHERE email = '{}'".format(firstName, lastName, address1, address2, zipcode, city, state, country, phone, email))

            conn.commit()
            msg = "Saved Successfully"
        except:
            conn.rollback()
            msg = "Error occured"
        return redirect(url_for('editProfile'))

@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('root'))
    else:
        return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('root'))
        else:
            error = 'Invalid UserId / Password'
            return render_template('login.html', error=error)

@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    cur = conn.cursor()
    cur.execute("SELECT productId, name, price, description, image, stock FROM products WHERE productId = '{0}'".format(productId))
    productData = cur.fetchone()
     
    return render_template("productDescription.html", data=productData, loggedIn = loggedIn, firstName = firstName, noOfItems = noOfItems)

@app.route("/addToCart")
def addToCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        productId = int(request.args.get('productId'))
        cur = conn.cursor()
        cur.execute("SELECT userId FROM users WHERE email = '{0}'".format(session['email']))
        userId = cur.fetchone()[0]
        try:
            cur.execute("INSERT INTO kart (userId, productId) VALUES ('{0}', '{1}')".format(userId, productId))
            conn.commit()
            msg = "Added successfully"
        except:
            conn.rollback()
            msg = "Error occured"
        return redirect(url_for('root'))

@app.route("/cart")
def cart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    cur = conn.cursor()
    cur.execute("SELECT userId FROM users WHERE email = '{}'".format(email))
    userId = cur.fetchone()[0]
    cur.execute("SELECT products.productId, products.name, products.price, products.image FROM products, kart WHERE products.productId = kart.productId AND kart.userId = '{}'".format(userId))
    products = cur.fetchall()
    totalPrice = 0
    for row in products:
        totalPrice += row[2]
    return render_template("cart.html", products = products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    productId = int(request.args.get('productId'))
    cur = conn.cursor()
    cur.execute("SELECT userId FROM users WHERE email = '{}'".format(email))
    userId = cur.fetchone()[0]
    try:
        cur.execute("DELETE FROM kart WHERE userId = '{}' AND productId = '{}'".format(userId, productId))
        conn.commit()
        msg = "removed successfully"
    except:
        conn.rollback()
        msg = "error occured"
     
    return redirect(url_for('root'))

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))

def is_valid(email, password):
    con = cx_Oracle.connect("system/system@localhost:1521/XE")
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        #Parse form data    
        password = request.form['password']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']

        cur = conn.cursor()

        #lets create a random userid
        import random
        userida = random.randint(0,10**10)
        msg=""
        try:
            str = "INSERT INTO users (userid, password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}', '{11}')".format(userida, hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, address1, address2, zipcode, city, state, country, phone)
            cur.execute(str) 
            conn.commit()
            msg = "Registered Successfully"
        except:
            msg = "Failed to register user"
        return render_template("login.html", error=msg)

@app.route("/registerationForm")
def registrationForm():
    return render_template("register.html")

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

if __name__ == '__main__':
    app.run(debug=True)

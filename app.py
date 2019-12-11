from flask import Flask, request, redirect, url_for, session, render_template
import sqlite3
app = Flask(__name__)

# Configuration for app starts here
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "lis161aquino"
# Configuration ends here

#DB helper functions

def connect_db():
    conn = sqlite3.connect('tenants.db')
    return conn

def read_all_users():
    # Read all contents of user table
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tenants')
    results = cur.fetchall()
    cur.close()
    #end of db transaction

    return results

@app.route('/')
def index():
    return "<h1>Welcome to the Tenant Organizer!</h1><br>"

@app.route('/home', defaults={"name":"Person"})
@app.route('/home/<name>')
def home(name):
    session["username"] = name #in this part, i am setting the value of the session["username"]
    person = {"name":"Jason","email":"arvinjasonaquino@gmail.com"}

    ### This is where I extract from DB

    return render_template("home.html", home_name = name, user_flag = 2, person=person)

#this page is the form
@app.route('/form', methods=["GET","POST"])
def form():
    if request.method == "GET":
        return render_template("form.html")
    else:
        # in this part i am extracting the values from the form
        var_name = request.form["Name"]
        var_amount = request.form["Amount"]
        var_status = request.form["Status"]


        ####
        ####This is where i save the variable to database
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO tenants (name,amount,status) VALUES (?,?,?)', (var_name,var_amount,var_status))
        conn.commit()
        cur.close()
        ####


        if var_name == '':
            return redirect(url_for('unsuccessful'))
        else:
            return redirect(url_for('showall'))

@app.route('/unsuccessful')
def unsuccessful():
    return "<h1>Username not found</h1><br><a class='btn btn-primary' href='/form' role='button'>Back to Form</a>"



@app.route('/about')
def about():
    if session.get("username") is None:
        return redirect(url_for("form"))
    else:
        name = session["username"]
        return render_template("about.html", about_name = name)

@app.route('/logout')
def logout():
    session.pop("username")
    return "<h1>Successfully logged out!</h1><br><a class='btn btn-primary' href='/home' role='button'>Back to Home</a>"


@app.route('/showall')
def showall():
    # Read all contents of user table
    results = read_all_users()
    #end of db transaction

    return render_template('showall.html', results=results)

@app.route('/edit',methods=['post','get'])
def edit():
    if request.method == 'GET':
        edit_id = request.args.get('edit')
        # Retrieve that record
        conn = connect_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM tenants WHERE id = ?',(edit_id))
        result = cur.fetchone()
        cur.close()
        #done

        return render_template('edit.html',result=result)
    elif request.method == 'POST':
        new_name = request.form['Name']
        new_amount = request.form['Amount']
        new_status = request.form['Status']
        edit_id = request.form['id']

        if request.form['edit'] == "update":
            #Update the record
            conn = connect_db()
            cur = conn.cursor()
            cur.execute('UPDATE tenants SET Name= ?, Amount = ?, Status = ? WHERE id = ?',(new_name,new_amount,new_status,edit_id))
            conn.commit()
            cur.close()
            #end of DB transaction
        elif request.form['edit'] == "delete":
            #Delete the record
            conn = connect_db()
            cur = conn.cursor()
            cur.execute('DELETE FROM tenants WHERE id = ?',(edit_id))
            conn.commit()
            cur.close()
            #end of DB transaction


        results = read_all_users()
        return render_template('showall.html',results=results)


if __name__ == "__main__":
    app.run()
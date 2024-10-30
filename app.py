from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector


app = Flask(__name__)
app.secret_key = 'cherry'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="intervieww",
    port=3308  
)

@app.route('/')
def home():

    return render_template('home.html')


##adding modifying or deleting item
@app.route('/invoicedetails', methods=['GET','POST'])
def invoicedetailsadd():
    if request.method=='POST':
        action = request.form['action']
        if action == 'save':
            productname = request.form['productname']
            unitno = request.form['unitno']
            price = request.form['price']
            quantity = request.form['quantity']
            total = request.form['total']
            expirydate = request.form['expirydate']
            cursor = db.cursor(dictionary=True)
            cursor.execute("INSERT INTO InvoiceDetails(productname,unitno,price,quantity,total,expirydate) VALUES (%s,%s,%s,%s,%s,%s)",(productname,unitno,price,quantity,total,expirydate))
            db.commit()
            flash('Date entered successfully', 'success')
            return redirect(url_for('invoicedetailsadd'))
        else:
            
            productname = request.form['productname']
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM InvoiceDetails WHERE productname = %s", (productname,))
            item = cursor.fetchone()
            
            if not item:
                flash(f'Product {productname} not found!', 'danger')
                return redirect(url_for('invoicedetails'))

            if action == 'modify':
                # Now handle the form inputs, keeping the old values if no input was provided
                unitno = request.form['unitno'] if request.form['unitno'] else item['unitno']
                price = request.form['price'] if request.form['price'] else item['price']
                quantity = request.form['quantity'] if request.form['quantity'] else item['quantity']
                total = request.form['total'] if request.form['total'] else item['total']
                expirydate = request.form['expirydate'] if request.form['expirydate'] else item['expirydate']

                # Update the item in the database with the new values or keep the existing ones
                cursor.execute("""UPDATE InvoiceDetails SET unitno = %s, price = %s, quantity = %s, total = %s, expirydate = %s WHERE productname = %s""", (unitno, price, quantity, total, expirydate, productname))

                db.commit()
                flash(f'Product {productname} updated successfully', 'success')
                return redirect(url_for('invoicedetailsadd'))
            elif action == 'delete':
                cursor.execute("DELETE FROM InvoiceDetails WHERE productname = %s",(productname,))
                db.commit()
                flash(f'Product {productname} deleted successfully', 'success')
                return redirect(url_for('invoicedetailsadd'))

                
        
        
            


        
        


    return render_template('invoicedetails.html')


##modifyign item
# @app.route('/invoicedetails',methods=['GET','POST'])
# def invoicedetailsmod():
#     if request.method=='POST':
#         action = request.form['action']
#         if action == 'modify':
#             productname = request.form['productname']
#             cursor = db.cursor(dictionary=True)
#             cursor.execute("SELECT * FROM InvoiceDetails WHERE productname = %s", (productname,))
#             item = cursor.fetchone()
            
#             if not item:
#                 flash(f'Product {productname} not found!', 'danger')
#                 return redirect(url_for('invoicedetails'))
            
#             # Now handle the form inputs, keeping the old values if no input was provided
#             unitno = request.form['unitno'] if request.form['unitno'] else item['unitno']
#             price = request.form['price'] if request.form['price'] else item['price']
#             quantity = request.form['quantity'] if request.form['quantity'] else item['quantity']
#             total = request.form['total'] if request.form['total'] else item['total']
#             expirydate = request.form['expirydate'] if request.form['expirydate'] else item['expirydate']

#             # Update the item in the database with the new values or keep the existing ones
#             cursor.execute("""UPDATE InvoiceDetails SET unitno = %s, price = %s, quantity = %s, total = %s, expirydate = %s WHERE productname = %s""", (unitno, price, quantity, total, expirydate, productname))

#             db.commit()
#             flash(f'Product {productname} updated successfully', 'success')
#             return redirect(url_for('invoicedetailsmod'))
       
        



#     return render_template('invoicedetails.html')


@app.route('/invoicelist', methods=['GET', 'POST'])
def invoicelist():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT lineno, productname, unitno, price, quantity, total, expirydate FROM InvoiceDetails")
    rows = cursor.fetchall()
    cursor.close()
    
    return render_template('invoicelist.html', rows=rows)










if __name__ == '__main__':
    app.run(debug=True , port=5006)
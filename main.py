import smtplib,random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, redirect,url_for,render_template,session,request,flash
from waitress import serve
from mongo_init import*
from settings import app

@app.route('/', methods=['POST','GET'])
def landing():
    if 'user' in session:
        if request.method == 'POST':
            query_email = request.form['email']
            query_msg = request.form['message']
            flash(' Your inquiry is sent, check your email for response')
            return redirect(url_for('inquiry', email=query_email, message=query_msg))
        else:
            return render_template('landing.html', user_in_session = session['user'][0].upper())
    else:
        if request.method == 'POST':
            query_email = request.form['email']
            query_msg = request.form['message']
            flash(' Your inquiry is sent, check your email for response')
            return redirect(url_for('inquiry', email=query_email, message=query_msg))
        else:
            return render_template('landing.html', user_in_session = None)
   

@app.route('/login', methods=['POST','GET'])
def login():
    if 'user' in session:
        return redirect(url_for('landing'))
    else:
        if request.method == 'POST':
            user_email = request.form['email']
            user_password = request.form['password']
            
            email_exist = machica_users.find_one({'email':user_email})
            password_exist = machica_users.find_one({'password':user_password})

            if email_exist and password_exist:
                session.permanent = True
                session['user'] = email_exist['first_name']
                return redirect(url_for('landing'))
            else:
                flash(' Your account is not registered yet.')
                return redirect(url_for('login'))

        else:
            return render_template('login.html',user_in_session = None)

@app.route('/register/<error>', methods=['POST','GET'])
def register(error):
    if 'user' in session:
        return redirect(url_for('landing'))
    else:
        if request.method == 'POST':
            session['firstname'] = request.form['first-name']
            session['lastname'] = request.form['last-name']
            session['gender'] = request.form['gender']
            session['phone_number'] = request.form['phone-number']
            session['registered_email'] = request.form['email']
            session['password' ]= request.form['password']
            session['confirm_password'] = request.form['confirm-password']

            generated_otp = ''
            for i in range(4):
                generated_otp += str(random.randint(0,9))

            session['gen_otp'] = generated_otp
            
            email_exist = machica_users.find_one({'email':session['registered_email']})
            if email_exist:
                flash(' Email is already taken, please use another email.')
                return redirect(url_for('register', error=401))
            elif session['password'] != session['confirm_password']:
                flash(' Password repeatition is not validated.')
                return redirect(url_for('register', error=402))
            else:
                return redirect(url_for('otp'))
                
        else:
            return render_template('register.html', user_in_session = None)

@app.route('/otp', methods=['POST','GET'])
def otp():
    if 'user' in session:
        return redirect(url_for('landing'))
    else:
        if request.method == 'POST':
            user_otp = request.form['user-otp']
            
            if 'gen_otp' in session:
                if user_otp == session['gen_otp']:

                    new_user = add_users(session['firstname'],session['lastname'],session['gender']
                    ,session['phone_number'],session['registered_email'],session['password'])
                    machica_users.insert_one(new_user)

                    flash('Your account is officially registered!')
                    return render_template('otp.html', user_in_session = None, email=session['registered_email'])

                else:
                    flash(' You entered a wrong OTP, try again')
                    return redirect(url_for('register', error=403))
            else:
                flash(' Something is wrong in geenrating otp, try again')
                return redirect(url_for('register', error=403))
        else:
            try:
                mail_content = f"YOU'RE OTP PIN IS: {session['gen_otp']}"
                #The mail addresses and password
                sender_address = 'otpsender47@gmail.com'
                sender_pass = 'xisnpznnkhkhcbls'
                receiver_address = session['registered_email']

                #Setup the MIME
                message = MIMEMultipart()
                message['From'] = sender_address
                message['To'] = receiver_address
                message['Subject'] = 'ONE TIME PIN REGISTRATION.'   #The subject line

                #The body and the attachments for the mail
                message.attach(MIMEText(mail_content, 'plain'))

                #Create SMTP session for sending the mail
                session_smtp = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
                session_smtp.starttls() #enable security
                session_smtp.login(sender_address, sender_pass) #login with mail_id and password
                text = message.as_string()
                session_smtp.sendmail(sender_address, receiver_address, text)
                session_smtp.quit()
                print('Mail Sent')

                return render_template('otp.html', user_in_session = None, email=session['registered_email'])
            
            except:
                return redirect(url_for('register', error=False))

@app.route('/appointment', methods=['POST','GET'])
def appointment():  
    if 'user' in session:
        if request.method == 'POST':
            firstname = request.form['first-name']
            lastname = request.form['last-name']
            phone_number = request.form['phone-number']
            session['confirmation_email'] = request.form['email']
            date = request.form['date']
            time = request.form['time']
            poa = request.form['POA']
            msg = request.form['message']

            if(not firstname and not lastname and not phone_number and not date and not time):
                flash(' You should check in on some of those fields above.')
                return render_template('appointment.html',  user_in_session = session['user'][0].upper())
            else:
                new_booking = add_booking(firstname,lastname,phone_number,session['confirmation_email'],date,time,poa,msg if msg else None)
                machica_bookings.insert_one(new_booking)
                return redirect(url_for('confirm', sender='booking_route'))
        else:
            return render_template('appointment.html',  user_in_session = session['user'][0].upper())
    else:
        return redirect(url_for('login'))

@app.route('/order', methods=['POST','GET'])
def order():
    if 'user' in session:
        if request.method == 'POST':
            firstname = request.form['first-name']
            lastname = request.form['last-name']
            phone_number = request.form['phone-number']
            session['confirmation_email'] = request.form['email']
            product = request.form['pr-name']
            quantity = request.form['quantity']
            msg = request.form['message']

            if(not firstname and not lastname and not phone_number and not product and not quantity):
                flash(' You should check in on some of those fields above.')
                return render_template('order.html',  user_in_session = session['user'][0].upper())
            else:
                new_order = add_orders(firstname,lastname,phone_number,session['confirmation_email'],product,quantity,msg if msg else None)
                machica_orders.insert_one(new_order)
                return redirect(url_for('confirm', sender='order_route'))
        else:
            return render_template('order.html',  user_in_session = session['user'][0].upper())
    else:
        return redirect(url_for('login'))


@app.route('/inquiry/<email>/<message>')
def inquiry(email,message):

    mail_content = f'User {email} ask,{message}' 
    #The mail addresses and password
    sender_address = 'inquirymachica20@gmail.com'
    sender_pass = 'meqfxsvprfyejvwn'
    receiver_address = 'Jvragudo6@gmail.com'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'User Inquiry'   #The subject line
    
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
   
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('the mail was sent')

    return redirect(url_for('landing'))


@app.route('/email_confirmation/<sender>')
def confirm(sender):
    mail_content = f"""
           <html>
                    <head>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css" integrity="sha384-xOolHFLEh07PJGoPkLv1IbcEPTNtaed2xpHsD9ESMhqIYd0nLMwNLD69Npy4HI+N" crossorigin="anonymous">
                    <link rel="stylesheet" href="{url_for('static', filename='confirm.css')}">
                    <title></title>
                    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
                    <body style="margin: 0 !important; padding: 0 !important; background-color: #eeeeee;" bgcolor="#eeeeee">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%">
                    <tr>
                    <td align="center" style="background-color: #eeeeee;" bgcolor="#eeeeee">
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;">
                    <tr>
                    <td align="center" valign="top" style="font-size:0; padding: 35px;" bgcolor="#003A33">
                    <div style="display:inline-block; max-width:50%; min-width:100px; vertical-align:top; width:100%;">
                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:300px;">
                    <tr>
                    <td align="left" valign="top" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 36px; font-weight: 800; line-height: 48px;" class="mobile-center">
                    <h1 style="font-size: 1.2rem; font-weight: 800; margin: 0; color: #ffffff;">Mahica Dental clinic</h1>
                    </td>
                    </tr>
                    </table>
                    </div>
                    <div style="display:inline-block; max-width:50%; min-width:100px; vertical-align:top; width:100%;" class="mobile-hide">
                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:300px;">
                    <tr>
                    <td align="right" valign="middle" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; line-height: 48px;">
                    <table cellspacing="0" cellpadding="0" border="0" align="right">
                    <tr>
                    <td style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 24px;"> <a href="#" target="_blank" style="color: #ffffff; text-decoration: none;"><img src="https://i.pinimg.com/564x/e7/b6/52/e7b652b5be3ef0ddcb90e1226049aa67.jpg" width="30" height="30" style="display: block; border: 0px;" /></a> </td>
                    </tr>
                    </table>
                    </td>
                    </tr>
                    </table>
                    </div>
                    </td>
                    </tr>
                    <tr>
                    <td align="center" style="padding: 35px 35px 20px 35px; background-color: #ffffff;" bgcolor="#ffffff">
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;">
                    <tr>
                    <td align="center" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding-top: 25px;"> <img src="https://img.icons8.com/carbon-copy/100/000000/checked-checkbox.png" width="125" height="120" style="display: block; border: 0px;" /><br>
                    <h2 style="font-size: 30px; font-weight: 800; line-height: 36px; color: #009886; margin: 0;">Your {'order' if sender == 'order_route' else 'booking'} is confirmed! </h2>
                    </td>
                    </tr>
                    <tr>
                    </tr>
                    <tr>
                    <td align="left" style="padding-top: 20px;">
                    <table cellspacing="0" cellpadding="0" border="0" width="100%">
                    <tr>
                    <td width="75%" align="left" bgcolor="#eeeeee" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 800; line-height: 24px; padding: 10px;"> Order Reference # </td>
                    <td width="25%" align="left" bgcolor="#eeeeee" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 800; line-height: 24px; padding: 10px;"> 2345678 </td>
                    </tr>
                    <tr>
                    <td width="75%" align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding: 15px 10px 5px 10px;"> Item price </td>
                    <td width="25%" align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding: 15px 10px 5px 10px;"> sample price </td>
                    </tr>
                    <tr>
                    <td width="75%" align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding: 5px 10px;"> Payment method </td>
                    <td width="25%" align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding: 5px 10px;"> Over the counter </td>
                    </tr>
                    </table>
                    </td>
                    </tr>
                    <tr>
                    <td align="left" style="padding-top: 20px;">
                    <table cellspacing="0" cellpadding="0" border="0" width="100%">
                    <tr>
                    <td width="75%" align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 800; line-height: 24px; padding: 10px; border-top: 3px solid #eeeeee; border-bottom: 3px solid #eeeeee;"> TOTAL </td>
                    <td width="25%" align="left" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 800; line-height: 24px; padding: 10px; border-top: 3px solid #eeeeee; border-bottom: 3px solid #eeeeee;"> sample total </td>
                    </tr>
                    </table>
                    </td>
                    </tr>
                    </table>
                    </td>
                    </tr>
                    <tr>
                    <td align="center" height="100%" valign="top" width="100%" style="padding: 0 35px 35px 35px; background-color: #ffffff;" bgcolor="#ffffff">
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:660px;">
                    </table>
                    </td>
                    </tr>
                    <tr>
                    </tr>
                    <tr>
                    <td align="center" style="padding: 35px; background-color: #ffffff;" bgcolor="#ffffff">
                    <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width:600px;">
                    <tr>
                    <td align="center"> <img src="https://i.pinimg.com/564x/75/8d/cc/758dccad44bd73e2a5f7106024b27fef.jpg" width="37" height="37" style="display: block; border: 0px;" /> </td>
                    </tr>
                    <tr>
                    <td align="center" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 24px; padding: 5px 0 10px 0;">
                    <p style="font-size: 14px; font-weight: 800; line-height: 18px; color: #333333;">Unit #1, G/F Aspiras Building,<br> Consolacion Street </p>
                    </td>
                    </tr>
                    <tr>
                    <td align="center" style="font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 24px;">
                    <p style="font-size: 14px; font-weight: 400; line-height: 20px; color: #777777;"> If you didn't create an account using this email address, please ignore this email or <a href="#" target="_blank" style="color: #777777;">unsusbscribe</a>. </p>
                    </td>
                    </tr>
                    </table>
                    </td>
                    </tr>
                    </table>
                    </td>
                    </tr>
                    </table>
                    </body>
                    </html> 
            """
    #The mail addresses and password
    sender_address = 'inquirymachica20@gmail.com'
    sender_pass = 'meqfxsvprfyejvwn'
    receiver_address = session['confirmation_email']
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = f"Machica {'Order' if sender == 'order_route' else 'Booking'}"   #The subject line
    
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html'))
   
    #Create SMTP session for sending the mail
    session_confirm = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session_confirm.starttls() #enable security
    session_confirm.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session_confirm.sendmail(sender_address, receiver_address, text)
    session_confirm.quit()

    if sender == 'order_route':
        flash('Your order has been confirmed. Check your email for details.')
        return redirect(url_for('order'))
    elif sender == 'booking_route':
        flash('Your booking has been confirmed. Check your email for details.')
        return redirect(url_for('appointment'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('confirmation_email',None)
    session.pop('firstname', None)
    session.pop('lastname', None)
    session.pop('gender', None)
    session.pop('phone_number', None)
    session.pop('registered_email', None)
    session.pop('password', None)
    session.pop('confirm_password', None)
    return redirect(url_for('landing'))


@app.route('/sample')
def sample():
    return render_template('sample.html')

if __name__ == '__main__':
    app.run(debug=True)
    # serve(app, host='0.0.0.0', port=5500, threads=1, url_prefix='/machica') 
   
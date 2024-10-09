# WhatBytes_Django_Assignment

This assignment consist of multiple pages,

FIRSTLY - LOGIN PAGE
-->In the login page, we have two different fields, one is the username and the other is the password.
--> From the post request made throught the html form used in signin.html in the templates section, we are accessing the entered data for the username and the password.
--> We are then checking if there is a user with such a username and the password in the database, using the default authenticate property that is available to us from the django auth libraries.

SECONDLY - SIGNUP PAGE
--> On the signup page, we are having couple of fields to fill in, which are general fields and are used almost on any of the websites. Such as username, firstname,lastname,email,password,confirm password etc.
--> From the html template signup.html, we are then sending a post request with all of the details filled in the form.
--> From this post request, in views.signup function, we are extracting all of this information of the fields, and we then check if we can filter out the User class objects based on the username or the email, if yes then we display a message saying that the user already exists, and the user can go and rightaway login
--> But if no such user is present, then we create a user with the username and the password entered by the user, and then save the user into the database.

THIRDLY - HOME/DASHBOARD
--> This webpage is only accessible when a known user(ie a user who has been saved into the database and is loggedin) tries to access, else the website will simply redirect to the signin page.
--> The home/dashboard simply greets the user with the respective username, and tells that the user has been logged in.

FOURTH - PROFILE
--> This webpage is also only accessible to the users whose data is saved into the database and is currently an active user, else it will redirect to the signin page.
--> The profile simply shows the details of the current user such as the username, email, date at which the profile was created, when was it last updated and so on.

FIFTH->FORGET PASSWORD
--> Here, we first take the username and check if the username is present in the database, if no, then we redirect it back, else we send a reset link to the mentioned email of the user.
--> For the reset password, we have created a profile model, in which it takes user and a forget_password_token, this user simply takes the default User library of django auth as the primary key.
--> Once the username is verified, we then generate a unique token using the uuid library in python, and pass the user and the token to create the profile model for that particular user.
--> Now, when we send the link to reset the password in the mail, we do this by simple send_mail function again given by django, it takes the subject, message, sender's email and the reciever's email as arguments and then sends the mail.
-->We also give the token number that has been generated, now when webpage is navigated, through the params we check whether the token number is the same as the forget_password_token as stored in the profile model for the user, if it is , then we give the option to enter the new password, and similarly update the password by extracting the user using the token. 
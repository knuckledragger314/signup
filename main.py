
#
import webapp2
import re

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Sign-up</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Sign--up</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

post_sign_form = """
<form method="post">
    <table>
    <label>
        <tr>
            <td>Username</td>
            <td><input type="text" name="username" value ='{4}'required/></td>
            <td class="error">{0}</td>
        </tr>
    </label>
    <label>
        <tr>
            <td>Password</td>
            <td><input type="password" name="password" required/></td>
            <td class="error">{1}</td>
        </tr>
    </label>
    <label>
        <tr>
            <td>Verify Password</td>
            <td><input type="password" name="verify-password" required/></td>
            <td class="error">{2}</td>
        </tr>
    </label>
    <label>
        <tr>
            <td>Email (optional)</td>
            <td><input type="text" value ='{5}' name="email"/></td>
            <td class="error">{3}</td>
        </tr>
    </label>
    </table>
    <input type="submit" value="Sign Up Now!"/>
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):

    #if user name passes the test, return the user name
    #no need for else, if it doesn't pass the test, it should return
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class MainHandler(webapp2.RequestHandler):
    def get(self):

        edit_header = "<h3>Sign up</h3>"

        username = self.request.get("username")
        password = self.request.get("password")
        verify_password = self.request.get("verify-password")
        email = self.request.get("email")

        # a form for signing up
        #fix these other three
        username_error = self.request.get("username_error")
        password_error = self.request.get("password_error")
        verify_error = self.request.get("verify_error")
        email_error = self.request.get("email_error")

        main_content = edit_header + post_sign_form.format(username_error, password_error, verify_error, email_error, username, email)
        user_response = page_header + main_content + page_footer
        self.response.write(user_response)

    def post(self):
        edit_header = "<h3>Sign up</h3>"

        username = self.request.get("username")
        password = self.request.get("password")
        verify_password = self.request.get("verify-password")
        email = self.request.get("email")

        username_error = self.request.get("username_error")
        password_error = self.request.get("password_error")
        verify_error = self.request.get("verify_error")
        email_error = self.request.get("email_error")

        has_error = False

        if not valid_username(username):
            username_error = "You didn't fill out a proper username."
            has_error = True

        if not valid_password(password):
            password_error = "The password isn't valid."
            has_error = True

        if verify_password != password:
            verify_error = "The passwords don't match."
            has_error = True
        #else:
        #    has_error = False

        if not valid_email(email):
            email_error = "That is not a valid email."
            has_error = True

#do work here
        if has_error == True:
            #needs to send information here, not just redirect
            #may need to include form or error.format along with the redirect
            #if errors self.response.write(errors)

            main_content = edit_header + post_sign_form.format(username_error, password_error, verify_error, email_error, username, email)
            user_response = page_header + main_content + page_footer
            self.response.write(user_response)
        else:
            self.redirect ("/welcome?username=" + username + "!")
            #Something in the page is skipping the validation or validation isn't working
            #and going straight to welcome

class Welcome(webapp2.RequestHandler):
    def get(self):
#welcome?username=userface
        username = self.request.get("username")
            #password = self.request.get("password")
            #verify_password = self.request.get("verify-password")
            #email = self.request.get("email")

        sentence = "<h3>Welcome to the jungle, {0}! We like fun and games!</h3>".format(username)
        welcome_page = page_header + sentence + page_footer
        self.response.write(welcome_page)

        #else:
        #    self.redirect("/")

    #def post(self):



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)

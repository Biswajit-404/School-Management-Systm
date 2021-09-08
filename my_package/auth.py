from functools import wraps

from flask import session, g, redirect, url_for, flash
from my_package.models import Users


def checkAdmin(func):
    @wraps(func)
    def authChecker(*args, **kwargs):
        try:
            print('middleware triggered')
            if "id" in session and "userType" in session and "userName" in session:
                print('Session exists')

                cuser = Users.query.get(session["id"])
                print(cuser)
                print(cuser.name, cuser.email)

                if cuser:
                    print('found user')
                    if cuser.usertype == 'admin':
                        g.cuser = {"id": cuser.id, "email": cuser.email, "usertype": cuser.usertype}
                        return func(*args, **kwargs)
                    else:
                        session.clear()
                        return redirect(url_for('login'))
                else:
                    flash('- you are not authenticated', 'failed')
                    return redirect(url_for('login'))
            else:
                session.clear()
                return redirect(url_for('login'))

        except Exception as e:
            print(e)
            session.clear()
            return redirect(url_for('login'))

    return authChecker



# TEACHER AUTH
def checkTeacher(func):
    @wraps(func)
    def authChecker(*args, **kwargs):
        try:
            if "id" in session and "userType" in session and "userName" in session:
                cuser = Users.query.get(session["id"])
                if cuser:
                    if cuser.usertype == 'teacher':
                        g.cuser = cuser
                        return func(*args, **kwargs)
                    else:
                        session.clear()
                        return redirect(url_for('login'))
                else:
                    flash('- you are not authenticated', 'failed')
                    return redirect(url_for('login'))
            else:
                session.clear()
                return redirect(url_for('login'))

        except Exception as e:
            print(e)
            session.clear()
            return redirect(url_for('login'))

    return authChecker


# USER AUTH

def checkUser(func):
    @wraps(func)
    def authChecker(*args, **kwargs):
        try:
            if "id" in session and "userType" in session and "userName" in session:
                cuser = Users.query.get(session["id"])
                if cuser:
                    if cuser.usertype == 'user':
                        g.cuser = cuser
                        return func(*args, **kwargs)
                    else:
                        session.clear()
                        return redirect(url_for('login'))

                else:
                    flash('- you are not authenticated', 'failed')
                    return redirect(url_for('login'))
            else:
                session.clear()
                return redirect(url_for('login'))

        except Exception as e:
            print(e)
            session.clear()
            return redirect(url_for('login'))

    return authChecker

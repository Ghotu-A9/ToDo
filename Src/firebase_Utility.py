import requests
import sqlite3
from sqlite3 import Error


class FirebaseUtility:

    def __init__(self):
        self.webKey = "AIzaSyB3qd07SM_ytd6IFqppMaIATtPavH8ZClI"
        self.emailSignupAddress = 'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=' + self.webKey
        self.emailVerificationSender = 'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=' + self.webKey
        self.emailSigninAddress = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=' + self.webKey
        self.userInfoAddress = 'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=' + self.webKey

class FirebaseAuth:
    def __init__(self):
        self.login = False
        self.base = FirebaseUtility()
        self.cookieFile = '../assets/data/co.db'

        self.Codes = {
            0: 'Unknown Error Occurred',
            1: 'Unknown Exception Occurred',
            11: 'The email address is already in use by another account',
            12: 'Password sign-in is disabled for this project',
            13: 'We have blocked all requests from this device due to unusual activity. Try again later',
            14: "The user's credential is no longer valid. The user must sign in again.",
            15: "There is no user record corresponding to this identifier. The user may have been deleted.",
            16: "The password is invalid or the user does not have a password.",
            17: " The user account has been disabled by an administrator.",
            18: "Email not verified",
            200: "Done"
        }

    def signupWithEmail(self, em, psw):

        payload = {
            'email': em,
            'password': psw,
            'returnSecureToken': True
        }

        try:
            res = requests.post(self.base.emailSignupAddress, data=payload)
            decRes = res.json()
            error = decRes.get('error')
            if error:
                # EMAIL_EXISTS
                if error.get('message') == 'EMAIL_EXISTS':
                    return {'signup': False, 'Reason': self.Codes[11]}
                elif error.get('message') == 'OPERATION_NOT_ALLOWED':
                    return {'signup': False, 'Reason': self.Codes[12]}
                elif error.get('message') == 'TOO_MANY_ATTEMPTS_TRY_LATER':
                    return {'signup': False, 'Reason': self.Codes[13]}
                else:
                    return {'signup': False, 'Reason': self.Codes[0]}
            else:
                idTok = decRes.get('idToken')
                reTok = decRes.get('refreshToken')
                uid = decRes.get('localId')
                return self.sendVerificationEmail(idTok, reTok, uid)

        except Exception:
            return {'signup': False, 'Reason': self.Codes[1]}

    def sendVerificationEmail(self, tok, ret, uid):

        payload = {
            'requestType': "VERIFY_EMAIL",
            'idToken': tok
        }

        try:
            res = requests.post(self.base.emailVerificationSender, data=payload)
            decRes = res.json()
            error = decRes.get('error')
            if error:
                if error.get('message') == 'INVALID_ID_TOKEN':
                    return {'signup': True, 'send': False, 'Reason': self.Codes[14]}
                elif error.get('message') == 'USER_NOT_FOUND':
                    return {'signup': True, 'send': False, 'Reason': self.Codes[15]}
                else:
                    return {'signup': True, 'send': False, 'Reason': self.Codes[0]}
            else:
                return {'signup': True, 'send': True, 'Reason': self.Codes[200]}

        except Exception:
            return {'signup': True, 'send': False, 'Reason': self.Codes[1]}

    def signinWithEmail(self, em, pwd):

        payload = {
            'email': em,
            'password': pwd,
            'returnSecureToken': True
        }

        try:
            res = requests.post(self.base.emailSigninAddress, data=payload)
            decRes = res.json()
            error = decRes.get('error')

            if error:
                if error.get('message') == 'EMAIL_NOT_FOUND':
                    return {'signin': False, 'Reason': self.Codes[15]}
                elif error.get('message') == 'INVALID_PASSWORD':
                    return {'signin': False, 'Reason': self.Codes[16]}
                elif error.get('message') == 'USER_DISABLED':
                    return {'signin': False, 'Reason': self.Codes[17]}
                else:
                    return {'signin': False, 'Reason': self.Codes[0]}
            else:
                idTok = decRes.get('idToken')
                reTok = decRes.get('refreshToken')
                uid = decRes.get('localId')
                reg = decRes.get('registered')

                if self.checkEmailVerified(idTok).get('check'):
                    return {'signin': True, 'Reason': self.Codes[200], "idTok": idTok, "reTok": reTok, "uid": uid}
                else:
                    return {'signin': False, 'Reason': self.Codes[18]}


        except Exception:
            return {'signin': False, 'Reason': self.Codes[1]}

    def checkEmailVerified(self, tok):
        payload = {
            'idToken': tok
        }
        try:
            res = requests.post(self.base.userInfoAddress, data=payload)
            decRes = res.json()
            error = decRes.get('error')
            if error:
                if error.get('message') == 'INVALID_ID_TOKEN':
                    return {'check': False, 'Reason': self.Codes[14]}
                elif error.get('message') == 'USER_NOT_FOUND':
                    return {'check': False, 'Reason': self.Codes[15]}
                else:
                    return {'check': False, 'Reason': self.Codes[0]}
            else:
                if decRes.get('users')[0].get('emailVerified'):
                    return {'check': True, 'Reason': self.Codes[200]}
                else:
                    return {'check': False, 'Reason': self.Codes[18]}
        except Exception:
            return {'check': False, 'Reason': self.Codes[1]}

    def saveCookie(self):
        conn = None
        try:
            conn = sqlite3.connect(self.cookieFile)
            print(sqlite3.version)
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()





# print(FirebaseAuth().signinWithEmail("ghotu101@gmail.com", "lorelsulphate"))

print(FirebaseAuth().signinWithEmail("ghotu101@gmail.com", "lorelsulphate"))

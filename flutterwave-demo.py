from flask import Flask, abort, flash, redirect, render_template, request, url_for
from flutterwave import Flutterwave
import json
flw = Flutterwave("tk_WKidq81NCpnoyeu5vZHU", "tk_pPXQd5L0Th", {"debug": True})
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def pay():
    err = None

    if request.method == 'POST':
        email = request.form['email']
        cardno = request.form['cardno']
        cvv = request.form['cvv']
        expmonth = request.form['expyear']
        expyear = request.form['expyear']
        data = {
            "amount": "100",
            "authModel": "NOAUTH",
            "cardNumber": cardno,
            "cvv": cvv,
            "expiryMonth": expmonth,
            "expiryYear": expyear[2:],
            "currency": "NGN",
            "country": "NG",
            "customerID": email,
            "narration": "donation"
        }

        r = flw.card.charge(data)
        json_data = json.loads(r.text)
        print "{}".format(r.text)
        if json_data["status"] == "error":
            err = json_data["data"]
            render_template('pay.html', error=err)
        else:
            return redirect(url_for('pay'))

    return render_template('pay.html', error=err)


if __name__ == '__main__':
    app.run()

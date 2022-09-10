from flask import Flask, redirect, request
from rave_python import Rave, RaveExceptions, Misc

rave = Rave('FLWPUBK_TEST-45235b0a1576cb129423399a9a94f229-X', 'FLWSECK_TEST-d74b3de8a108c185ad309a123cae280b-X',production=False, usingEnv = False)

app = Flask(__name__)

@app.route('/test', methods =['GET', 'POST'])
def momo():
    if request.method == 'POST':

        payload = {
        "amount": "5000",
        "email": "david@gmail.com",
        "network": "MTN",
        #"currency" "ZMW"
        "phonenumber": "08030930236",
        "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
        "IP": "192.05.01.1",
        "order_id":"234",
        "txRef": "MC-15852113s09v5050e8"
        
        }
        res = rave.ZBMobile.charge(payload)
        print(res)
        try:
            res = rave.ZBMobile.charge(payload)
            #res = rave.ZBMobile.verify(res["txRef"])
            print(res)

        except RaveExceptions.TransactionChargeError as e:
            print(e.err)
            print(e.err["flwRef"])

        except RaveExceptions.TransactionVerificationError as e:
            print(e.err["errMsg"])
            print(e.err["txRef"])

        return redirect(res["link"])

@app.route('/card', methods = ["POST", "GET"])
def card_payment():
    # Payload with pin
    # payload = {
    # "cardno": "5438898014560229",
    # "cvv": "890",
    # "expirymonth": "09",
    # "expiryyear": "23",
    # "amount": "10",
    # "email": "user@gmail.com",
    # "phonenumber": "0902620185",
    # "firstname": "temi",
    # "lastname": "desola",
    # "IP": "355426087298442",
    # }
    # global res
    if request.method == "POST":
        payload = {
            "cardno": request.args.get('cardno'),
            "cvv": request.args.get('cvv'),
            "expiryyear": request.args.get('expirymonth'),
            "amount": request.args.get('amount'),
            "expirymonth": request.args.get('expirymonth'),
            "email": request.args.get('email'),
            "phonenumber": request.args.get('phonenumber'),
            "firstname": request.args.get('firstname'),
            "lastname": request.args.get('lastname'),
            "IP": request.args.get('IP'),
            "currency": request.args.get('currency'),
            "country": request.args.get('country')
            # "lastname": request.args.get('lastname')

        }

        try:
            res = rave.Card.charge(payload)
            print(res)

            if res["suggestedAuth"]:
                arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

                if arg == "pin":
                    Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
                if arg == "address":
                    Misc.updatePayload(res["suggestedAuth"], payload, address= {"billingzip": "07205", "billingcity": "Hillside", "billingaddress": "470 Mundet PI", "billingstate": "NJ", "billingcountry": "US"})
                
                res = rave.Card.charge(payload)
            if res["validationRequired"]:
                rave.Card.validate(res["flwRef"], "12345")

            ress = rave.Card.verify(res["txRef"])
            print(ress["transactionComplete"])

        except RaveExceptions.CardChargeError as e:
            print(e.err["errMsg"])
            print(e.err["flwRef"])

        except RaveExceptions.TransactionValidationError as e:
            print(e.err)
            print(e.err["flwRef"])

        except RaveExceptions.TransactionVerificationError as e:
            print(e.err["errMsg"])
            print(e.err["txRef"])
        res = rave.Card.charge(payload)

        return redirect(res['authUrl'])

if __name__ == '__main__':
    app.run(debug=True)
    
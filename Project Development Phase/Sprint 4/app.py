from flask import Flask, render_template, redirect, url_for, request
import requests


app = Flask(__name__, template_folder='templates')


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        arr = []
        print(request.form)
        for i in request.form:
            val = request.form[i]
            if val == '':
                return redirect(url_for("index"))
            arr.append(float(val))

        # deepcode ignore HardcodedNonCryptoSecret: <please specify a reason of ignoring this>
        API_KEY = "CB8dTF8Y0_o4amdiEL2FfNBLZ-EdGUGdLqrDk7Z2gzDP"
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={
            "apikey": API_KEY,
            "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
        })
        mltoken = token_response.json()["access_token"]
        header = {'Content-Type': 'application/json',
                  'Authorization': 'Bearer ' + mltoken}
        payload_scoring = {
            "input_data": [{"field": ['GRE Score',
                                      'TOEFL Score',
                                      'University Rating',
                                      'SOP',
                                      'LOR ',
                                      'CGPA',
                                      ],
                            }]
        }
        temp = []
        temp.append(arr[:6])

        payload_scoring["input_data"][0]["values"] = temp

        response_scoring = requests.post(
            'https://us-south.ml.cloud.ibm.com/ml/v4/deployments/f68fb233-7af6-473e-8e77-0b1ca625695f/predictions?version=2022-11-18',
            json=payload_scoring,
            headers={'Authorization': 'Bearer ' + mltoken}
        ).json()

        result = response_scoring['predictions'][0]['values']

        if float(result[0][0][0]) > 0.5:
            return render_template("yes.html", content=result[0][0][0]*100)

        else:
            return render_template("no.html", content=abs(result[0][0][0]*100))
    else:
        return redirect(url_for("demo2"))


@app.route("/home")
def demo2():
    return render_template("index.html")


if __name__ == "__main__":

    app.run('0.0.0.0', port=5000, debug=True)

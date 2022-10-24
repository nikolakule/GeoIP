from flask import Flask, render_template, request, url_for, redirect
import requests


app = Flask(__name__)

def get_ip_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response_json = response.json()

        if isinstance(response_json, dict):
            if response_json.get('status') == 'error':
                print(f"We got error for {url}: {response_json['errmsg']}")

        return response.json()
    except requests.exceptions.HTTPError as http_error:
        if http_error.response.status_code == 404:
            print("Maybe url is wrong?")
        else:
            print(http_error)
    except Exception as e:
        print(f'Some error occurred: {e}')


@app.route("/")
@app.route("/", methods=["POST"])
def geoip():
    ip = request.form.get("inputip")
    if not ip:
        geoip_data = get_ip_api('http://ip-api.com/json/?fields=58065')
    else:
        geoip_data = get_ip_api(f'http://ip-api.com/json/{ip}?fields=58065')
    return render_template("geoip.html", geoip_data=geoip_data, ip=ip)

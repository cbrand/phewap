from phew import access_point, is_connected_to_wifi, dns, server
from phew.server import redirect
from phew.template import render_template
from os import stat

AP_NAME = "pi pico"
AP_DOMAIN = "pipico.net"
WIFI_FILE = "wifi.json"

# TODO check for a wifi.json file or something and load secrets from 
# that if it is there, then connect to wifi and add different routes.
# if no wifi.py then go with the captive portal routes you see below.

wifi_configured = False

try:
    stat(WIFI_FILE)
    # TODO load wifi stuff and make a connection...
    wifi_configured = True
except OSError:
    pass
    # TODO do access point stuff...

def ap_index(request):
    if request.headers.get("host") != AP_DOMAIN:
        return render_template("redirect.html", domain = AP_DOMAIN)

    return render_template("index.html")

def ap_configure(request):
    print("Request data...")
    print(request.form)
    return render_template("configured.html", ssid = request.form["ssid"])

def ap_catch_all(request):
    if request.headers.get("host") != AP_DOMAIN:
        return render_template("redirect.html", domain = AP_DOMAIN)

    return "Not found.", 404


server.add_route("/", handler = ap_index, methods = ["GET"])
server.add_route("/configure", handler = ap_configure, methods = ["POST"])
server.set_callback(ap_catch_all)

ap = access_point(AP_NAME)
ip = ap.ifconfig()[0]
dns.run_catchall(ip)
server.run()
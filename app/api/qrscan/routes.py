from flask import render_template
from . import qrscan_bp


@qrscan_bp.route("/scanning")
def scanning():
    return render_template("qrscan/scan.html")

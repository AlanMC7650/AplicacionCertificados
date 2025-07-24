from flask import render_template
from . import qrscan_bp
from flask_login import login_user, logout_user, login_required, current_user


@qrscan_bp.route("/scanning")
@login_required
def scanning():
    return render_template("qrscan/scan.html")

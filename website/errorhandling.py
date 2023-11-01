from flask import render_template, abort

def error_404(error):
    return render_template('404.html'), 404

def error_500(error):
    return render_template('50x.html'), 500

def error_502(error):
    return render_template('50x.html'), 502

def error_503(error):
    return render_template('50x.html'), 503
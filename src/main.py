import os
import datetime
from flask import Flask, render_template, url_for, request, redirect
from trackmap import get_html_tracklist, create_html_track

template_path = os.path.abspath("src/templates")
static_path = os.path.abspath("src/static")

app = Flask(
    __name__,
    template_folder=template_path,
    static_folder=static_path,
)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save("tracks/" + uploaded_file.filename)
            create_html_track(uploaded_file.filename)
        return redirect(url_for('index'))
    return render_template('index.html', tracks=get_html_tracklist())



if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
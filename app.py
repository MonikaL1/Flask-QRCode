from flask import Flask, render_template, request, send_from_directory
import pyqrcode
import os

app = Flask(__name__)

# Directory to store generated QR codes
QR_CODE_DIR = "static/qrcodes"
if not os.path.exists(QR_CODE_DIR):
    os.makedirs(QR_CODE_DIR)


@app.route('/', methods=['GET', 'POST'])
def index():
    img_url = None
    if request.method == 'POST':
        link_name = request.form['link_name']
        link = request.form['link']

        # Generate the QR Code
        qr_code = pyqrcode.create(link)

        # Save the QR Code as a PNG file
        file_path = os.path.join(QR_CODE_DIR, f"{link_name}.png")
        qr_code.png(file_path, scale=8)

        # Pass the link name and the file path to the template
        img_url = f"/static/qrcodes/{link_name}.png"

        # Return the template with the image URL for download
        return render_template('index.html', img_url=img_url, link_name=link_name)

    # Render the template with no image initially
    return render_template('index.html', img_url=None)


@app.route('/download/<filename>')
def download(filename):
    # Send the file from the 'static/qrcodes' directory
    return send_from_directory(QR_CODE_DIR, filename)


if __name__ == '__main__':
    app.run(debug=True)

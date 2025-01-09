from flask import Flask, render_template, request, url_for, send_from_directory
import os, subprocess
from PIL import Image

app = Flask(__name__)

app.config['UPLOAD'] = 'uploads'
app.config['OUTPUT'] = 'outputs'
os.makedirs(app.config['UPLOAD'],exist_ok=True)
os.makedirs(app.config['OUTPUT'], exist_ok=True)

@app.route('/')
def index():
	return render_template('index.html')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_img():
	file = request.files['image']
	file_path = os.path.join(app.config['UPLOAD'],file.filename)
	file_extension = os.path.splitext(file.filename)[1].lower()
	file.save(file_path)

	input_image = Image.open(file_path)
	input_resolution = input_image.size

	subprocess.run(['python3', 'Real-ESRGAN/inference_realesrgan.py', '-i', file_path, '-o', 'outputs', '-n', 'RealESRGAN_x4plus', '--tile', '400', '--fp32'])
	output_filename = os.path.splitext(file.filename)[0] + '_out'+file_extension

	output_image_path = os.path.join(app.config['OUTPUT'], output_filename)
	output_image = Image.open(output_image_path)
	output_resolution = output_image.size

	return render_template(
        'compare.html',
        input_image=file.filename,
        output_image=output_filename,
        input_resolution=input_resolution,
        output_resolution=output_resolution
    )

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD'], filename)

@app.route('/outputs/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT'], filename)



if __name__ == '__main__':
	app.run(debug=True)
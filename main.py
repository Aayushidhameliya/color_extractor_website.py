from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from colorthief import ColorThief
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max limit for file size


def get_most_common_colors(image_path, num_colors=5):
    try:
        # Open image using PIL
        image = Image.open(image_path)

        # Resize image for faster processing (optional)
        image.thumbnail((200, 200))

        # Use ColorThief to get the dominant colors
        color_thief = ColorThief(image)
        dominant_colors = color_thief.get_palette(color_count=num_colors)

        return dominant_colors

    except Exception as e:
        print(f"Error processing image: {e}")
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # If user does not select file, browser also submits an empty file without filename
        if file.filename == '':
            return redirect(request.url)

        if file:
            # Save the uploaded file to the uploads folder
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Get most common colors
            colors = get_most_common_colors(file_path)

            if colors:
                return render_template('result.html', filename=filename, colors=colors)
            else:
                return "Error processing image. Please try again."

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

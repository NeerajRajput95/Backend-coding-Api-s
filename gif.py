from flask import Flask, request, jsonify
from PIL import Image
import os  # Import the os module

app = Flask(__name__)

def generate_gif(image_files, output_path, duration=1500):
    # Open the images and resize them to match the dimensions of the first image
    images = [Image.open(image_file).resize(Image.open(image_files[0]).size) for image_file in image_files]

    # Save the frames as an animated GIF
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=duration, loop=0)

@app.route('/generate-gif', methods=['POST'])
def generate_gif_from_images():
    try:
        # Get input data from request JSON
        input_data = request.json
        
        # Check if input_data is None or empty
        if not input_data:
            return jsonify({'error': 'No data provided in the request.'}), 400

        # Check if the required fields are present in the input_data
        if 'image_folder' not in input_data or 'output_folder' not in input_data:
            return jsonify({'error': 'Required fields "image_folder" or "output_folder" are missing in the request.'}), 400

        image_folder = input_data.get('image_folder')
        output_folder = input_data.get('output_folder')
        duration = input_data.get('duration', 1500)  # Default duration is 1500 milliseconds

        # Generate the animated GIF
        image_files = [os.path.join(image_folder, filename) for filename in os.listdir(image_folder)]
        output_path = os.path.join(output_folder, 'animated.gif')
        generate_gif(image_files, output_path, duration)

        return jsonify({'message': 'Animated GIF generated successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

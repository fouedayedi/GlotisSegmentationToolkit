from flask import Flask, session, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = './static/uploads/input'
OUTPUT_FOLDER = './static/uploads/output'
VIDEO_UPLOAD_FOLDER = './static/uploads/videos'
frames_folder = './static/uploads/frames'

import secrets
from model import segment_image,calculate_surface,calculate_iou
from utils import extract_frames,plot

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['VIDEO_UPLOAD_FOLDER'] = VIDEO_UPLOAD_FOLDER
app.config['frames_folder'] = frames_folder
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def allowed_video(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'mp4'


@app.route('/', methods=['GET'])
def index():
    original_path = session.get('original', None)
    segmented_path = session.get('segmented', None)
    plot_img_path = session.get('plot_img', None)
    original_frame_path = session.get('original_frame', None)
    segmented_frame_path = session.get('segmented_frame', None)

    # Calculate surface and IOU only if segmented_path exists
    surface = calculate_surface(segmented_path) if segmented_path else None
    iou_score = calculate_iou("./static/uploads/output/true_seg_1468.png", "./static/uploads/output/seg_01468_rgb.png") if segmented_path else None

    return render_template('index.html', 
                           original=original_path, 
                           segmented=segmented_path, 
                           surface=surface,
                           iou_score="{:.3f}".format(iou_score) if iou_score else None,
                           plot_img=plot_img_path,
                           original_frame=original_frame_path,
                           segmented_frame=segmented_frame_path,
                           )
    
@app.route('/segment', methods=['POST'])

def segment():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    
    file = request.files['file']
    selected_model = request.form['model']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        output_file= segment_image(filepath,filename,OUTPUT_FOLDER,selected_model)
       
        session['original'] = './' + url_for('static', filename=f'uploads/input/{filename}')[1:]
        session['segmented'] = './' + url_for('static', filename=f'uploads/output/seg_{filename}')[1:]



        return redirect(url_for('index'))
    
    
@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        flash('No video part')
        return redirect(request.url)

    video = request.files['video']

    if video.filename == '':
        flash('No selected video')
        return redirect(request.url)

    if video and allowed_video(video.filename):
        filename = secure_filename(video.filename)
        filepath = os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], filename)
        video.save(filepath)
        extract_frames(filepath,"./static/uploads/frames")
        frames = [f for f in os.listdir(frames_folder) if os.path.isfile(os.path.join(frames_folder, f))]

        segmented_frames = []
        surfaces = []
        
        for frame_filename in sorted(frames):
            frame_path = os.path.join(frames_folder, frame_filename)

            frame_number = frame_filename.split('_')[1].split('.')[0]
            segmented_filename = f"seg_frame_{frame_number}.png"
            
            
            segmented_path = segment_image(frame_path, segmented_filename, OUTPUT_FOLDER)
            segmented_frames.append(segmented_path)
            print(segmented_path)

            surface = calculate_surface(segmented_path)
            surfaces.append(surface)
        max_surface=max(surfaces)
        max_surface_index = surfaces.index(max_surface)
        max_surface_frame = segmented_frames[max_surface_index]
        print(surfaces)
        plot(surfaces,max_surface_index)
        # ... after plotting ...
        plot_img_path = plot(surfaces,max_surface_index)
        original_frame_path = os.path.join(frames_folder, frames[max_surface_index])
        
        session['plot_img'] = './' + url_for('static', filename=f'uploads/plot/surface_plot.png')[1:]
        session['original_frame'] = './' + url_for('static', filename=f'uploads/frames/{frames[max_surface_index]}')[1:]
        session['segmented_frame'] = './' + url_for('static', filename=f'uploads/output/seg_{frames[max_surface_index]}')[1:]


        flash('Video processed successfully!')
        return redirect(url_for('index'))

    
    


if __name__ == "__main__":
    app.run(debug=True)





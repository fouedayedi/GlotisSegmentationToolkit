import cv2
import os
import matplotlib.pyplot as plt

def extract_frames(video_path, output_folder):
    """Extract frames from video and save them to output_folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"Error: Couldn't open video file {video_path}")
        return

    frame_number = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.png")
        cv2.imwrite(frame_filename, frame)

        frame_number += 1
    video.release()
    print(f"Extracted {frame_number} frames and saved to {output_folder}")

#extract_frames("./static/uploads/videos/4_seg.mp4","./static/uploads/input")

def plot(surfaces,max_surface_index):
    plt.figure(figsize=(10,6))
    plt.plot(surfaces, label="Glottis Surface", color="blue")
    plt.axvline(max_surface_index, color="red", linestyle="--", label=f"Max Surface at frame {max_surface_index}")
    plt.legend()
    plt.title("Variance of Glottis Surface over Frames")
    plt.xlabel("Frame")
    plt.ylabel("Surface")
    plt.savefig('./static/uploads/plot/surface_plot.png')
    plt.show()
    
    return()
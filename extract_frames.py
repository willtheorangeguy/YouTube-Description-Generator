# This script extracts frames from all .mp4 files in the current directory
# and saves them in a subdirectory named after the video file with "_frames" suffix.
import os
import glob
import cv2

# Function to extract frames from a video file and save them as images
def extract_frames(video_path, output_dir):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
 
    # Check if the video file was opened successfully
    if not cap.isOpened():
        print(f"Error: Cannot open video file {video_path}")
        return
  
    # Get frames per second of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        print("Error: Cannot determine FPS of video.")
        return

    # Get total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = int(total_frames / fps)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Extract frames at each second
    for second in range(duration + 1):
        frame_number = int(second * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        
        if ret:
            frame_filename = os.path.join(output_dir, f"frame_{second:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"Saved {frame_filename}")
        else:
            print(f"Warning: Couldn't read frame at {second}s")

    # Confirm
    cap.release()
    print("Done extracting frames.")

# Main function to process all .mp4 files in the current directory
if __name__ == "__main__":
    mp4_files = glob.glob("*.mp4")
    if not mp4_files:
        print("No .mp4 files found in the current directory.")
    else:
        for video_file in mp4_files:
            output_dir = os.path.splitext(video_file)[0] + "_frames"
            print(f"Extracting frames from {video_file} to {output_dir}")
            extract_frames(video_file, output_dir)

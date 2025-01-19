import os
import time
import shutil
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
WATCH_FOLDER = "./images"  # Folder to monitor
UPLOADED_FOLDER = "./uploaded"  # Folder to move uploaded images
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"
UPLOAD_ATTRIBUTE = "imageFile"
UPLOAD_DELAY = 30  # Time to wait before uploading a new file (in seconds)

# Ensure the uploaded folder exists
os.makedirs(UPLOADED_FOLDER, exist_ok=True)

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            print(f"New image detected: {event.src_path}")
            time.sleep(UPLOAD_DELAY)  # Wait before uploading
            self.upload_image(event.src_path)

    def upload_image(self, image_path):
        try:
            # Use curl to upload the image
            result = subprocess.run(
                ["curl", "-X", "POST", "-F", f"{UPLOAD_ATTRIBUTE}=@{image_path}", UPLOAD_URL],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"Successfully uploaded: {image_path}")
                self.move_to_uploaded(image_path)
            else:
                print(f"Failed to upload {image_path}: {result.stderr}")
        except Exception as e:
            print(f"Error uploading {image_path}: {e}")

    def move_to_uploaded(self, image_path):
        try:
            filename = os.path.basename(image_path)
            destination = os.path.join(UPLOADED_FOLDER, filename)
            shutil.move(image_path, destination)
            print(f"Moved {image_path} to {destination}")
        except Exception as e:
            print(f"Error moving file {image_path}: {e}")

if __name__ == "__main__":
    print("Starting folder monitoring...")
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

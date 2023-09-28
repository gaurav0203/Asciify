import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2 as cv
from asciify import pillowImagePrintGray, pillowImagePrintColor, modifyContrastAndBrightness


def open_image_file_dialog():
    file_path = filedialog.askopenfile(filetypes=[("Image files", "*jpg *.jpeg *.png")])
    if file_path:
        try:
            image = cv.imread(file_path.name)
            if enable_contrast_brightness.get():
                image = modifyContrastAndBrightness(image, float(contrast_var.get()), int(brightness_var.get()))

            if selected_option.get() == "normal":
                image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            elif selected_option.get() == "grayscale":
                image = pillowImagePrintGray(image, fontSize=slider_var.get())
            else:
                image = pillowImagePrintColor(image, fontSize=slider_var.get())
                image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            image_label.config(image=image)
            image_label.image = image
        except Exception as e:
            print(f"Error:{e} and {file_path.name}")


def open_video_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4 *.avi *.mkv *.mov *.wmv")])
    if file_path:
        cap = cv.VideoCapture(file_path)
        if not cap.isOpened():
            print("Error: Could not open video file.")
            return
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Process and display the frame here (e.g., using cv2.imshow)
            if enable_contrast_brightness.get():
                frame = modifyContrastAndBrightness(frame, float(contrast_var.get()), int(brightness_var.get()))

            if selected_option.get() == "normal":
                # frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                pass
            elif selected_option.get() == "grayscale":
                frame = pillowImagePrintGray(frame, fontSize=slider_var.get())
            else:
                frame = pillowImagePrintColor(frame, fontSize=slider_var.get())
                # frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

            cv.imshow("Video", frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv.destroyAllWindows()


def open_webcam():
    cap = cv.VideoCapture(0)  # 0 is the default index for the primary webcam
    if not cap.isOpened():
        print("Error: Could not access the webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if enable_contrast_brightness.get():
            frame = modifyContrastAndBrightness(frame, float(contrast_var.get()), int(brightness_var.get()))

        if selected_option.get() == "normal":
            # frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            pass
        elif selected_option.get() == "grayscale":
            frame = pillowImagePrintGray(frame, fontSize=slider_var.get())
        else:
            frame = pillowImagePrintColor(frame, fontSize=slider_var.get())
            # frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        cv.imshow("Webcam", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()


def update_font_value(value):
    # global fontSize = value
    label.config(text=f"Font Size: {value}")


def update_contrast_value(value):
    # global fontSize = value
    contrast_label.config(text=f"Contrast: {value}")


def update_brightness_value(value):
    # global fontSize = value
    brightness_label.config(text=f"Brightness: {value}")


def toggle_sliders():
    if enable_contrast_brightness.get():
        # Enable the sliders
        contrast.config(state="normal")
        brightness.config(state="normal")
    else:
        # Disable the sliders
        contrast.config(state="disabled")
        brightness.config(state="disabled")


root = tk.Tk()
root.title("Asciify")

selected_option = tk.StringVar()
selected_option.set("grayscale")

slider_var = tk.IntVar()
enable_contrast_brightness = tk.DoubleVar()
contrast_var = tk.IntVar()
brightness_var = tk.IntVar()

label = tk.Label(root, text="Select an media: ")
label.grid(row=0, column=0, padx=10, pady=10)

button = tk.Button(root, text="Image", command=open_image_file_dialog)
button.grid(row=0, column=1, padx=10, pady=10)

button = tk.Button(root, text="Video", command=open_video_file_dialog)
button.grid(row=0, column=2, padx=10, pady=10)


button = tk.Button(root, text="Webcam", command=open_webcam)
button.grid(row=0, column=3, padx=10, pady=10)

label3 = tk.Label(root, text="Press 'q' to exit video/webcam.")
label3.grid(row=1, column=1, columnspan=10, padx=10, pady=10)

label2 = tk.Label(root, text="Mode: ")
grayscale = tk.Radiobutton(root, text="Gray Scale ASCII", variable=selected_option, value="grayscale")
colored = tk.Radiobutton(root, text="Colored ASCII", variable=selected_option, value="colored")
normal = tk.Radiobutton(root, text="Normal View", variable=selected_option, value="normal")


label2.grid(row=2, column=0, padx=10, pady=10)
grayscale.grid(row=2, column=1, padx=10, pady=10)
colored.grid(row=2, column=2, padx=10, pady=10)
normal.grid(row=2, column=3, padx=10, pady=10)

slider = tk.Scale(root, from_=5, to=25, orient="horizontal", command=update_font_value, variable=slider_var)
slider.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

# Create a label to display the slider value
label = tk.Label(root, text="Font Size: 5")
label.grid(row=3, column=0, padx=10, pady=10)


checkbox = tk.Checkbutton(root, text="Modify Contrast and Brightness",variable=enable_contrast_brightness, command=toggle_sliders)
checkbox.grid(row=4, column=0,columnspan=10, padx=10, pady=10)

contrast_label = tk.Label(root, text="Contrast: 1.0")
contrast = tk.Scale(root, from_=1.0, to=3.0, orient="horizontal", state="disabled", command=update_contrast_value, variable=contrast_var, resolution=0.01)
brightness_label = tk.Label(root, text="Brightness: 0")
brightness = tk.Scale(root, from_=0, to=100, orient="horizontal", state="disabled", command=update_brightness_value, variable=brightness_var)

contrast_label.grid(row=5, column=0, padx=10, pady=10)
contrast.grid(row=5, column=1, padx=10, pady=10)
brightness_label.grid(row=5, column=2, padx=10, pady=10)
brightness.grid(row=5, column=3, padx=10, pady=10)

image_label = tk.Label(root)
image_label.grid(row=6, column=0, columnspan=10, padx=10, pady=10)

root.mainloop()

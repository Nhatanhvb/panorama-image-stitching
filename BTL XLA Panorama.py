import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
import imutils
import time
import os

def select_images():
    
    # Mở hộp thoại để chọn nhiều tệp ảnh
    files_selected = filedialog.askopenfilenames()
    if files_selected:
        return files_selected
    else:
        print("Bạn chưa chọn ảnh nào.")
        return None

def create_panorama(select_images):

    # Đọc các ảnh và thêm vào danh sách
    img_list = [cv2.imread(img) for img in select_images]

    start_time1 = time.time()

    # Tạo đối tượng Stitcher
    stitcher = cv2.Stitcher_create()

    # Ghép các ảnh lại với nhau để tạo panorama
    status, panorama = stitcher.stitch(img_list)
        
    # Kiểm tra xem việc ghép ảnh có thành công không
    if status != cv2.Stitcher_OK:
        messagebox.showerror("Lỗi", f"Lỗi ghép ảnh, mã lỗi: {status}")
        return None
    
    end_time1 = time.time()
    create_time = end_time1 - start_time1
    print(f"Thời gian tạo ảnh panorama: {create_time:.4f} giây")
        
    return panorama

def resize_to_fit_screen(panorama):

    start_time2 = time.time()

    root = tk.Tk()
    root.withdraw()  # Ẩn cửa sổ gốc

    # Lấy kích thước của màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Lấy kích thước của ảnh
    image_height, image_width = panorama.shape[:2]

    # Tính tỉ lệ để giảm kích thước ảnh
    scale = min(screen_width / (1.2*image_width), screen_height / (1.2*image_height))

    # Thay đổi kích thước ảnh
    resized_image = cv2.resize(panorama, (int(image_width * scale), int(image_height * scale)))

    end_time2 = time.time()
    resize_time = end_time2 - start_time2
    print(f"Thời gian resize ảnh panorama: {resize_time:.4f} giây")

    return resized_image

def crop_image(panorama):

    start_time3 = time.time()
    panorama = cv2.copyMakeBorder(panorama, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0,0,0))

    gray = cv2.cvtColor(panorama, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray, 0, 255 , cv2.THRESH_BINARY)[1]

    contours = cv2.findContours(thresh_img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = imutils.grab_contours(contours)
    areaOI = max(contours, key=cv2.contourArea)

    mask = np.zeros(thresh_img.shape, dtype="uint8")
    x, y, w, h = cv2.boundingRect(areaOI)
    cv2.rectangle(mask, (x,y), (x + w, y + h), 255, -1)

    minRectangle = mask.copy()
    sub = mask.copy()

    while cv2.countNonZero(sub) > 0:
        minRectangle = cv2.erode(minRectangle, None)
        sub = cv2.subtract(minRectangle, thresh_img)

    contours = cv2.findContours(minRectangle.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = imutils.grab_contours(contours)
    areaOI = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(areaOI)

    panorama = panorama[y:y + h, x:x + w]

    end_time3 = time.time()
    crop_time = end_time3 - start_time3
    print(f"Thời gian crop ảnh panorama: {crop_time:.4f} giây")
    return panorama

def display_panorama(panorama):    
    cv2.imshow('Panorama', panorama)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def open_image_selection():
    images = select_images()
    if images:
        begin = time.time()
        result = create_panorama(images)
        
        if result is not None:
            if crop_checked.get():  # Kiểm tra trạng thái của checkbox
                cropped = crop_image(result)
                save_panorama(cropped)
                resized = resize_to_fit_screen(cropped)
            else:
                save_panorama(result)
                resized = resize_to_fit_screen(result)
        end = time.time()
        cal = end - begin
        print(f"Thời gian thực hiện ảnh vừa rồi: {cal:.4f} giây")
        print("====================================================================================================")
        display_panorama(resized)

def save_panorama(panorama):
    folder = save_path_entry.get()
    current_time = time.strftime("%Y%m%d_%H%M%S")
    save_path = os.path.join(folder, f"panorama_{current_time}.jpg")  # Đường dẫn lưu ảnh
    cv2.imwrite(save_path, panorama)
    print(f"Đã lưu ảnh panorama vào {save_path}")

def open_save_path():
    save_folder = 'C:/Users/nhata/Pictures/pano result'
    save_folder = filedialog.askdirectory()
    if save_folder:
        save_path_entry.delete(0, tk.END)  # Xóa nội dung hiện tại trong Entry
        save_path_entry.insert(0, save_folder)  # Chèn đường dẫn lưu ảnh vào Entry
    return save_folder

# Main GUI window
root = tk.Tk()
root.title("BTL Xử lý ảnh | Tạo ảnh Panorama")
root.geometry("500x300")  # Thiết lập kích thước cửa sổ

# Function selection frame
function_frame = tk.Frame(root)
function_frame.pack(padx=20, pady=20, expand=True)  # Thêm expand=True để phần tử lấp đầy không gian

# Function selection label
function_label = tk.Label(function_frame, text="Chọn chức năng:")
function_label.pack()

# Button to select images
select_button = tk.Button(function_frame, text="Chọn ảnh", command=open_image_selection)
select_button.pack(pady=15, padx=50)  # Đặt padx để căn giữa nút button
select_button.configure(width=15, height=2)  # Cài đặt kích thước của nút button

# Checkbox for cropping image
crop_checked = tk.BooleanVar()
crop_checkbox = tk.Checkbutton(function_frame, text="Crop ảnh", variable=crop_checked)
crop_checkbox.pack()

# Entry to display save path
save_path_entry = tk.Entry(function_frame, width=50)
save_path_entry.insert(0, 'C:/Users/nhata/Pictures/pano result')
save_path_entry.pack(side=tk.LEFT, padx=10, pady=30)

# Button to select save path
save_path_button = tk.Button(function_frame, text="...", command=open_save_path)
save_path_button.pack(side=tk.LEFT, padx=5, pady=30)

credit = tk.Label(root, text="@Nguyễn Nhật Ánh - 93397 - Xử lý ảnh N08")
credit.pack(side=tk.LEFT)

# Run the main loop
root.mainloop()
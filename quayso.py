import tkinter as tk
from tkinter import messagebox
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Danh sách số và tên tương ứng
numbers = list(range(1, 18))
names = {
    1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 
    6: "F", 7: "G", 8: "H", 9: "I", 10: "J", 
    11: "K", 12: "L", 13: "M", 14: "N", 15: "O", 
    16: "P", 17: "Q"
}

def spin_wheel():
    if not numbers:
        messagebox.showinfo("Hết lượt", "Tất cả các số đã được quay!")
        return
    
    result = random.choice(numbers)
    selected_number.set(result)
    result_name.set(names[result])
    numbers.remove(result)

def send_email():
    recipient_email = email_entry.get()
    if not recipient_email:
        messagebox.showerror("Lỗi", "Vui lòng nhập email!")
        return

    if not selected_number.get():
        messagebox.showerror("Lỗi", "Vui lòng quay trước khi gửi email!")
        return
    
    selected_char = result_name.get()
    
    # Gửi email
    try:
        sender_email = "*******************"  # Thay bằng email của bạn
        sender_password = "******************"  # Thay bằng mật khẩu ứng dụng

        subject = "Kết quả bốc thăm mất quà"
        body = f"Bạn sẽ tặng quà cho: {selected_char}"

        # Tạo email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Kết nối và gửi
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        messagebox.showinfo("Thành công", f"Đã gửi email tới {recipient_email}!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể gửi email: {e}")

# Giao diện chính
app = tk.Tk()
app.title("Bốc thăm mất quà")
app.geometry("800x600")

selected_number = tk.StringVar()
result_name = tk.StringVar()

# Giao diện vòng quay
tk.Label(app, text="Kết quả:", font=("Arial", 24)).pack(pady=10)
tk.Label(app, textvariable=selected_number, font=("Arial", 50), fg="red").pack()
# Nút quay
spin_button = tk.Button(app, text="Bốc thăm", font=("Arial", 24), command=spin_wheel)
spin_button.pack(pady=10)

# Nhập email
tk.Label(app, text="Email:", font=("Arial", 24)).pack(pady=10)
email_entry = tk.Entry(app, font=("Arial", 24), width=30)
email_entry.pack()

# Nút gửi email
send_button = tk.Button(app, text="Gửi email", font=("Arial", 24), command=send_email)
send_button.pack(pady=10)

# Chạy giao diện
app.mainloop()

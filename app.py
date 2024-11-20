 from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Đặt khóa bí mật cho Flask

# Cấu hình gửi email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'linhkienvang.sell@gmail.com'  # Thay bằng email của bạn
app.config['MAIL_PASSWORD'] = 'pbiwvptfncfwfwji'  # Mật khẩu ứng dụng

mail = Mail(app)

# Danh sách số và tên tương ứng
numbers = list(range(1, 18))
names = {
    1: "A", 2: "B", 3: "C", 4: "D", 5: "E",
    6: "F", 7: "G", 8: "H", 9: "I", 10: "J",
    11: "K", 12: "L", 13: "M", 14: "N", 15: "O",
    16: "P", 17: "Q"
}

@app.route("/", methods=["GET", "POST"])
def index():
    global numbers
    selected_number = None
    selected_name = None
    remaining_numbers = numbers  # Danh sách các số chưa quay

    if request.method == "POST":
        email = request.form.get("email")
        
        if "reset" in request.form:  # Kiểm tra xem người dùng có nhấn nút reset không
            numbers = list(range(1, 18))  # Reset lại danh sách số
            flash("Danh sách số đã được reset!", "info")
            return redirect("/")  # Tải lại trang để reset

        if not email:
            flash("Vui lòng nhập email!", "danger")
        elif not numbers:
            flash("Tất cả các số đã được quay!", "warning")
        else:
            # Bốc thăm
            selected_number = random.choice(numbers)
            selected_name = names[selected_number]
            numbers.remove(selected_number)

            # Gửi email
            try:
                msg = Message(
                    "Kết quả bốc thăm mất quà",
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[email]
                )
                msg.body = f"Bạn sẽ tặng quà cho: {selected_name}"
                mail.send(msg)
                flash(f"Đã gửi kết quả đến {email}!", "success")
            except Exception as e:
                flash(f"Lỗi khi gửi email: {e}", "danger")

    return render_template("index.html", selected_number=selected_number, selected_name=selected_name, remaining_numbers=remaining_numbers)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)

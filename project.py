import customtkinter as ctk
import pyttsx3
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import tkinter as tk
import random
import os
import tkinter.messagebox as messagebox
import speech_recognition as sr
import json
import qrcode
import csv

# Initialize TTS
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Theme setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Main app window
app = ctk.CTk()
app.geometry("1000x720")
app.title("Wanderlust Travel Agency")

nav_bar = ctk.CTkFrame(app, height=60, fg_color="#003049")
nav_bar.pack(fill="y", side="top")

main_content = ctk.CTkFrame(app, fg_color="transparent")
main_content.pack(fill="both", expand=True)
def recognize_and_fill(entry_widget, field_name):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak(f"Listening for {field_name}")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, text)
            speak(f"{field_name} set to {text}")
        except sr.UnknownValueError:
            speak("Sorry, I could not understand.")
        except sr.RequestError:
            speak("Could not request results; check your internet.")
        except sr.WaitTimeoutError:
            speak("Listening timed out.")


def clear_main_content():
    for widget in main_content.winfo_children():
        widget.destroy()

def show_home():
    clear_main_content()
    frame = ctk.CTkFrame(main_content, fg_color="white")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    if os.path.exists("welcome.jfif"):
        img = Image.open("welcome.jfif").resize((1300, 670))
        photo = ImageTk.PhotoImage(img)
        img_label = ctk.CTkLabel(frame, image=photo, text="")
        img_label.image = photo
        img_label.pack(pady=20)
    else:
        ctk.CTkLabel(frame, text="welcome.jfif not found", text_color="red").pack(pady=10)

def show_packages():
    clear_main_content()
    scroll_frame = ctk.CTkScrollableFrame(main_content, width=950, height=620)
    scroll_frame.pack(padx=20, pady=20, fill="both", expand=True)

    ctk.CTkLabel(scroll_frame, text="Explore Top Packages", font=("Segoe UI", 26, "bold"), text_color="#003049").pack(pady=20)
    cards_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    cards_frame.pack()

    row = column = 0

    destinations = [
        {"name": "Paris", "image": "paris.jpg", "description": "Explore the romantic city of Paris, with its Eiffel Tower, museums, and world-class cuisine.", "price": "$1200"},
        {"name": "Bali", "image": "bali.jpg", "description": "Discover the beaches and culture of Bali, known for its stunning temples and resorts.", "price": "$800"},
        {"name": "New York", "image": "newyork.jpg", "description": "Visit iconic landmarks like Times Square, Central Park, and Broadway.", "price": "$1500"},
        {"name": "Tokyo", "image": "tokyo.jpg", "description": "Modern skyscrapers meet traditional temples. Explore its vibrant districts.", "price": "$1300"},
    ]

    def open_detail_page(dest, back_to_packages_callback):

        detail_win = ctk.CTkToplevel(app)
        detail_win.title(dest["name"])
        detail_win.geometry("600x600+20+20")
        detail_win.lift()
        detail_win.attributes('-topmost', True)
        detail_win.after(10, lambda: detail_win.attributes('-topmost', False))
        detail_win.grab_set()
        detail_win.focus_force()

        scroll = ctk.CTkScrollableFrame(detail_win, width=580, height=550)

        scroll.pack(padx=10, pady=10, fill="both", expand=True)

        if os.path.exists(dest["image"]):
            img = Image.open(dest["image"]).resize((500, 300))
            photo = ImageTk.PhotoImage(img)
            lbl = ctk.CTkLabel(scroll, image=photo, text="")
            lbl.image = photo
            lbl.pack(pady=10)

        ctk.CTkLabel(scroll, text=dest["name"], font=("Segoe UI", 24, "bold"), text_color="#003049").pack(pady=(10, 5))
        ctk.CTkLabel(scroll, text=dest["description"], wraplength=550, font=("Segoe UI", 14), text_color="#4B5563").pack(pady=10)
        ctk.CTkLabel(scroll, text=f"Price: {dest['price']}", font=("Segoe UI", 18, "bold"), text_color="#003049").pack(pady=10)

        ctk.CTkButton(scroll, text="Book Now", fg_color="#FF6F00", text_color="white", font=("Segoe UI", 16, "bold"),
                      command=lambda: open_booking_form(dest["name"])).pack(pady=10)
        ctk.CTkButton(scroll, text="← Back to Packages", fg_color="#6c757d", text_color="white",
              command=lambda: [detail_win.destroy(), back_to_packages_callback()]).pack(pady=10)

    for dest in destinations:
        if os.path.exists(dest["image"]):
            img = Image.open(dest["image"]).resize((280, 180))
            photo = ImageTk.PhotoImage(img)
        else:
            continue
        card = ctk.CTkFrame(cards_frame, width=300, height=250, corner_radius=15, fg_color="white")
        card.grid(row=row, column=column, padx=20, pady=20)
        img_label = ctk.CTkLabel(card, image=photo, text="")
        img_label.image = photo
        img_label.pack(pady=10)
        ctk.CTkLabel(card, text=dest["name"], font=("Segoe UI", 18, "bold"), text_color="#003049").pack()
        ctk.CTkButton(card, text="View Package", fg_color="#FF6F00", text_color="white",
              font=("Segoe UI", 14), command=lambda d=dest: open_detail_page(d, show_packages)).pack(pady=10)

        column += 1
        if column >= 2:
            column = 0
            row += 1

def open_booking_form(destination_name):
    win = ctk.CTkToplevel(app)
    win.title("Booking Form")
    win.geometry("600x850+20+20")
    win.lift()
    win.attributes('-topmost', True)
    win.after(10, lambda: win.attributes('-topmost', False))
    win.grab_set()
    win.focus_force()

    otp_code = None

    ctk.CTkLabel(win, text=f"Book Your Trip to {destination_name}", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

    # Name with mic button
    ctk.CTkLabel(win, text="Name:", anchor="w").grid(row=1, column=0, padx=20, sticky="w")
    name = ctk.CTkEntry(win)
    name.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
    ctk.CTkButton(win, text="🎤", width=30, command=lambda: recognize_and_fill(name, "name")).grid(row=1, column=2, padx=5)


    ctk.CTkLabel(win, text="Phone Number:", anchor="w").grid(row=2, column=0, padx=20, sticky="w")
    phone = ctk.CTkEntry(win)
    phone.grid(row=2, column=1, padx=20, pady=5, sticky="ew")

    ctk.CTkLabel(win, text="Email:", anchor="w").grid(row=3, column=0, padx=20, sticky="w")
    email = ctk.CTkEntry(win)
    email.grid(row=3, column=1, padx=20, pady=5, sticky="ew")

    ctk.CTkLabel(win, text="Travel Type:", anchor="w").grid(row=4, column=0, padx=20, sticky="w")
    travel_type_menu = ctk.CTkOptionMenu(win, values=["Flight", "Bus", "Cab", "Train"])
    travel_type_menu.grid(row=4, column=1, padx=20, pady=5, sticky="ew")

    ctk.CTkLabel(win, text="Number of Travelers:", anchor="w").grid(row=5, column=0, padx=20, sticky="w")
    travelers = tk.Spinbox(win, from_=1, to=20, width=10)
    travelers.grid(row=5, column=1, padx=20, pady=5, sticky="w")

    ctk.CTkLabel(win, text="Accommodation:", anchor="w").grid(row=6, column=0, padx=20, sticky="w")
    accommodation = ctk.CTkComboBox(win, values=["3-Star", "4-Star", "5-Star", "Hostel", "None"])
    accommodation.grid(row=6, column=1, padx=20, pady=5, sticky="ew")

    ctk.CTkLabel(win, text="Departure Date:", anchor="w").grid(row=7, column=0, padx=20, sticky="w")
    date_picker = DateEntry(master=win, date_pattern='dd/mm/yyyy')
    date_picker.grid(row=7, column=1, padx=20, pady=5, sticky="ew")

    ctk.CTkLabel(win, text="Trip Type:", anchor="w").grid(row=8, column=0, padx=20, sticky="w")
    trip_type_var = tk.StringVar(value="One Way")
    one_way_radio = ctk.CTkRadioButton(win, text="One Way", variable=trip_type_var, value="One Way", command=lambda: toggle_return_date(False))
    round_trip_radio = ctk.CTkRadioButton(win, text="Round Trip", variable=trip_type_var, value="Round Trip", command=lambda: toggle_return_date(True))
    one_way_radio.grid(row=8, column=1, padx=10, pady=5, sticky="w")
    round_trip_radio.grid(row=8, column=1, padx=95, pady=5, sticky="w")

    return_date_label = ctk.CTkLabel(win, text="Return Date:", anchor="w")
    return_date_picker = DateEntry(master=win, date_pattern='dd/mm/yyyy')


    def toggle_return_date(show):
        if show:
            return_date_label.grid(row=9, column=0, padx=20, pady=5, sticky="w")
            return_date_picker.grid(row=9, column=1, padx=20, pady=5, sticky="ew")
        else:
            return_date_label.grid_forget()
            return_date_picker.grid_forget()

    # Initially hidden
    toggle_return_date(False)

    otp_label = ctk.CTkLabel(win, text="")
    otp_entry = ctk.CTkEntry(win, placeholder_text="Enter OTP")
    confirm_otp_btn = ctk.CTkButton(win, text="Verify OTP")
    success_label = ctk.CTkLabel(win, text="", text_color="green")


    def send_otp():
        nonlocal otp_code
        number = phone.get().strip()

        # ✅ Check for empty phone number
        if number == "":
            messagebox.showerror("Missing Phone Number", "Please fill in the phone number.")
            speak("Please fill in the phone number.")
            return

        # ✅ Check for invalid phone number length or format
        if not number.isdigit() or len(number) != 10:
            messagebox.showerror("Invalid Phone Number", "Phone number must be 10 digits.")
            speak("Invalid phone number.")
            return

        # ✅ Generate and speak OTP
        otp_code = str(random.randint(1000, 9999))
        speak(f"Your OTP is {otp_code}")
        messagebox.showinfo("OTP Sent", f"OTP has been sent to {number}.\n(For demo, OTP is: {otp_code})")

        # ✅ Show OTP entry
        otp_label.configure(text="Enter OTP sent to your phone:")
        otp_label.grid(row=10, column=0, padx=20, sticky="w")
        otp_entry.grid(row=10, column=1, padx=20, pady=5, sticky="ew")
        confirm_otp_btn.grid(row=11, column=0, columnspan=2, pady=5)

        

    def verify_otp():
        entered_otp = otp_entry.get().strip()
        if entered_otp == otp_code:
            success_label.configure(text="✅ Phone Verified!")
            success_label.grid(row=12, column=0, columnspan=2, pady=5)
            otp_label.grid_forget()
            otp_entry.grid_forget()
            confirm_otp_btn.grid_forget()
            submit_button.grid(row=13, column=0, columnspan=2, pady=20)
        else:
            messagebox.showerror("Invalid OTP", "Incorrect OTP entered.")
            speak("Incorrect OTP")

    confirm_otp_btn.configure(command=verify_otp)
    ctk.CTkButton(win, text="Send OTP", fg_color="#0d6efd", text_color="white", command=send_otp).grid(row=2, column=2, padx=10)

    def validate_and_book():
        if not success_label.cget("text"):
            messagebox.showerror("Phone Not Verified", "Please verify your phone number with OTP before booking.")
            return

        n, e, p, t = name.get().strip(), email.get().strip(), phone.get().strip(), travelers.get()
        d = date_picker.get()
        a = accommodation.get()
        tt = travel_type_menu.get()
        trip_type = trip_type_var.get()
        return_date = return_date_picker.get() if trip_type == "Round Trip" else "N/A"

        if not (n and e and p and t and d and a and tt):
            messagebox.showerror("Missing Fields", "All fields are required!")
            speak("Please fill in all fields.")
            return

        if not p.isdigit() or len(p) != 10:
            messagebox.showerror("Invalid Phone Number", "Phone number must be 10 digits.")
            speak("Invalid phone number.")
            return

        if "@" not in e or "." not in e or e.startswith("@") or e.endswith("@") or e.startswith(".") or e.endswith("."):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            speak("Invalid email address.")
            return

        # --- Payment simulation popup ---
        def payment_success():
            payment_win.destroy()

            summary = (
                f"Destination: {destination_name}\n"
                f"Name: {n}\nEmail: {e}\nPhone: {p}\nTravelers: {t}\n"
                f"Accommodation: {a}\nDeparture: {d}\nReturn: {return_date}\n"
                f"Travel Type: {tt}\nTrip Type: {trip_type}"
            )

            # Save booking info to a text file
            save_path = "bookings.txt"
            with open(save_path, "a") as f:
                f.write("----- New Booking -----\n")
                f.write(summary + "\n\n")

            # Save booking info to a CSV file
            csv_file = "bookings.csv"
            file_exists = os.path.isfile(csv_file)

            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                # Write header only if file does not exist
                if not file_exists:
                    writer.writerow(["Destination", "Name", "Email", "Phone", "Travelers",
                                     "Accommodation", "Departure Date", "Return Date",
                                     "Travel Type", "Trip Type"])
                    writer.writerow([destination_name, n, e, p, t, a, d, return_date, tt, trip_type])


            # Generate QR code
            qr = qrcode.make(summary)
            qr_path = "booking_qr.png"
            qr.save(qr_path)

            # Create QR window
            qr_win = ctk.CTkToplevel(win)
            qr_win.title("Booking QR Code")
            qr_win.geometry("350x400+60+60")
            qr_win.grab_set()

            ctk.CTkLabel(qr_win, text="Your Booking QR Code", font=("Segoe UI", 16, "bold")).pack(pady=10)

            # Show QR code image
            img = Image.open(qr_path).resize((250, 250))
            photo = ImageTk.PhotoImage(img)
            qr_label = ctk.CTkLabel(qr_win, image=photo, text="")
            qr_label.image = photo
            qr_label.pack(pady=10)

            # Button to close
            ctk.CTkButton(qr_win, text="Close", command=lambda: [qr_win.destroy(), win.destroy()]).pack(pady=10)

            speak(f"Thank you {n}, your booking to {destination_name} is confirmed!")
            messagebox.showinfo("Booking Confirmed", f"✅ Booking Confirmed!\n\n{summary}")


        def payment_cancel():
            payment_win.destroy()
            messagebox.showinfo("Payment Cancelled", "Payment was cancelled. You can complete booking later.")

        payment_win = ctk.CTkToplevel(win)
        payment_win.title("Payment Gateway")
        payment_win.geometry("300x150+50+50")
        payment_win.grab_set()

        ctk.CTkLabel(payment_win, text="Simulated Payment Gateway", font=("Segoe UI", 14, "bold")).pack(pady=15)
        ctk.CTkButton(payment_win, text="Pay", fg_color="#28a745", text_color="white", command=payment_success).pack(pady=5)
        ctk.CTkButton(payment_win, text="Cancel", fg_color="#dc3545", text_color="white", command=payment_cancel).pack(pady=5)

    submit_button = ctk.CTkButton(win, text="Confirm Booking", fg_color="#28a745", text_color="white", command=validate_and_book)
    win.grid_columnconfigure(1, weight=1)

    back_btn = ctk.CTkButton(win, text="Back", fg_color="#6c757d", text_color="white", command=win.destroy)
    back_btn.grid(row=14, column=0, columnspan=2, pady=(0, 20))


def show_about_us():
    clear_main_content()
    frame = ctk.CTkFrame(main_content, fg_color="white")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    if os.path.exists("aboutus.jfif"):
        img = Image.open("aboutus.jfif").resize((1300, 670))
        photo = ImageTk.PhotoImage(img)
        img_label = ctk.CTkLabel(frame, image=photo, text="")
        img_label.image = photo
        img_label.pack(pady=20)

nav_items = {
    "Home": show_home,
    "Packages": show_packages,
    "About Us": show_about_us,
}

for text, cmd in nav_items.items():
    ctk.CTkButton(nav_bar, text=text, fg_color="#003049", text_color="white",
                  hover_color="#0077b6", corner_radius=0, font=("Segoe UI", 14, "bold"),
                  width=130, command=lambda c=cmd, t=text: [c(), speak(f"You clicked on {t}")]).pack(side="left", padx=5, pady=10)

footer = ctk.CTkLabel(app, text="© 2025 Wanderlust Travel Agency", font=("Segoe UI", 12), text_color="#6c757d")
footer.pack(pady=10)

show_home()
app.mainloop()

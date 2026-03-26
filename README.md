# 🚀 Smart Send - WhatsApp Automation Tool

Smart Send is a Python-based automation tool that enables users to send bulk WhatsApp messages efficiently using CSV data. It uses WhatsApp Web for seamless communication without requiring any official API.

---

## 📌 Overview

This project automates the process of sending WhatsApp messages to multiple contacts or groups. It is designed for ease of use and can be extended for real-world applications like notifications, marketing, and alerts.

---

## ✨ Features

* 📩 Send bulk WhatsApp messages using CSV input
* 👥 Send messages to WhatsApp groups
* ⚡ Fast and automated workflow
* 🔐 Works with WhatsApp Web (no API required)
* 🧩 Simple and customizable code structure

---

## 🛠️ Tech Stack

* Python
* PyWhatKit
* Pandas

---

## 📂 Project Structure

smart-send/
│── smart-send.py       
│── contacts.csv         
│── requirements.txt    
│── README.md           

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/smart-send.git
cd smart-send
```

### 2️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Prepare Input File

Edit `contacts.csv` and add your data:

```
name,phone,message
Demo,+911234567890,Hello Demo!
```

⚠️ Make sure:

* Phone numbers include country code (e.g., +91)
* No empty rows in CSV

---

### 4️⃣ Run the Project

```
python smart-send.py
```

---

## ⚠️ Important Notes

* Ensure WhatsApp Web is already logged in
* Do not use the system while messages are being sent
* Avoid sending too many messages quickly (to prevent blocking)
* Keep internet connection stable

---

## 🎯 Use Cases

* Marketing campaigns
* Event notifications
* Customer communication
* Reminder systems
* Personal bulk messaging

---

## 🚧 Limitations

* Depends on WhatsApp Web session
* May fail if internet is unstable
* Not suitable for large-scale enterprise messaging

---

## 📈 Future Enhancements

* GUI-based interface (desktop/web app)
* Message scheduling feature
* Personalized message templates
* Contact filtering options
* Logging and analytics dashboard

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

---

## 📜 License

This project is intended for educational and experimental purposes only. 
Any misuse of this tool is not the responsibility of the developer.

---

## 👨‍💻 Author

Developed by Manvi raj



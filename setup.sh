#!/bin/bash
# Install package sistem yang dibutuhkan Termux
pkg update && pkg upgrade
pkg install python git -y

# Buat virtual environment baru
python -m venv venv
source venv/bin/activate

# Install semua library dari requirements.txt
pip install --upgrade pip
pip install -r requirements.txt

echo "Setup selesai! Jalankan 'source venv/bin/activate' untuk mulai."

echo "root ALL=(ALL) NOPASSWD: /usr/sbin/chpasswd" | sudo tee /etc/sudoers.d/userapi
sudo chmod 440 /etc/sudoers.d/userapi
mkdir /opt/userapi
echo "Przenoszenie plików main.py i userapi.service"
sudo cp main.py /opt/userapi/main.py
sudo cp userapi.service /etc/systemd/system/userapi.service
echo "Instalowanie rozszerzen do dzialania"
sudo pip install fastapi uvicorn python-multipart --break-system-packages
echo "Uruchamianie usługi"
sudo systemctl daemon-reload
sudo systemctl enable --now userapi

ssh-keygen -p -f /home/kali/Desktop/my_ssh_key #key 

import paramiko
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

# Đường dẫn đến tệp khóa bí mật đã mã hóa
private_key_path = "/home/kali/Desktop/my_encrypted_ssh_key"

# Mật khẩu để giải mã khóa bí mật
private_key_password = b"your_private_key_password"

try:
    # Đọc nội dung khóa bí mật từ tệp
    with open(private_key_path, "rb") as key_file:
        private_key_data = key_file.read()

    # Giải mã khóa bí mật
    private_key = serialization.load_pem_private_key(
        private_key_data,
        password=private_key_password,
        backend=default_backend()
    )

    # Tạo SSH client
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Kết nối tới máy chủ SSH bằng khóa bí mật đã giải mã
    client.connect(hostname="127.0.0.1", port=22, username="kali", pkey=private_key)

    # Thực hiện các lệnh trên máy chủ SSH
    stdin, stdout, stderr = client.exec_command("ls -l")
    print(stdout.read().decode())

    # Đóng kết nối SSH
    client.close()

except Exception as e:
    print(f"Đã xảy ra lỗi: {str(e)}")
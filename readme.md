Лучше создать приватный и публичный ключи командой:

ssh-keygen -t rsa

Ничего не вводить, постоянно на все вопросы нажимать Enter
После чего на гитхабе добавить ssh-ключ, который будет в home_dir/.ssh/id_pub.rsa

Для копирования в буфер из файла:

sudo apt install xclip
xclip -sel c < input_file

-sel означает -selection . c означает clipboard

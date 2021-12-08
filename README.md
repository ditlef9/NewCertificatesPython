# New Certificates Python 


# 1. Licence
Please read GNU GENERAL PUBLIC LICENSE.txt

# 2 Install
a) Download and install latest version of Python<br />
b) Download and install PyCharm<br />
c) Check out this project in PyCharm. <br />
d) Upgrade PIP by opening CMD as Administrator and enter:

* cd C:\Users\{username}\AppData\Local\Programs\Python\Python{version}
* python.exe -m pip install --upgrade pip

e) In the same CMD window install the following libraries: 

* python.exe -m pip install wheel<br />
* python.exe -m pip install certstream<br />
* python.exe -m pip install mysql-connector-python<br />
* python.exe -m pip install pygame

f) Inside PyCharm project select "Add a Configuration" and make it point to file Main.py.

# 3 Setup MySQL
a) Install MySQL<br />
b) Createa a database with name "quick"

# 4 Configurations
Run the script and a file named filters_include_contains.txt will be created.
Inside this file you can add domain names that you want the script to find. 

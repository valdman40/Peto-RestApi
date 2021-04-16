first check that port 5000 is open in your computer, otherwise you'll not be able to connect the server from remote device.
after we did that, check your local ip address and enter it to BASE_URL variable which is located in shared.py.
example: BASE_URL = "http://192.168.43.72:5000" means my local ip address is BASE_URL = 192.168.43.72.

same thing goes to the remote devices you're using.. for example in the application there is defenition of urlBase is the same as BASE_URL.

now to make it run open current folder from command line.
run python server.py
now your server is up. notice in main function if debug=True, it means everytime you 
make changes in server.py and save, it will reload the server.


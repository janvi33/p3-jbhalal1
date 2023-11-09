janvi bhalala
jbhalal1@binghamton.edu
yes, My code was tested on remote.cs

Steps to execute
1) run "python3 genpassword.py"  which will ask user for id and password and stored that in hashpasswd
2) run "python3 server.py <port number>" which will start the server on mentioned port number, also it will take the id and password sent by client and check whether it exists in hashpassword or not. If the id and password exists it will return "correct id/password" else it will return "incorrect id/password"
3) run "python3 client.py remote00-07.cs.binghamton.edu <same port number(as entered for server)>" on different terminal , this will ask for id and password and sent that info to server. 

No software is needed to install in remote.cs

There are one key and one certificate and I have used SHA-256 for encrypting password
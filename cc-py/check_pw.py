import getpass

print("Enter your password:")
password = "secret"
typed_password = "SOME"
while password != typed_password:
    typed_password = getpass.getpass()  ##input()
    if typed_password == password:
        print("Access Granted !")
    else:
        print("Access DENIED - HAxr")

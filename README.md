# infidel-II
A pure python version of the Infidel vulnserver Stack Buffer Overflow exploit.

I was displeased with relying on Mona to generate my exploit. I have opted to create my own.
You'll note unusable reverse shell handlers in the code - at this time, a reverse shell is simply not viable. I opted for a bind shell instead due to the static shellcode opportunity.

This shellcode is made with the Metasploit Framework, version 4. It is a bind TCP connection, which listens on port 9998. A homemade handler connects to the target, providing an attacker with a shell with the priveleges of the comprimised instance of vulnserver. You are, of course, welcome to substitute your own shellcode.

The exploit stack is compiled like so.
{TRUN /.:/}{A * 2003}{EIP Ret2DLL for jmp esp}{NOP sled, 300 in length (\x90)}{shellcode} so shellcode length is not (much of) a concern.
The handlers work well, but can be disabled or switched to Reverse mode by doing the following.
bshell=false #turn off bind handler
rshell=true  #use reverse handler
or 
bshell=false
rshell=false #Useful for, for example, msf's "speak_pwnd" shellcode, where a handler is not necessary

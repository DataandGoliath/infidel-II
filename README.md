# infidel-II
A pure python version of the Infidel vulnserver Stack Buffer Overflow.

I was displeased with relying on Mona to generate my exploit. I have opted to create my own.
You'll note unusable reverse shell handlers in the code - at this time, a reverse shell is simply not viable. I opted for a bind shell instead due to the static shellcode opportunity.

This shellcode is made with the Metasploit Framework, version 4. It is a bind TCP connection, which listens on port 9998. A homemade handler connects to the target, providing an attacker with a shell with the priveleges of the comprimised instance of vulnserver.

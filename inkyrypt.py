from hashlib import sha512

def xor(s1,s2):    
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

e_or_d = raw_input("Write 'e' for Encrypt or 'd' Decrypt  :\n")
 
x=raw_input("Enter file path:\n").strip()
#x=x[:-1].replace("'","").replace("\\","/")
with open(x,"rb") as f:
    c = f.read()
    
p=raw_input("Enter password to (Decrypt/Encrypt):\n")

k = sha512(p).hexdigest()

#Hashing the password with SHA512
if e_or_d == 'e':
    c = c + sha512(c).hexdigest()
    div = len(c) / len(k)
    k=div*k+k
    k=k[:len(c)]
    wr=xor(c,k)
    with open(x,"wb") as f:
        f.write(wr)
        print "Encrypted successfully!"
    
if e_or_d == 'd':
    div = len(c) / len(k)
    k=div*k+k
    k=k[:len(c)]
    m=xor(c,k)
    sign = m[-128:]
    m = m[:-128]
    verify = sha512(m).hexdigest()
    if sign == verify:
        with open(x,"wb") as f:
            f.write(m)
        print "Decrypted successfully!"
            
    else:
        print "Wrong password!!!"    







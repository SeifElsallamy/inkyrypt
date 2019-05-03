from hashlib import sha512

def string_to_bits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def bits_to_string(bits):
    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)
    
def xor(x1,x2):
    x=[]
    if len(x1) != len(x2):
        print "x1 and x2 not same length"
        return False
    for i in range(len(x1)):
        x.append(x1[i] ^ x2[i])
    return x

def key_pad(string_to_expand, length):
   return (string_to_expand * ((length/len(string_to_expand))+1))[:length]

def enc(f,k):
    f = f + sha512(f).hexdigest()
    diff = len(f) - len(k)
    if diff > 0:
        k = k + key_pad(k, diff)
    if diff < 0:
        k = k[:len(f)]
    
    f = string_to_bits(f)
    k = string_to_bits(k)
    
    return xor(f,k)
  
def dec(f,k):
    f = f + sha512(f).hexdigest()
    diff = len(f) - len(k)
    if diff > 0:
        k = k + key_pad(k, diff)
    if diff < 0:
        k = k[:len(f)]
    
    f = string_to_bits(f)
    k = string_to_bits(k)
    m = xor(f,k)
    m = bits_to_string(m)[:-128]
    
    sign = m[-128:]
    m = m[:-128]
    verify = sha512(m).hexdigest()
    if sign == verify:
        return m
    return False
     



e_or_d = raw_input("Write 'e' for Encrypt or 'd' Decrypt  :\n")
 
x=raw_input("Enter file path:\n").strip()
#x=x[:-1].replace("'","").replace("\\","/")
with open(x,"rb") as f:
    c = f.read()
    
p=raw_input("Enter password to (Decrypt/Encrypt):\n")

k = sha512(p).hexdigest()

if e_or_d == 'e':
    c=enc(c,k)
    with open(x,"wb") as f:
        f.write(bits_to_string(c))
    
if e_or_d == 'd':
    m=dec(c,k)
    
    if m:
        with open(x,"wb") as f:
            f.write(m)
            
    else:
        print "Wrong password!!!"    







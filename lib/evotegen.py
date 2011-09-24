import sys, os, re, base64
from M2Crypto import RSA, X509, m2, EVP

class eVoteGEN:
  keys  = []
  cert  = []
  loaded= 0
  acert = None
  akey  = None

  def load_keys(self):
    if (self.loaded & 1) == 1:
      return
    l = os.listdir("../CA")
    l.sort()
    for e in l:
      if re.match("(part.*)\.key", e) != None:
        self.keys.append(RSA.load_key('../CA/'+e))
    self.acert = X509.load_cert('../CA/arbiter.pem')
    self.loaded |= 1
    self.keys.reverse()

  def load_pub(self):
    if (self.loaded & 2) == 2:
      return
    l = os.listdir("../CA")
    l.sort()
    for e in l:
      if re.match("(part.*)\.pem", e) != None:
        self.cert.append(X509.load_cert('../CA/'+e))
    self.acert = X509.load_cert('../CA/arbiter.pem')
    self.akey = RSA.load_key('../CA/arbiter.key')
    self.loaded |= 2

  def round_encrypt(self, text):
    self.load_pub()
    for cert in self.cert:
      pad = m2.no_padding
      if len(text) != 128:
        pad = m2.pkcs1_padding
      text = cert.get_pubkey().get_rsa().public_encrypt(text, pad)
    md = EVP.MessageDigest('sha1')
    md.update(text)
    md = md.final()
    sign = self.akey.sign(md, 'sha1')
    return text+sign

  def round_decrypt(self, enc):
    self.load_keys()
    sign = enc[-128:]
    enc = enc[:-128]
    md = EVP.MessageDigest('sha1')
    md.update(enc)
    md = md.final()
    self.akey.verify(md, sign)
    for key in self.keys[:-1]:
      pad = m2.no_padding
      enc = key.private_decrypt(enc, pad)
    return self.keys[-1].private_decrypt(enc, m2.pkcs1_padding)

if __name__ == '__main__':
  e = eVoteGEN()
  enc = e.round_encrypt("bf9b9267-61bd-4619-9202-4c0bf38542b6\n13\n16\n1\n")
  print "Enveloped:", base64.b64encode(enc)
  print "Decrypted:\n-------------\n", e.round_decrypt(enc), "-------------"

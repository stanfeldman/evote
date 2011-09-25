import sys, os, re, base64, uuid
from M2Crypto import RSA, X509, m2, EVP
from django.conf import settings

class eVoteGEN:
  keys  = []
  cert  = []
  loaded= 0
  acert = None
  akey  = None

  ca_path = settings.TEMPLATE_DIRS[0] + '/CA/'

  def load_keys(self):
    if (self.loaded & 1) == 1:
      return
    l = os.listdir(self.ca_path)
    l.sort()
    for e in l:
      if re.match("(part.*)\.key", e) != None:
        self.keys.append(RSA.load_key(self.ca_path + e))
    self.acert = X509.load_cert(self.ca_path + 'arbiter.pem')
    self.keys.reverse()
    self.loaded |= 1

  def load_pub(self):
    if (self.loaded & 2) == 2:
      return
    l = os.listdir(self.ca_path)
    l.sort()
    for e in l:
      if re.match("(part.*)\.pem", e) != None:
        self.cert.append(X509.load_cert(self.ca_path + e))
    self.acert = X509.load_cert(self.ca_path + 'arbiter.pem')
    self.akey  = RSA.load_key(self.ca_path + 'arbiter.key')
    self.loaded |= 2

  def round_encrypt(self, text):
    self.load_pub()
    uid  = str(uuid.uuid4())
    text = uid+"\n"+text
    for cert in self.cert:
      pad = m2.no_padding
      if len(text) != 128:
        pad = m2.pkcs1_padding
      while True:
        try:
          text = cert.get_pubkey().get_rsa().public_encrypt(text, pad)
        except:
          pass
        finally:
          break
    md = EVP.MessageDigest('sha1')
    md.update(text)
    md = md.final()
    sign = self.akey.sign(md, 'sha1')
    return { 'uuid' : uid, 'evp' : base64.b64encode(text+sign) }

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
      while True:
        try:
          enc = key.private_decrypt(enc, pad)
        except:
          pass
        finally:
          break
    while True:
      try:
        enc = self.keys[-1].private_decrypt(enc, m2.pkcs1_padding)
      except:
        pass
      finally:
        break
    return enc

  def sign_vote(self, evp, vote, date):
    self.load_pub()
    md = EVP.MessageDigest('sha1')
    md.update(evp)
    md.update(str(vote))
    md.update(str(date))
    md = md.final()
    sign = self.akey.sign(md, 'sha1')
    return base64.b64encode(sign)

  def check_vote(self, evp, vote, date, sign):
    self.load_keys()
    md = EVP.MessageDigest('sha1')
    md.update(evp)
    md.update(str(vote))
    md.update(str(date))
    md = md.final()
    return self.akey.verify(md, base64.b64decode(sign))

if __name__ == '__main__':
  import time

  e = eVoteGEN()
  enc = e.round_encrypt("13\n16\n1\n")
  print "Enveloped:", enc['evp']
  print "Decrypted:\n-------------\n", e.round_decrypt(base64.b64decode(enc['evp'])), "-------------"
  date  = time.time()
  svote = e.sign_vote(enc['evp'], 16, date)
  print e.check_vote(enc['evp'], 16, date, svote)

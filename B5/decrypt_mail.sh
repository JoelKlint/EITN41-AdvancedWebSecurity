# Verify email
openssl cms -decrypt -inkey keyreceiver.pem -in mail1.msg | openssl cms -digest_verify

# See email subject
openssl cms -decrypt -inkey keyreceiver.pem -in mail1.msg


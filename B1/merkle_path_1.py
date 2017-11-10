import hashlib

file = open("merkle_1_input.txt", "r", encoding='utf-8')

prev_digest = ""
for i in enumerate(file):
    index = i[0]
    string = i[1].strip()

    if index == 0:
        prev_digest = string
    else:
        direction = string[0]
        string = string[1:]
        concat_string = string + prev_digest if direction == "L" else prev_digest + string
        prev_digest = hashlib.sha1(bytearray.fromhex(concat_string)).hexdigest()

print(prev_digest)
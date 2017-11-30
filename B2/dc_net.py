def hex_to_binary_string(hex):
    return bin(int(hex, 16))[2:].zfill(16)

def binary_string_to_hex(binary):
    return hex(int(binary, 2))[2:].zfill(4).upper()

def did_not_pay_for_meal(conf):
    return conf["SA"]^conf["SB"]

def did_pay_for_meal(conf):
    return 1 - did_not_pay_for_meal(conf)

def calculate_output(conf):
    SA = hex_to_binary_string(conf["SA"])
    SB = hex_to_binary_string(conf["SB"])
    DA = hex_to_binary_string(conf["DA"])
    DB = hex_to_binary_string(conf["DB"])
    M = hex_to_binary_string(conf["M"])

    our_broadcast_binary = ""

    should_send_message = conf["b"]

    for i in range(16):
        conf_i = {
            "SA": int(SA[i]),
            "SB": int(SB[i]),
            "DA": int(DA[i]),
            "DB": int(DB[i]),
            "M": int(M[i])
        }

        # Construct out broadcasted message
        XOR = conf_i["SA"]^conf_i["SB"]
        if should_send_message:
            our_broadcast_i = XOR^conf_i["M"]
        else:
            our_broadcast_i = XOR

        our_broadcast_binary += str(our_broadcast_i)
    
    our_broadcast = binary_string_to_hex(our_broadcast_binary)
    # print("Our broadcast: {}".format(our_broadcast))

    if not should_send_message:
        secret_message_binary = ""
        for i in range(16):
            conf_i = {
                "WE": int(our_broadcast_binary[i]),
                "DA": int(DA[i]),
                "DB": int(DB[i]),
            }

            XOR = conf_i["WE"]^conf_i["DA"]^conf_i["DB"]
            secret_message_binary += str(XOR)
        secret_message = binary_string_to_hex(secret_message_binary)
        # print("Secret message: {}".format(secret_message))
        return our_broadcast + secret_message
    else:
        return our_broadcast



conf_1 = {
    "SA": "0C73",
    "SB": "80C1",
    "DA": "A2A9",
    "DB": "92F5",
    "M": "9B57",
    "b": 0
}
conf_2 = {
    "SA": "27C2",
    "SB": "0879",
    "DA": "35F6",
    "DB": "1A4D",
    "M": "27BC",
    "b": 1
}
conf_quiz = {
    "SA": "DA12",
    "SB": "5050",
    "DA": "C826",
    "DB": "4264",
    "M": "ADE4",
    "b": 1
}
a = calculate_output(conf_quiz)
print(a)

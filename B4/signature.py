import requests
import time
import math
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def send_request(name, grade, signature):
    url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name={}&grade={}&signature={}".format(name, grade, signature)
    return requests.get(url, verify=False)

def all_chars():
    return "0123456789abcdef"

def cheat_for_cousin(name, grade):
    signature = ""

    response_times = []
    response_times.append(send_request(name, grade, signature).elapsed.microseconds)
    print("Initial response time: {}s".format(round(response_times[-1]/1000000, 2)))    

    continous_failed_iterations = 0

    while(len(signature) < 20):

        print()

        if continous_failed_iterations > 2:
            print("Removing last letter from signature")
            print("Signature: {}".format(signature))
            signature = signature[:-1]
            response_times = response_times[:-1]
            continous_failed_iterations = 0
            continue

        letter = None
        largest_time_diff = 0

        start_time = time.time()

        for char in all_chars():
            response = send_request(name, grade, signature + char)
            response_time = response.elapsed.microseconds
            response_time_addition = response_time - response_times[-1]

            # print("Char: {}\ttime added: {}".format(char, response_time_addition))
            if response_time_addition > largest_time_diff:
                largest_time_diff = response_time_addition
                letter = char
                response_times.append(response_time)

        # Append the letter that was the best
        if letter != None:
            signature += letter
            print("Adding char: {}".format(letter))
            print("Added response time: {}s".format(round(largest_time_diff/1000000, 2)))
            print("Current signature: {}".format(signature))
        else:
            continous_failed_iterations += 1
        
        end_time = time.time()
        iteration_time = round(end_time - start_time, 2)
        print("Iteration time: {}s".format(iteration_time))

    print("_____Created a signature!_____")
    response = send_request(name, grade, signature)
    print("Response from server: {}".format(response.text))
    print("Signature: {}".format(signature))

cheat_for_cousin("Micaela", 5)

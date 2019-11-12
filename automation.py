from groundstation.backend_api.communications import CommunicationList
import json

def main():
    sender = CommunicationList()
    fail = True
    while fail:
        fail = False
        seq = input("Enter file name: ")
        test = seq.split(".")
        if len(test) != 2:
            print("Invalid file name. Must be like file.txt")
            fail = True
        elif test[1] != "txt":
            print("Invalid file type. Must be .txt")
            fail = True

    f = open(seq, "r")

    for line in f:
        line = line.strip("\n")
        pieces = line.split(",")
        message = {
            'command': pieces[0],
            'sender': pieces[1],
            'receiver': pieces[2]
        }

        print(line, message)

        message = json.dumps(message)

        sender.post(local_data=message)

main()
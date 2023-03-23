from huskylens import Huskylens, COMMAND_PING, COMMAND_FORGET, COMMAND_ALGORITM_COLOR_RECOGNITION, COMMAND_LEARNED, COMMAND_LEARN

HUSKYLENS_SERIALNO = "AB0O5A7Z"

huskylens = Huskylens(None, None, HUSKYLENS_SERIALNO)

response = huskylens.command(command = COMMAND_PING)
print(response)
response = huskylens.command(command = COMMAND_FORGET)
print(response)
response = huskylens.command(command = COMMAND_LEARN, id=1)
print(response)

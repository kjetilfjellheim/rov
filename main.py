from huskylens import Huskylens, COMMAND_PING, COMMAND_FORGET, COMMAND_ALGORITHM_COLOR_RECOGNITION, COMMAND_LEARN, COMMAND_SCREESNSHOT, COMMAND_SAVE_PICTURE, COMMAND_ARROWS_BY_ID

HUSKYLENS_SERIALNO = "AB0O5A7Z"

huskylens = Huskylens(None, None, HUSKYLENS_SERIALNO)

response = huskylens.command(command = COMMAND_PING)
print(response.success)
response = huskylens.command(command = COMMAND_FORGET)
print(response.success)
response = huskylens.command(command = COMMAND_ALGORITHM_COLOR_RECOGNITION)
print(response.success)
response = huskylens.command(command = COMM)
print(response.success)
response = huskylens.command(command = COMMAND_LEARN, id = 1)
print(response.success)
response = huskylens.command(command = COMMAND_SCREESNSHOT)
print(response.success)
response = huskylens.command(command = COMMAND_SAVE_PICTURE)
print(response.success)
response = huskylens.command(command = COMMAND_ARROWS_BY_ID, id = 1)
print(response.success)
print(response.numberOfElements)
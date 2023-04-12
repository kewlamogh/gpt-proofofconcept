import os  # used for most things related to the computer
import openai  # openai is a library by the company OpenAI and it allows you to use ML models
import hashlib  # hashlib is a library that is used for hashing
from replit import db  # simple Replit database

directory = 'logs'  # sets which directory to iterate through
logs = []  # defining the log list
# comment
# comment 3

# iterates through the items in the directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)  # creates the path of the object
    file = open(f, 'r')  # opens up the file, with mode 'r' (read mode)
    logs.append(file.read())  # appends the contents of that file to logs

# assigns the API key to the library's variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# creating a hasher that hashes from a string to sha256
h = hashlib.new('sha256')
msgs_hash = "\n".join(logs)  # joining the log list together with a newline
h.update(msgs_hash.encode())  # creates the hash
msgs_hash = h.hexdigest()  # makes the hash a string

if msgs_hash in db:  # checks if msgs_hash is in db
  print(db[msgs_hash])  # if so, prints it out
else:
  completion = openai.ChatCompletion.create(
      # specifies the model that we want to use, in this case GPT 3.5 Turbo
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": f"Return this in a  {ch}"}
                for ch in logs]
  )  # creating the API model and giving it messages

  completion = openai.ChatCompletion.create(
      # specifies the model that we want to use, in this case GPT 3.5 Turbo
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": f"Understand these logs and diagnose a problem and a solution, also using the logs previously given. {ch}"} for ch in logs]
  )  # creating the API model and giving it messages

  response = completion.choices[0].message.content
  db[msgs_hash] = response
  print(response)  # prints the response

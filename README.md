# CS361_Credential_Fetcher
CS361 Bank Credential API

#How To use#

Start the server by running python ./fetcher.py
The test script can be used by running a command of the following form:

python test.py <User_ID> <Token> <host> <port(if not 8000)>

For example on how to request data: 

python test.py 1 token1

returns a JSON and a HTTP status code (defined in fetcher.py): 

Name:     Alice
Account:  ACCT123
Password: password123

UML Sequence Diagram of Bank Credential Fetcher:

<img width="442" height="373" alt="UML_SEQ drawio" src="https://github.com/user-attachments/assets/6c912abb-3525-497a-bf92-a2cbaba0e322" />

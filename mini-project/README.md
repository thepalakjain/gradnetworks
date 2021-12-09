LOCAL COMPUTER:
	1. To get a list of 15 hashes of randomly chosen passwords, run 
		$ python generate-hashes.py 
	2. On a new terminal, start the web server 
		$ python3 http-server.py
	3. On a new terminal, start the manager
		$ python manager.py
	4. Start as many worker nodes as desired on new terminals
		$ python worker.py
	5. submit the 15 generated hashes from step 1 to the open webpage one by one, looking at the server terminal to make sure each one is cracked before you send the next input.

GENI

	1. Use generate-hashes.py on your local machine to get a list of 15 hashes of randomly chosen passwords

	2. Reserve resources on GENI
		use reserve.rspec

	3. Get files
		ssh into manager node and retrieve:
		$ wget https://raw.githubusercontent.com/thepalakjain/gradnetworks/main/mini-project/manager.py
	
		ssh into server node and retrieve:
		$ wget https://raw.githubusercontent.com/thepalakjain/gradnetworks/main/mini-project/http-server.py
		$ https://raw.githubusercontent.com/thepalakjain/gradnetworks/main/mini-project/index.html

		ssh into each of the 5 worker nodes and retrieve:
		$ wget https://raw.githubusercontent.com/thepalakjain/gradnetworks/main/mini-project/worker.py

	4. Open the python files on each of the nodes and replace the HOST values with the IP addresses of the relevant machines as found on GENI. If you look at the details of your slice on GENI, you can find the IP address of the nodes.

	5. Run the code like you would on a local machine.

GENI FASTER option

	1. generate hashes and reserve resources as in the previous case

	3. Get files
		ssh into manager node and retrieve:
		$ wget https://raw.githubusercontent.com/thepalakjain/gradnetworks/main/mini-project/manager_without_server.py

		ssh into each of the 5 worker nodes and retrieve:
		$ wget https://raw.githubusercontent.com/thepalakjain/gradnetworks/main/mini-project/worker.py

	4. Open the python files on each of the worker nodes and replace the HOST values with the IP address of the manager as found on GENI.

	5. On the manager node, run:
		$ python manager_without_server.py
		when asked for the number of workers, provide a number between 1 and 5

	6. On the number of worker nodes provided above, run:
		$ python worker.py

	7. The results will be printed on the manager node when ready.

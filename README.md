Consistent Hashing :

	With ever increasing activity on the web , people realized they needed more and more machines to serve the information quickly and efficiently.
	But no one can be sure how many servers one may require.
	The requirement of servers is ever increasing.

	But how to manage data so that no one server get too much load.
	This is known as load balancing.
		i.e, to distribute data loads between the machines so that all of them are utilized efficiently and no single machine get overloaded.

	A simple way to distribute objects among various machines is:
		1. Select the object
		2. Hash it
		3. Send it to the machine : HASH_VAL(KEY) mod NUM_MACHINES

	But what if a machine goes down or a new machine is added.
	In both the cases approximately all the objects need to be Re Hashed and distributed again. (Not efficient)
		The percentage of obects re-mapped in both cases is (NUM_MACHINES / (NUM_MACHINES + 1)) * 100 ~ 100%.

	This led to the more efficient Consistent Hashing.
	In Consistent Hashing if a machine goes down or a new machine is added the number of keys re-mapped is:
		NUM_OBJECTS / NUM_MACHINES,
	which is much more effiecient then normal mapping.


Consistent Hash Ring Implementation :

	The implementation of Hash Ring is simple and straight forward :
		1. Add Machines => O(log(NUM_MACHINES)) using dictionary lists and maintaing them in sorted order.
		2. Remove Machine => O(log(NUM_MACHINES)) using the same and binary search on hashed Values.
		3. Add Object => O(log(NUM_MACHINES)) using binary search on machines hash value to get the INDEX of machine greater than the objects hash value.
		4. Hashing => sha256 converted to float values between [0,1) to lie on a circle ring.
		
	Syntax : 
		1. add "Key Name" => add key with value "Key Name"
		2. new => create a new machine.
		3. del "Machine Index" => delete machine with given index.
		4. exit => exit console.

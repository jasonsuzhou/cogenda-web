Cogenda Web
===========

- Install pip.

	```
	$ sudo easy_install pip
	```

- Install virtualenv and build dependencies.

	```
	$ pip install virtualenv
	$ ./setenv.sh
	```

- SQLite db migration

    ```
    $ make script 'eg. add new table/column'
    $ make upgrade
    $ make version
    ```

- Start server

	```
	$ make run
	```
> Open url http://localhost:8088

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
    $ make sync
    $ make version
    ```

- Babel I18n
	
    ```
    $ make babel-extract
    ``` 
    > If you added new i18n message in *.py or *.html, this command will collect the i18n message, put into message.pot

    ```
    $ make babel-update
    ```
    > After message.pot updated, this command will sync the new i18n message into en/zh *.po files.

    ```
    $ make babel-compile
    ```
    > After *.po file modified by dev, this command will compile the *.po to *.mo for application use.

- Start server

	```
	$ make run
	```
> Open url http://localhost:8088

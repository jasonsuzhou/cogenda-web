	   ______                                __          _       __       __  
	  / ____/____   ____ _ ___   ____   ____/ /____ _   | |     / /___   / /_ 
	 / /    / __ \ / __ `// _ \ / __ \ / __  // __ `/   | | /| / // _ \ / __ \
	/ /___ / /_/ // /_/ //  __// / / // /_/ // /_/ /    | |/ |/ //  __// /_/ /
	\____/ \____/ \__, / \___//_/ /_/ \__,_/ \__,_/     |__/|__/ \___//_.___/ 
	             /____/                                                       

===========

- Preparation: Install pip, virtualenv and dependency libs.

	```
	$ sudo easy_install pip
	$ pip install virtualenv
	$ ./setenv.sh
	$ source venv/bin/activate
	```

- SQLite migration

    ```
    $ make script 'eg. add new table/column'
    ```
    >  When create or update model, we need to run this command to generate schema version file. Under migration/version folder, then we need to edit generated file for db changes.

    ```
    $ make sync
    ```
    > Once we finished edit the db version file, use this command to sync with SQLite.

    ```
    $ make version
    ```
    > Run this command to verify current database schema version.

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

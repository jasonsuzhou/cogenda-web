	   ______                                __          _       __       __  
	  / ____/____   ____ _ ___   ____   ____/ /____ _   | |     / /___   / /_ 
	 / /    / __ \ / __ `// _ \ / __ \ / __  // __ `/   | | /| / // _ \ / __ \
	/ /___ / /_/ // /_/ //  __// / / // /_/ // /_/ /    | |/ |/ //  __// /_/ /
	\____/ \____/ \__, / \___//_/ /_/ \__,_/ \__,_/     |__/|__/ \___//_.___/ 
	             /____/                                                       

[![Build Status](https://travis-ci.org/cogenda/cogenda-web.svg?branch=master)](https://travis-ci.org/cogenda/cogenda-web)

---

- Preparation: Install pip, virtualenv and dependency libs.

    ```
    $ sudo easy_install pip
    $ pip install virtualenv
    $ ./setenv.sh
    $ source venv/bin/activate
    $ brew install node
    $ make web
    ```

- Start Web Server

    ```
    $ make db-init (optional: If migration/cogenda-app.db not create yet)
    $ make run
    ```
    > Open url http://localhost:8088

- SQLite Migration

    ```
    $ make db-init
    ```
    > Initial SQLite database file under migration/ folder.

    ```
    $ make db-script 'eg. add new table/column'
    ```
    >  When create or update model, we need to run this command to generate schema version file. Under migration/version folder, then we need to edit generated file for db changes.

    ```
    $ make db-migrate
    ```
    > Once we finished edit the db version file, use this command to sync with SQLite.

    ```
    $ make db-version
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
    > This command combined babel-extract, then will sync the new i18n message into en/zh *.po files.

    ```
    $ make babel-compile
    ```
    > After *.po file modified by dev, this command will compile the *.po to *.mo for application use.

- Web assets optimizing

    ```
    make web
    ```
    > Optimize web static files.

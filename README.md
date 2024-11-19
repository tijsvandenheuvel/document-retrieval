# document-retrieval

## setup

### 1. Download the repository

On [this page](https://github.com/tijsvandenheuvel/document-retrieval)

click the green ` < > Code ▾ ` Button

click Download ZIP

Extract the zip file

### 2. Install python (on mac)

Here you can find [a very basic introduction video on the mac Terminal](https://www.youtube.com/watch?v=18xmmGiIIwU)

Note: you can use the up and down arrow keys to select earliers commands.

#### 2.1 Check if it is allready installed

In the Terminal, run this command to check if python is already installed:

`python3 --version`

#### 2.2 Install the [Homebrew package manager](https://brew.sh/)

This is a package manager for macOS. It allows you to install and manage software packages easily.

In the Terminal, run this command: 

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

#### 2.3 Install python

In the Terminal, run this command:

`brew install python`

check installation with

`python3 --version`

### 3. Setup environment

#### 3.1 navigate to project

Open the project in the Terminal

You can navigate to the project folder using the `cd` and `ls` commands.

You can also right-click the folder and click `New Terminal at Folder`

### 4. Run the code

in `open_search_database` run thhis command in terminal

`sh install.sh`

to start monitoring the documents run

`sh monitor.sh`

to start the query app

`sh run.sh`

### 5. Next steps

- setup a document database 
- compare different document retrieval methods
- create a nice interface to interact with the database
# DataBase project
 
This project was realized for the Master Data Science's course Databases teached by Sylvain Salvati (2022).

You will find a file untitled requirements.txt, feel free to use it to make sure  that you have all the required libraries installed on your python interpreter. 

Here is a small summary that can help you to avoid being confused by
the different folders you will go through :
-  data → a go-to folder for any type of external data. Currently only containing
a python file with the film database furnished.
- etc → a go-to folder for any type of configuration file. Currently only con-
taining an YML format file that I recommend you to modify to hard-code the
root directory absolute path on your local machine (you’ll need to do it to be
able to launch tests).
- examples → folder filled with multiple kind of ready-to-launch examples on
several classes, functions, methods and etc. Feel free to use them to acquire a
better (and faster) understanding of this repository.
- old → outdated files once useful but that are no longer used, still kept in order
to be retrieved if necessary.
- src → main folder of this repository containing the major part of the work
done and several sub-folders.
- tests → testing repository, containing multiple tests on several parts of the
code. 

We used the testing framework Pytest for this project. All tests can be
run at once using the following command in a shell <strong>pytest -v</strong> (either from the
root directory or the tests/ directory).
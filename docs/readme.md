## create virtual environment on ubuntu
 
1. `sudo apt install python3-venv`
2. `python3 -m venv [venv-name]`
3. `source venv/bin/activate`
4. which python - to check if the venv is activated 
[output]: /home/kennedy-anyidoho/devmode/python/python-pastebin/venv/bin/python
5. add a .gitignore file in the venv folder and put * in it for git to ignore everything in that dir
6. install fastAPI - `pip install "fastapi[standard]"`
7. create a main.py file in the roor of your directory and run `python main.py`
8 you can deactivate the venv after you are done with your work - `deactivate`

# coen281-proj

## Steps to run the project

### Step 0
Create a copy of of ```./coen281/.env.default``` file in the same directory and name it as ```.env```.
Update the ```.env``` file to reflect necessary keys for Twitter developer account.

### Step 1
Install all dependencies given in ```requirements.txt```

### Step 2
Create a database in mysql called ```coen281```

### Step 3
Add mysql credentials in ```./coen281/coen281/settings.py``` file at ```Line 82```

### Step 4
Run ```$ python ./coen281/manage.py migrate```

### Step 5
Run stages 1 through 4 ( IN SEPERATE SHELLS ) as follows:
```
$ python ./coen281/manage.py stage_1 --num_tweets=100
$ python ./coen281/manage.py stage_2
$ python ./coen281/manage.py stage_3_1
$ python ./coen281/manage.py stage_3_2
$ python ./coen281/manage.py stage_4
```
### Step 6
Run stage 5 in a new shell as follows
```
$ python ./coen281/manage.py runserver 8000
```
### Step 7
Open link [http://127.0.0.1:8000/app/](http://127.0.0.1:8000/app/) in a browser to see the dashboard interface
#### Note:
The overall statistics are refreshed after every 5 seconds while author statistics are updated every 10 seconds

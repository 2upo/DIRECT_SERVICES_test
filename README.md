# Weather Service (Direct Services test task)

### Prerequisites
- Python3.8+
- Docker Engine (>= 20.10.22)
- docker-compose (>= 1.29.1)
- OS: Linux or Windows

Steps to run all 5 tasks:

### Task 1

0. DO NOT cd inside `task1/` folder.
1. Create virtual env: `python3 -m venv task1/venv && source task1/venv/bin/activate`
2. Install requiremets: `pip install -r task1/requirements.txt`
3. Paste `75a4824b5333b04{{{{{{{{{{{75151a799dbafebd0` API KEY to `task1/configuration.ini` (**Important: REMOVE {{{{{{{{{{{ from API KEY BEFORE PASTING**)  

Next you have different options to choose:
- `python -m task1` will display weather info for **5 random cities**.
- `python -m task1 -city <cityname>` if you replace **<cityname>** with e.g. Sofia, will display weather **for given city**.
- `python -m task1 -h` will display help.

Example usage:
    
![image](https://github.com/2upo/DIRECT_SERVICES_test/assets/66561266/e69c69fd-a167-4d7e-8458-509e89f436ea)

### Task 2

0. DO NOT cd inside `task2/` folder.
1. Create virtual env: `python3 -m venv task2/venv && source task2/venv/bin/activate`
2. Install requiremets: `pip install -r task2/requirements.txt`
3. Paste `75a4824b5333b04{{{{{{{{{{{75151a799dbafebd0` API KEY to `task2/configuration.ini` (**Important: REMOVE {{{{{{{{{{{ from API KEY BEFORE PASTING**)  
4. Run program with command: `python -m task2`

Example usage:
    
![image](https://github.com/2upo/DIRECT_SERVICES_test/assets/66561266/9b8e2a70-f389-459e-a9e9-275de13f347c)


### Task 3
0. **CD** inside `task3/` folder.

1. Create file `.env`: 
    ```
       API_KEY = 75a4824b5333b04{{{{{{{{{{75151a799dbafebd0 # <- Remove {{{{{{{{ here
       URL="https://api.openweathermap.org/data/2.5/weather"
    ```
    (**Important: REMOVE {{{{{{{{{{{ from API KEY BEFORE PASTING**)
2. Run `docker-compose up --build`.
3. Open [localhost:80](http://localhost:80).

Example usage for task 3,4:
                                                                 
 ![image](https://github.com/2upo/DIRECT_SERVICES_test/assets/66561266/793c29e4-4892-46ae-924f-a68569b62ea8)

 ![image](https://github.com/2upo/DIRECT_SERVICES_test/assets/66561266/d18e5976-1516-4cf2-af2e-53d138477fd7)


### Task4
0. **CD** inside `task4/weather_project` folder.

1. Create file `.env`: 
    ```
       API_KEY = 75a4824b5333b04{{{{{{{{{{75151a799dbafebd0 # <- Remove {{{{{{{{ here
       URL="https://api.openweathermap.org/data/2.5/weather"
    ```
    (**Important: REMOVE {{{{{{{{{{{ from API KEY BEFORE PASTING**)
2. Run `docker-compose up --build`.
3. Open [localhost:80](http://localhost:80).

### Task5
0. **CD** inside `task3/` folder.

1. Create file `.env`: 
    ```
       API_KEY = 75a4824b5333b04{{{{{{{{{{75151a799dbafebd0 # <- Remove {{{{{{{{ here
       URL="https://api.openweathermap.org/data/2.5/weather"
    ```
    (**Important: REMOVE {{{{{{{{{{{ from API KEY BEFORE PASTING**)
2. `docker-compose run -w "/usr/src/app" app flask db upgrade`
3. `docker-compose up --build`      
4. Open [localhost:80](http://localhost:80).

Example usage:

![image](https://github.com/2upo/DIRECT_SERVICES_test/assets/66561266/53000178-75d4-4fe3-bd87-f6014b2010d7)

![image](https://github.com/2upo/DIRECT_SERVICES_test/assets/66561266/05efa4f9-6b02-48e5-840f-6d9ca285c4d0)
                                                                 

#  Junior SysAdmin Task
                                                                 
1. `netstat -tna | grep ':80.*ESTABLISHED' | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr`
2. `for ip in $(netstat -tna | grep ':80.*ESTABLISHED' | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -nr | head -n 5 | awk '{print $2}'); do iptables -A INPUT -s $ip -j DROP; done` 
3. `grep "12/May/2023" /var/log/apache2/access.log | awk '{print $1}' | sort | uniq -c | sort -nr`
4. `hdparm -i /dev/sda | grep Model | awk '{print $3" "$4" "$5" "$6" "$7" "$8}'; hdparm -i /dev`
5. `mysqldump -u <username> -p<password> <database_name> > dump.sql`
6.  `mysql -u <username> -p<password> -h <host> <database_name> < dump.sql`
7. `find . -maxdepth 3 -name "*.tar.gz" -type f -delete`
8. За да спрете mysqld, може да използвате команда kill -9 <pid> където <pid> е идентификаторът на процеса на mysqld. Тази команда е крайно средство и ще прекъсне процеса незабавно без да предостави възможност за запис на диска на отворените данни. В случай че имате информация, която трябва да бъде записана на диска, е по-добре да използвате командата /etc/init.d/mysqld stop, която ще спре процеса, като позволи на MySQL да записва данните на диска преди да го спре. Ако нито една от тези команди не работи, може да използвате командата killall mysqld, която ще прекрати всички процеси на mysqld.

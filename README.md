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


### Task 2

0. DO NOT cd inside `task2/` folder.
1. Create virtual env: `python3 -m venv task2/venv && source task2/venv/bin/activate`
2. Install requiremets: `pip install -r task2/requirements.txt`
3. Paste `75a4824b5333b04{{{{{{{{{{{75151a799dbafebd0` API KEY to `task2/configuration.ini` (**Important: REMOVE {{{{{{{{{{{ from API KEY BEFORE PASTING**)  
4. Run program with command: `python -m task2`

Example usage:


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

Example usage for task 3,4,5:

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


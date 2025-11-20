# Testing MOBILE UI using mocked mobile session on 

# Testing API's on Mocked streaming server on http://127.0.0.1:8082 

## See .env for urls

## Instalation(for mac/linux):

1. Install Python 3.12
2. install pip
3. Run(install virtual env)
   python3 -m venv .venv
   source .venv/bin/activate
4. pip install -r requirements.txt
5. brew install allure(for mac only)
6. run chmod +x /run_tests_and_report_allure.sh

## Run Tests and report Allure report:
./run_tests_and_report_allure.sh


The framework supports:

1)retries on failed api calls
2)Allure reporting
3)Friendly for ci by pytest.ini & .env
4)BaseSession abstract class to share functionality on mobile and api sessions

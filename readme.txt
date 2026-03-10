#create venv
python3 -m venv .venv
# start venv
source .venv/bin/activate
# save current requirements
pip freeze > requirements.txt
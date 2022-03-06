# Crear el entorno para ejecutarlo

conda create --name rasa python=3.8

conda active rasa

python -m pip install --upgrade pip

conda install ujson

conda install tensorflow

pip install rasa

pip install spacy

python -m spacy download es_core_news_md

pip install unidecode

pip install -U numpy (da error pero funciona)

# Comandos útiles

conda activate rasa

rasa shell

rasa run actions

docker run - p 8000:8000 rasa/duckling
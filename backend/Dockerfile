FROM python:3

# Dodaj niestandardowego użytkownika
RUN groupadd -r myuser && useradd -r -g myuser myuser

# Ustaw katalog roboczy
WORKDIR /backend

# Zmień właściciela katalogu roboczego
# RUN chown -R myuser:myuser /backend

# Skopiuj zawartość aktualnego katalogu do katalogu roboczego w kontenerze
COPY . /backend

# RUN pip install --no-cache-dir -r algorithm_running/requirements_run.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir numpy

# Zmień właściciela skopiowanych plików
RUN chown -R myuser:myuser /backend

# Zmodyfikuj uprawnienia dla katalogu roboczego
RUN chmod -R 755 /backend

# Przełącz się na użytkownika non-root
USER myuser

# Uruchom skrypt Pythona
CMD ["python3", "algorithm_running/ranking_calc.py"]

# CMD id
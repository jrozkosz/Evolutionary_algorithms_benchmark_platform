import subprocess

def run_bandit_on_file(file_path):
    """
    Uruchamia narzędzie Bandit na podanym pliku i zwraca wynik analizy.
    :param file_path: Ścieżka do pliku z kodem Pythona.
    :return: Wynik analizy Bandit w postaci tekstu.
    """
    try:
        # Wywołanie Bandit na pliku
        result = subprocess.check_output(["bandit", "-r", file_path], stderr=subprocess.STDOUT, text=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Błąd podczas uruchamiania Bandit: {e.output}"

def detect_risks(analysis):
    """
        Code scanned:
                Total lines of code: 267
                Total lines skipped (#nosec): 0

        Run metrics:
                Total issues (by severity):
                        Undefined: 0
                        Low: 1
                        Medium: 0
                        High: 0
                Total issues (by confidence):
                        Undefined: 0
                        Low: 0
                        Medium: 0
                        High: 1
        Files skipped (0):
    """
    start_metrics = analysis.find("Total issues (by severity):")
    end_metrics = analysis.find("Total issues (by confidence):")
    metrics = analysis[start_metrics:end_metrics]
    for line in metrics.splitlines():
        if 'Low' in line and int(metrics[metrics.find('Low')+5]) != 0:
            print(metrics[metrics.find('Low')+5])
            print("We got a problem!")

if __name__ == "__main__":
    user_code_file = "algorithm.py"  # Wprowadź ścieżkę do pliku z kodem użytkownika
    analysis_result = run_bandit_on_file(user_code_file)
    print(analysis_result)
    detect_risks(analysis_result)

import bandit
from bandit.core import manager as b_manager

def scan_code_for_security(code):
    # Inicjalizacja menedżera Bandit
    manager = b_manager.BanditManager()

    # Przekazanie kodu do zeskanowania
    manager.b_ts.add_string(code)

    # Uruchomienie skanowania
    manager.run()

    # Pobranie wyników skanowania
    issues = manager.get_issue_list()

    return issues

if __name__ == "__main__":
    # Przykładowy kod do zeskanowania
    user_code = """
    import os
    os.system("rm -rf /")
    """

    # Przeskanowanie kodu
    security_issues = scan_code_for_security(user_code)

    if security_issues:
        print("Znaleziono następujące problemy z bezpieczeństwem:")
        for issue in security_issues:
            print(issue)
    else:
        print("Brak problemów z bezpieczeństwem.")

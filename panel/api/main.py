from fastapi import FastAPI, Form
import subprocess
import pwd
import uvicorn

app = FastAPI(title="User Password API")

def has_login_shell(username: str) -> bool:
    try:
        pw = pwd.getpwnam(username)
        shell = pw.pw_shell or ""
        # jeśli shell to coś innego niż /bin/false lub /usr/sbin/nologin -> traktujemy jako "login shell"
        return shell not in ("/bin/false", "/usr/sbin/nologin", "")
    except KeyError:
        return False

@app.post("/change_password")
def change_password(username: str = Form(...), old_password: str = Form(None), new_password: str = Form(...)):
    try:
        # czy istnieje user
        try:
            pw = pwd.getpwnam(username)
        except KeyError:
            return {"status": "error", "message": "Nie ma takiego użytkownika"}

        if has_login_shell(username):
            # użytkownik ma powłokę loginową -> wymagamy starego hasła i weryfikujemy je
            if not old_password:
                return {"status": "error", "message": "Trzeba podać stare hasło dla tego konta"}
            check = subprocess.run(
                ["su", "-", username, "-c", "true"],
                input=f"{old_password}\n",
                text=True,
                capture_output=True
            )
            if check.returncode != 0:
                return {"status": "error", "message": "Nieprawidłowe stare hasło"}

        # wykonujemy zmianę hasła (dla obu typów kont)
        subprocess.run(
            ["sudo", "chpasswd"],
            input=f"{username}:{new_password}\n",
            text=True,
            check=True
        )

        return {"status": "ok", "message": "Hasło zostało zmienione pomyślnie"}

    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Błąd systemowy: {e}"}
    except Exception as e:
        return {"status": "error", "message": f"Wystąpił błąd: {e}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)

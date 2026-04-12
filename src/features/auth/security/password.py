import bcrypt


class PasswordManager:
    def hash_password(self, password: str) -> str:
        pw_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(pw_bytes, salt)
        return hashed.decode("utf-8")

    def verify_password(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

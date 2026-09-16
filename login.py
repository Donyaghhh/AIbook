# Simple command-line login.
set -euo pipefail
MAX_ATTEMPTS=3
hash_password() {
  local password="$1"
  printf '%s' "$password" | sha256sum | awk '{print $1}'
}
ADMIN_HASH="$(hash_password "admin123")"
GUEST_HASH="$(hash_password "guest123")"
check_credentials() {
  local username="$1"
  local password="$2"
  local stored=""
  local given
  given="$(hash_password "$password")"
  case "$username" in
    admin) stored="$ADMIN_HASH" ;;
    guest) stored="$GUEST_HASH" ;;
    *) return 1 ;;
  esac
  [[ "$given" == "$stored" ]]
}

login() {
  echo "=== Login ==="
  local attempt username password remaining
  for ((attempt = 1; attempt <= MAX_ATTEMPTS; attempt++)); do
    read -r -p "Username: " username
    read -r -s -p "Password: " password
    echo
    if check_credentials "$username" "$password"; then
      echo "Welcome, ${username}."
      return 0
    fi
    remaining=$((MAX_ATTEMPTS - attempt))
    if ((remaining > 0)); then
      echo "Invalid username or password. ${remaining} attempt(s) left."
    else
      echo "Invalid username or password. Too many failed attempts."
    fi
  done
  return 1
}
login

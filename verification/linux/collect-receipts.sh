#!/bin/sh
# Frost-Sec-Home Linux look-only receipts collector.
# Runs inside an ubuntu container. LOOK-ONLY commands only; the one exception
# is `apt-get -s upgrade` (simulation, changes nothing) and package INSTALLS
# needed to syntax-check tool commands, clearly labeled. No model behavior
# is tested here.
set -u
echo "# container identity"
cat /etc/os-release | head -2
echo "kernel: $(uname -r)"
echo

run() {
  echo "## $*"
  out=$("$@" 2>&1); ec=$?
  printf '%s\n' "$out" | head -12
  echo "exit=$ec"
  echo
}

echo "=== BASE IMAGE (tools may be absent — absence receipts) ==="
run ip addr
run ip neigh
run ss -tulpn
run crontab -l
run ufw status
run clamscan --version
run hostname -I
run cat /etc/hosts
run tail -5 /root/.bashrc
run ls -la /root/.config/autostart
run systemctl list-unit-files --state=enabled
run apt-get -s upgrade

echo "=== INSTALL tooling for syntax verification (labeled change, container-only) ==="
apt-get update -qq >/dev/null 2>&1
apt-get install -y -qq iproute2 cron ufw clamav >/dev/null 2>&1
echo "install exit=$?"
echo

echo "=== WITH TOOLS INSTALLED ==="
run ip addr
run ip neigh
run ss -tulpn
run crontab -l
run ufw status
run clamscan --version
run systemctl list-unit-files --state=enabled
run apt-get -s upgrade

echo "=== freshclam signature update (container-only, labeled network download) ==="
out=$(timeout 120 freshclam 2>&1); ec=$?
printf '%s\n' "$out" | tail -6
echo "freshclam exit=$ec"
echo

echo "=== clamscan exit-code behavior on synthetic files ==="
mkdir -p /root/scan-demo
printf 'hello world\n' > /root/scan-demo/clean.txt
# EICAR standard test string — the industry-standard harmless AV test file.
printf 'X5O!P%%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*' > /root/scan-demo/eicar.txt
out=$(clamscan -r -i /root/scan-demo/clean.txt 2>&1); ec=$?
printf '%s\n' "$out" | grep -E "Infected files|Scanned"
echo "clean-file exit=$ec"
out=$(clamscan -r -i /root/scan-demo/eicar.txt 2>&1); ec=$?
printf '%s\n' "$out" | grep -E "FOUND|Infected files"
echo "eicar-file exit=$ec"
rm -rf /root/scan-demo
echo "(demo folder removed; container is disposable)"
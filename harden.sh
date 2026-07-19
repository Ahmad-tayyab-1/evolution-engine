#!/bin/bash
set -e

echo "[1/7] Hardening SSH..."
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak
sudo tee /etc/ssh/sshd_config.d/hardened.conf > /dev/null << 'SSHEOF'
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
LoginGraceTime 20
ClientAliveInterval 300
ClientAliveCountMax 2
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no
PermitEmptyPasswords no
SSHEOF
sudo systemctl reload sshd
echo "   SSH hardened."

echo "[2/7] Configuring UFW firewall..."
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp comment 'SSH'
sudo ufw allow 80/tcp comment 'HTTP Dashboard'
sudo ufw --force enable
echo "   UFW active."

echo "[3/7] Configuring fail2ban..."
sudo tee /etc/fail2ban/jail.local > /dev/null << 'F2BEOF'
[DEFAULT]
bantime = 1800
findtime = 600
maxretry = 5
banaction = ufw

[sshd]
enabled = true
port = 22
maxretry = 3
bantime = 3600

[nginx-http-auth]
enabled = true
port = 80
logpath = /var/log/nginx/error.log
maxretry = 5

[nginx-botsearch]
enabled = true
port = 80
logpath = /var/log/nginx/access.log
maxretry = 3
bantime = 86400
F2BEOF

# Custom filter for dashboard login brute force
sudo tee /etc/fail2ban/filter.d/dashboard-login.conf > /dev/null << 'FILTEOF'
[Definition]
failregex = ^<HOST> .* "POST /login HTTP/.*" (303|200)
ignoreregex =
FILTEOF

sudo tee -a /etc/fail2ban/jail.local > /dev/null << 'JAILEOF'

[dashboard-login]
enabled = true
port = 80
filter = dashboard-login
logpath = /var/log/nginx/access.log
maxretry = 5
findtime = 300
bantime = 1800
JAILEOF

sudo systemctl enable fail2ban
sudo systemctl restart fail2ban
echo "   fail2ban active."

echo "[4/7] Kernel network hardening (sysctl)..."
sudo tee /etc/sysctl.d/99-hardened.conf > /dev/null << 'SYSEOF'
# Disable IP source routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.default.accept_source_route = 0

# Disable ICMP redirect acceptance
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0

# Enable SYN flood protection
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 2048
net.ipv4.tcp_synack_retries = 2

# Ignore ICMP broadcasts
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Log suspicious packets
net.ipv4.conf.all.log_martians = 1
net.ipv4.conf.default.log_martians = 1

# Disable IPv6 if not needed
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1

# Protect against time-wait assassination
net.ipv4.tcp_rfc1337 = 1
SYSEOF
sudo sysctl -p /etc/sysctl.d/99-hardened.conf > /dev/null 2>&1
echo "   Kernel hardened."

echo "[5/7] Enabling automatic security updates..."
sudo tee /etc/apt/apt.conf.d/20auto-upgrades > /dev/null << 'AUTOEOF'
APT::Periodic::Update-Package-Lists "1";
APT::Periodic::Unattended-Upgrade "1";
APT::Periodic::AutocleanInterval "7";
AUTOEOF
echo "   Auto-updates enabled."

echo "[6/7] Setting restrictive file permissions..."
sudo chmod 600 /var/www/yt-agent/.env
sudo chmod 600 /var/www/yt-agent/secrets/*
sudo chmod 700 /var/www/yt-agent/secrets
sudo chmod 750 /var/www/yt-agent/db
echo "   Permissions locked."

echo "[7/7] Enabling NGINX access logging for fail2ban..."
sudo tee /etc/nginx/conf.d/logging.conf > /dev/null << 'LOGEOF'
log_format security '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';
access_log /var/log/nginx/access.log security;
LOGEOF
sudo nginx -t && sudo systemctl reload nginx
echo "   Logging configured."

echo ""
echo "=== ALL HARDENING COMPLETE ==="
echo "UFW:        $(sudo ufw status | head -1)"
echo "fail2ban:   $(sudo fail2ban-client status | head -1)"
echo "SSH:        Root disabled, password disabled, max 3 tries"
echo "Sysctl:     SYN flood protection, ICMP hardened, IPv6 disabled"
echo "Auto-updates: Enabled"
echo "File perms: .env(600) secrets/(700) db/(750)"

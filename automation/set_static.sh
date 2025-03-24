sudo nmcli con modify "Wired connection 1" ipv4.addresses 172.22.41.22/24
sudo nmcli con modify "Wired connection 1" ipv4.gateway 172.22.41.1
sudo nmcli con modify "Wired connection 1" ipv4.dns "172.22.41.11,172.22.41.12"
sudo nmcli con modify "Wired connection 1" ipv4.method manual

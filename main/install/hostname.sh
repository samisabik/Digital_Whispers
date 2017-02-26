echo "Setting new hostname..."
echo "=========================="
hostn=$(cat /etc/hostname)
echo "hostname is: $hostn"
echo "enter new hostname: "
read newhost
sed -i "s/$hostn/$newhost/g" /etc/hosts
sed -i "s/$hostn/$newhost/g" /etc/hostname
echo "new hostname: $newhost"
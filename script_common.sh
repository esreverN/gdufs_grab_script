#!/bin/bash
read -p "student number:" username
stty -echo
read -p "password:" password
stty echo

curl -c cookie1.txt -d "USERNAME=$username&PASSWORD=$password" http://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap
curl -b cookie1.txt "http://jxgl.gdufs.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=425DF1EBE9644E6297C4D54B3EAD7A93"

echo "请选择需要选的课程编号："

sed 's/20152016[0-9]*//g' course.dump

read line
declare -a cn

t=0
for i in $line
do
temp=`awk '$1 ~ "^'$i'、" {print $2}' course.dump`
cn[$t]=$temp
t=$(($t+1))
done

while true ; do
for item in ${cn[@]};do
    echo $item
    curl -b cookie1.txt "http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id="$item
done
python -c "import time;time.sleep(0.05)"; done

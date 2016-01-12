
# login example
curl -c cookie1.txt -d "USERNAME=20131003726&PASSWORD=080392" http://jxgl.gdufs.edu.cn/jsxsd/xk/LoginToXkLdap
#curl -b cookie1.txt http://jxgl.gdufs.edu.cn/jsxsd/framework/main.jsp # 抓取主页
#curl -b cookie1.txt http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xsxkXxxk > course.json #get course json

#select panel page
curl -b cookie1.txt "http://jxgl.gdufs.edu.cn/jsxsd/xsxk/xsxk_index?jx0502zbid=425DF1EBE9644E6297C4D54B3EAD7A93"
# select example
curl -b cookie1.txt "http://jxgl.gdufs.edu.cn/jsxsd/xsxkkc/xxxkOper?jx0404id=20152016200000000000000017496"

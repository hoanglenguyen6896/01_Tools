import re

tmp_str="<h2><span style=\"font-weight: 400;\">1. Tại sao những chiếc đầm đen lại được ưa chuộng?</span></h2>" + \
"<h2><span style=\"font-weight: 400;\"><span style=\"font-size: 150%; color: #00aae7;\">1.</span> Tại sao những chiếc đầm đen lại được ưa chuộng?</span></h2>"

tmp_str="<h2><span style=\"font-weight: 400;\">1. Tại sao những chiếc đầm đen lại được ưa chuộng?</span></h2><h3><span style=\"font-weight: 400;\">3.2 Giày thể thao</span></h3>;\">1..7.8.9"

tmp_str="<a href=\"https://1102style.vn/giay-louis-vuitton-nu/\"><span style=\"font-weight: 400;\">giày Louis Vuitton nữ</span></a><span style=\"font-weight: 400;\">"
# regex object
phoneNumRegex = re.compile(r'href="(?:[^"]|"")*"', re.IGNORECASE)
mo = re.findall(phoneNumRegex, tmp_str)
print(mo)
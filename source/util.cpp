#include <string>
#include <vector>

#include <sotd.h>

std::string sotd::extract(const std::string & strobj, const std::string & start, const std::string & end) {
	std::size_t i = 0, j = 0;
	i = strobj.find(start);
	if (i == std::string::npos) return std::string("");
	j = strobj.find(start,i);
	if (j == std::string::npos) return strobj.substring(i,strobj.length() - i);
	return strobj.substr(i,j - i);
}

std::vector<std::string> sotd::split(const std::string &str, const std::string &sub, const std::string pre = "") {
	std::vector<std::string> v();
	std::size_t i = 0, j = str.find(sub), l = sub.length();

	v.push_back(pre + str.substr(i,j - i));

	while (j != std::string::npos)
	{
		i = j + l;
		j = str.find(sub,i);
		v.push_back(pre + str.substr(i,j - i));
	}

	return v;
}

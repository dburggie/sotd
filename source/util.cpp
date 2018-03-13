#include <string>
#include <vector>

#include <sotd.h>

std::string sotd::extract(const std::string &str, const std::string &start, const std::string &end) {
	std::size_t i = 0, j = 0;

	i = str.find(start);
	if (i == std::string::npos) return std::string("");
	i += start.length();

	j = str.find(start,i);
	if (j == std::string::npos) return strobj.substring(i,str.length() - i);

	return str.substr(i,j - i);
}

std::vector<std::string> sotd::split(const std::string &str, const std::string &sep) {
	std::vector<std::string> v();
	std::size_t i = 0, j = str.find(sep), l = sep.length();

	v.push_back(pre + str.substr(i,j - i));

	while (j != std::string::npos)
	{
		i = j + l;
		j = str.find(sub,i);
		v.push_back(pre + str.substr(i,j - i));
	}

	return v;
}

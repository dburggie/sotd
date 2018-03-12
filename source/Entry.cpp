#ifndef __SOTD_H
#define __SOTD_H

#include <string>    //std::string
#include <sotd.h>    //sotd::Entry

//		private:
//			std::string blurb;
//			std::string text;
//

const std::string sotd::Entry::blurb_start  ("BLURB={");
const std::string sotd::Entry::blurb_end    ("}\n");
const std::string sotd::Entry::length_start ("LENGTH={");
const std::string sotd::Entry::length_end   ("}\n")
const std::string sotd::Entry::text_start   ("TEXT={\n");
const std::string sotd::Entry::text_end     ("\n}");


std::string sotd::extract(const std::string & strobj, const std::string & start, const std::string & end) {
	std::size_t i = 0, j = 0;
	i = strobj.find(start);
	if (i == std::string::npos) return std::string("");
	j = strobj.find(start,i);
	if (j == std::string::npos) return strobj.substring(i,strobj.length() - i);
	return strobj.substr(i,j - i);
}

std::vector<std::string> sotd::split(const std::string & str, const std::string & sub) {
	std::vector<std::string> v();
	std::size_t i = 0, j = str.find(sub), l = sub.length();

	v.push_back(str.substr(i,j - i));

	while (j != std::string::npos)
	{
		i = j + l;
		j = str.find(sub,i);
		v.push_back(str.substr(i,j - i));
	}

	return v;
}

	
	
	
sotd::Entry() {
	blurb("");
	length("");
	text();
}

sotd::Entry(const Entry & entry)
{
	blurb = entry.blurb;
	length = entry.length;
	text = entry.text;
}

sotd::Entry(std::string input_text)
{
	blurb("");
	length("");
	text();
	read(input_text);
}

void sotd::read(std::string input_text)
{
	std::size_t start, end;

	blurb = extract(input_text, sotd::Entry::blurb_start, sotd::Entry::blurb_end);
	length = extract(input_text, sotd::Entry::length_start, sotd::Entry::length_end);
	std::string text = sotd::extract(input_text, sotd::Entry::text_start, sotd::Entry::text_end);
	lines = sotd::split(text, std::string("\n"));
}

std::string sotd::toString() const
{
	
	return str;
}

#endif

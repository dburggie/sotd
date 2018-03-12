#ifndef __SOTD_H
#define __SOTD_H

#include <string>    //std::string
#include <vector>    //std::vector
#include <sotd.h>    //sotd::Entry,split,extract

const std::string sotd::Entry::blurb_start  ("BLURB={");
const std::string sotd::Entry::blurb_end    ("}\n");
const std::string sotd::Entry::length_start ("LENGTH={");
const std::string sotd::Entry::length_end   ("}\n")
const std::string sotd::Entry::text_start   ("TEXT={\n");
const std::string sotd::Entry::text_end     ("\n}");

sotd::Entry() {
	blurb = std::string("");
	length = std::string("");
	lines = std::vector<std::string>();
}

sotd::Entry(const Entry & entry)
{
	blurb = std::string(entry.blurb);
	length = std::string(entry.length);
	lines = std::vector<std::string>(entry.lines);
}

sotd::Entry(const std::string &input_text)
{
	blurb = std::string("");
	length = std::string("");
	lines = std::vector<std::string>();
	read(input_text);
}

void sotd::read(std::string input_text)
{
	std::size_t start, end;

	blurb = extract(input_text, sotd::Entry::blurb_start, sotd::Entry::blurb_end);
	length = extract(input_text, sotd::Entry::length_start, sotd::Entry::length_end);
	std::string text = sotd::extract(input_text, sotd::Entry::text_start, sotd::Entry::text_end);
	lines = sotd::split(text, "\n", "  ");
}

std::string sotd::toString() const
{
	std::string str = "\n" + blurb + "\n\n";

	std::vector<std::string>::iterator i = lines.begin();
	for (i = lines.begin(); i != lines.end(); i++)
	{
		str += *i;
	}

	str += "\n\n";
	return str;
}

#endif

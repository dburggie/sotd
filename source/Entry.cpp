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

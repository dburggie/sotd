#ifndef __SOTD_H
#define __SOTD_H

#include <sotd>		//sotd::Entry
#include <string>	//std::string

//		private:
//			std::string blurb;
//			std::string text;
//

const std::string sotd::Entry::blurb_start  ("BLURB={");
const std::string sotd::Entry::blurb_end    ("}\n");
const std::string sotd::Entry::length_start ("LENGTH={");
const std::string sotd::Entry::length_end   ("}\n")
const std::string sotd::Entry::text_start   ("TEXT={\n");
const std::string sotd::Entry::text_end     ("\n}")

sotd::Entry() {
	blurb("");
	length("");
	text("");
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
	text("");
	read(input_text);
}

void sotd::read(std::string input_text)
{
	int start, end;

	start = input_text.find(blurb_start);
	start += blurb_start.length();
	end = input_text.find(blurb_end, start);
	blurb = input_text.substr(start, end - start);

	start = input_text.find(length_start);
	start += length_start.length();
	end = input_text.find(length_end, start);
	length = input_text.substr(start, end - start);

	start = input_text.find(text_start, end);
	start += text_start.length();
	end = input_text.find(text_end, start);
	text = input_text.substr(start, end - start);
}

std::string sotd::toString() const {
	std::string str = blurb_start;
	str += blurb;
	str += blurb_end;
	str += length_start;
	str += length;
	str += length_end;
	str += text_start;
	str += text;
	str += text_end;
	return str;
}

#endif

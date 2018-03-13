#include <string>    //std::string
#include <vector>    //std::vector
#include <sotd.h>    //sotd::Entry,split,extract

static const char * toString_start  = "\n";
static const char * toString_sep    = "\n\n";
static const char * toString_indent = "  ";
static const char * toString_end    = "\n\n";

const std::string sotd::Entry::blurb_start  ("#ENTRY_BLURB=");
const std::string sotd::Entry::blurb_end    ("\n");
const std::string sotd::Entry::length_start ("#ENTRY_LENGTH=");
const std::string sotd::Entry::length_end   ("\n");
const std::string sotd::Entry::text_start   ("#BEGIN_ENTRY_TEXT=\n");
const std::string sotd::Entry::text_end     ("\n#END_ENTRY_TEXT");

sotd::Entry::Entry() {
	blurb = std::string("");
	length = std::string("");
	lines = std::vector<std::string>();
}

sotd::Entry::Entry(const Entry & entry)
{
	blurb = std::string(entry.blurb);
	length = std::string(entry.length);
	lines = std::vector<std::string>(entry.lines);
}

sotd::Entry::Entry(const std::string &input_text)
{
	blurb = std::string("");
	length = std::string("");
	lines = std::vector<std::string>();
	read(input_text);
}

void sotd::Entry::read(const std::string &input_text)
{
	std::size_t start, end;

	blurb = sotd::extract(input_text, sotd::Entry::blurb_start, sotd::Entry::blurb_end);
	length = sotd::extract(input_text, sotd::Entry::length_start, sotd::Entry::length_end);
	std::string text = sotd::extract(input_text, sotd::Entry::text_start, sotd::Entry::text_end);
	lines = sotd::split(text, "\n");
}

std::string sotd::Entry::toString() const
{
	std::string str = toString_start + blurb + toString_sep;

	for (auto iter = lines.begin(); iter != lines.end(); ++iter)
	{
		str += toString_indent + *iter;
	}

	str += toString_end;
	return str;
}


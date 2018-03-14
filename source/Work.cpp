#include <string>
#include <vector>
#include <sotd.h>

const std::string sotd::Work::title_start   ("#WORK_TITLE=");
const std::string sotd::Work::title_end     ("\n");
const std::string sotd::Work::count_start   ("#ENTRY_COUNT=");
const std::string sotd::Work::count_end     ("\n");
const std::string sotd::Work::entries_start ("#BEGIN_ENTRIES\n");
const std::string sotd::Work::entries_sep   ("\n#NEW_ENTRY\n");
const std::string sotd::Work::entries_end   ("\n#END_ENTRIES");

sotd::Work::Work()
{
	title = std::string("");
	entries = std::vector<sotd::Entry>();
}
					     
sotd::Work::Work(const Work &work)
{
	title = std::string(work.title);
	entries = std::vector<sotd::Entry>(work.entries);
}

sotd::Work::Work(const std::string &input_text)
{
	title = std::string("");
	entries = std::vector<sotd::Entry>();
	read(input_text);
}

sotd::Work::~Work() { }

void sotd::Work::read(const std::string &input_text)
{
	//get work title
	title = sotd::extract(
			input_text,
			sotd::Work::title_start,
			sotd::Work::title_end
		);

	//get work body
	std::string text = sotd::extract(
			input_text,
			sotd::Work::entries_start,
			sotd::Work::entries_end
		);
	
	//split work body into entries and collect
	std::vector<std::string> entry_text_vector
			= sotd::split(text, sotd::Work::entries_sep);
01234567890123456789012345678901234567890123456789012345678901234567890123456789
	for (auto i = entry_text_vector.begin(); 
	     i != entry_text_vector.end(); 
	     ++i)
	{
		entries.push_back(sotd::Entry(*i));
	}
}

const sotd::Entry & sotd::Work::getRandomEntry() const
{
	return entries[sotd::random(entries.size())];
}

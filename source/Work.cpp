#include <string>
#include <vector>
#include <sotd.h>

const std::string sotd::Work::title_start   ("#WORK_TITLE=");
const std::string sotd::Work::title_end     ("\n");
const std::string sotd::Work::count_start   ("#ENTRY_COUNT=");
const std::string sotd::Work::count_end     ("\n");
const std::string sotd::Work::entries_start ("#BEGIN_ENTRIES=\n");
const std::string sotd::Work::entries_sep   ("\n#NEW_ENTRY\n");
const std::string sotd::Work::entries_end   ("\n#END_ENTRIES");

sotd::Work::Work()
{
	title = std::string("");
	works = std::vector<sotd::Entry>();
}
					     
sotd::Work::Work(const Work &work)
{
	title = std::string(work.title);
	works = std::vector<sotd::Entry>(work.works);
}

sotd::Work::Work(const std::string &input_text)
{
	title = std::string("");
	works = std::vector<sotd::Entry>();
	read(input_text);
}

sotd::Work::~Work() { }

void sotd::Work::read(const std::string &input_text)
{
	title = extract(input_text, sotd::Work::title_start, sotd::Work::title_end);
	std::vector<std::string> entry_text_vector = sotd::split(input_text, sotd::Entry::title_start, sotd::Entry::title_start);
	entry_text_vector.erase(0);
	std::vector<std::string>::iterator i;
	for (i = entry_text_vector.begin(); i != entry_text_vector.end(); i++)
	{
		works.push_back(sotd::Entry(entry_text_vector[i]));
	}
}

const sotd::Entry & sotd::Work::getRandomEntry() const
{
	return works[0]; //chosen by random dice roll, guaranteed to be random
}

#include <string>
#include <vector>
#include <sotd.h>

const std::string sotd::Data::author_start ("#AUTHOR=");
const std::string sotd::Data::author_end   ("\n");
const std::string sotd::Data::count_start  ("#WORK_COUNT=");
const std::string sotd::Data::count_end    ("\n");
const std::string sotd::Data::works_start  ("#BEGIN_WORKS=\n");
const std::string sotd::Data::works_sep    ("\n#NEW_WORK\n");
const std::string sotd::Data::works_end    ("\n#END_WORKS\n");

sotd::Data::Data()
{
	author = std::string("");
	works = std::vector<sotd::Work>();
}

sotd::Data::Data(const sotd::Data &data)
{
	author = std::string(data.author);
	works = std::vector<sotd::Work>(data.works);
}

sotd::Data::Data(const std::string &text)
{
	author = std::string("");
	works = std::vector<sotd::Work>();
	read(text);
}

sotd::Data::~Data() { }

void sotd::Data::read(const std::string &text)
{
	author = sotd::extract(
			text,
			sotd::Data::author_start,
			sotd::Data::author_end
		);

	std::string works_text = sotd::extract(
			text,
			sotd::Data::works_start,
			sotd::Data::works_end
		);

	std::vector<std::string> work_text_vector = sotd::split(
			works_text,
			sotd::Data::works_sep
		);

	for (auto it = work_text_vector.begin(); it != work_text_vector.end(); ++it)
	{
		works.push_back(sotd::Work(*it));
	}
}

const sotd::Work & sotd::Data::getRandomWork() const
{
	return works[sotd::random(works.size())];
}

#include <string>
#include <vector>
#include <sotd.h>

const std::string sotd::Data::author_start ("#AUTHOR=");
const std::string sotd::Data::author_end   ("\n");
const std::string sotd::Data::count_start  ("#WORK_COUNT=");
const std::string sotd::Data::count_end    ("\n");
const std::string sotd::Data::works_start  ("#BEGIN_WORKS\n");
const std::string sotd::Data::works_sep    ("\n#NEW_WORK\n");
const std::string sotd::Data::works_end    ("\n#END_WORKS");

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
	//get author's name
	author = sotd::extract(
			text,
			sotd::Data::author_start,
			sotd::Data::author_end
		);

	//get the number of works for this author
	std::string count = sotd::extract(
			text,
			sotd::Data::count_start,
			sotd::Data::count_end
		);

	//get text of all the works for this author
	std::string works_text = sotd::extract(
			text,
			sotd::Data::works_start,
			sotd::Data::works_end
		);

	//separate text body into separate work strings
	std::vector<std::string> work_text_vector = sotd::split(
			works_text,
			sotd::Data::works_sep
		);

	//translate strings to work objects and collect them
	for (auto it = work_text_vector.begin(); it != work_text_vector.end(); ++it)
	{
		works.push_back(sotd::Work(*it));
	}
}

const sotd::Work & sotd::Data::getRandomWork() const
{
	return works[sotd::random(works.size())];
}

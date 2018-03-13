#include <string>
#include <vector>
#include <sotd.h>
//		std::string author;
//		std::vector<Work> works;
const std::string sotd::Data::author_start ("#AUTHOR=");
const std::string sotd::Data::author_end   ("\n");
const std::string sotd::Data::count_start  ("#WORK_COUNT=");
const std::string sotd::Data::count_end    ("\n");
const std::string sotd::Data::works_start  ("#BEGIN_WORKS=\n");
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

sotd::Data::Data(const std::string &filename)
{
	author = std::string("");
	works = std::vector<sotd::Work>();
	read(filename);
}

sotd::Data::~Data() { }

void sotd::Data::read(const std::string &filename)
{
}

const sotd::Work & sotd::Data::getRandomWork() const
{
	return works[0];
}

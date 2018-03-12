#include <string>
#include <vector>
#include <sotd.h>
//		std::string author;
//		std::vector<Work> works;
const std::string sotd::Data::author_start = std::string("AUTHOR={");
const std::string sotd::Data::author_end = std::string("}\n");
const std::string sotd::Data::count_start = std::string("WORK_COUNT={");
const std::string sotd::Data::count_end = std::string("}\n");
const std::string sotd::Data::works_start = std::string("WORKS={\n");
const std::string sotd::Data::works_end = std::string("\n}");

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

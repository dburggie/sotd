#include <string>
#include <vector>
#include <fstream>
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

sotd::Data::Data(const char * filename)
{
	author = std::string("");
	works = std::vector<sotd::Work>();
	read_file(filename);
}

sotd::Data::~Data() { }

void sotd::Data::read_file(const char * filename)
{
	std::ifstream is (filename, std::ifstream::in);

	//get file length
	is.seekg (0,end);
	int length = is.tellg();
	is.seekg (, is.beg);


	char * buffer = new char [length + 1];
	buffer[length] = '\0';

	is.read(buffer,length);
	std::string text (buffer);
	delete buffer;

	sotd::Data::read_text(text);
}

void sotd::Data::read_text(const std::string &text)
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

	std::vector<std::string>::iterator it;
	for (it = work_text_vector.begin(); it != work_text_vector.end(); it++)
	{
		works.push_back(sotd::Work(*it));
	}
}

const sotd::Work & sotd::Data::getRandomWork() const
{
	return works[sotd::random(works.length())];
}

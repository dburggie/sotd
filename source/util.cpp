#include <string>   //std::string
#include <vector>   //std::vector
#include <cstdlib>  //std::srand,rand
#include <ctime>    //std::time
#include <iostream> //std::cerr,endl
#include <fstream>  //std::ifstream

#include <sotd.h>

std::string sotd::extract(
		const std::string &str,
		const std::string &start,
		const std::string &end
	)
{
	std::size_t i = 0, j = 0;

	//get index of %start
	//end early if not found
	//adjust index by $start length
	i = str.find(start);
	
	if (i == std::string::npos)
	{
		return std::string("");
	}
	
	i += start.length();

	//get index of $end and return
	j = str.find(end,i);
	
	if (j == std::string::npos)
	{
		return str.substr(i, str.length() - i);
	}
	
	return str.substr(i,j - i);
}

std::vector<std::string> sotd::split(
		const std::string &str,
		const std::string &sep
	)
{
	std::vector<std::string> v;
	std::size_t i = 0, j = str.find(sep), l = sep.length();

	v.push_back(str.substr(i,j - i));

	while (j != std::string::npos)
	{
		i = j + l;
		j = str.find(sep,i);
		v.push_back(str.substr(i,j - i));
	}

	return v;
}

static bool random_initialized = false;
static void init_random()
{
	std::srand(std::time(NULL));
	random_initialized = true;
}

int sotd::random(int max)
{
	if (!random_initialized) init_random();
	return std::rand() % max;
}


std::string sotd::readfile(const char * path)
{
	std::ifstream is (path, std::ifstream::in);

	//get file length
	is.seekg(0, is.end);
	unsigned long int length = is.tellg();
	is.seekg(0, is.beg);

	//allocate buffer and just-in-case null-terminate
	char * buffer = new char [length + 1];
	buffer[length] = '\0';

	//do read and make sure we read the whole file
	is.read(buffer,length);

	std::string contents;

	if (is)
	{
		contents = buffer;
	}

	else
	{
		contents = "";
	}

	//cleanup and return
	delete buffer;

	return contents;
}

void sotd::log(const char * msg)
{
	std::cerr << msg << std::endl;
}

void sotd::log(const std::string &msg)
{
	std::cerr << msg << std::endl;
}


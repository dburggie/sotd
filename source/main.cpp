#include <iostream> //std::cout
#include <string>   //std::string
#include <sotd.h>   //sotd::Data,Work,Entry,readfile

int main(int argc, const char *argv[])
{
	//determine run mode
	sotd::runmode mode = sotd::cmdline;
	if (2 == argc)
	{
		if (sotd::servicemode_option == argv[1])
		{
			mode = sotd::service;
		}
	}
	//read data file
	std::string data_text = sotd::readfile(DATA_PATH);
	if (0 == data_text.length())
	{
		data_text = sotd::readfile(DATA_FALLBACK);
	}

	//parse data
	sotd::Data data(data_text);
	std::string msg = data.getRandomWork().getRandomEntry().toString();
	
	//write output
	if (sotd::cmdline == mode)
	{
		std::cout << msg;
	}

	else
	{
		bool writefail = sotd::writefile(sotd::servicemode_path, msg);
		if (writefail)
		{
			std::string errmsg = "main(): failed to write to ";
			errmsg += sotd::servicemode_path;
			sotd::log(errmsg);
		}
	}

	return 0;
}

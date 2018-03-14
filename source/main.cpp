#include <iostream> //std::cout
#include <string>   //std::string
#include <sotd.h>   //sotd::Data,Work,Entry,readfile

int main(void)
{
	//read data file
	std::string data_text = sotd::readfile(DATA_PATH);
	if (0 == data_text.length())
	{
		data_text = sotd::readfile(DATA_FALLBACK);
	}

	//parse data
	sotd::Data data(data_text);
	
	//print a random entry
	std::cout << data.getRandomWork().getRandomEntry().toString();

	return 0;
}

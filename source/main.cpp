#include <iostream> //std::cout
#include <string>   //std::string
#include <sotd.h>   //sotd::Data,Work,Entry

int main(void)
{
	std::string data_text = sotd::readfile(DATA_PATH);
	if (0 == data_text.length())
	{
		data_text = sotd::readfile(DATA_FALLBACK);
	}

	sotd::Data data(data_text);
	sotd::Work work = data.getRandomWork();
	sotd::Entry entry = work.getRandomEntry();
	std::cout << data.getRandomWork().getRandomEntry().toString();

	return 0;
}

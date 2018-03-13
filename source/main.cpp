#include <iostream>		//std::cout
#include <sotd.h>		//sotd::Data,Work,Entry

int main(void)
{
	sotd::Data data(sotd::readfile(DATA_PATH));
	sotd::Work work = data.getRandomWork();
	sotd::Entry entry = work.getRandomEntry();
	std::cout << entry.toString();

	return 0;
}

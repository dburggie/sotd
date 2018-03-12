#include <string>
#include <vector>
#include <sotd.h>

const std::string sotd::Work::title_start   ("TITLE={");
const std::string sotd::Work::title_end     ("}\n");
const std::string sotd::Work::count_start   ("COUNT={");
const std::string sotd::Work::count_end     ("}\n");
const std::string sotd::Work::entries_start ("ENTRIES={\n");
const std::string sotd::Work::entries_end   ("\n}"

sotd::Work::Work();
sotd::Work::Work(const Work &work);
sotd::Work::Work(const std::string &input_text);
sotd::Work::~Work();
void sotd::Work::read(const std::string &input_text);
const sotd::Entry & sotd::Work::getRandomEntry() const;

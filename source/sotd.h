#ifndef SOTD_H
#define SOTD_H

#ifndef DATA_PATH
#define DATA_PATH "/usr/share/sotd/sotd.dat"
#endif

#ifndef DATA_FALLBACK
#define DATA_FALLBACK "./data/sotd.dat"
#endif

#include <string>	//std::string
#include <vector>	//std::vector

namespace sotd {

	//implemented in: util.cpp
	//get string between $start and $end inside $str
	std::string extract(
			const std::string &str,
			const std::string &start,
			const std::string &end
		);

	//implemented in: util.cpp
	//split string at $sep substrings of $str
	std::vector<std::string> split(
			const std::string &str,
			const std::string &sep
		);

	//implemented in: util.cpp
	//get a random int in [0,max)
	int random(int max);

	//implemented in util.cpp
	//return file contents as a string
	std::string readfile(const char * path);

	//implemented in util.cpp
	//i think we can remove these now, but it can wait
	void log(const char * msg);
	void log(const std::string &msg);

	//implemented in Entry.cpp
	class Entry {
	private:
		std::string blurb;
		std::string length;
		std::vector<std::string> lines;

	public:
		static const std::string blurb_start;
		static const std::string blurb_end;
		static const std::string length_start;
		static const std::string length_end;
		static const std::string text_start;
		static const std::string text_end;

		Entry();
		Entry(const Entry &entry);
		Entry(const std::string &input_text);
		~Entry();
		void read(const std::string &input_text);

		//returns entry formatted for final displaying
		std::string toString() const;
	};

	//implemented in: Work.cpp
	class Work {
	private:
		std::string title;
		std::vector<Entry> entries;
	public:
		static const std::string title_start;
		static const std::string title_end;
		static const std::string count_start;
		static const std::string count_end;
		static const std::string entries_start;
		static const std::string entries_sep;
		static const std::string entries_end;

		Work();
		Work(const Work &work);
		Work(const std::string &input_text);
		~Work();
		void read(const std::string &input_text);
		const Entry & getRandomEntry() const;
	};

	//implemented in: Data.cpp
	class Data {
	private:
		std::string author;
		std::vector<Work> works;
	public:
		static const std::string author_start;
		static const std::string author_end;
		static const std::string count_start;
		static const std::string count_end;
		static const std::string works_start;
		static const std::string works_sep;
		static const std::string works_end;

		Data();
		Data(const Data &data);
		Data(const std::string &text);
		~Data();
		void read(const std::string &text);
		const Work & getRandomWork() const;
	};
};

#endif

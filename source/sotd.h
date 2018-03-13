#ifndef __SOTD_H
#define __SOTD_H

#include <string>	//std::string
#include <vector>	//std::vector

namespace sotd {

	//get string between $start and $end inside $str
	std::string extract(const std::string &str, const std::string &start, const std::string &end);

	//split string at $sep substrings of $str
	std::vector<std::string> split(const std::string &str, const std::string &sep);

	class Entry {
	private:
		std::string blurb;
		std::string length;
		std::vector<string> lines;

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
		std::string toString() const;
	};

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
		Data(const std::string &filename);
		~Data();
		void read(const std::string &filename);
		const Work & getRandomWork() const;
	};
}

#endif

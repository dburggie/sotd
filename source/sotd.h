#ifndef __SOTD_H
#define __SOTD_H

#include <string>	//std::string
#include <vector>	//std::vector

namespace sotd {
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
		Entry(const Entry & entry);
		Entry(std::string input_text);
		~Entry();
		void read(std::string input_text);
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
		static const std::string entries_end;

		Work();
		Work(const Work & work);
		Work(std::string input_text);
		~Work();
		void read(std::string input_text);
		Entry getRandomEntry();
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
		static const std::string works_end;

		Data();
		Data(const Data & data);
		Data(std::string filename);
		~Data();
		void read(std::string filename);
		Work getRandomWork();
	};
}

#endif

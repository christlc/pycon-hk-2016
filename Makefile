data/yob*.txt:
	./download.sh

data/names_by_decade.csv: data/yob*.txt clean_data.py
	python clean_data.py

output/presentation.html: compile_reports.py data/names_by_decade.csv templates/content.j2 templates/base.j2
	python compile_reports.py

all: data/yob*.txt data/names_by_decade.csv output/presentation.html

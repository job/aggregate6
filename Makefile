all:
	cp README.md aggregate6.7.ronn
	ronn -r --pipe aggregate6.7.ronn > aggregate6.7
	rm aggregate6.7.ronn
	pandoc --from=markdown --to=rst --output=README.rst README.md

clean:
	rm -rf *.egg *.egg-info dist build

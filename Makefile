all:
	cp README.md aggregate6.7.ronn
	ronn -r --pipe aggregate6.7.ronn > aggregate6/aggregate6.7
	rm aggregate6.7.ronn

clean:
	rm -rf *.egg *.egg-info dist build

#!/usr/bin/env python3

from google.chrome_driver import get_driver


d = get_driver()
d.search("Talentsoft")
d.count_results()

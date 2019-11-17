#!/usr/bin/env python3


import yaml
import glob
import os
import json
from bs4 import BeautifulSoup
import lxml


board_root = "boards"

boards = []

BOARD_HTML = """

<figure class="grid__brick mt-3 col-6 col-md-4 col-xl-3 picture-item figure" data-groups='["{arch}"]' data-date-created="2016-08-12"
		data-title="{name}">
	<div class="aspect aspect--16x9">
		<div class="aspect__inner">
			<img class="figure-img img-fluid rounded"
                 src="_images/{image}"
				 alt="{name}"/>
		</div>
	</div>
    <figcaption class="picture-item__title figure-caption"><h4><a href="https://docs.zephyrproject.org/latest/boards/{arch}/{identifier}/doc/index.html">{name}</a></h4>
		<p>{intro}</p>
	</figcaption>
</figure>
"""
BOARD_HTML2 = """

<figure class="grid__brick mt-3 col-6 col-md-4 col-xl-3 picture-item figure" data-groups='["{arch}"]' data-date-created="2016-08-12"
		data-title="{name}">
	<div class="aspect aspect--16x9">
		<div class="aspect__inner">
		</div>
	</div>
    <figcaption class="picture-item__title figure-caption"><h4><a href="https://docs.zephyrproject.org/latest/boards/{arch}/{identifier}/doc/index.html">{name}</a></h4>
		<p>{intro}</p>
	</figcaption>
</figure>
"""

output = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Boards</title>

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css"
          integrity="sha384-GJzZqFGwb1QTTN6wy59ffF1BuGJpLSa9DkKMp0DgiMDm4iYMj70gZWKYbI706tWS" crossorigin="anonymous">


    <link rel="stylesheet" href="css/shuffle.css" >
	<link rel="stylesheet" href="css/zephyr.css">

    <script src="https://cdnjs.cloudflare.com/ajax/libs/Shuffle/5.2.1/shuffle.js" language="JavaScript">
    </script>

    <script src="https://code.jquery.com/jquery-3.3.1.min.js"
            integrity="sha256-FgpCb/KJQlLNfOu91ta32o/NMZxltwRo8QtmkMRdAu8=" crossorigin="anonymous"></script>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/json2html/1.2.0/json2html.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.json2html/1.2.0/jquery.json2html.min.js"></script>


</head>
<body>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">Zephyr Boards</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
            aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav mr-auto">

        </ul>
        <form class="form-inline my-2 my-lg-0">
            <input class="form-control mr-sm-2 filter__search js-shuffle-search" type="search" placeholder="Search"
                   aria-label="Search">

        </form>
    </div>
</nav>
<main role="main" id="main">
  <style>
  /* Allow bootstrap grid elements to fit on mobile */
  @media (max-width: 575px) {
    .row > [class*="col-"] {
      padding-left: 8px;
      padding-right: 8px;
    }
  }
</style>

<div class="container">
  <div class="row">

      <div class="col-12@sm filters-group-wrap">
        <div class="filters-group">
          <p class="filter-label">Filter</p>
          <div class="btn-group filter-options">
           <button class="btn btn--primary" data-group="all">All</button>
            <button class="btn btn--primary" data-group="arm">ARM</button>
            <button class="btn btn--primary" data-group="x86">X86</button>
              <button class="btn btn--primary" data-group="arc">ARC</button>
              <button class="btn btn--primary" data-group="riscv32">RISCV32</button>
              <button class="btn btn--primary" data-group="xtensa">Xtensa</button>
              <button class="btn btn--primary" data-group="nios2">NIOS-II</button>
              <button class="btn btn--primary" data-group="posix">Posix</button>
          </div>
        </div>
        <fieldset class="filters-group">
          <legend class="filter-label">Sort</legend>
          <div class="btn-group sort-options">
            <label class="btn active">
              <input type="radio" name="sort-value" value="dom" /> Default
            </label>
            <label class="btn">
              <input type="radio" name="sort-value" value="title" /> Title
            </label>
            <label class="btn">
              <input type="radio" name="sort-value" value="date-created" /> Date Created
            </label>
          </div>
        </fieldset>
      </div>
    </div>

</div>
<div class="container mb-4" style="margin-top: 30px;">
    <div id="grid" class="row my-shuffle-container">
"""

for fn in glob.glob(os.path.join(board_root, "*", "*", "*.yaml")):
    with open(fn, 'r') as f:
        board = yaml.safe_load(f)

        ff = fn.split("/")
        bpath = "/".join(ff[0:3])
        dir_name = ff[-2]
        html_file = os.path.join("./doc/_build/html/" + bpath +  "/doc/index.html")
        if board['identifier'] != dir_name:
            print("skipping {}".format(fn))
            continue
        else:
            print("working on {}".format(fn))
        if os.path.exists(html_file):
            with open (html_file, "r") as myfile:
                data=myfile.read()
            soup = BeautifulSoup(data, 'lxml')
            intro = soup.find('p').text
            board['intro'] = intro
            image_p = "doc/_build/html/_images/{}".format(board['identifier'])
            if os.path.exists(image_p + ".png"):
                image_file = "{}.png".format(board['identifier'])
                output += BOARD_HTML.format(name=board['name'],arch=board['arch'],intro=intro, image=image_file, identifier=board['identifier'])
            elif os.path.exists(image_p + ".jpg"):
                image_file = "{}.jpg".format(board['identifier'])
                output += BOARD_HTML.format(name=board['name'],arch=board['arch'],intro=intro, image=image_file,identifier=board['identifier'])
            else:
                output += BOARD_HTML2.format(name=board['name'],arch=board['arch'],intro=intro, identifier=board['identifier'])

        boards.append(board)


with open('boards.json', 'w') as outfile:
	json.dump(boards, outfile)

output += """


    </div>
        <div class="col-3 my-sizer-element"></div>

</div>

</main>
    <script language="JavaScript" src="js/boards.js"></script>

</body>
</html>

"""

with open("output.html", 'w') as outfile:
    outfile.write(output)

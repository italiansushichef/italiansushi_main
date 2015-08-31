iTahmSets 
==============

About
----
iTahmSets isn't endorsed by Riot Games and neither reflects the views or opinions of Riot Games nor anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.

iTahmSets was originally created for the Riot API Challenge 2.0 in August 2015, Entry's Category: Item Sets.
It provides 5 distinct item set features for users. See the website tutorials in the tabs for how to use. 

Made by: Kevin Wang (NA: donutgodking) and Alex Zhang (NA: ACannibal)

Live URL
----
http://itahmsets.herokuapp.com/

(We are currently hosting using a free Hobby-dev account.)

Features
----
* <strong>Uploading Item Sets</strong>: Store your item set JSON files on our website. Our website will check the file format to make sure it is in the appropriate format. You can download them on any computer.

* <strong>Matchup Generator</strong>: From our dataset, we parse item information from thousands of matches and use a weighted algorithm based on the lane, opponent champion, and who won the game to generate an item sets of 5 blocks: Starting Items, Early Game, Mid Game, Late Game, Full Build. The algorithm can be found in the <b> generateItemSetForMatchup(champ1_id, champ2_id, lane) </b> function in <i>italiansushi_main/italiansushi/views.py</i>

* <strong>Item Set Builder</strong>: Design a custom item set in-browser that can be downloaded and used in-game.

* <strong>Search Tool</strong>: Browse by champion and lane to see the most popular item sets that other users have uploaded or designed. You can vote on your favorites too!

* <strong>Saved Item Set Manager</strong>:View, edit, and download all item sets saved to your account. You can save up to 10 item sets to a single account.

Data Set for Matchup Generator
----
Using the Riot Developmental API, we collected ~11,000 ranked players from the Plat-Diamond range and ~50,000 of their unique ranked SR matches. Due to GitHub repo limits, we currently only use a smaller set of ~5000 matches to generate lane matchups.  In the future this will be increased, which will drastically improve the generated matchup results.

Development Stack
----
* Django
* Python scripts for Riot API Calls
* Bootstrap, JQuery, Font-awesome.css, Bootbox.js
* Postgresql (hosted on Heroku) for database 
* Photoshop for Website Images

(See requirements.txt for full list of Python libraries used)

Limitations
----
* We are currently hosting using a free Hobby-dev account, which is limited in the database size and app awake time, though it will support any expected traffic for the purposes of the competition.
* As mentioned, our data set for the matchup generator is limited in the live version because of the repo limits. This drastically limits the quality of the generated item sets, but the underlying algorithm is what we'd like to highlight.
* There are likely minor bugs through, since we did not have time for widespread open user testing.


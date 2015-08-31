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

Features
----
* Uploading Item Sets: Store your item set JSON files on our website. Our website will check the file format to make sure it is in the appropriate format. You can download them on any computer.

* Matchup Generator: From our dataset, we parse item information from thousands of matches and use a weighted algorithm based on the lane, opponent champion, and who won the game to generate an item sets of 5 blocks: Starting Items, Early Game, Mid Game, Late Game, Full Build.

* Item Set Builder:
Design a custom item set in-browser that can be downloaded and used in-game.

* Search Tool:
Browse and vote on the most popular item sets that other users have uploaded or designed.

* Saved Item Set Manager: View, edit, and download all item sets saved to your account. You can have 3 item sets at a time.

Data Set for Matchup Generator
----
Using the Riot Developmental API, we collected ~11,000 ranked players from the Plat-Diamond range and ~50,000 of their unique ranked SR matches. Due to GitHub repo limits, we currently only use a smaller set of ~5000 matches to generate lane matchups. In the future (after competition) this will be increased, which should also provide better matchup results. 

Development Stack
----
* Django
* Python scripts for Riot API Calls
* Javascript/JQuery
* Bootstrap, Font-awesome.css, Bootbox.js
* Photoshop for Website Images

iTahmSets 
==============

iTahmSets isn't endorsed by Riot Games and neither reflects the views or opinions of Riot Games nor anyone officially involved in producing or managing League of Legends. League of Legends and Riot Games are trademarks or registered trademarks of Riot Games, Inc. League of Legends © Riot Games, Inc.

Made by: Kevin Wang (NA: donutgodking) and Alex Zhang (NA: ACannibal)

About
----
iTahmSets was created for the Riot API Challenge 2.0 in August 2015, for the Category: Item Sets. We strived to the "go-to" all-encompassing online hub for working with items sets through 5 distinct tools for users. Detailed tutorials for each tool are available on the live website. We woud like to highlight the site's single-page app design, with a user-interface that is both intuitive and easy to pick up. At the same time, our site encompasses a wide array of features that other websites won't all provide. Due to time constraints, we weren't able to include everything we wanted, which is addressed in the Limitations section. The site's 5 core tools are featured in more detail below.

Features
----
* <strong>Uploading Item Sets</strong>: Store your item set JSON files on our website. Our website will check the file format to make sure it is in the appropriate format. You can download them on any computer. 
 
This tool requires a free website account to use, and is intended to allow users to store, edit, and download any valid item set JSON files with our website.

* <strong>Matchup Generator</strong>: From our dataset, we parse item information from thousands of matches and use a weighted algorithm based on the lane, opponent champion, and who won the game to generate an item sets of 5 blocks: Starting Items, Early Game, Mid Game, Late Game, Full Build. The algorithm can be found in the <b> generateItemSetForMatchup(champ1_id, champ2_id, lane) </b> function in <i>italiansushi_main/italiansushi/views.py</i>
 
This tool makes use of the match data collected by the Riot API to generate item sets specific for lane matchups, and can be used without a website account. It is intended to provide benefit for users in ranked games; if you know your lane matchup during pick and ban phase of a ranked game, you can quickly use our site to generate an optimized item set, and as long as you download and save it before the game starts loading, you can use the item set to get that extra edge on your opponent. You can also save item sets to your website account and tweak it as necessary.

* <strong>Item Set Builder</strong>: Design a custom item set in-browser that can be downloaded and used in-game.
 
This tool provides the functionality of building an item set completely from scratch, thus providing an alternative, out-of-client option for building item sets. Users do not need a website account to start building a set, but will need to create an account for free in order to save the custom item set and download it.

* <strong>Search Tool</strong>: Browse by champion and lane to see the most popular item sets that other users have uploaded or designed. You can vote on your favorites too!
 
This tool allows users, with or without an account, to view and vote for the highest rated item sets on our site. You can search by champion or lane or matchup, and are returned a list of the top 20 item sets (including your own!) which are then available for download, voting (you can star the ones you like!), or saving to your account to modify as necessary.

* <strong>Saved Item Set Manager</strong>:View, edit, and download all item sets saved to your account. You can save up to 10 item sets to a single account.

This tool also users to manage the item sets saved to their account on the website, with features like preview, download, and delete. The website user accounts currently only allows 10 item sets to be saved per account. This also provides the functionality to edit existing item sets or tweak any sets saved from the matchup generator or the search tool as you see fit.

Live URL (Demo)
----
http://itahmsets.herokuapp.com/

(Developed and tested on Chrome, Firefox, intended for desktop browser use, though it will work reasonably well on a mobile screen as well.)

Data Set for Matchup Generator
----
Using the Riot Developmental API, we collected ~11,000 ranked players from the Plat-Diamond range, and used those players to collect ~52,000 matchids of recent (within last 2 weeks) ranked solo-queue games. We pre-processed the match information to take only the relevant information: duration, and for each participant the champion id and item events. This preprocessed info is stored as a static file on our website, which we access to generate the matchup item sets. Due to GitHub repo limits, we currently only store and use a smaller set of ~5000 matches to generate lane matchups. In the future this will be increased when we scale up, which will result in drastically improving the generated matchup results (right now it's only really good for popular champions). We also plan to make this process a scheduled Cron Job in the future, updating the match information every few days in order to keep the data fresh, while updating the static data (champion and item info) every patch.

Development Stack
----
All code is provided on GitHub, with comments to guide.
* Python via Django -- website backend 
* Python scripts for Riot API Calls -- for data collecting
* Bootstrap, JQuery, Font-awesome.css, Bootbox.js -- website front-end, code is organized by the tool
* Postgresql (hosted on Heroku) -- database 
* Photoshop -- Background images for various pages, and the site icon.

(See requirements.txt for full list of Python libraries used)

Limitations
----
* We are currently hosting using a free Hobby-dev account, which is limited in the database size and app awake time, though it will support any expected traffic for the purposes of the competition.
* As mentioned, our data set for the matchup generator is limited in the live version because of the repo limits. This drastically limits the quality of the generated item sets, but the underlying algorithm is what we'd like to highlight.
* Our website is designed to be easier scaled to a large user base, which will be when the tools become much more beneficial. 
 * For example, the Search tool is currently not as useful as it potentially could be, due to the lack of users on our website. The item sets that can currently be found from search were created during development for us and a small number of test users; but when the site pick ups more users, the Search tool becomes drastically more interesting, highlighting popular builds searchable by champion and/or lane and rated by the community. 
* There are likely many minor bugs throughout, since we did not have time for widespread open user testing.

In the future (aka if we had more time), we'd add more features to building item sets with the more advanced (optional) fields listed in the item set documentation, add support for Item Sets for modes outside of SR, and fine-tune the matchup item set generator algorithm. Our front-end tools are well organized and easily modifiable to allow for additional features. We look forward to pushing more features and seeing the impact of iTahmSets when we gain a critical mass of users in the future!


Running Locally
----
To run this website locally, you must:
* Clone this repo
* Install all needed libraries from requirements.txt (pip recommended)
* Set-up local postgresql database (LOCAL DB SETTINGS) with settings matched at <i>italiansushi_main/italiansushi_project/settings.py</i>. 
  * Make sure that the HEROKU DB SETTINGS are commented out and the LOCAL DB SETTINGS are not
* Run python manage.py runserver

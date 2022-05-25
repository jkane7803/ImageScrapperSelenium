# ImageScrapperSelenium

Use Yahoo.py to test how my microservice works using Google and Yahoo. An important part of my main mode of indirect communication between my microservice
and the project in question is via the text file "image-service.txt". In order for the microservice to correctly read said text file, you must write 
each line in the text file in a particular way:

"Chrome 1 Dogs"; "Yahoo 3 20"; "Chrome 9 Money"; ...

The word "Chrome" or "Yahoo" represents which search engine you want to scrap through (Yahoo being Yahoo, and Chrome being Google). After that word, make sure
you input a single space before the next one, which is a number. This number ranges from 1 to 9 (anything higher would screw up how my program reads the
text file), and represents the number of images you want to scrap. Again, place a single space between the number and the next value coming up, the query. 
The query represents the topic you want to search for (i.e. what you type into the search bar) like "Dogs", "20", and "Money". This query does not have a 
character limit, at least one that I could think of, but it is definitely safer to just keep your query small.

Bing.py does not work as intended (either overworks or does not work at all), and if you wish to take look at it, look at the if statements on line 
40, 60, and 81 (all of which contain important paths, objects, or classes for my Selenium to automatically interact with the website). If your wondering
how I figured these paths or classes out, I just clicked on the Bing link on line 41, and inspected images in the top results.

Main.py is for my project, and only does "Chrome", which is fine for me. 

Lastily, and this is very important for testing reasons, make you downloaded "ChromeDriver" onto your computer, and change the value of the variable 
"DRIVER_PATH" to the path that your "ChromeDriver" executable is located at in your files. Without this, my microservice would not function at all. 
So please, download it before using my microservice. If you wish to know more about how to downloard said "ChromeDriver", DM me on Microsoft Teams.

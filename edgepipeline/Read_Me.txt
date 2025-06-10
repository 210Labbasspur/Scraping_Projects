************************************************************************************************************************************************************************************************************************
	Here are detailed instructions for using the files in the "input" folder for your scraping project:

Input Folder :
 input folder contains these file and details of each file is given below:
    ├── login_credentials.csv
    ├── filters.csv
    ├── vehicles_redflag_keywords.txt
    ├── auctions_details.csv

File Details

1. (login_credentials.csv) Contains the username and password for logging into the site. You can update the username and password fields as per your convenience.

2. (filters.csv) Contains the filters for the scraping process. Adjust the values in this file to modify the filters for year range (year_from, year_to), maximum odometer reading (odometer_max), 
maximum price (price_max), and Auction ID (auction_id) further detail of auction_id is given in ser-4.

3. (vehicles_redflag_keywords.txt) Contains brands of vehicles you do not wish to scrape, I have placed some brands for example (audi, mercedes etc) in the file for your understanding. 
Add or remove vehicle brands as needed. Each brand should be on a separate line.

4. (auctions_details.csv) Contains details of available auctions.Copy the "auction_id" of the auction you want to scrape and paste it into the "auction_id" field in "filters.csv".



 ****** Step-by-Step Instructions ****** 

1. Prepare login credentials:
	- Open login_credentials.csv.
	- Update the username and password fields with your login credentials.
	- Set your filters:

2. Open filters.csv.
	- Adjust the values for year_from, year_to, odometer_max, and price_max to set your desired filters.
	- Open auctions_details.csv and find the auction_id of the auction you want to scrape.
	- Copy the desired auction_id and paste it into the auction_id field in filters.csv.

3. Manage vehicle redflag keywords: 
	- Open vehicles_redflag_keywords.txt.
	- Add or remove vehicle brands based on your preferences. Each brand should be on a new line.

4. Run the scraping script:
	- Ensure your script reads these input files correctly
	- The script should use the credentials from login_credentials.csv to log into the site.
	- Apply the filters specified in filters.csv to refine the scraping process.
	- Exclude vehicles that match the brands listed in vehicles_redflag_keywords.txt.


************************************************************************************************************************************************************************************************************************
# The final dashboard can be accessed here:
*https://airlinedelayanalysis-final.streamlit.app*

## Our initial prototype:
*https://airlinedelayanalysis.streamlit.app*

---

# Airport Reliability Dashboard
Filter & Fly, a travel agency, has had historical problems with airports and airlines constantly delaying or canceling their flights. This leads to frustrations with their customers who demand a refund for their trip. They have tasked us, Two Peas in a Plot, to identify and calculate risks for different airports and airlines. The dataset selected will allow Filter & Fly to look at historical airport and airline trends in order to plan their flight itineraries. This may help reduce customer frustration and avoid rebooking and refund costs.

## Key questions include:
* Which airlines have the lowest likelihood of delay, and which airports are consistently most on-time?
* How do delay rates and average delay minutes change by season or month?
* What are the most common delay causes (carrier, weather, airport) for specific airline–airport combinations?
* Correlation with airlines and airports?
* Ranking reliability on the dashboard (low risk or high risk filters)?
* Risk by state/location and by season?

## Dataset Description
The dataset (Airline_Delay_Cause) selected includes U.S. domestic airline delay statistics by cause over two decades. Some notable columns include year, month, operating carrier, origin airport, total number of flights, number of delayed flights and other columns that allow for more granular analysis. Column names and descriptions can be viewed at the end of the file.

The data was collected by Kaggle expert, AbdElaziz Ahmed Elsayed. They are a Senior Software Developer with over 5+ years of experience. The data was sourced from the Bureau of Transportation Statistics (BTS) Airline On-Time Statistics and Delay Causes tools. Light data cleaning was done to the original source to ensure integers were parsed as integers/floats. There are no apparent risks or ethical concerns for the dataset. The dataset comes from publicly available sources with light cleaning from the collector.

## Column Names and Descriptions
* year - The calendar year of the recorded flight operations.
* month - The month (1–12) corresponding to the data entry.
* carrier - The airline’s IATA carrier code (e.g., “9E”).
* carrier_name - Full official name of the airline (e.g., “Endeavor Air Inc.”).
* airport - The IATA airport code of the origin airport (e.g., “ABE”).
* airport_name - Full name of the origin airport, including city and state.
* arr_flights - Total number of arrival flights operated in that month for the given airline–airport pair.
* arr_del15 - Number of arrival flights delayed by 15 minutes or more (DOT standard definition of a delay)
* carrier_ct - Count of flights delayed due to airline-related issues (e.g., crew delays, maintenance, equipment problems).
* weather_ct - Count of flights delayed because of significant weather conditions.
* nas_ct - Count of flights delayed due to National Airspace System issues (e.g., air traffic control, heavy traffic volume, system
* security_ct - Count of flights delayed due to security-related factors (e.g., screening issues, security breaches).
* late_aircraft_ct - Count of flights delayed because the aircraft arrived late from a previous flight.
* arr_cancelled - Number of flights that were cancelled in that month for the given airline–airport pair.
* arr_diverted - Number of flights that were diverted to another airport in that month for the given airline–airport pair.
* arr_delay - Total arrival delay minutes across all causes for that airline/airport/month.
* carrier_delay - Total minutes of delay caused by carrier-related issues.
* weather_delay - Total minutes of delay caused by weather.
* nas_delay - Total minutes of delay caused by NAS/air-traffic system constraints.
* security_delay - Total minutes of delay caused by security-related disruptions.
* late_aircraft_delay - Total minutes of delay caused by late-arriving aircraft.

SELECT 
    country, 
    year, 
    ROUND(AVG(amount), 2) AS avgsales
FROM 
    FACTSALES
LEFT JOIN 
    DIMCOUNTRY ON FACTSALES.countryid = DIMCOUNTRY.countryid
LEFT JOIN 
    DIMDATE ON FACTSALES.dateid = DIMDATE.dateid
GROUP BY 
    CUBE (country, year)
ORDER BY 
    country, year;
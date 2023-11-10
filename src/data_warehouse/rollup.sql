SELECT 
    country, 
    year, 
    SUM(amount) AS totalsales
FROM 
    FACTSALES
LEFT JOIN 
    DIMCOUNTRY ON FACTSALES.countryid = DIMCOUNTRY.countryid
LEFT JOIN 
    DIMDATE ON FACTSALES.dateid = DIMDATE.dateid
GROUP BY 
    ROLLUP (country, year)
ORDER BY 
    country, year;
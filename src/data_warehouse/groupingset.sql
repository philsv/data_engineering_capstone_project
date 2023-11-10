SELECT 
    country, 
    category, 
    SUM(amount) AS totalsales
FROM 
    FACTSALES
LEFT JOIN 
    DIMCOUNTRY ON FACTSALES.countryid = DIMCOUNTRY.countryid
LEFT JOIN 
    DIMCATEGORY ON FACTSALES.categoryid = DIMCATEGORY.categoryid
GROUP BY 
    GROUPING SETS (country, category)
ORDER BY 
    country, category;
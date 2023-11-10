CREATE TABLE "TKH81297".total_sales_per_country (country, total_sales)
AS (
    SELECT 
        country, 
        SUM(amount)
    FROM 
        FACTSALES
    LEFT JOIN 
        DIMCOUNTRY ON FACTSALES.countryid = DIMCOUNTRY.countryid
    GROUP BY 
        country
 ) 
    DATA INITIALLY DEFERRED
    REFRESH DEFERRED
    MAINTAINED BY SYSTEM;
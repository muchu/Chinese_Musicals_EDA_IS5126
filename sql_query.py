


theatre_number_in_citys = """
    select COUNT(c.city_name) as numberOfTheatre, c.city_name from theatres t
    join citys c on t.city_id = c.city_id
    group by c.city_name
    order by numberOfTheatre desc
    """
seat_number_in_citys = """
select SUM(s.seats) as totalNumberOfSeats,c.city_name from theatres t
join citys c on t.city_id = c.city_id
join stages s on s.theatre_id = t.theatre_id
group by c.city_name
order by totalNumberOfSeats desc
"""
shows_performed_last_month = """
select count(show_id) as shows_perform_a_month, city  from shows
where shows.date >= current_date - interval '30 days'
group by city
order by shows_perform_a_month desc
"""
original_musical_persentage_by_date_range = """
SELECT 
    is_original,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM musicals
WHERE premiere_date BETWEEN %s AND %s
GROUP BY is_original
ORDER BY count DESC

"""
musical_perform_by_date_range = """
SELECT 
    city,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM shows
WHERE date BETWEEN %s AND %s
GROUP BY city
ORDER BY count DESC
"""
get_monthly_number_of_shows_by_city = """
SELECT 
    city,
    EXTRACT(YEAR FROM date) AS year,
    EXTRACT(MONTH FROM date) AS month,
    COUNT(show_id) AS total_shows
FROM 
    shows
GROUP BY 
    city, 
    EXTRACT(YEAR FROM date), 
    EXTRACT(MONTH FROM date)
ORDER BY 
    city, year, month;

"""

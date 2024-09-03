


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
    